# api.py
import os

from fastapi import FastAPI, HTTPException
from hubspot import HubSpot
from pydantic import BaseModel

from custom_crew import create_crew

app = FastAPI()

# Initialize HubSpot client
hubspot_client = HubSpot(access_token=os.environ.get("HUBSPOT_API_KEY"))

# Create CrewAI application_crew
crew = create_crew(hubspot_client)


class CallerIdentificationRequest(BaseModel):
    phone_number: str


class BeneficiaryChangeRequest(BaseModel):
    contact_id: str
    action: str  # "add", "remove", or "update"
    beneficiary_data: dict


@app.post("/identify_caller")
async def identify_caller(request: CallerIdentificationRequest):
    caller_id_agent = crew.agents[0]
    result = caller_id_agent.identify_caller(request.phone_number)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Caller not found")


@app.post("/manage_beneficiaries")
async def manage_beneficiaries(request: BeneficiaryChangeRequest):
    beneficiary_agent = crew.agents[1]
    current_beneficiaries = beneficiary_agent.get_current_beneficiaries(request.contact_id)

    if request.action == "add":
        current_beneficiaries.append(request.beneficiary_data)
    elif request.action == "remove":
        current_beneficiaries = [b for b in current_beneficiaries if b["name"] != request.beneficiary_data["name"]]
    elif request.action == "update":
        current_beneficiaries = request.beneficiary_data
    else:
        raise HTTPException(status_code=400, detail="Invalid action")

    success = beneficiary_agent.update_beneficiaries(request.contact_id, current_beneficiaries)
    if success:
        return {"message": "Beneficiaries updated successfully", "beneficiaries": current_beneficiaries}
    raise HTTPException(status_code=500, detail="Failed to update beneficiaries")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
