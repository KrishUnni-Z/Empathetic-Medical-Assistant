import streamlit as st
from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel, ModelProvider, Model

# Setup GPT client using GitHub Token for Inference API
client = AsyncOpenAI(
    base_url="https://models.inference.ai.azure.com",       # GitHub Inference endpoint
    api_key=st.secrets["GITHUB_TOKEN"]                      # GitHub PAT with access to inference
)

# Define model provider
class EmpatheticModelProvider(ModelProvider):
    def get_model(self, model_name) -> Model:
        return OpenAIChatCompletionsModel(model=model_name, openai_client=client)

# Choose model — typically "gpt-4o"
model = "gpt-4o"
MODEL_PROVIDER = EmpatheticModelProvider()
