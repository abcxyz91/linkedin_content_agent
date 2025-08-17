from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from dotenv import load_dotenv
import os

# Load environment variable
load_dotenv()
os.environ["CREWAI_DISABLE_TELEMETRY"] = "True" # Disable telemetry message in the terminal

@CrewBase
class ContentCrew():
    """Set up agents and tasks from yaml file"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def content_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['content_writer'], # type: ignore[index]
            verbose=False
        )

    @agent
    def content_editor(self) -> Agent:
        return Agent(
            config=self.agents_config['content_editor'], # type: ignore[index]
            verbose=False
        )

    @task
    def drafting_task(self) -> Task:
        return Task(
            config=self.tasks_config['drafting_task'], # type: ignore[index]
        )

    @task
    def editing_task(self) -> Task:
        return Task(
            config=self.tasks_config['editing_task'], # type: ignore[index]
            context=[self.drafting_task()],
            output_file="content_result.txt"
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Content crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=False,
        )
