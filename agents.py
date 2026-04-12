from crewai import Agent, LLM
from Tools import file_reader, csv_searcher, report_writer
from dotenv import load_dotenv
import os

load_dotenv()

# Using Groq Llama 3.3 70b as the primary model for high-reasoning accuracy.
primary_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

DEFAULT_SETTINGS = {
    "cache": True,
    "verbose": False,
    "respect_context_window": True,
    "use_system_prompt": True,
    "max_execution_time": 300,
}


# CONSOLIDATED AGENTS (To prevent 429 Quota issues)
Senior_Fairness_Auditor = Agent(
  role='Senior Algorithmic Fairness Auditor & Strategist',
  goal='Detect bias, explain its impact, and suggest mitigation strategies in a single unified analysis.',
  llm=primary_llm,
  backstory="""You are a world-class AI Ethics consultant with 20 years of experience. You combine 
  the skills of a data scientist (detecting bias), a communicator (explaining it clearly), and 
  a legal strategist (suggesting fixes). You strictly analyze only the provided data and never 
  hallucinate information or sectors not present in the source.""" ,
  tools=[file_reader, csv_searcher,report_writer],
  max_rpm=15,
  max_iter=3,
  **DEFAULT_SETTINGS
)

Updater = Agent(
  
  role='Model Improvement Executor',
  goal='To apply approved fixes and update the model for better fairness',
  llm=primary_llm,
  backstory="""You are a machine learning engineer responsible for transforming recommendations into real improvements, has a 18 years of experience. You takes approved fixes and carefully applies them to production systems.""",
  tools=[file_reader,report_writer],
  max_rpm=10,
  max_iter=3,
  **DEFAULT_SETTINGS
)

Technical_Reporter = Agent(
    role='Chief Fairness Auditor & Technical Reporter',
    goal='Synthesize complex auditing metrics into a professional, data-driven technical report.',
    llm=primary_llm,
    backstory="""You are a world-class technical writer and AI auditor with 20 years of experience 
    writing whitepapers for the IEEE and leading ethical consulting firms. Your expertise lies in 
    documenting algorithmic bias with extreme precision and faithfulness to the source data. You 
    convert findings into a cohesive report that is strictly evidence-based, avoiding generic 
    boilerplate and forced length padding.""" ,
    tools=[report_writer],
    max_rpm=20,
    max_iter=5,
    **DEFAULT_SETTINGS
)
