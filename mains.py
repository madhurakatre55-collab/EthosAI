from agents import Bias_lens,Explainer,Fix_advisor,Updater,Log_generator,Log_insights
from work import (Bias_detection,Explains_issue,Fix,Update,Log_generate,Insights)
from crewai import Crew, Process 

# Define the Ethos Crew with the requested sequential workflow
Ethos_crew = Crew(
  agents=[Bias_lens, Explainer, Fix_advisor, Updater, Log_generator, Log_insights ],
  tasks=[Bias_detection, Explains_issue, Fix, Update, Log_generate, Insights ],
  process=Process.sequential,
  respect_context_window=True,
  verbose=True,
  cache=True
)

# --- Corrected Execution Block ---
print("🚀 Launching EthosAI Crew...")
result = Ethos_crew.kickoff(
    inputs={
        "log_file_path": "./task_outputs/log.txt"
    }
)

# Accessing the output
print("\n✨ Crew Execution Complete!")
print("Final Output:")
print(result.raw)