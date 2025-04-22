#from langchain_community.document_loaders import PDFPlumberLoader, TextLoader, AzureAIDocumentIntelligenceLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ollama import Client
#import ollama
import os
import numpy as np

from PyPDF2 import PdfReader
import docx2txt
#import textract
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

client = Client(
  #host='http://192.168.200.18:11434'#,
  #host='http://127.0.0.1:11434'
  #host='http://192.168.201.123:11434'
  host='http://10.0.0.138:11434'
  #host='host.docker.internal:11434'
  #headers={'x-some-header': 'some-value'}
)

embedding_model_name = "mxbai-embed-large"#"nomic-embed-text"
qna_model_name = "deepseek-r1:7b"#"deepseek-r1:14b"

PROMPT_TEMPLATE = """
    You are provided a user query and top n relevant sections, as context, extracted from a document mostly related to 
    a capital venture industry like a termsheet, financials, legal documents, etc. 
    You are an expert Question and Answer assistant. Please provide the relevant answer in brief 
    to the user query based on the input context. If there is no relevant answer to the user query, please say "I don't know".
    Don't get stuck in calculations, give answers in real-time. 
 
    --- USER QUERY ---
    {user_query}
    
    --- CONTEXT ---
    {context}
    """
def read_document_to_text(file_path, read_first_page=False):
    text = ""
    try:
        if file_path.lower().endswith(".docx"):  # | file_path.endswith(".doc"):
            text = docx2txt.process(file_path)
            print("Reading Docx File")
        #elif file_path.lower().endswith(".doc"):
        #    text = textract.process(file_path)
        #    text = text.decode('utf-8')
        #    print("Reading Doc File")
        elif file_path.lower().endswith(".pdf"):
            # Read the PDF file
            print("Reading PDF File")
            pdf_reader = PdfReader(file_path)
            for page in pdf_reader.pages:
                text += page.extract_text()
            # if the text is empty, or the length of the text is less than 1000, then pdf could be scanned one
            # and need ocr method to extract text.
            print("Length of Text: ", len(text))
            if len(text) <= 1000:
                print("Reading Scanned PDF File")
                images = convert_from_path(file_path)
                if read_first_page:
                    img = images[0]
                    text += pytesseract.image_to_string(img)
                else:
                    for img in images:
                        text += pytesseract.image_to_string(img)
        elif file_path.lower().endswith(".jpg") | file_path.lower().endswith(".jpeg") | file_path.lower().endswith(".png"):
            img = Image.open(file_path)
            text = pytesseract.image_to_string(img)
        else:
            print("Not generating txt file for this file type")

    except Exception as e:
        print("Error in reading file:", file_path)
        print(e)

    return text

def chunk_the_text_and_get_embeddings(text: str, chunk_size: int = 1000, chunk_overlap: int = 0) -> list:
    '''
    Since giving full document as context to the small model i.e. 7b parameter is not a good idea, we need to chunk the document into smaller chunks.
    To do that we need to use a text splitter. The text splitter will split the document into smaller chunks and then we can get the embeddings for each chunk.

    :param text:
    :param chunk_size:
    :param chunk_overlap:
    :return: Text Chunk as list, Text Embeddings as list.
    '''
    # -- Split documents into smaller overallaping chunks --
    # The text splitter changes the size of Documents. i.e. if you want smaller chunks of bigger chunks.
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, add_start_index=True)
    chunked_documents = text_splitter.create_documents([text])
    #print(chunked_documents[0].page_content)
    #print(chunked_documents[1].page_content)

    # Do you want to see the embeddings for the first two documents?
    # Each document is an vector of float numbers total size 5120.
    doc_embeds_list = []
    for doc in chunked_documents:
        doc_embeddings = client.embeddings(model=embedding_model_name, prompt=doc.page_content)
        doc_embeds_list.append(doc_embeddings['embedding'])

    #print(len(doc_embeds_list[0]))
    assert len(doc_embeds_list) == len(chunked_documents)

    return chunked_documents, doc_embeds_list

def get_cosine_similarity(embd1, embd2):
    vec1 = np.array(embd1)
    vec2 = np.array(embd2)
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

def get_relevant_context_to_the_query(user_input: str, chunked_documents: list, doc_embeds_list: list, top_k: int = 3) -> str:
    '''
    Get the relevant chunks to the user query based on maximum cosine similarity between the embeddings of query and that
    of all chunks of the documnet. The function will return the top k relevant chunks to the user query, json format.
    :param user_input:
    :param chunked_text:
    :param doc_embeds_list:
    :param top_k:
    :return: json as string
    '''
    query_embeds = client.embeddings(model=embedding_model_name, prompt=user_input)['embedding']

    similarity_scores = np.array([0.0] * len(doc_embeds_list))
    for i in range(len(doc_embeds_list)):
        similarity_scores[i] = get_cosine_similarity(doc_embeds_list[i], query_embeds)

    top_docs_index = similarity_scores.argsort()[-top_k::]  # sort the similarity scores in descending order
    #print(top_docs_index)

    j = 0
    context = '{\n'
    for i in top_docs_index:
        context += f'"chunk-{j}": "{chunked_documents[i].page_content}"\n\n'
        j += 1
    context += '}\n'

    #print(context)
    return context

def invoke_llm_stream( user_input: str, context: str, qna_model_name: str = "deepseek-r1:7b") -> (str, str):
    prompt = PROMPT_TEMPLATE.format(user_query=user_input, context=context)
    print(prompt)
    messages = [
        {
            'role': 'user',
            'content': prompt,
        },
    ]
    for part in client.chat(
            model=qna_model_name, messages=messages, stream=True
    ):
        yield part['message']['content']

#def invoke_llm_stream_and_write_to_log(user_input, context, file_name):
#    with open(file_name, 'a') as f:
#        for word in invoke_llm_stream(user_input, context):
#            word = word.replace('$', '\$')
#            f.write(word)
#            yield word

def invoke_llm_stream_and_write_to_log(user_input, context, file_name, trigger_word="</think>"):
    before_trigger_text = ""
    after_trigger_started = False

    with open(file_name, 'a') as f:
        for chunk in invoke_llm_stream(user_input, context):
            f.write(chunk)
            chunk = chunk.replace('$', '\\$')
            if not after_trigger_started:
                if trigger_word in chunk:
                    after_trigger_started = True
                    yield "TRIGGER", before_trigger_text + chunk  # Send buffer to expander
                    #yield "AFTER_TRIGGER", chunk           # Send current chunk normally
                else:
                    before_trigger_text += chunk
                    yield "STREAM", before_trigger_text
            else:
                yield "AFTER_TRIGGER", chunk


def invoke_llm( user_query: str, context_text: str) -> (str, str):
    PROMPT_TEMPLATE.format(user_query=user_query, document_context=context_text)
    response_chain = prompt | LANGUAGE_MODEL
    response = response_chain.invoke({"user_query": user_query, "document_context": context_text})
    think_tags = ["<think>", "</think>"]
    idx = response.find("</think>")
    if idx != -1:
        think_notes = response[len(think_tags[0]):idx].strip('\n').strip()
        final_response = response[idx + len(think_tags[1]):].strip('\n').strip()
    else:
        final_response = response
    return think_notes, final_response


