# openAI
Exploring OpenAI APIs

The DocumentSummarizer is a Streamlit application designed to simplify document summarization. Users can upload PDF, CSV, and Excel documents, which are then summarized using the Stuff Chain from Langchain. However, it's important to note that the Stuff Chain has a limitation on token count, which can be problematic for lengthy documents. To address this issue, the application offers alternative summarization methods such as Map-Reduce or Refine chains, which are available in the Summarizer.py file.

To ensure smooth functionality, users are required to input a valid OpenAI API key. This key enables access to the OpenAI API, which powers the summarization process.
