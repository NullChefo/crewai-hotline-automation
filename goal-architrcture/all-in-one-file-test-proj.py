# Import necessary libraries
import os
from typing import Optional

import httpx
from crewai import Agent, Task, Crew
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# HubSpot API configuration
HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")
HUBSPOT_BASE_URL = "https://api.hubapi.com"

# Voiceflow API configuration (placeholder)
VOICEFLOW_API_KEY = os.getenv("VOICEFLOW_API_KEY")
VOICEFLOW_BASE_URL = "https://general-runtime.voiceflow.com"


# Define data models
class Caller(BaseModel):
    phone_number: str
    name: Optional[str] = None
    email: Optional[str] = None
    policy_number: Optional[str] = None
    last_call_topic: Optional[str] = None
    last_call_status: Optional[str] = None


class CallDetails(BaseModel):
    caller_id: str
    intent: Optional[str] = None


# HubSpot functions
async def get_contact_from_hubspot(phone_number: str) -> Optional[Caller]:
    url = f"{HUBSPOT_BASE_URL}/crm/v3/objects/contacts/search"
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "filterGroups": [{
            "filters": [{
                "propertyName": "phone",
                "operator": "EQ",
                "value": phone_number
            }]
        }]
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        if response.status_code == 200:
            results = response.json()["results"]
            if results:
                contact = results[0]["properties"]
                return Caller(
                    phone_number=phone_number,
                    name=contact.get("firstname", "") + " " + contact.get("lastname", ""),
                    email=contact.get("email"),
                    policy_number=contact.get("policy_number"),
                    last_call_topic=contact.get("last_call_topic"),
                    last_call_status=contact.get("last_call_status")
                )
    return None


# CrewAI functions
def create_search_agent():
    return Agent(
        role='Search Agent',
        goal='Find and retrieve caller information',
        backstory='You are an AI agent specialized in searching and retrieving caller information from various sources.',
        allow_delegation=False
    )


def create_task_for_caller_lookup(caller_id: str):
    return Task(
        description=f'Find information for caller with phone number {caller_id}',
        agent=create_search_agent()
    )


def run_crew_for_caller_lookup(caller_id: str) -> Optional[Caller]:
    crew = Crew(
        agents=[create_search_agent()],
        tasks=[create_task_for_caller_lookup(caller_id)]
    )
    result = crew.kickoff()
    # Parse the result and return a Caller object
    # This is a placeholder and should be implemented based on the actual output format of your CrewAI setup
    return Caller(phone_number=caller_id, name="John Doe")  # Placeholder


# FastAPI routes
@app.post("/lookup_caller")
async def lookup_caller(call_details: CallDetails):
    # First, try to get the contact from HubSpot
    caller = await get_contact_from_hubspot(call_details.caller_id)

    if not caller:
        # If not found in HubSpot, use CrewAI to search
        caller = run_crew_for_caller_lookup(call_details.caller_id)

    if not caller:
        raise HTTPException(status_code=404, detail="Caller not found")

    return caller


@app.post("/process_intent")
async def process_intent(call_details: CallDetails):
    # This function would handle different intents like beneficiary change, death claim, etc.
    # It would interact with CrewAI to process the intent and return appropriate responses
    # Placeholder implementation
    return {"message": f"Processing intent: {call_details.intent}"}


# Main execution
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
