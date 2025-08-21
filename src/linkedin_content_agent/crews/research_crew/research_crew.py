from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool, WebsiteSearchTool
from linkedin_content_agent.schemas import ResearchReport
from typing import List
from dotenv import load_dotenv
import os, warnings

# Load environment variable
load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = os.environ.get("MODEL")
os.environ["CREWAI_DISABLE_TELEMETRY"] = "True" # Disable telemetry message in the terminal
warnings.filterwarnings("ignore") # Suppress unimportant warnings

# Initialize LLM model
gemini_llm = LLM(
    model=GEMINI_MODEL,
    api_key=GEMINI_API_KEY,
    max_tokens=2048,
    response_format=ResearchReport
)

# Initialize the tools
search_tool = SerperDevTool()
website_search_tool = WebsiteSearchTool(
    config=dict(
        llm={
            "provider": "google",
            "config": {
                "model": GEMINI_MODEL,
                "api_key": GEMINI_API_KEY
            }
        },
        embedder={
            "provider": "google",
            "config": {
                "model": "models/text-embedding-004",
                "task_type": "retrieval_document"
            }
        }
    )
)

# Initialize the Research crew
@CrewBase
class ResearchCrew():
    """Set up agents and tasks from yaml file"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            verbose=True,
            tools=[search_tool, website_search_tool],
            llm=gemini_llm
        )

    @agent
    def fact_checker(self) -> Agent:
        return Agent(
            config=self.agents_config['fact_checker'], # type: ignore[index]
            verbose=True,
            tools=[search_tool],
            llm=gemini_llm
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )

    @task
    def fact_checking_task(self) -> Task:
        return Task(
            config=self.tasks_config['fact_checking_task'], # type: ignore[index]
            context=[self.research_task()],
            output_file="output/research_result.json"
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=False,
        )
