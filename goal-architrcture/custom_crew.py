import json

from crewai import Task, Agent, Crew
from hubspot.crm.contacts import SimplePublicObjectInput, ApiException


class CallerIdentificationAgent(Agent):
    def __init__(self, hubspot_client):
        super().__init__(
            name="Caller ID Agent",
            goal="Identify the caller and retrieve their information",
            backstory="I am an AI agent specialized in identifying callers and retrieving their information from "
                      "HubSpot."
        )
        self.hubspot_client = hubspot_client

    def identify_caller(self, phone_number):
        try:
            filter = {"propertyName": "phone", "operator": "EQ", "value": phone_number}
            public_object_search_request = {"filters": [filter]}
            api_response = self.hubspot_client.crm.contacts.search_api.do_search(
                public_object_search_request=public_object_search_request
            )
            if api_response.results:
                contact = api_response.results[0]
                return {
                    "name": contact.properties.get("firstname", "") + " " + contact.properties.get("lastname", ""),
                    "email": contact.properties.get("email", ""),
                    "phone": contact.properties.get("phone", ""),
                    "policy_number": contact.properties.get("policy_number", ""),
                    "last_call_topic": contact.properties.get("last_call_topic", ""),
                    "last_call_status": contact.properties.get("last_call_status", "")
                }
            return None
        except ApiException as e:
            print(f"Exception when calling search_api->do_search: {e}")
            return None


class BeneficiaryChangeAgent(Agent):
    def __init__(self, hubspot_client):
        super().__init__(
            name="Beneficiary Change Agent",
            goal="Manage beneficiary changes for policyholders",
            backstory="I am an AI agent specialized in handling beneficiary changes for insurance policies."
        )
        self.hubspot_client = hubspot_client

    def get_current_beneficiaries(self, contact_id):
        try:
            contact = self.hubspot_client.crm.contacts.basic_api.get_by_id(
                contact_id=contact_id,
                properties=["beneficiaries"]
            )
            beneficiaries = contact.properties.get("beneficiaries", "")
            # Assuming beneficiaries are stored as a JSON string
            return json.loads(beneficiaries)
        except ApiException as e:
            print(f"Exception when calling basic_api->get_by_id: {e}")
            return []

    def update_beneficiaries(self, contact_id, beneficiaries):
        properties = {
            "beneficiaries": json.dumps(beneficiaries)
        }
        simple_public_object_input = SimplePublicObjectInput(properties=properties)
        try:
            self.hubspot_client.crm.contacts.basic_api.update(
                contact_id=contact_id,
                simple_public_object_input=simple_public_object_input
            )
            return True
        except ApiException as e:
            print(f"Exception when calling basic_api->update: {e}")
            return False


def create_crew(hubspot_client):
    caller_id_agent = CallerIdentificationAgent(hubspot_client)
    beneficiary_agent = BeneficiaryChangeAgent(hubspot_client)

    identify_caller_task = Task(
        description="Identify the caller using their phone number",
        agent=caller_id_agent
    )

    manage_beneficiaries_task = Task(
        description="Manage beneficiary changes for the policyholder",
        agent=beneficiary_agent
    )

    return Crew(
        agents=[caller_id_agent, beneficiary_agent],
        tasks=[identify_caller_task, manage_beneficiaries_task]
    )
