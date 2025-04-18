import streamlit as st
import time
# Simulated generator with chunks
def my_generator():
    yield "Thinking deeply...\n"
    time.sleep(1)
    yield "Evaluating hypothesis...\n"
    time.sleep(1)
    yield "Almost there...\n"
    time.sleep(1)
    yield "Conclusion: The result is positive.\n"
    time.sleep(1)
    yield "Next steps will follow...\n"

# Function to stream, detect trigger, and manage output
def stream_with_trigger_and_clear(generator_func, trigger_word):
    before_trigger_text = ""
    after_trigger_started = False

    for chunk in generator_func():
        if not after_trigger_started:
            if trigger_word in chunk:
                after_trigger_started = True
                yield "TRIGGER", before_trigger_text  # Send buffer to expander
                yield "AFTER_TRIGGER", chunk           # Send current chunk normally
            else:
                before_trigger_text += chunk
                yield "STREAM", before_trigger_text
        else:
            yield "AFTER_TRIGGER", chunk

# --- Streamlit UI ---
st.title("🧠 Smart Stream-to-Expander")

if st.button("Start Streaming"):
    placeholder = st.empty()
    expander_text = ""
    post_trigger_text = ""
    trigger_word = "Conclusion"

    for status, content in stream_with_trigger_and_clear(my_generator, trigger_word):
        if status == "STREAM":
            placeholder.text(content)
        elif status == "TRIGGER":
            with st.expander("🧠 Thinking Process"):
                st.text(content)
            placeholder.text("")  # Clear current stream
        elif status == "AFTER_TRIGGER":
            post_trigger_text += content
            placeholder.text(post_trigger_text)
