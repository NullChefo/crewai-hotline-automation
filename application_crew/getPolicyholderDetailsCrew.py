from typing import Optional

from custom_types.contactInformation import ContactInformation
from utils.hubspot.hubSpotIntegration import get_record_by


def get_contact_information_by_policy_number(policy_number: str) -> Optional[ContactInformation]:
    # Add more
    return get_record_by("policy_number", policy_number)


# get_contact_information_by_phone_number(phone_number)
def get_contact_information_by_phone_number(phone_number: str) -> Optional[ContactInformation]:
    # Add more
    return get_record_by("phone_number_property", phone_number)


def get_contact_information_policyholder_name(policyholder_name: str) -> Optional[ContactInformation]:
    return get_record_by("policyholder_name", policyholder_name)
