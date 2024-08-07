import os
from typing import Optional

import requests
from hubspot.crm.contacts import PublicObjectSearchRequest
from hubspot.events import ApiException
from hubspot.hubspot import HubSpot

from custom_types.contactInformation import ContactInformation

API_KEY = os.getenv('HUBSPOT_API_KEY')
if API_KEY is None:
    print("HUBSPOT_API_KEY is not set")
    exit(1)
BASE_URL = 'https://api.hubapi.com'

# Initialize HubSpot client with OAuth
api_client = HubSpot()
api_client.access_token = API_KEY


def get_record_by(property_name: str, property_value) -> Optional[ContactInformation]:
    # Construct the search request
    search_request = PublicObjectSearchRequest(
        filter_groups=[
            {
                "filters": [
                    {
                        "propertyName": property_name,
                        "operator": "EQ",
                        "value": property_value
                    }
                ]
            }
        ],
        properties=[
            "firstName", "policyholder_name", "policy_number", "beneficiary_1", "beneficiary_2",
            "beneficiary_3", "beneficiary_1_percent", "beneficiary_2_percent", "beneficiary_3_percent",
            "last_call_topic", "last_call_status", "phone_number_property", "email"
        ],
        limit=1
    )

    try:
        # Search for the contact by policy number
        search_response = api_client.crm.contacts.search_api.do_search(
            public_object_search_request=search_request
        )
    except ApiException as e:
        print(f"Exception when calling SearchApi->do_search: {e}")
        return None

    if not search_response.results:
        return None

    contact = search_response.results[0]
    print(contact)

    def safe_float(value):
        return float(value) if value is not None else 0.0

    return ContactInformation(
        name=contact.properties.get("firstName"),
        policyholder_name=contact.properties.get("policyholder_name"),
        policy_number=contact.properties.get("policy_number"),
        beneficiary_1=contact.properties.get("beneficiary_1"),
        beneficiary_2=contact.properties.get("beneficiary_2"),
        beneficiary_3=contact.properties.get("beneficiary_3"),
        beneficiary_1_percent=safe_float(contact.properties.get("beneficiary_1_percent")),
        beneficiary_2_percent=safe_float(contact.properties.get("beneficiary_2_percent")),
        beneficiary_3_percent=safe_float(contact.properties.get("beneficiary_3_percent")),
        last_call_topic=contact.properties.get("last_call_topic"),
        last_call_status=contact.properties.get("last_call_status"),
        phone_number_property=contact.properties.get("phone_number_property"),
        email=contact.properties.get("email")
    )


client = HubSpot(api_key=API_KEY)


def create_contact(contact_data):
    url = f'{BASE_URL}/contacts/v1/contact'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    response = requests.post(url, json=contact_data, headers=headers)
    return response.json()


# def search_contact_by_property(property_name, property_value):
#     search_payload = {
#         "filterGroups": [{
#             "filters": [{
#                 "propertyName": property_name,
#                 "operator": "EQ",
#                 "value": property_value
#             }]
#         }],
#         "properties": [property_name]
#     }
#     response = client.crm.contacts.search_api.do_search(body=search_payload)
#     if response:
#         return response.to_dict()
#     else:
#         print("Error in search_contact_by_property")
#         return None


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
    {"name": "phone_number_property", "label": "Phone Number Property", "groupName": "contactinformation",
     "type": "string",
     "fieldType": "text"},
    {"name": "last_call_topic", "label": "Last Call Topic", "groupName": "contactinformation", "type": "string",
     "fieldType": "text"},
    {"name": "last_call_status", "label": "Last Call Status", "groupName": "contactinformation", "type": "string",
     "fieldType": "text"},
    {"name": "email", "label": "Email", "groupName": "contactinformation", "type": "string", "fieldType": "text"}
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
