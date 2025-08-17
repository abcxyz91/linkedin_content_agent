from crewai.flow.flow import Flow, listen, start
from linkedin_content_agent.crews.research_crew.research_crew import ResearchCrew
from linkedin_content_agent.crews.content_crew.content_crew import ContentCrew
from linkedin_content_agent.schemas import ResearchFlowState, ResearchReport
from pydantic import BaseModel, ValidationError
import json, os

class LinkedinContentFlow(Flow[ResearchFlowState]):
    """Flow for researching & creating a comprehensive & engaging content on any topic, ready to post on LinkedIn"""
    @start()
    def get_user_input(self):
        """Get input from the user about the content topic and industry space"""
        print("\n=== Create Your Content ===\n")

        # Get user input & validate
        while True:
            topic = input("What topic would you like to research for? ")
            if topic:
                self.state.topic = topic.strip()
                break
            print("Please enter a topic")

        while True:
            industry = input(f"What industry space of this topic {topic}? ")
            if industry:
                self.state.industry = industry.strip()
                break
            print("Please enter topic's industry")

        # Inject current date into Flow state
        # No need due to default schemas
        
        print(f"\nStart reseach on {self.state.topic} for {self.state.industry}...\n")
        return self.state
    
    @listen(get_user_input)
    def research(self, state):
        """Call the specialized crew to research"""
        result = ResearchCrew().crew().kickoff(inputs={
                "topic": self.state.topic,
                "industry": self.state.industry,
                "current_date": self.state.current_date,
            })
        
        try:
            # LLM response could be a dict or a string, hence the parsing will handle both case
            data = result if isinstance(result, dict) else json.loads(result)

            # Parse the data return from Research crew into Flow state
            self.state.research_report = ResearchReport(**data)
        except (json.JSONDecodeError, ValidationError, TypeError) as e:
            print(f"Error happenning: {e}")

        print(f"\nFinish reseach on {self.state.topic} for {self.state.industry}...\n")
        return self.state
    
    @listen(research)
    def content(self, state):
        """Call the specialized crew to write content"""
        result = ContentCrew().crew().kickoff(inputs={
                "topic": self.state.topic,
                "industry": self.state.industry,
            })
        
        print(f"\nFinish content creating on {self.state.topic} for {self.state.industry}...\n")
        return self.state
    
def kickoff():
    """Run the LinkedIn Content flow"""
    LinkedinContentFlow().kickoff()
    print("\n=== Flow Complete ===")
    print("Your comprehensive content is ready in the output directory.")
    print("Open output/content_result.txt to view it.")

def plot():
    """Generate a visualization of the flow"""
    flow = LinkedinContentFlow()
    flow.plot("linkedin_content_agent")
    print("Flow visualization saved to linkedin_content_agent.html")

if __name__ == "__main__":
    kickoff()
    
