import os
from dotenv import load_dotenv
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

load_dotenv()

# NOTE: crewai-tools package was removed because installing it pulls in
# ChromaDB, HuggingFace sentence-transformers, and embedchain (~300MB RAM),
# which crashes Render's 512MB free tier with a 502.
# These lightweight custom tools replicate the same functionality.


class _FileReadInput(BaseModel):
    file_path: str = Field(description="The path to the file to read.")


class _FileReadTool(BaseTool):
    name: str = "Read File"
    description: str = "Reads the full text content of any file (CSV, TXT, MD, etc.) given its path."
    args_schema: Type[BaseModel] = _FileReadInput

    def _run(self, file_path: str) -> str:
        try:
            with open(file_path.strip(), 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file '{file_path}': {str(e)}"


class _FileWriteInput(BaseModel):
    filename: str = Field(description="Name of the file to write, e.g. 'report.md'")
    content: str = Field(description="The full text content to write into the file.")
    directory: str = Field(default="audit_reports", description="Directory to save the file in.")


class _FileWriteTool(BaseTool):
    name: str = "Write File"
    description: str = "Saves text content to a file on disk. Use this to persist audit reports and resolution logs."
    args_schema: Type[BaseModel] = _FileWriteInput

    def _run(self, filename: str, content: str, directory: str = "audit_reports") -> str:
        try:
            os.makedirs(directory, exist_ok=True)
            filepath = os.path.join(directory, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Successfully saved report to '{filepath}'."
        except Exception as e:
            return f"Error writing file '{filename}': {str(e)}"


# Exported tool instances used by agents
file_reader = _FileReadTool()
report_writer = _FileWriteTool()
