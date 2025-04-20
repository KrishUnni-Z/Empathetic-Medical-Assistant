from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel, ModelProvider, Model
import os
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.environ["GITHUB_TOKEN"],
)

class EmpatheticModelProvider(ModelProvider):
    def get_model(self, model_name) -> Model:
        return OpenAIChatCompletionsModel(model=model_name, openai_client=client)

model = "gpt-4o"
MODEL_PROVIDER = EmpatheticModelProvider()
