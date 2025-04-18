from langchain_community.document_loaders import PDFPlumberLoader, TextLoader, AzureAIDocumentIntelligenceLoader
import requests


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


# Function to interact with Ollama API
def query_ollama_api(context, user_query, model="deepseek-r1:7b"):
  ollama_url = "http://localhost:11434/v1/chat/completions"  # Assuming Ollama is running locally
  headers = {
    "Content-Type": "application/json",
  }

  # Formatting the system message (instructions + context) and user message (query)
  prompt = f"""
    You are provided a context extracted from a document mostly related to a capital venture industry like a termsheet, 
    financials, legal documents, etc. You are an expert Question and Answer assistant. Please provide the relevant answer 
    to the user query embedded in the user message. Only answer if the answer is in the context. If the answer is not in the context, say "I don't know".
 
    --- USER QUERY ---
    "{user_query}"
    
    --- CONTEXT ---
    "{context}"
    
  """
  print(prompt)
  payload = {
    "model": model,#"llama3.1",#"deepseek-r1:7b",  # Adjust model if necessary
    "messages": [
      #{"role": "system", "content": system_message},  # System message with instructions and context
      {"role": "user", "content": prompt}  # User message with the query
    ],
  }

  response = requests.post(ollama_url, json=payload, headers=headers)

  if response.status_code == 200:
    return response.json()['choices'][0]['message']['content']
  else:
    return f"Error: {response.status_code}, {response.text}"



# Example Usage:
if __name__ == "__main__":
  # Path to the PDF document
  pdf_path = '/Users/vss/Work/Learnings_2024/ExtractInformation/sample_files/Pyze Termsheet - 2019_0404_final.pdf'
  # Extract text from the PDF
  context = read_document_to_text(pdf_path)

  # Example user query
  user_query = "Who are the investors in attached document?"
  user_query = "What's the amount being raised for the round?"

  # Get the response
  answer = query_ollama_api(context[0:2000], user_query, model="llama3.1:8b")
  print(f"Answer: {answer}")

