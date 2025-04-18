


#---------------------------------
import fitz  # PyMuPDF
import requests


# Example Usage:
if __name__ == "__main__":
  # Path to the PDF document
  pdf_path = "your_pdf_file.pdf"

  # Example user query
  user_query = "What is the main theme of the document?"

  # Get the response
  answer = main(pdf_path, user_query)
  print(f"Answer: {answer}")

#---------------------------------
import pandas as pd
from langchain_ollama import OllamaLLM
llm_model  = OllamaLLM(base_url='http://192.168.200.18:11434', model="deepseek-r1:1.5b")  # Language model for answe generation
prompt = "Hi"
response = llm_model.invoke(prompt)
print(response)

#---------------------------------
import ollama
from ollama import Client
client = Client(
  host='http://192.168.200.18:11434'#,
  #headers={'x-some-header': 'some-value'}
)
# write code to check time
import time
start = time.time()
response = client.chat(model='deepseek-r1:1.5b', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(response)
print(response['message']['content'])
end = time.time()
print(end - start)

#---------------------------------
# streaming on
import time
start = time.time()
for part in client.generate(
  model='deepseek-r1:1.5b', prompt= 'Why is the sky blue?', stream=True
):
  print(part['response'], end='', flush=True)
end = time.time()
print(end - start)


#---------------------------------
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

llm_model  = OllamaLLM(base_url='http://192.168.200.18:11434', model="deepseek-r1:1.5b")  # Language model for answe generation
#llm_model  = OllamaLLM(base_url='http://127.0.0.1:11434', model="deepseek-r1:1.5b")  # Language model for answe generation

PROMPT_TEMPLATE = """
You are an expert Question and Answer assistant. Use the provided context to answer the query in brief.

Query: {user_query} 
Context: {document_context} 
"""
user_query="Why is the sky blue?"
context_text=""
prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
response_chain = prompt | llm_model
import time
start = time.time()
response = response_chain.invoke({"user_query": user_query, "document_context": context_text})
print(response)
end = time.time()
print(end - start)


#---------------------------------

curl http://192.168.200.18:11434/api/generate -d '{
  "model": "deepseek-r1:1.5b",
  "prompt": """Why is the sky
             blue?""", "stream":true,
  "options": {
    "num_ctx": 4096
  }
}'
