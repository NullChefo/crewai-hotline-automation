# from application_crew import Agent, Task, Crew, Process
from utils.hubspot.hubSpotIntegration import get_record_by


def knownNumberChecker(caller_id: str) -> bool:
    # Get from the HubSpot cms filed phone number
    record = get_record_by("phone_number_property", caller_id)
    # if the record is empty return false
    if record is None:
        return False
    print(record)

    return True
