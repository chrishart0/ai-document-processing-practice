import os
import openai
import ebooklib
from ebooklib import epub
import html2text
import subprocess
import shutil
import sys

openai.api_key  = os.environ['OPENAI_API_KEY']

llm_name = "gpt-3.5-turbo"
# llm_name = "gpt-4"


from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain.document_loaders import TextLoader
from langchain.chains import RetrievalQA,  ConversationalRetrievalChain
from langchain.document_loaders import UnstructuredEPubLoader
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader

from langchain.vectorstores import Chroma



def epub_to_markdown(epub_path):
    book = epub.read_epub(epub_path)
    markdown_output = ''

    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            html_content = item.get_body_content().decode('utf-8')
            markdown_output += html2text.html2text(html_content)

    return markdown_output


def create_db_from_one_epub(file, embedding):
    # load documents
    print("Loading epub file:", file)
    loader = UnstructuredEPubLoader(file)
    documents = loader.load()

    # Convert epub to markdown because langchain processes the metadata better into the vectorstore
    # print("Converting epub to markdown")
    # markdown = epub_to_markdown(file)

    # # First split on markdown headers to ensure good context in the text splits
    # print("Splitting file with MarkdownHeaderTextSplitter")

    # headers_to_split_on = [
    #     ("#", "Header 1"),
    #     ("##", "Header 2"),
    #     ("###", "Header 3"),
    #     ("###", "Header 4"),
    # ]

    # markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    # md_header_splits = markdown_splitter.split_text(markdown)
    

    # Split document futher on characters
    print("Splitting file with RecursiveCharacterTextSplitter")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
    splits = text_splitter.split_documents(documents)

    # Try to remove the tree; if it fails, throw an error using try...except.
    if os.path.exists(persist_directory) and os.path.isdir(persist_directory):
        print("Deleting old choma data store")
        shutil.rmtree(persist_directory)

    # Create the vector store
    print("Creating Vector Store")
    vectordb = Chroma.from_documents(
        documents=splits,
        embedding=embedding,
        persist_directory=persist_directory
    )
    print("Vector DB Collection Count:", vectordb._collection.count())

    return vectordb

def create_db_from_one_pdf(file, embedding):
    # load documents
    print("Loading pdf file:", file)
    loader = PyPDFLoader(file)
    documents = loader.load()

    # split documents
    print("Splitting file")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    splits = text_splitter.split_documents(documents)

    # Try to remove the tree; if it fails, throw an error using try...except.
    if os.path.exists(persist_directory) and os.path.isdir(persist_directory):
        print("Deleting old choma data store")
        shutil.rmtree(persist_directory)

    # Create the vector store
    print("Creating Vector Store")
    vectordb = Chroma.from_documents(
        documents=splits,
        embedding=embedding,
        persist_directory=persist_directory
    )
    print("Vector DB Collection Count:", vectordb._collection.count())

    return vectordb

def load_db(vectordb, chain_type, k):

    print("Define retriever")
    # retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": k})
    retriever = vectordb.as_retriever()

    # create a chatbot chain. Memory is managed externally.
    print("Create chatbot chain")
    qa = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model_name=llm_name, temperature=0), 
        chain_type=chain_type, 
        retriever=retriever, 
        return_source_documents=True,
        return_generated_question=True,
    )
    return qa 

def ask_a_question(query, chat_history):
    result = qa({"question": query, "chat_history": chat_history})
    chat_history.extend([(query, result["answer"])])
    # db_query = result["generated_question"]
    # db_response = result["source_documents"]
    answer = result['answer'] 

    print("User:", query)
    print("ChatBot:", answer)
    print("")

    return chat_history
    

# define embedding
embedding = OpenAIEmbeddings()


##############################
### Testing By Hard Coding ###
##############################

### PDF
# persist_directory = 'docs/chroma/chat'

# # If vectorDB hasn't been created, create it. Else, load it in
# if not os.path.exists(persist_directory) and not os.path.isdir(persist_directory):
#     print("Creating vector database")
#     vectordb = create_db_from_one_pdf("data/aws-lambda-docs.pdf", embedding)
# else:
#     print("Loading vector database")
#     vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

# qa = load_db(vectordb, "stuff", 4)

# chat_history = []

# chat_history = ask_a_question("What is AWS Lambda?", chat_history)
# chat_history = ask_a_question("Tell me about the supported runtime.", chat_history)
# chat_history = ask_a_question("Are any of these reccomended over others?", chat_history)


### Test EPUB
persist_directory = 'docs/chroma/epub_test'

# If vectorDB hasn't been created, create it. Else, load it in
# if not os.path.exists(persist_directory) and not os.path.isdir(persist_directory):
#     print("Creating vector database")
#     vectordb = create_db_from_one_epub("data/roman/History_of_Rome_by_Titus_Livius.epub", embedding)
# else:
#     print("Loading vector database")
#     vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

vectordb = create_db_from_one_epub("data/roman/History_of_Rome_by_Titus_Livius.epub", embedding)


    # Print out list of all collections in vectorDB
    # print(vectordb[0])


qa = load_db(vectordb, "stuff", 4)

chat_history = []

chat_history = ask_a_question("What books do you have access to?", chat_history)