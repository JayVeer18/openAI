import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores.faiss import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain_community.callbacks import get_openai_callback
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

class Chatbot:
    def __init__(self, model_name, api_key, file_name, file_content, chain_type):
        self.embeddings = OpenAIEmbeddings(api_key=api_key)
        self.file_name = file_name
        self.file_content = file_content
        self.llm = ChatOpenAI(model_name=model_name, api_key=api_key)
        self.chat_history = []
        self.chain_type = chain_type
        if chain_type == 'RAG':
            self.chain = self._create_RAG_chain()
        else:
            self.chain = self._create_conversation_retrival_chain()

    def _load_VS_as_retriever(self):
        if os.path.exists(f"{self.file_name}.faiss"):
            vectorStore = FAISS.load_local(folder_path="./faiss_db", index_name=self.file_name, embeddings=self.embeddings)
        else:
            vectorStore = FAISS.from_documents(documents=self.file_content, embedding=self.embeddings)
            vectorStore.save_local(folder_path="./faiss_db", index_name=self.file_name)
        return vectorStore.as_retriever()

    def _create_RAG_chain(self):
        template = """You are a chatbot where user asks questions. Answer those questions based only on the following context:{context}
        Question: {question}"""
        prompt = ChatPromptTemplate.from_template(template)
        retriever = self._load_VS_as_retriever()
        chain = ({"context": retriever, "question": RunnablePassthrough()} | prompt | self.llm | StrOutputParser())
        return chain

    def _create_conversation_retrival_chain(self):
        retriever = self._load_VS_as_retriever()
        return ConversationalRetrievalChain.from_llm(llm=self.llm, retriever=retriever, return_source_documents=True)

    def invoke(self, query):
        if self.chain_type == 'RAG':
            return self.invoke_without_history(query)
        return self.invoke_with_history(query)

    def invoke_without_history(self, query):
        with get_openai_callback() as cb:
            response = self.chain.invoke(query)
            print(cb)
        return response

    def invoke_with_history(self, query):
        section_history = self.chat_history
        with get_openai_callback() as cb:
            response = self.chain.invoke({"question": query, "chat_history": section_history})
            self.chat_history = [(query, response["answer"])]
            print(cb)
        return response["answer"]