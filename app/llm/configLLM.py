import os
from dotenv import load_dotenv

try:
    load_dotenv()

    class Config:
        AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
        AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
        AZURE_OPENAI_VERSION = os.getenv("AZURE_OPENAI_VERSION")
except Exception as e:
    print(f"Error loading configuration: {str(e)}")
