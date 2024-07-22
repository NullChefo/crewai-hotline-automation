import os

from crewai_tools import SerperDevTool
# Set desired LLM (llama3:8b) from the Ollama running in local.
from langchain.llms import Ollama

from crewai import Agent, Task, Crew, Process

ollama_model = Ollama(
    base_url='http://ollama:11434',
    model="llama3:8b")

os.environ["OTEL_SDK_DISABLED"] = "true"

# Use server.dev API for Researcher agent to access to the web
os.environ["SERPER_API_KEY"] = "{Please insert your serper API key}"  # serper.dev API key
search_tool = SerperDevTool()

# Define required role and goal of agents by using Crewai Pacakge
# Define Researcher agent
researcher = Agent(
    role='Researcher',
    goal='Discover a newest and attracting topic about DevOps',
    backstory="You're world class researcher working on a big IT company",
    verbose=True,
    allow_delegation=False,
    llm=ollama_model,
    tools=[search_tool]
)

# Define Writer agent
writer = Agent(
    role='Writer',
    goal='Create DevOps blog post',
    backstory="You're a best technical writer who is specialized on writing IT content",
    verbose=True,
    allow_delegation=False,
    llm=ollama_model
)

# Define Proofreader agent
proofreader = Agent(
    role='Proofreader',
    goal='Edit and proofread technical article',
    backstory="You're a famous proofreader who is specialized on IT domain",
    verbose=True,
    allow_delegation=False,
    llm=ollama_model
)

# Define tasks executed by the defined agents
research_task = Task(
    description='Investigate the latest DevOps news',
    agent=researcher,
    expected_output = 'A comprehensive 3 paragraphs long report on the latest and famous DevOps.'
)

writing_task = Task(
    description='Write a blog post about DevOps with one topic provided from the researcher',
    agent=writer,
    expected_output='A 4 paragraph article about DevOps formatted as markdown.',
)

proofreading_task = Task(
    description='Proofread the provided blog post to make more natural article',
    agent=proofreader,
    expected_output='A 4 paragraph article about DevOps formatted as markdown.',
)

# Define workflow withe the defined agents and tasks
crew = Crew(
    agents=[researcher, writer, proofreader],
    tasks=[research_task, writing_task, proofreading_task],
    llm=ollama_model,
    verbose=2,
    process=Process.sequential # Tasks will be executed by the agents sequentially (researcher -> writer -> proofreader)
)

# Start the workflow and print its logs
result = crew.kickoff()
print(result)