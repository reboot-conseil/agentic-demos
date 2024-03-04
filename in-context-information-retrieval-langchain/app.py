from dotenv import load_dotenv
load_dotenv()

from langchain.chains.question_answering import load_qa_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_vertexai import VertexAI
from langchain.prompts import PromptTemplate
import os
from urllib3 import request

# using the latest model from Google
chat_model = VertexAI(
    # context window of 32k tokens
    model_name="gemini-pro",
    safety_settings={}
)

# creating a `./data` directory to store our raw contents if not exists
if not os.path.exists('./data'):
    os.makedirs('./data')

# using an example pdf file
pdf_url = "https://blog.mozilla.org/wp-content/blogs.dir/278/files/2023/12/Mozilla-2023-AI-Year-in-Review.pdf"
loader = PyPDFLoader(pdf_url)
pages = loader.load_and_split()

# crafting a generic prompt
prompt_template ="""You are a knowledge worker.
You will be provided a question and an input text.
Your job is to answer to the provided question using ONLY the provided input text.
If the answer to the question '{question}' is not present in the input text, you should answer 'The answer to the question is not present in the input text.'
Here is the input text, delimited by the dashes below:
------------------------------------
{context}
------------------------------------"""
prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

# using a stuff chain
stuff_chain = load_qa_chain(
    chat_model,
    chain_type="stuff",
    prompt=prompt
)
# now let's try a question about content that is in the beginning of the document
question = "What is the fastest-growing consumer internet app of all time?"
# # ! do note that this will cost you some tokens
answer = stuff_chain(
    {
        "input_documents": pages[0:10],
        "question": question
    }
)
print(answer['output_text'])
stupid_question = "What do we have for lunch?"
answer = stuff_chain(
    {
        "input_documents": pages[0:10],
        "question": stupid_question
    }
)
print("\n")
print(answer['output_text'])