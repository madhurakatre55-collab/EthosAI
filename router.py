import os
# Removed google.generativeai for Groq migration
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

# Initialize the router model using Groq
router_llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)
USE_GROQ = True

def determine_intent(user_input, has_file=False):
    # FAST PATH: If it's a file or clearly a data source, skip the LLM call to save quota.
    user_input_lower = user_input.lower()
    if has_file or user_input.startswith("http") or user_input.startswith("/") or user_input.startswith("c:\\") or ".csv" in user_input_lower or ".json" in user_input_lower:
        return "PHASE_1"
        
    prompt = f"""
    You are an intent router for an AI Auditing system.
    Analyze the user's input and classify it into EXACTLY ONE of the following three categories: GENERAL, PHASE_1, or PHASE_2.
    
    - GENERAL: Greetings, general questions.
    - PHASE_1: Analyze data, find bias, check fairness, or URL/file path provided.
    - PHASE_2: Approve fix, update model, generate logs.
    
    User Input: "{user_input}"
    Classification:"""
    
    if USE_GROQ:
        response = router_llm.call([{"role": "user", "content": prompt}])
        intent = response.strip().upper()
    else:
        # Fallback (Should not be reached if USE_GROQ is True)
        intent = "GENERAL"
    
    if "PHASE_1" in intent: return "PHASE_1"
    if "PHASE_2" in intent: return "PHASE_2"
    return "GENERAL"

def get_general_response(user_input):
    prompt = f"A user has asked: {user_input}. Respond briefly (3-4 sentences) as EthosAI, an automated fairness auditor."
    
    if USE_GROQ:
        return router_llm.call([{"role": "user", "content": prompt}])
    else:
        return "EthosAI is currently switching to Groq. Please try again in a moment."
