from fastapi import FastAPI, Form

from crewai.getPolicyholderDetailsCrew import get_contact_information_by_policy_number
from crewai.knownNumberCheckerCrew import knownNumberChecker
from custom_types.contactInformation import ContactInformation

app = FastAPI(
    title="AI Hotline Automation API",
    description="The hotline automation API.",
    version="0.0.1",
    # terms_of_service="http://example.com/terms/",
    # contact={
    #     "name": "API Support",
    #     "url": "http://example.com/contact/",
    #     "email": "support@example.com",
    # },
    # license_info={
    #     "name": "Apache 2.0",
    #     "url": "http://www.apache.org/licenses/LICENSE-2.0.html",
    # },
    # openapi_url="/api/v1/openapi.json",
    # docs_url="/api/v1/docs",
    # redoc_url="/api/v1/redoc",
)


@app.get("/health")
def read_health():
    return {"message": "Healthy"}


@app.post("/caller_automation")
async def caller_automation(caller_id: str = Form(...)):
    # Assign Known_Number, "False" and Policyholder_Name, Intent, Latest_Status to "Null"

    known_number: bool = False
    policyholder_name: str = "Null"
    intent: str = "Null"
    latest_status: str = "Null"
    isKnown: bool = False
    contactInformation: ContactInformation

    # Run KnownNumberChecker Crew and update Known_Number to "True" if number is found
    isKnown = knownNumberChecker(caller_id)

    if (isKnown == True):
        # Run PolicyholderNameExtractor Crew and update Policyholder_Name
        contactInformation = get_contact_information_by_policy_number(caller_id)

    # Return Known_Number, Policyholder_Name, Intent, Latest_Status
    return {"caller_id": caller_id}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
