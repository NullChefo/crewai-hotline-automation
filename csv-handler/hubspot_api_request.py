import requests
import os

BASE_URL = 'https://api.hubapi.com'

API_KEY = os.getenv('HUBSPOT_API_KEY')
if API_KEY is None:
    print("HUBSPOT_API_KEY is not set")
    exit(1)


def create_contact(contact_data):
    url = f'{BASE_URL}/contacts/v1/contact'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    response = requests.post(url, json=contact_data, headers=headers)
    return response.json()


def search_contact_by_property(property_name, property_value):
    url = f"{BASE_URL}/contacts/v1/search/query"
    params = {
        'hapikey': API_KEY,
        'q': f"{property_name}:{property_value}"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None


# csv properties
properties = [
    {"name": "policyholder_name", "label": "Policyholder Name", "groupName": "contactinformation", "type": "string",
     "fieldType": "text"},
    {"name": "policy_number", "label": "Policy Number", "groupName": "contactinformation", "type": "string",
     "fieldType": "text"},
    {"name": "beneficiary_1", "label": "Beneficiary 1", "groupName": "contactinformation", "type": "string",
     "fieldType": "text"},
    {"name": "beneficiary_2", "label": "Beneficiary 2", "groupName": "contactinformation", "type": "string",
     "fieldType": "text"},
    {"name": "beneficiary_3", "label": "Beneficiary 3", "groupName": "contactinformation", "type": "string",
     "fieldType": "text"},
    {"name": "beneficiary_1_percent", "label": "Beneficiary 1 %", "groupName": "contactinformation", "type": "number",
     "fieldType": "number"},
    {"name": "beneficiary_2_percent", "label": "Beneficiary 2 %", "groupName": "contactinformation", "type": "number",
     "fieldType": "number"},
    {"name": "beneficiary_3_percent", "label": "Beneficiary 3 %", "groupName": "contactinformation", "type": "number",
     "fieldType": "number"},
]


# Function to create a property in HubSpot
def create_property(property_data):
    url = f'{BASE_URL}/properties/v1/contacts/properties'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    res = requests.post(url, json=property_data, headers=headers)
    return res.json()
