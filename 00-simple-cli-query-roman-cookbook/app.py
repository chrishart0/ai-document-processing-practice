import os
from llama_index import VectorStoreIndex, SimpleDirectoryReader

# Get key and put into env so it can be used by llama index
with open('key.txt', 'r') as file:
    api_key = file.read().strip()

os.environ["OPENAI_API_KEY"] = 'YOUR_OPENAI_API_KEY'

documents = SimpleDirectoryReader('data').load_data()
index = VectorStoreIndex.from_documents(documents)