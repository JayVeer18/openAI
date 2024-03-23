from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import load_summarize_chain, AnalyzeDocumentChain
from langchain_community.callbacks import get_openai_callback

class Summarizer:
    def __init__(self, model_name, api_key, chain_type):
        self.final_prompt = self._create_prompt("""Write a detailed analytical summary of the following text delimited by triple backquotes, by including all the necessary data along with trends and explanation. 
                            ```{text}``` SUMMARY: """,input_variables=["text"])
        self.intermitent_prompt = self._create_prompt("""Please provide a detailed analytical summary of the following text by including all the necessary data along with trends and explanation.
                    TEXT: {text} SUMMARY: """,input_variables=["text"])
        
        self.llm = ChatOpenAI(model_name=model_name, api_key=api_key)
        self.chain = self._load_summarize_chain(chain_type)

    def _create_prompt(self, template, input_variables):
        return PromptTemplate(template=template, input_variables=input_variables)

    def _load_summarize_chain(self, chain_type:str):
        if chain_type == 'refine':
            return load_summarize_chain(llm=self.llm, chain_type="refine", return_intermediate_steps=True,
                                        question_prompt=self.intermitent_prompt, 
                                        refine_prompt=self.final_prompt)
        elif chain_type == 'map_reduce':
            return load_summarize_chain(llm=self.llm, chain_type='map_reduce', return_intermediate_steps=True,
                                            map_prompt=self.intermitent_prompt, 
                                            combine_prompt=self.final_prompt)
        else :
            return load_summarize_chain(llm=self.llm, chain_type='stuff', prompt=self.final_prompt)
    
    def invoke(self, content):
        if isinstance(content, str):
            # Handle single document
            summary_chain = AnalyzeDocumentChain(combine_docs_chain=self.chain)
            with get_openai_callback() as cb:
                summary = summary_chain.invoke({"input_document": content})
                print(cb)
            return summary.get('output_text')
        
        elif isinstance(content, list):
            # Handle list of documents
            with get_openai_callback() as cb:
                summary = self.chain.invoke({"input_documents": content})
                print(cb)
            return summary.get('output_text')
        
        else:
            raise ValueError("Invalid input type. Expected str or list.")    