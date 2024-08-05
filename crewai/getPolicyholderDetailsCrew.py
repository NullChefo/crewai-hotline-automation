import os

from hubspot.hubspot import HubSpot

from typing import Optional

from custom_types.contactInformation import ContactInformation


API_KEY = os.getenv('HUBSPOT_API_KEY')
if API_KEY is None:
    print("HUBSPOT_API_KEY is not set")
    exit(1)


def get_contact_information_by_policy_number(policy_number: str) -> Optional[ContactInformation]:
    # Initialize HubSpot client with your access token
    api_client = HubSpot(api_key=API_KEY)

    # Search for the contact by policy number
    search_response = api_client.crm.contacts.search_api.do_search(
        body={
            "filterGroups": [
                {
                    "filters": [
                        {
                            "propertyName": "policy_number",
                            "operator": "EQ",
                            "value": policy_number
                        }
                    ]
                }
            ],
            "properties": ["name, policyholder_name", "policy_number", "beneficiary_1", "beneficiary_2", "beneficiary_3",
                           "beneficiary_1_percent", "beneficiary_2_percent", "beneficiary_3_percent"],
            "limit": 1
        }
    )

    if not search_response.results:
        return None

    contact = search_response.results[0]
    return ContactInformation(
        name=contact.properties.get("name"),
        policyholder_name=contact.properties.get("policyholder_name"),
        policy_number=contact.properties.get("policy_number"),
        beneficiary_1=contact.properties.get("beneficiary_1"),
        beneficiary_2=contact.properties.get("beneficiary_2"),
        beneficiary_3=contact.properties.get("beneficiary_3"),
        beneficiary_1_percent=float(contact.properties.get("beneficiary_1_percent", 0)),
        beneficiary_2_percent=float(contact.properties.get("beneficiary_2_percent", 0)),
        beneficiary_3_percent=float(contact.properties.get("beneficiary_3_percent", 0))
    )
