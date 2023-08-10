from llama_index import StorageContext, load_index_from_storage
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# rebuild storage context
storage_context = StorageContext.from_defaults(persist_dir="./storage")

# load index
index = load_index_from_storage(storage_context)

query_engine = index.as_query_engine()

while True:
    try:
        print("")
        print("What is your question? (type 'quit' to exit):")
        inp = input()
        print("")

        # Allow user to exit the loop
        if inp.lower() == 'quit':
            print("Exiting the program. Bye!")
            break

 
        response = query_engine.query(inp)
        print(response)
        print("")
        print("=====================")

    except Exception as e:
        print("An error occurred:", e)
