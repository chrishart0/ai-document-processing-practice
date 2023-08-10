import os
import openai

# import panel as pn  # GUI
# pn.extension()

openai.api_key  = os.environ['OPENAI_API_KEY']

llm_name = "gpt-3.5-turbo"


### Prepare Vectore Store ###
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
persist_directory = 'docs/chroma/'
embedding = OpenAIEmbeddings()
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)


question = "What are major topics for this class?"
docs = vectordb.similarity_search(question,k=3)


from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(model_name=llm_name, temperature=0)
print(llm.predict("Hello world!"))


# Build prompt
from langchain.prompts import PromptTemplate
template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use three sentences maximum. Keep the answer as concise as possible. Always say "thanks for asking!" at the end of the answer. 
{context}
Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"],template=template,)

# Run chain
print("Prompt with no history")
from langchain.chains import RetrievalQA
question = "Is probability a class topic?"
qa_chain = RetrievalQA.from_chain_type(llm,
                                       retriever=vectordb.as_retriever(),
                                       return_source_documents=True,
                                       chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})


result = qa_chain({"query": question})
print(result["result"])
print("")
print("-----------------")

########################
### Configure memory ###
########################

from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

######################################
### Conversational Retrieval Model ###
######################################
# Pass in LLM, pass in retriever, and pass in memory and this will add a step to condense the question and the hisotry into one prompt

print("Conversation starts")
from langchain.chains import ConversationalRetrievalChain
retriever=vectordb.as_retriever()
qa = ConversationalRetrievalChain.from_llm(
    llm,
    retriever=retriever,
    memory=memory
)

question = "Is probability a class topic?"
result = qa({"question": question})

print("User:", question)
print("LLM:", result['answer'])
print("")

question = "why are those prerequesites needed?"
result = qa({"question": question})

print("User:", question)
print("LLM:", result['answer'])
print("")

question = "What other prerequisits are there?"
result = qa({"question": question})

print("User:", question)
print("LLM:", result['answer'])
print("")



question = "Look through the rest of the lectures. Are there any other prereqs required for the class?"
result = qa({"question": question})

print("User:", question)
print("LLM:", result['answer'])
print("")




print("")