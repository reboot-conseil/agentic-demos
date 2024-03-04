from dotenv import load_dotenv
load_dotenv()

from langchain_google_vertexai import VertexAI

# using the latest model from Google
chat_model = VertexAI(
    model_name="gemini-pro",
    safety_settings={}
)

prompt = [
    "tell me something nice",
]
res = chat_model.invoke(prompt)
print(res)
