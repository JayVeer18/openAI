''' Install all the dependent libraries mentioned in requirements.txt file 
        pip install -r requirements.txt
'''

import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from file_loader import FileLoader
from langchain_chatbot import Chatbot

# Sidebar contents
with st.sidebar:
    st.title('Insight Chat: Unlocking Wisdom from Documents')
    st.markdown('''
    ## About
    This smart chatbot is powered by:
    - [Streamlit](https://streamlit.io/)
    - [LangChain](https://python.langchain.com/)
    - [OpenAI](https://platform.openai.com/docs/models) LLM model 
    ''')
    add_vertical_space(5)

def chat_with_document(chatbot: Chatbot):  
    if query := st.chat_input("Ask questions about your file"):
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
        
        with st.spinner("Querying... please wait..."), st.chat_message("assistant"):
                response = chatbot.invoke(query)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

def display_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def main():
    api_key = st.text_input("Enter your OpenAI api key...")
    if api_key:
        file = st.file_uploader("Upload your file",type=['pdf','xlsx','csv','xls'])

        if file is not None:
            name_with_Extension = file.name.split('.')
            file_name = name_with_Extension[0]
            file_type = name_with_Extension[-1]
            doc_chunks = FileLoader(file, file_type).load_and_split()
            chatbot = Chatbot(model_name="gpt-3.5-turbo", api_key=api_key, file_name=file_name, file_content=doc_chunks, chain_type='RAG')
            display_chat_history()
            chat_with_document(chatbot)

if __name__ == '__main__':
    main()