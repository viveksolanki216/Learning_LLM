import os
import time
import streamlit as st
from Utils_AI import *
from streamlit_pdf_viewer import pdf_viewer

st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 2000px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)
#PDF_STORAGE_PATH = './data/'
#PDF_STORAGE_PATH = './uploaded_pdfs/'
LOG_DIR = './logs/'

st.title("CorrelationAI 👩🏻‍💻")
st.markdown("### AI Chat Assistant for PDFs")

text = ""
with st.sidebar:
    #if "qna_model_name" not in st.session_state:
    #    qna_model_name = st.selectbox(
    #        "Select LLM Model",
    #        ("deepseek-r1:1.5b", "deepseek-r1:7b", "deepseek-r1:14b", "llama3.1:8b"),
    #        index=0,
    #        help="If the answer are not correct, choose a model with more parametes i.e. 7b or 14b. It will take more time to generate the answer.",
    #    )
    #    st.session_state.qna_model_name = qna_model_name

    uploaded_doc = st.file_uploader(
        "Upload a PDF file",
        type=["pdf"],
        help="Select a PDF document for QnA",
        accept_multiple_files=False
    )

    if uploaded_doc and 'current_file' in st.session_state:
        if uploaded_doc.name != st.session_state.current_file:
            st.session_state.clear()

    if uploaded_doc and 'pdf_text' not in st.session_state:
        st.session_state.current_file = uploaded_doc.name
        # Write everythin for logs purpose
        # First create a dictory with current date and time for the current session
        current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        st.session_state.session_dir = os.path.join(LOG_DIR, current_time)
        os.makedirs(st.session_state.session_dir, exist_ok=True)
        # Save file into the
        print("Storing the uploaded document to local store")
        with open(os.path.join(st.session_state.session_dir, uploaded_doc.name), "wb") as f:
            f.write(uploaded_doc.getbuffer())

            # Read Text from the file
        print("Reading Text from the pdf")
        st.session_state.pdf_text = read_document_to_text(os.path.join(st.session_state.session_dir, uploaded_doc.name))
        # To implement RAG, we need to split the document into smaller chunks
        print("Chunking the text")
        st.session_state.chunked_documents, st.session_state.doc_embeds_list = chunk_the_text_and_get_embeddings(
            st.session_state.pdf_text, chunk_size=1000,
            chunk_overlap=0
        )
        print("Logging down the text and chunked text")
        # Save the text into a file
        with open(os.path.join(st.session_state.session_dir, "doc_to_text.txt"), "w") as f:
            f.write(st.session_state.pdf_text)
        # write chunked text into a file
        with open(os.path.join(st.session_state.session_dir, "chunked_documents.txt"), "w") as f:
            for item1 in st.session_state.chunked_documents:
                f.write(item1.page_content)
                f.write("\n-----------\n")
        with open(os.path.join(st.session_state.session_dir, "embeddings.txt"), "w") as f:
            for item2 in st.session_state.doc_embeds_list:
                f.write(str(item2))
                f.write("\n-----------\n")

        #with st.chat_message("user"):
        #    st.write(text)
        # write success message
        st.success("✅ Document Uploaded! Ask your questions below.")

    if uploaded_doc:
        print("pdf viwer")
        pdf_viewer(os.path.join(st.session_state.session_dir, st.session_state.current_file))


if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("User Question:")
if user_input:

    for role, msg in st.session_state.chat_history:
        if role == "user":
            st.markdown(
            f"""
            <div style='text-align: right; margin: 10px 0;'>
                <span style='background-color:#d1e7dd;padding:10px;border-radius:10px;display:inline-block;'>{msg}</span> 🧑
            </div>
            """,
            unsafe_allow_html=True,
        )
        else:
            st.markdown(
            f"""
            <div style='text-align: left; margin: 10px 0;'>
               👩🏻‍💻<span style='background-color:#f8f9fa;padding:10px;border-radius:10px;display:inline-block;'>{msg}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
               <div style='text-align: right; margin: 10px 0;'>
                   <span style='background-color:#d1e7dd;padding:10px;border-radius:10px;display:inline-block;'>{user_input}</span> 🧑
               </div>
               """,
        unsafe_allow_html=True,
   )
    #with st.spinner("Thinking..."):
        # Generate AI response.
        #ai_response = generate_answer(user_input, relevant_docs)
        #ai_think_notes, ai_response = invoke_llm(user_input, text)
        #print(ai_think_notes)
        #st.write(ai_response)

    context = get_relevant_context_to_the_query(user_input, st.session_state.chunked_documents, st.session_state.doc_embeds_list, top_k=5)

    with open(os.path.join(st.session_state.session_dir, "query.log"), "a") as f:
        f.write("User Query:\n\n" + user_input+ "\n\n")
        f.write("Revelvant Context:\n\n" + context + "\n\n")
        f.write("Answer:\n\n")

    #st.write_stream(
    #    invoke_llm_stream_and_write_to_log(
    #        user_input, context, os.path.join(st.session_state.session_dir, "query.log"))
    #)
    placeholder = st.empty()
    expander_text = ""
    post_trigger_text = ""
    trigger_word = "</think>"

    for status, content in invoke_llm_stream_and_write_to_log(
            user_input, context, os.path.join(st.session_state.session_dir, "query.log"), trigger_word
    ):
        if status == "STREAM":
            placeholder.text(content)
        elif status == "TRIGGER":
            with st.expander("🧠Thinking Process"):
                st.markdown(content)
            placeholder.text("")  # Clear current stream
        elif status == "AFTER_TRIGGER":
            post_trigger_text += content
            #placeholder.text(post_trigger_text)
            placeholder.markdown(
                f"""
                <div style='text-align: left; margin: 10px 0;'>
                   👩🏻‍💻<span style='background-color:#f8f9fa;padding:10px;border-radius:10px;display:inline-block;'>{post_trigger_text}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.session_state.chat_history.append(("user", user_input))
    st.session_state.chat_history.append(("assistant", post_trigger_text))
