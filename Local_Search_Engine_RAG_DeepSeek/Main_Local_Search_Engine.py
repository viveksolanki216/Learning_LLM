import numpy as np
from langchain_community.document_loaders import PDFPlumberLoader, TextLoader, AzureAIDocumentIntelligenceLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS, InMemoryVectorStore, Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import InMemoryVectorStore # use chroma for storing the embeddings into a file on disk to retain.
from langchain_ollama import OllamaEmbeddings # To instatiate different llm embeddings model supported by ollama running locally
from langchain_ollama import OllamaLLM
from langchain_core.documents import Document # Format to store documents and its content
import os
from getpass import getpass # to give key for openai

LANGUAGE_MODEL = OllamaLLM(model="deepseek-r1:7b") # Language model for answe generation
EMBEDDING_MODEL = OllamaEmbeddings(model="nomic-embed-text") # Embedding model for internal database documents
#EMBEDDING_MODEL = OpenAIEmbeddings(model="text-embedding-3-large")
#EMBEDDING_MODEL = HuggingFaceEmbeddings(model_name="jina_embeddings")

VECTOR_STORE = InMemoryVectorStore(EMBEDDING_MODEL) # store the embeddings for the text

PROMPT_TEMPLATE = """
You are an expert research assistant. Use the provided context to answer the query. 
If unsure, state that you don't know. Be concise and factual (max 3 sentences).

Query: {user_query} 
Context: {document_context} 
Answer:
"""


def read_text_to_documents(file_path: str) -> list:
    # PDFPlumberLoader is a class that loads the PDF file and extracts the text from it
    # It returns a list of specific type of object i.e. Document, each object for a each page
    # consider each page as a Document, each page can be considered as a chunk
    if file_path.endswith(".pdf"):
        loader = PDFPlumberLoader(file_path)
    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path)
    elif file_path.endswith(".docx"):
        loader = AzureAIDocumentIntelligenceLoader(file_path)

    return loader.load() # docs is a list of Document objects


# -- Read document from a PDF or other document --
dir_to_docs = "/Users/vss/Work/Learnings_2024/ExtractInformation/output/runs/all_termsheets_run/txt_files/"
import os
file_path_list = [dir_to_docs+file_path for file_path in os.listdir(dir_to_docs) if file_path.endswith(".txt") or file_path.endswith(".pdf")]
documents = list(map(read_text_to_documents, file_path_list))
documents = [doc for docs in documents for doc in docs] # flatten the list of list of documents

# example of running a single document
#file_path = "/Users/vss/Work/Learnings_2024/ExtractInformation/sample_files/Milkrun Spark Termsheet 031121-2.pdf"
#docs = read_text_to_documents(file_path) # documents is a list of Document objects

# -- Split documents into smaller overallaping chunks --
# The text splitter changes the size of Documents. i.e. if you want smaller chunks of bigger chunks.
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0, add_start_index=True)
chunked_documents = documents #text_splitter.split_documents(documents) # split_docs is a list of Document objects

# Do you want to see the embeddings for the first two documents?
# Each document is an vector of float numbers total size 5120.
embds = EMBEDDING_MODEL.embed_documents([documents[420].page_content, 'scoot networks'])
print(len(embds), len(embds[0]), len(embds[1]), '\n', embds[0][0:10], '\n', embds[1][0:10])
# The above document is for scoot networks, but we see that the query and document are not similar according to the embeddings
# how to resolve this??
(np.array(embds[0]) * np.array(embds[1])).sum()


# -- Create and store the embeddings for the text --
# vector_store is a class that stores the embeddings for the text
_ = VECTOR_STORE.add_documents(chunked_documents)

# -- Search for documents And Generate Answer
# For a user query, LLM will first find the relevand document in the vector store using similarity search between query
# and vector store and then generate the answer using the language model
query = "Can you tell me which companies term-sheets mentions forerunner ventures as investor, and the amount of investment, date of investment, and the post money valuation."
query_similarity_search = "Scoot Networks"
similar_context_docs = VECTOR_STORE.similarity_search_with_score(query_similarity_search, k=1)
#similar_context_docs
#[print(True) for doc, score in similar_context_docs if 'forerunner' in doc.page_content.lower() ]
# generate the context text for the answer.
_ = [print(score) for doc, score in similar_context_docs]
context_text = '\n\n'.join(doc.page_content for doc, score in similar_context_docs)
print(context_text)

query = '''Extract the following fields to create an output JSON for Scoot Networks Seed Termsheet:
 - 'Date': The creation or execution date of the term sheet (YYYY-MM-DD format).
 - 'MCE': 1 if multiple closings of the round are expected, else 0.
 - 'TR': The total amount being raised by the company ($). Return integer.
 - 'TBM': The total number of board members in the company.
 - 'MBMs': The number of board members from the company's management.
 - 'IBMs': The number of board members from the investors.
 - 'IndBMs': The number of independent board members.
 - 'BMsName': A comma seperated list of board members' name. Arrange them in the order of Management BMs, Investor BMs, Independent BMs.
 - 'Tr': 1 if VCs make payments over a specified period in multiple tranche, else 0 if they are paying in a single tranche.
 - 'Round': The round of funding (Seed, Series A, Series B, etc.). 
If some information is not available, leave it blank'''
# generate the answer using the language model
prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
response_chain = prompt | LANGUAGE_MODEL
response = response_chain.invoke({"user_query": query, "document_context": context_text})
print(response)
