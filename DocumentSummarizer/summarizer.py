''' Install all the dependent libraries mentioned in requirements.txt file 
        pip install -r requirements.txt
'''

import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from DocumentSummarizer.langchain_summarizer import Summarizer
from file_loader import FileLoader

# Sidebar contents
with st.sidebar:
    st.title('Summarizer: Unlocking Wisdom from Documents')
    st.markdown('''
    ## About
    This smart chatbot is powered by:
    - [Streamlit](https://streamlit.io/)
    - [LangChain](https://python.langchain.com/)
    - [OpenAI](https://platform.openai.com/docs/models) LLM model 
    ''')
    add_vertical_space(5)

def main():
    api_key = st.text_input("Enter your OpenAI api key...")
    if api_key:
        file = st.file_uploader("Upload your file",type=['pdf','xlsx','csv','xls'])

        if file is not None:
            name_with_Extension = file.name.split('.')
            file_name = name_with_Extension[0]
            file_type = name_with_Extension[-1]
            with st.spinner("Summarizing... please wait..."), st.chat_message("assistant"):
                    content = FileLoader(file, file_type).load_and_split()
                    summarizer = Summarizer(model_name="gpt-3.5-turbo", api_key=api_key, chain_type="stuff")
                    st.write(summarizer.invoke(content))
        
if __name__ == '__main__':
    main()
