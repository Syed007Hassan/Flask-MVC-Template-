import json
from flask import Flask, jsonify
import smtplib
from email.message import EmailMessage
from src.models.emailModel import EmailDTO
from src.models.reorderModel import ReorderModel
from src.services.palm_api_Service import palm_create_response


class ReorderService:
    def __init__(self):
        self.model = ReorderModel()

    def save_reorder_data(self, reorder_data):
        self.model.add_reorder_data(reorder_data)

    def save_vendor_data(self, vendor_data):
        self.model.add_vendor_data(vendor_data)

    def get_reorder_data(self):
        return self.model.get_reorder_data()

    def get_vendor_data(self):
        return self.model.get_vendor_data()


def reorder_logic(reorder_data):
    try:
        reorder_service = ReorderService()
        reorder_service.save_reorder_data(reorder_data)
        message = "These are the items of which Reorder Quantity is greater than quantity: "
        return [message] + reorder_data
    except Exception as e:
        return {'error': "Error generating reorder response: " + str(e)}


def vendor_logic(vendor_data,itemCode):
    try:
        reorder_service = ReorderService()
        reorder_service.save_vendor_data(vendor_data)
        message = "These are the vendors that deal with the items with id of: " + itemCode
        for vendor in vendor_data:
            vendor['itemCode'] = itemCode
        return [message] + vendor_data
    except Exception as e:
        return {'error': "Error generating vendor response: " + str(e)}


def send_email(itemData, vendorData, itemQuantity):
    try:
        body = palm_create_response('Write an email to vendor name ' + vendorData['name'] + ' and email ' + vendorData['emailId'] + ' and I want to add order a item ' + itemData['itemName'] + ' and its quantity is ' + itemQuantity + '. It should be a professional email and my email address is muhammad.ahsan@onetechnologyservices.com so get name from instead of writing [Your Name].')
        # Set up the email message
        emailDTO = EmailDTO()
        emailDTO.header = "Reorder Item " + itemData['itemName']
        emailDTO.body = body
        emailDTO.recipient_email = vendorData['emailId']
        if len(emailDTO.recipient_email) <= 2:
            return {'error': "Email is invalid: "}
        smtp_host = "smtp.office365.com"
        msg = EmailMessage()
        msg["Subject"] = emailDTO.header
        msg["From"] = "muhammad.ahsan@onetechnologyservices.com"  # Replace with your email address
        msg["To"] = emailDTO.recipient_email
        msg.set_content(emailDTO.body)

        # Send the email using SMTP
        with smtplib.SMTP(smtp_host, 587) as server:
            server.starttls()
            server.login("xyz", "1234")  # Replace with your email credentials
            server.send_message(msg)

        # Return itemData and vendorData as JSON with success message
        return body

    except Exception as e:
        return {'error': "Error generating email response: " + str(e)}