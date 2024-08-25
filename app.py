import streamlit as st
from pdf_processing import get_text, get_chunks
from chroma_db import store_embeddings_chroma, query_db, delete_previous_data

def main():
    st.set_page_config(page_title="Chat PDF")
    st.title("Chat with Multiple PDF 💻📃")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Ask a question related to PDF files"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = query_db(prompt)
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})


    with st.sidebar:
        pdf_files = st.file_uploader("Upload your PDF Files", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing..."):
                text_with_metadata = get_text(pdf_files)
                chunks_with_metadata = get_chunks(text_with_metadata)
                store_embeddings_chroma(chunks_with_metadata)
                st.success("Done")

        if st.button("Delete Previous Data"):
            delete_previous_data()
            st.success("Previous data deleted.")

if __name__ == "__main__":
    main()
