# openAI
Requirements:
Python and pip are required to run the application. Ensure that both are installed on your system.

To install the necessary libraries, use the command:
```
pip install -r requirements.txt
```
This command will install all the required libraries listed in the requirements.txt file.

To run the application, use the following command:
```
streamlit run .\DocumentSummarizer\langchain_Summarizer.py
```
This command will execute the DocumentSummarizer application and allow you to upload and summarize documents.

Exploring OpenAI APIs

The DocumentSummarizer is a Streamlit application designed to simplify document summarization. Users can upload PDF, CSV, and Excel documents, which are then summarized using the Stuff Chain from Langchain. However, it's important to note that the Stuff Chain has a limitation on token count, which can be problematic for lengthy documents. To address this issue, the application offers alternative summarization methods such as Map-Reduce or Refine chains, which are available in the Summarizer.py file.

To ensure smooth functionality, users are required to input a valid OpenAI API key. This key enables access to the OpenAI API, which powers the summarization process.
