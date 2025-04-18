import streamlit as st
from streamlit import button
import time


st.title("Ask Question")
question = st.text_input("Enter your question here:")
button = st.button("Search")

if button:
    #time.sleep(5)
    # use st.progress to show the progress of the search
    latest_iteration = st.empty()
    bar = st.progress(0)

    for i in range(100):
        # Update the progress bar with each iteration.
        latest_iteration.text(f'Iteration {i + 1}')
        bar.progress(i + 1)
        time.sleep(0.1)

    st.write("Your anseer is here: ")
    st.write(question)
    import pandas as pd

    df = pd.DataFrame({
        'first column': [1, 2, 3, 4],
        'second column': [10, 20, 30, 40]
    })

    df

    st.write(df)
# Runt the above app in the terminal in current dir using:
# > streamlit run basic_streamlit_app.py