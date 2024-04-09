from dotenv import load_dotenv
load_dotenv()

import logging
from llama_index.core import (
    load_index_from_storage,
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex
)
from os import path
import sys

# ! uncomment if you want to see what's happening under the hood
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


# check if storage already exists
PERSIST_DIR = "./storage"
index = None
# if not exists, building an index over the documents in the `data` directory
if not path.exists(PERSIST_DIR):
    documents = SimpleDirectoryReader("data").load_data()
    index = VectorStoreIndex.from_documents(documents)
    # storing the index
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

query_engine = index.as_query_engine()

# getting the query from the command line
query = "what is this text about"
if len(sys.argv) >= 2:
    query = " ".join(sys.argv[1:])

response = query_engine.query(query)
print(response)