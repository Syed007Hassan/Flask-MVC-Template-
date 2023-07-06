import json
from src.services.palm_api_Service import palm_create_response


def index(prompt):
    return palm_create_response(prompt)
