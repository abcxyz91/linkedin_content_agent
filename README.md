# LinkedIn Content Agent

This project is a CrewAI-powered workflow designed to automate the
creation of engaging LinkedIn content. It leverages a team of AI agents
to research a given topic, verify the information, and then write and
edit a LinkedIn post.

## Features ✨

-   **Automated Research**: The research crew, consisting of a Research
    Specialist and a Fact Checker, gathers and validates up-to-date
    information on any given topic.
-   **Content Creation**: The content crew, with a Content Strategist
    and a Content Editor, drafts and polishes a LinkedIn post based on
    the researched information.
-   **Sequential Workflow**: The entire process is orchestrated in a
    sequential flow, ensuring that each step is completed before the
    next one begins.
-   **Customizable**: The agents and tasks are defined in YAML files,
    making it easy to customize their roles, goals, and instructions.

## Project Structure 🌳

    ├── src
    │   └── linkedin_content_agent
    │       ├── __pycache__
    │       ├── crews
    │       │   ├── content_crew
    │       │   │   ├── __pycache__
    │       │   │   ├── config
    │       │   │   │   ├── agents.yaml
    │       │   │   │   └── tasks.yaml
    │       │   │   └── content_crew.py
    │       │   └── research_crew
    │       │       ├── __pycache__
    │       │       ├── config
    │       │       │   ├── agents.yaml
    │       │       │   └── tasks.yaml
    │       │       └── research_crew.py
    │       ├── tools
    │       │   └── custom_tool.py
    │       ├── main.py
    │       └── schemas.py
    ├── output
    ├── .env
    ├── .gitignore
    ├── pyproject.toml
    ├── README.md
    └── uv.lock


## Getting Started 🚀

### Prerequisites

-   Python 3.10+
-   crewAI
-   google-generativeai
-   An API key for a supported LLM provider (e.g., Google's Gemini)

### Installation

Clone the repository:

``` bash
git clone <https://github.com/abcxyz91/linkedin_content_agent>
cd <linkedin_content_agent>
```

Install the dependencies:

``` bash
# Install uv package manager and crewai framework
pip install uv
uv tool install crewai

# Recommended: setup virtual environment with uv
uv venv
.venv\Scripts\activate # Windows
source .venv/bin/activate # macOS and Linux
crewai install
uv sync
```

Set up your environment variables:\
Create a `.env` file in the root of the project and add your API key:

    OPENAI_API_KEY=your_openai_api_key
    # or
    GEMINI_API_KEY=your_gemini_api_key
    # or
    ANTHROPIC_API_KEY=your_anthropic_api_key
    MODEL="gemini/gemini-2.5-flash-lite" or "openai/gpt-4o" or "anthropic/claude..."

## Usage ▶️

To run the LinkedIn Content Flow, execute the script:

``` bash
crewai flow kickoff
```

The script will prompt you to enter a topic and an industry. Once
provided, the flow will kick off, and the final content will be saved in
the `output/content_result.txt` file.

You can also generate a visual representation of the flow by running:

``` bash
crewai flow plot
```

This will create a `linkedin_content_agent.html` file.

## Crews and Agents 🤖

This project consists of two main crews, each with specialized agents:

### Research Crew

-   **Researcher**: This agent is responsible for gathering relevant and
    up-to-date information about a given topic. It uses the
    SerperDevTool and WebsiteSearchTool to find statistics, trends, and
    expert opinions.
-   **Fact Checker**: This agent meticulously verifies the accuracy and
    credibility of the information gathered by the researcher, ensuring
    that all claims are backed by reliable evidence.

### Content Crew

-   **Content Writer**: A LinkedIn Content Strategist who crafts a
    compelling and engaging post based on the validated research report.
-   **Content Editor**: A professional editor who refines and polishes
    the drafted content, optimizing it for clarity, tone, and
    engagement.

## Tasks ✅

The workflow is broken down into the following tasks:

1.  **Research Task**: The researcher conducts comprehensive research on
    the given topic and industry.
2.  **Fact-Checking Task**: The fact-checker reviews the research report
    for accuracy and credibility.
3.  **Drafting Task**: The content writer creates a LinkedIn post using
    the validated research.
4.  **Editing Task**: The content editor reviews and polishes the draft,
    adding relevant hashtags and formatting.
