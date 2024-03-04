from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import HumanMessage
from langchain_google_vertexai import ChatVertexAI

llm = ChatVertexAI(model_name="gemini-1.0-pro-vision")

image_message = {
    "type": "image_url",
    "image_url": {"url": "https://cdn.snapi.dev/images/v1/d/e/498-2305697.jpg"},
    # you can also pass a file url
    # "image_url": {"url": "vertexai-role.png"},
}
text_message = {
    "type": "text",
    "text": "What is shown in this image?",
}
message = HumanMessage(content=[text_message, image_message])

output = llm([message])
print(output.content)