
from agents import Bias_lens,Explainer,Fix_advisor,Updater,Log_generator,Log_insights
from Tasks import (Bias_detection,Explains_issues,Correction_advise,Updates_data,Log_generation,Insights_data)
from crewai import Crew, Process 

# Define the Ethos Crew with the  sequential workflow
Ethos_crew = Crew(
  agents=[Bias_lens, Explainer, Fix_advisor, Updater, Log_generator, Log_insights ],
  tasks=[Bias_detection, Explains_issues, Correction_advise, Updates_data, Log_generation, Insights_data ],
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