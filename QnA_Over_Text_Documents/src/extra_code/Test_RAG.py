import numpy as np
from langchain_community.document_loaders import PDFPlumberLoader, TextLoader, AzureAIDocumentIntelligenceLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import ollama

embedding_model_name = "mxbai-embed-large"#"nomic-embed-text"


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
    documents = loader.load()  # docs is a list of Document objects
    text_in_pages = (doc.page_content for doc in documents)  # a generator function
    text = "\n".join(text_in_pages)
    return text  #
    #return loader.load() # docs is a list of Document objects

def read_document_to_text(file_path: str) -> list:
    # PDFPlumberLoader is a class that loads the PDF file and extracts the text from it
    # It returns a list of specific type of object i.e. Document, each object for a each page
    # consider each page as a Document, each page can be considered as a chunk
    if file_path.endswith(".pdf"):
        loader = PDFPlumberLoader(file_path)
    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path)
    elif file_path.endswith(".docx"):
        loader = AzureAIDocumentIntelligenceLoader(file_path)

    documents = loader.load() # docs is a list of Document objects
    text_in_pages = (doc.page_content for doc in documents) # a generator function
    text = "\n".join(text_in_pages)
    return text # docs is a list of Document objects


def get_cosine_similarity(embd1, embd2):
    vec1 = np.array(embd1)
    vec2 = np.array(embd2)
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)


# -- Read document from a PDF or other document --
file_path = "/Users/vss/Work/Learnings_2024/ExtractInformation/sample_files/Pyze Termsheet - 2019_0404_final.pdf"
text = read_text_to_documents(file_path) # documents is a list of Document objects

# -- Split documents into smaller overallaping chunks --
# The text splitter changes the size of Documents. i.e. if you want smaller chunks of bigger chunks.
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0, add_start_index=True)
chunked_documents = text_splitter.create_documents([text])
print(chunked_documents[0].page_content)
print(chunked_documents[1].page_content)

# Do you want to see the embeddings for the first two documents?
# Each document is an vector of float numbers total size 5120.
doc_embeds_list = []
for doc in chunked_documents:
    doc_embeddings = ollama.embeddings(model=embedding_model_name, prompt=doc.page_content)
    doc_embeds_list.append(doc_embeddings['embedding'])

print(len(doc_embeds_list[0]))
assert len(doc_embeds_list) == len(chunked_documents)

user_query = "Who are the investors in this round?"
user_query = "What is the capital raised in this termsheet?"
user_query = "what is the composition of board of directors?"
user_query = "summarize binding terms"
user_query = "conditions to closing?"
user_query = "at what valuation the company is raising capital?"
user_query = "what is the valuation for the round?"
user_query = "what are the conditions for liquidation preference and option pool?"

query_embeds = ollama.embeddings(model=embedding_model_name, prompt=user_query)['embedding']

similarity_scores = np.array([0.0] * len(doc_embeds_list))
for i in range(len(doc_embeds_list)):
    similarity_scores[i] = get_cosine_similarity(doc_embeds_list[i], query_embeds)

top_docs_index = similarity_scores.argsort()[-3::]  # sort the similarity scores in descending order
print(top_docs_index)

j = 0
context = '{\n'
for i in top_docs_index:
    context += f'"chunk-{j}": "{chunked_documents[i].page_content}"\n\n'
    j += 1
context += '}\n'

print(context)

for word in invoke_llm_stream(user_query, context):
    print(word, end='', flush=True)



answer = query_ollama_api(context, user_query)
print(f"Answer: {answer}")
