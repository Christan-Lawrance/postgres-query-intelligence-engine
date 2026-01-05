# Author: S Christan Lawrance

from openai import AzureOpenAI
from app.llm.configLLM import Config


class LLM:
    @staticmethod
    def execute(user_prompt):
        try:
            client = AzureOpenAI(
                azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
                api_key=Config.AZURE_OPENAI_API_KEY,
                api_version=Config.AZURE_OPENAI_VERSION,
            )

            # Build initial messages
            messages = [
                {
                    "role": "system",
                    "content": "You are a PostgreSQL performance expert.",
                },
                {"role": "user", "content": user_prompt},
            ]

            llm_response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
            )
            return llm_response.choices[0].message.content

        except Exception as e:
            print(f"LLM execution error: {e}")
            raise
        return None
