import os
from dotenv import load_dotenv
from crewai_tools import FileReadTool, FileWriterTool, CSVSearchTool

load_dotenv()

# Hack to bypass Pydantic validation in crewai_tools that strictly checks for OpenAI Key
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = "sk-placeholder"

# 1. Log Reader Tool
# Used by agents to read raw data, logs, and technical metrics from local files.
file_reader = FileReadTool()

# We specify an absolute path to avoid file generation conflicts or nested db paths
LOCAL_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".ethosai_chroma_clean")

# 2. In-Depth CSV Search Tool
# Configured via embedchain config standard
csv_searcher = CSVSearchTool(
    config={
        "llm": {
            "provider": "groq",
            "config": {
                "model": "groq/llama-3.3-70b-versatile",
            },
        },
        "embedder": {
            "provider": "huggingface",
            "config": {
                "model": "sentence-transformers/all-MiniLM-L6-v2",
            },
        },
        "vectordb": {
            "provider": "chromadb",
            "config": {
                "dir": LOCAL_DB_PATH,
                "allow_reset": True
            },
        },
    }
)

# 3. Log/Report Writer Tool
# Enables agents to explicitly save their findings, refined logs, or 
# technical reports directly to the workspace.
report_writer = FileWriterTool()

# Note: These tools are initialized without specific paths, allowing agents 
# to provide paths dynamically at runtime based on user input.
