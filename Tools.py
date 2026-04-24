import os
from dotenv import load_dotenv
from crewai_tools import FileReadTool, FileWriterTool

load_dotenv()

# Hack to bypass Pydantic validation in crewai_tools that strictly checks for OpenAI Key
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = "sk-placeholder"

# 1. File Reader Tool
# Used by agents to read raw data, logs, and technical metrics from local files.
file_reader = FileReadTool()

# NOTE: CSVSearchTool (ChromaDB + HuggingFace embeddings) was removed.
# It required ~300MB of RAM to load the embedding model — too heavy for Render's
# 512MB free tier and caused 502 crashes. The CSV data is already injected into
# the agent prompt as text by app.py, so vector search is not needed.

# 2. Report Writer Tool
# Enables agents to explicitly save their findings and technical reports.
report_writer = FileWriterTool()
