from typing import Optional


class ContactInformation:
    def __init__(self,
                 name: Optional[str] = None,
                 policyholder_name: Optional[str] = None,
                 policy_number: Optional[str] = None,
                 beneficiary_1: Optional[str] = None,
                 beneficiary_2: Optional[str] = None,
                 beneficiary_3: Optional[str] = None,
                 beneficiary_1_percent: Optional[float] = None,
                 beneficiary_2_percent: Optional[float] = None,
                 beneficiary_3_percent: Optional[float] = None,
                 phone_number: Optional[str] = None,
                 last_call_topic: Optional[str] = None,
                 last_call_status: Optional[str] = None
                 ):
        self.name = name
        self.policyholder_name = policyholder_name
        self.policy_number = policy_number
        self.beneficiary_1 = beneficiary_1
        self.beneficiary_2 = beneficiary_2
        self.beneficiary_3 = beneficiary_3
        self.beneficiary_1_percent = self._validate_percentage(beneficiary_1_percent)
        self.beneficiary_2_percent = self._validate_percentage(beneficiary_2_percent)
        self.beneficiary_3_percent = self._validate_percentage(beneficiary_3_percent)
        self.phone_number = phone_number
        self.last_call_topic = last_call_topic
        self.last_call_status = last_call_status

    def _validate_percentage(self, percent: Optional[float]) -> Optional[float]:
        if percent is not None and (percent < 0 or percent > 100):
            raise ValueError(f"Percentage {percent} is out of range. It must be between 0 and 100.")
        return percent

    def __repr__(self) -> str:
        return (f"ContactInformation(name={self.name!r}, policyholder_name={self.policyholder_name!r}, "
                f"policy_number={self.policy_number!r}, beneficiary_1={self.beneficiary_1!r}, "
                f"beneficiary_2={self.beneficiary_2!r}, beneficiary_3={self.beneficiary_3!r}, "
                f"beneficiary_1_percent={self.beneficiary_1_percent!r}, beneficiary_2_percent={self.beneficiary_2_percent!r}, "
                f"beneficiary_3_percent={self.beneficiary_3_percent!r}, phone_number={self.phone_number!r}, "
                f"last_call_topic={self.last_call_topic!r}, last_call_status={self.last_call_status!r})")

    def __str__(self) -> str:
        return (f"Contact Information:\n"
                f"Name: {self.name}\n"
                f"Policyholder Name: {self.policyholder_name}\n"
                f"Policy Number: {self.policy_number}\n"
                f"Beneficiary 1: {self.beneficiary_1} ({self.beneficiary_1_percent}%)\n"
                f"Beneficiary 2: {self.beneficiary_2} ({self.beneficiary_2_percent}%)\n"
                f"Beneficiary 3: {self.beneficiary_3} ({self.beneficiary_3_percent}%)\n"
                f"Phone Number: {self.phone_number}\n"
                f"Last Call Topic: {self.last_call_topic}\n"
                f"Last Call Status: {self.last_call_status}")
