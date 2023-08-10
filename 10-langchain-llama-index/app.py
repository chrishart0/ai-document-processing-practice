from langchain.agents import Tool
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from llama_index import VectorStoreIndex, SimpleDirectoryReader

# try using GPT List Index!
from langchain import OpenAI
from langchain.llms import OpenAIChat
from langchain.agents import initialize_agent

from llama_index import ListIndex
from llama_index.langchain_helpers.memory_wrapper import GPTIndexChatMemory

import logging
import sys


# Example pulled from: https://github.com/jerryjliu/llama_index/blob/main/examples/langchain_demo/LangchainDemo.ipynb

logging.basicConfig(stream=sys.stdout, level=logging.INFO) # set Logging to DEBUG for more detailed outputs
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout)) 

logging.info("Reading data...")
documents = SimpleDirectoryReader("./data").load_data()

logging.info("making vector store...")
index = VectorStoreIndex.from_documents(documents=documents)


tools = [
    Tool(
        name="LlamaIndex",
        func=lambda q: str(index.as_query_engine().query(q)),
        description="useful for when you want to answer questions about the author. The input to this tool should be a complete english sentence.",
        return_direct=True,
    ),
]

logging.info("Define index")
index = ListIndex([])

# NOTE: you can also use a conversational chain

logging.info("Set memory")
memory = GPTIndexChatMemory(
    index=index,
    memory_key="chat_history",
    query_kwargs={"response_mode": "compact"},
    # return_source returns source nodes instead of querying index
    return_source=True,
    # return_messages returns context in message format
    return_messages=True,
)

logging.info("Define LLM")
llm = OpenAIChat(temperature=0)
# llm=OpenAI(temperature=0)

logging.info("Intialize Agent")
agent_executor = initialize_agent(
    [], llm, agent="conversational-react-description", memory=memory
)

# memory = ConversationBufferMemory(memory_key="chat_history")
# llm = ChatOpenAI(temperature=0)
# agent_executor = initialize_agent(
#     tools, llm, agent="conversational-react-description", memory=memory
# )

print(agent_executor.run(input="hi, i am bob"))

print(agent_executor.run(input="What did the author do growing up?"))

# print(agent_executor.run(input="What is the authors name?"))

# print(agent_executor.run(input="Do you remeber my name?"))

# print(agent_executor.run(input="What was my first question"))