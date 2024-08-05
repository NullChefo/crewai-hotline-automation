from langchain_community.tools import DuckDuckGoSearchRun

from utils.voiceFlowIntegration import get_transcripts


# from crewai import Agent, Task, Crew, Process


def knownNumberChecker(caller_id: str) -> bool:

    # Get the phone number from the HubSpot when provide
    # if present return true

    voiceflowTranscripts = get_transcripts(caller_id)

    return True



# def startKnownNumberCheckerCrew(caller_id: str):