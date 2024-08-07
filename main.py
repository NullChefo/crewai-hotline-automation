from fastapi import FastAPI, Form

from application_crew.getPolicyholderDetailsCrew import get_contact_information_by_phone_number, \
    get_contact_information_policyholder_name
from application_crew.knownNumberCheckerCrew import knownNumberChecker

app = FastAPI(
    title="AI Hotline Automation API",
    description="The hotline automation API.",
    version="0.0.1",
)


@app.get("/health")
def read_health():
    return {"message": "Healthy"}


# @app.post("/caller_automation")
# async def caller_automation(caller_id: str = Form(...)):
#     # Assign Known_Number, "False" and Policyholder_Name, Intent, Latest_Status to "Null"
#
#     known_number: bool = False
#     policyholder_name: str = "Null"
#     intent: str = "Null"
#     latest_status: str = "Null"
#     isKnown: bool = False
#     contactInformation: ContactInformation
#
#     # Run KnownNumberChecker Crew and update Known_Number to "True" if number is found
#     isKnown = knownNumberChecker(caller_id)
#
#     if (isKnown == True):
#         # Run PolicyholderNameExtractor Crew and update Policyholder_Name
#         contactInformation = get_contact_information_by_policy_number(caller_id)
#
#     # Return Known_Number, Policyholder_Name, Intent, Latest_Status
#     return {"caller_id": caller_id}


@app.post("/check_phone_number")
async def check_phone_number(phone_number: str = Form(...)):
    # get the phone umber from the form data
    is_known = knownNumberChecker(phone_number)
    return {"is_known": is_known}


@app.post("/check_policyholder_name")
async def check_policyholder_name(phone_number: str = Form(...)):
    # get the phone number and get the record from the hubspot and then get the policyholder name
    contact_information = get_contact_information_by_phone_number(phone_number)

    # contact_information is optional if empty return 404
    if contact_information is None:
        return {"message": "Contact information not found"}

    # if the contact information is not found return status 404
    if contact_information.policyholder_name is None:
        return {"message": "Contact information not found"}

    return {"policyholder_name": contact_information.policyholder_name}


@app.post("/policy_by_policyholder_name")
async def policy_by_policyholder_name(policyholder_name: str = Form(...)):
    # get the phone number and get the record from the hubspot and then get the policyholder name
    contact_information = get_contact_information_policyholder_name(policyholder_name)

    # if the contact information is not found return status 404
    if contact_information is None:
        return {"message": "Contact information not found"}

    return {"phone_number": contact_information.phone_number_property,
            "email": contact_information.email,
            "policy_number": contact_information.policy_number,
            "last_call_topic": contact_information.last_call_topic,
            "last_call_status": contact_information.last_call_status}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
