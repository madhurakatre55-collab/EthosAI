import os
import urllib.request

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
if __name__ == "__main__":
    print("Welcome to EthosAI!")
    user_input = input("Please enter your data, or paste an external file link (URL / path):\n> ").strip()

    # Check if it is a website or raw URL link
    if user_input.startswith("http://") or user_input.startswith("https://"):
        print("Detected external link! Downloading data...")
        try:
            response = urllib.request.urlopen(user_input)
            user_data = response.read().decode('utf-8')
        except Exception as e:
            print(f"Error fetching URL: {e}")
            user_data = user_input
    # Check if it is a local file path
    elif os.path.exists(user_input) and os.path.isfile(user_input):
        print("Detected local file! Reading contents...")
        try:
            with open(user_input, 'r', encoding='utf-8') as f:
                user_data = f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            user_data = user_input
    else:
        user_data = user_input

    print("\nLaunching EthosAI Crew...")
    result = Ethos_crew.kickoff(
        inputs={
            "user_data": user_data
        }
    )

    # Accessing the output
    print("\nCrew Execution Complete!")
    print("Final Output:")
    print(result.raw)