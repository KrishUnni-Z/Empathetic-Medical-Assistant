import streamlit as st
from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel, ModelProvider, Model

# Setup GPT client using secrets
client = AsyncOpenAI(
    base_url=st.secrets["AZURE_OPENAI_ENDPOINT"],
    api_key=st.secrets["AZURE_OPENAI_API_KEY"],
)

# Model Provider
class EmpatheticModelProvider(ModelProvider):
    def get_model(self, model_name) -> Model:
        return OpenAIChatCompletionsModel(model=model_name, openai_client=client)

model = st.secrets["AZURE_OPENAI_DEPLOYMENT"]
MODEL_PROVIDER = EmpatheticModelProvider()
