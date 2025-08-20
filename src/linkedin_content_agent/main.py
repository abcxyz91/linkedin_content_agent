from crewai.flow.flow import Flow, listen, start
from linkedin_content_agent.crews.research_crew.research_crew import ResearchCrew
from linkedin_content_agent.crews.content_crew.content_crew import ContentCrew
from linkedin_content_agent.schemas import ResearchFlowState, ResearchReport
from pydantic import BaseModel, ValidationError
from dotenv import load_dotenv
import json, os, warnings, asyncio


# Load environment variables
load_dotenv()
os.environ["CREWAI_DISABLE_TELEMETRY"] = "True" # Disable telemetry message in the terminal
warnings.filterwarnings("ignore") # Suppress unimportant warnings

class LinkedinContentFlow(Flow[ResearchFlowState]):
    """Flow for researching & creating a comprehensive & engaging content on any topic, ready to post on LinkedIn"""

    # Construct the class to accept parameters such as topic & industry
    def __init__(self, topic: str, industry: str):
        super().__init__() # # call the parent class initializer to set up inherited attributes
        self._topic = topic # set instance attributes
        self._industry = industry # set instance attributes

    @start()
    def get_user_input(self):
        self.state.topic = self._topic.strip()
        self.state.industry = self._industry.strip()

        # Inject current date into Flow state
        # No need due to default schemas
        
        print(f"\nStart reseach on {self.state.topic} for {self.state.industry}...\n")
        return self.state
    
    @listen(get_user_input)
    async def research(self, state):
        """Call the specialized crew to research"""
        # Ensure output directory exists before saving
        os.makedirs("output", exist_ok=True)

        result = await ResearchCrew().crew().kickoff_async(inputs={
                "topic": self.state.topic,
                "industry": self.state.industry,
                "current_date": self.state.current_date.isoformat(), # Change from Python object to string format
            })
        
        try:
            # LLM response could be a dict or a string, hence the parsing will handle both case
            data = result if isinstance(result, dict) else json.loads(result.raw)

            # Parse the data return from Research crew into Flow state
            self.state.research_report = ResearchReport(**data)
        except (json.JSONDecodeError, ValidationError, TypeError) as e:
            print(f"Error happening: {e}")

        print(f"\nFinish reseach on {self.state.topic} for {self.state.industry}...\n")
        return self.state
    
    @listen(research)
    async def content(self, state):
        """
        Call the specialized crew to write content.
        The content will be based on research result of other crew.
        """
        result = await ContentCrew().crew().kickoff_async(inputs={
                "topic": self.state.topic,
                "industry": self.state.industry,
                "current_date": self.state.current_date.isoformat(), # Change from Python object to string format
                "research_report": self.state.research_report.model_dump() # Change from ResearchReport object to a dictionary
            })
        
        print(f"\nFinish content creating on {self.state.topic} for {self.state.industry}...\n")
        return self.state
    
async def kickoff():
    """Get input from the user about the content topic and industry space"""
    print("\n=== Create Your Content ===\n")

    # Get user input & validate
    while True:
        topic = input("What topic would you like to research for? ")
        if topic:
            break
        print("Please enter a topic")

    while True:
        industry = input(f"What industry space of this topic {topic}? ")
        if industry:
            break
        print("Please enter topic's industry")

    """Run the LinkedIn Content flow"""
    try:
        flow = LinkedinContentFlow(topic=topic, industry=industry)
        await flow.kickoff_async()
        
        print("\n=== Flow Complete ===")
        print("Your comprehensive content is ready in the output directory.")
        print("Open output/content_result.txt to view it.")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")

def plot():
    """Generate a visualization of the flow"""
    flow = LinkedinContentFlow(topic="example", industry="example")
    flow.plot("linkedin_content_agent")
    print("Flow visualization saved to linkedin_content_agent.html")

if __name__ == "__main__":
    asyncio.run(kickoff())