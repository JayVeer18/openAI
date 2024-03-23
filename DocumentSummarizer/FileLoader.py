import os
from tempfile import NamedTemporaryFile
from PyPDF2 import PdfReader
from langchain_community.document_loaders import PyPDFLoader, UnstructuredExcelLoader, CSVLoader

class FileLoader:
    def __init__(self, file, filetype:str):
        self.file = file
        self.type = filetype.lower()

    def load_and_split(self):
        with NamedTemporaryFile(delete=False) as tmp:
            tmp.write(self.file.read())
            if self.type == 'pdf':
                pages = PyPDFLoader(tmp.name).load_and_split()
            elif self.type == 'csv':
                pages = CSVLoader(tmp.name).load_and_split()
            else :
                pages = UnstructuredExcelLoader(tmp.name).load_and_split()
        os.remove(tmp.name)
        return pages
    
    def read_PDF(file):
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text