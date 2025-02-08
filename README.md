# Building a RAG System with DeepSeek-R1 & Ollama for Local Deployment

## Basic Overview
RAG (i.e. Retrieval-Augmented Generation) integrates a retrieval mechanism with a generative model (local llm in this case) to fetch relevant data from a external (external to llm) knowledge source i.e. enterprise knowledge base. 
Making AI generated content more accurate and contextually relevant.

In this tutorial, we will be building a fully functional RAG system with DeepSeek-R1 and Ollama for local deployment.
 
Tools used:
 - *DeepSeek-R1:* An open-source reasoning model.
 - *Ollama:* A framework for running LLMs locally.
 - *Python 3.11+, Conda, Pip*
 - *streamlite:* for building the simple web app
 - *FastAPI:* for building the API endpoints
 - *FAISS:* A vector database for fast retriveal 
 - *LangChain:* For connecting the retrieval and generation components.

### Langchain
An open-source framework allows developers to combine LLLms with other external components to build LLM-powered applications. 
It can be used to build chatbots, vitrual agents, NLP applications, and more.

To creat a generative AI app, it needs various tools, langachain simplifies and streamlines the process. i.e. LLM must access
a large volumes of big data, so LangChain organizes these large quantities of data so that they can be accessed with ease.
Another examples, switching between LLMs i.e. openai or hugging face with minimal code changes.

Example: How to extract structured data from unstructured text using LangChain.
reference: [here](https://python.langchain.com/docs/tutorials/extraction/)

### Vector Stores i.e. FAISS
Vector stores are used to store and retrieve vectors which usually created via embeddings from a pre-trained model i.e. gpt-4.
FAISS (Facebook AI Similarity Search) is one of the example of open-source vector-stores.

```pip install faiss-cpu```

reference: [here](https://python.langchain.com/v0.1/docs/modules/data_connection/vectorstores/)
reference: [here](https://python.langchain.com/docs/integrations/vectorstores/)

### Ollama
Again an open-source framework, that allows developers to run LLMs locally. It can be used to run LLMs on local machines, servers, or edge devices.
 - install ollama from the website.
 - Use CLI to pull the model i.e. ```ollama pull deepseek-r1:14b```
 - Start server using ```ollama serve```
 - If get error "Error: listen tcp 127.0.0.1:11434: bind: address already in use", that means port is used by some other process.
 - If the port is not using by any other critical process. or use by other ollam service.
 - Just find the PID by command ```lsof -i:11434``` and kill the process by ```kill -9 PID```
 - If the port getting reassigned to other proces, quit the app in the toolbar and kill the process again.


 # Install Dependencies
```python --version```

a conda enviornment is already setup using pycharm so just install the following dependencies.
```fastapi uvicorn langchain streamlit pdfplumber faiss-cpu```



