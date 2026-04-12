import os
import urllib.request
from agents import Senior_Fairness_Auditor, Updater, Technical_Reporter
from Tasks import (Unified_Fairness_Analysis, Updates_data, Comprehensive_Audit_Report)
from crewai import Crew, Process 

# Define Phase 1 Crew (Analysis & Advisory)
# Optimized for Lean Architecture: Only 2 agents to minimize API calls
Phase1_Crew = Crew(
  agents=[Senior_Fairness_Auditor, Technical_Reporter],
  tasks=[Unified_Fairness_Analysis, Comprehensive_Audit_Report],
  process=Process.sequential,
  respect_context_window=True,
  verbose=False,
  cache=True
)

# Define Phase 2 Crew (Execution)
Phase2_Crew = Crew(
  agents=[Updater],
  tasks=[Updates_data],
  process=Process.sequential,
  respect_context_window=True,
  verbose=False,
  cache=True
)

def run_phase1(user_data):
    """Runs the primary auditing crew."""
    result = Phase1_Crew.kickoff(inputs={"user_data": user_data})
    return result.raw

def run_phase2(user_data="Apply approved fixes."):
    """Runs the execution crew."""
    result = Phase2_Crew.kickoff(inputs={"user_data": user_data})
    return result.raw

# --- Main Execution (For CLI/Direct usage) ---
if __name__ == "__main__":
    from router import determine_intent, get_general_response
    print("Welcome to EthosAI!")
    user_input = input("Please enter your data, or paste a link:\n> ").strip()

    # Data ingestion logic...
    user_data = user_input
    if user_input.startswith("http"):
        try:
            response = urllib.request.urlopen(user_input)
            user_data = response.read().decode('utf-8')
        except: pass

    intent = determine_intent(user_input, has_file=False)
    
    if intent == "GENERAL":
        print(get_general_response(user_input))
    elif intent == "PHASE_1":
        print("Launching Lean Auditing Crew...")
        result = run_phase1(user_data)
        print(result)
    elif intent == "PHASE_2":
        print("Launching Model Update Crew...")
        result = run_phase2(user_data)
        print(result)