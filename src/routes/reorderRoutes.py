from flask import Blueprint
from src.controllers.reorderController import getData, emailService,getVendorData

reorderBlueprint = Blueprint('blueprintt', __name__)

reorderBlueprint.route('/', methods=['GET'])(getData)
reorderBlueprint.route('/getVendorData/<itemCode>', methods=['GET'])(getVendorData)
reorderBlueprint.route('/emailService/<itemCode>/<vendorId>/<itemQuantity>', methods=['GET'])(emailService)

