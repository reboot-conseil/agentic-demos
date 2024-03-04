from dotenv import load_dotenv
load_dotenv()

from langchain.chains.question_answering import load_qa_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores.redis import Redis
from langchain_google_vertexai import VertexAI, VertexAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
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

# setting up an embeddings model instance
embeddings = VertexAIEmbeddings(
    model_name="textembedding-gecko@003",
)

# using a text splitter that will split the joined context of the document into chunks of overlapping tokens
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1700, chunk_overlap=300)
context = "\n\n".join([str(page.page_content) for page in pages])
chunks = text_splitter.split_text(context)

# using Redis as a vector store
redis_url = "redis://redis:6379"
rds = Redis.from_texts(
    chunks,
    embeddings,
    redis_url=redis_url,
    index_name="rag_documents",
)

# you can run (from within the container):
    # `rvl index listall --port 6379 --host redis` to see the list of indexes
    # `rvl index info --index rag_documents --port 6379 --host redis` to see the index info
    # `rvl stats -i rag_documents --port 6379 --host redis` to see the stats of the index

# now let's try vectory similarity search
question = "What happened in Texas regarding AI in 2023?"
# the lambda_mult parameter controls the diversity of the results, the lower the more diverse
docs = rds.max_marginal_relevance_search(question, lambda_mult=0.5)
# print(docs)

# using a stuff chain
stuff_chain = load_qa_chain(
    chat_model,
    chain_type="stuff",
    prompt=prompt
)

# # ! do note that this will cost you some tokens
answer = stuff_chain(
    {
        "input_documents": docs,
        "question": question
    }
)
print(answer["output_text"])
# controlling the output on irrelevant questions
stupid_question = "What do we have for lunch?"
answer = stuff_chain(
    {
        "input_documents": docs,
        "question": stupid_question
    }
)
print("\n")
print(answer['output_text'])