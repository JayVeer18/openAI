import os
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain.agents import Tool, AgentType, initialize_agent
from langchain.chains import RetrievalQA
from langchain_community.callbacks import get_openai_callback

class DocumentInput(BaseModel):
    question: str = Field()

class DocComparator:
    def __init__(self, model_name, api_key, files):
        self.embeddings =  OpenAIEmbeddings(api_key=api_key)
        self.files = files
        self.llm = ChatOpenAI(model_name=model_name, api_key=api_key)
        self.tools = self._create_retriever_tool()
        self.agent = self._create_agent()

    def _create_retriever_tool(self):
        # Wrap retrievers in a Tool
        tools = []
        for file in self.files:
            ### To save money as we are using chatGPT APIs, we Store chunks in disk
            if os.path.exists(f"{file['file_name']}.faiss"):
                vectorStore = FAISS.load_local(folder_path="./faiss_db",index_name=file['file_name'], embeddings=self.embeddings)
            else:
                vectorStore = FAISS.from_documents(documents=file['chunks'], embedding=self.embeddings)
                vectorStore.save_local(folder_path="./faiss_db",index_name=file['file_name'])

            tools.append(
                Tool(
                    args_schema=DocumentInput,
                    name=file['file_name'],
                    description=f"useful when you want to answer questions about {file['file_name']}",
                    func=RetrievalQA.from_chain_type(llm=self.llm, retriever=vectorStore.as_retriever()),
                )
            )
        return tools
    
    def _create_agent(self):
        agent = initialize_agent(
                agent=AgentType.OPENAI_FUNCTIONS,
                tools=self.tools,
                llm=self.llm,
                verbose=True,
            )
        return agent
        
    def invoke(self, query):
        with get_openai_callback() as cb:
            response = self.agent({"input": query})
            print(cb)
        return response["output"]
