from llama_index import VectorStoreIndex, SimpleDirectoryReader

import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


print("Loading Data...")
documents = SimpleDirectoryReader('./data').load_data()

print("Making vector store...")
index = VectorStoreIndex.from_documents(documents)

# Persiste the data store
index.storage_context.persist()
