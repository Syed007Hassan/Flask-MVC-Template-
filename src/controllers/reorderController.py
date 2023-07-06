import requests
from src.models.emailModel import EmailDTO
from src.services.reorderService import reorder_logic, send_email, vendor_logic
from flask import Flask, request, jsonify
from config import baseUrl


def set_response_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    return response

def getData():
    try:
        url = baseUrl+"/api/Item/GetItemsReorderStatus"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the response status code is not 2xx
        data = response.json()
        structured_data = reorder_logic(data)
        response = jsonify(data=structured_data)
        response = set_response_headers(response)
        return response, 200
    except requests.exceptions.RequestException as e:
        # Return an error message and a 500 status code if there was an error with the request
        return jsonify(error=str(e)), 500
    except Exception as e:
        # Return an error message and a 400 status code if there was an error with the data
        return jsonify(error=str(e)), 400


def getVendorData(itemCode):
    try:
        url = baseUrl+"/api/Contact/GetContactNamesWithReorderItems/{}".format(itemCode)
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the response status code is not 2xx
        data = response.json()
        structured_data = vendor_logic(data,itemCode)
        response = jsonify(data=structured_data)
        response = set_response_headers(response)
        return response, 200
    except requests.exceptions.RequestException as e:
        # Return an error message and a 500 status code if there was an error with the request
        return jsonify(error=str(e)), 500
    except Exception as e:
        # Return an error message and a 400 status code if there was an error with the data
        return jsonify(error=str(e)), 400


def emailService(itemCode,vendorId,itemQuantity):
    try:
        url = baseUrl+"/api/Contact/GetContactByID/{}".format(vendorId)
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the response status code is not 2xx
        vendorData = response.json()
        url = baseUrl+"/api/Item/GetItemByNo/{}".format(itemCode)
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the response status code is not 2xx
        itemData = response.json()
        # Call the send_email function with the EmailDTO object
        email_msg = send_email(itemData, vendorData,itemQuantity)
        structuredData = jsonify(data=email_msg)
        response = set_response_headers(structuredData)
        return response, 200
    
    except requests.exceptions.RequestException as e:
        # Return an error message and a 500 status code if there was an error with the request
        return jsonify(error=str(e)), 500
    except Exception as e:
        # Return an error message and a 400 status code if there was an error with the data
        return jsonify(error=str(e)), 400