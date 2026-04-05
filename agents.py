import os
from crewai import Agent ,LLM
from dotenv import load_dotenv


load_dotenv()




gemini_flash_llm= LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)



DEFAULT_SETTINGS = {
    "cache": True,
    "verbose": True,
    "respect_context_window": True,
    "use_system_prompt": True,
    "max_execution_time": 300,
}


# AGENTS
Bias_lens = Agent(
  role='Bias Detection Specialist',
  llm=gemini_flash_llm,
  goal='To identify hidden bias in training data and model predictions across different groups (gender, age, etc.)',
  backstory="""You are a senior algorithmic auditor who has spent 15 years in investigating how machine learning systems unintentionally discriminate. You have worked on multiple high-stakes systems where fairness was critical.""",
  tools=[],
  max_rpm=300,
  max_iter=5,
  **DEFAULT_SETTINGS
)


Explainer = Agent(
  role='AI Explanation Specialist',
  goal='To translate technical bias results into simple, human-understandable explanations',
  llm=gemini_flash_llm,
  backstory="""You are an AI expert communicator with deep knowledge of data insights and deep understanding of biased systems and data. Your expertise lies in breaking down intricate model behavior into digestible insights.""",
  tools=[],
  max_rpm=50,
  max_iter=35,
  **DEFAULT_SETTINGS
)




Fix_advisor = Agent(
  role='Bias Mitigation Strategist',
  goal='To suggest effective fixes for detected bias and ensure safe implementation through human approval',
  llm=gemini_flash_llm,
  backstory="""You are a senior AI ethics consultant who has worked on improving fairness in real-world machine learning systems and having 16 years of experience. You specialize in designing mitigation strategies that are both effective and practically implementable.""",
  tools=[],
  max_rpm=10,
  max_iter=3,
  **DEFAULT_SETTINGS
)


Updater = Agent(  
  role='Model Improvement Executor',
  goal='To apply approved fixes and update the model for better fairness',
  llm=gemini_flash_llm,
  backstory="""You are a machine learning engineer responsible for transforming recommendations into real improvements, has a 18 years of experience. You takes approved fixes and carefully applies them to production systems.""",
  tools=[],
  max_rpm=10,
  max_iter=3,
  **DEFAULT_SETTINGS
)


Log_generator = Agent(
  role='Log Data Processor',
  goal='To capture and store every decision made by the ML model for future analysis',
  llm=gemini_flash_llm,
  backstory="""You are a reliability and monitoring engineer responsible for ensuring complete transparency in AI systems. You believe that every decision made by a model should be traceable and auditable.""",
  tools=[],
  max_rpm=10,
  max_iter=3,
  **DEFAULT_SETTINGS
)


Log_insights = Agent(
  role='Behavior Analysis Expert',
  goal='To analyze stored logs and detect bias patterns in real-world model usage',
  llm=gemini_flash_llm,
  backstory="""You are a seasoned data analyst specializing in monitoring deployed AI systems. You've seen how models that appear fair in testing can behave very differently in real-world environments.""",
  tools=[],
  max_rpm=10,
  max_iter=3,
  **DEFAULT_SETTINGS
)
