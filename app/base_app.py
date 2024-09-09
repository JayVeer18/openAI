import streamlit as st
from chatbot import Chatbot
from langchain_community.document_loaders import PyPDFLoader
import os
from dotenv import load_dotenv

class App:
    def __init__(self, section_name, file_path, video_url):
        self.section_name = section_name
        self.file_path = file_path
        self.video_url = video_url

        # load environment variables from .env file
        load_dotenv()
        self.api_key = os.environ.get("OPENAI_API_KEY")

        # Load document content
        file_name_with_ext = os.path.basename(file_path)
        self.file_name = file_name_with_ext.split('.')[0]
        
        self.doc_chunks = self.file_load_and_split()

        # Initialize chatbot
        self.chatbot = Chatbot(
            model_name="gpt-3.5-turbo",
            api_key=self.api_key,
            file_name=self.file_name,
            file_content=self.doc_chunks,
            chain_type='RAG'
        )

        # Initialize session state
        self.init_session_state()

    def init_session_state(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []

    def file_load_and_split(self):
        loader = PyPDFLoader(file_path=self.file_path, extract_images=True)
        pages = loader.load_and_split()
        return pages
    
    def chat_with_document(self):
        # Display chat history before the input box
        self.display_chat_history()

        # Query input
        if query := st.chat_input("Ask questions about The video"):
            st.chat_message("user").markdown(query)
            
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": query})

            with st.spinner("Querying... please wait..."), st.chat_message("assistant"):
                response = self.chatbot.invoke(query)
                st.markdown(response)

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
     

    def display_chat_history(self):
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def run(self):
        # Streamlit page configuration
        st.set_page_config(layout="wide")
        st.markdown(self.section_name)
        st.sidebar.markdown(self.section_name)

        # Layout for video, summary, and chatbox
        video_col, chat_col = st.columns([0.55, 0.45])

        # Display the video
        with video_col:
            st.video(self.video_url)

        # Display the chat history with scrollable container
        with chat_col:
            with st.container(height=500):
                self.chat_with_document()

# Example usage
# if __name__ == "__main__":
#   app = App("# Section_name ", r"path\to\file_name", "video_url")
#   app.run()