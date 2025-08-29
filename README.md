# Chatbots-with-LangChain-Large-Language-Model

### Summary

The primary goal of this project is to create a system that can programmatically ingest, process, and store the information contained within a package of data sets from an equity research analyst in the pharmacy space. This system will store the information in a vector database that stores embeddings, enabling an LLM to effectively query and reason with this data.

The system will be evaluated based on its ability to accurately answer a set of sample questions provided by the sponsors, such as " How many scripts were written for Biktarvy in Quarter 1, 2023?" A stretch goal is to use an LLM chain, such as LangChain, to build an end-to-end pipeline to interact with the documents that have been stored and processed. This would enable the system to handle complex queries. The ultimate goal is to create a scalable foundation that can be expanded upon later, enhancing Ultima's decision-making processes and financial risk assessments, and providing them with a competitive advantage in the market.

Multiple CSV files can be uploaded with this Chatbot. Following that, it loads the data into text documents based on the data source. 
Next, these text documents are embedded using instructor embeddings, which are stored as vector datasets in ActiveLoop's database hub. Then the vector store is used as the retriever of a langchain that consists of an LLM model (default GPT-4). After embedding the input prompt, the chain performs a similarity search in the vector store and then renders the appropriate response based on the best results. Lastly, the chat history is cached locally so that Q&A conversations can be conducted similarly to ChatGPT. The following are details of some of the key techniques and technologies used to develop this chatbot (Figure 1).

Figure 1:
 
<img width="351" height="205" alt="image" src="https://github.com/user-attachments/assets/5f03f380-2324-41b2-86a0-32c20ef647a4" />


### Data Loading:
The app works by uploading files from the local directory. Afterward, the app detects and loads the data source into text documents. It embeds the documents using instructor-XL embeddings, then stores the embeddings in a vector dataset on ACTIVELOOP's Deep Lake Cloud. For details on loading and execution, please refer to the terminal logs below (Figure 2).


Figure 2:

<img width="468" height="205" alt="image" src="https://github.com/user-attachments/assets/9ca2e8a1-0635-4975-93b3-319b7cd1794f" />

### Instructor Embedding:
Ultima-2 chatbot uses instructor embeddings to index and search text documents. Instructors generate text embeddings tailored to any task including classification, retrieval, clustering, and text evaluation in science and finance. The instructor embedding technique converts the text into tokens first. Using these tokens, a vector representation of the text is generated. Next, this vector representation is used to train a model that predicts how text was generated. The following diagram illustrates how instructor embedding works (Figure 3).

Figure 3:

<img width="236" height="140" alt="image" src="https://github.com/user-attachments/assets/23a0b933-20d4-487a-bd30-26bc07025b19" />

Image Credit: https://itnext.io/harnessing-local-language-models-a-guide-to-transitioning-from-openai-to-on-premise-power-81cfc159bf1e

### Vector Store:
As mentioned earlier, the embeddings generated from text documents are stored in Deep Lake [4], a vector database that is used by the Ultima-2 chatbot. It is efficient and optimized to use vector databases for large datasets. A major advantage that Deep Lake has over other vector databases is that it supports multiple types of data and stores embedded metadata more efficiently. As a result of the data integration capabilities it offers, it is a great choice when it comes to developing chat applications.

### Large Language Models & LangChain: 
The Ultima-2 chatbot utilizes large language models (LLMs) like GPT-4 to generate responses to user inquiries. Generally, LLMs are highly capable models, which are trained on large amounts of text data, which allows them to generate natural language responses to a wide variety of questions. Ultima-2 chatbot employs LangChain to merge embeddings and large language models (LLMs) into a unified retrieval chain, enabling it to respond to user queries effectively.  
Parameters: As part of the functionality of this chatbot, the user has the flexibilities to adjust some of the key parameters mentioned below that play key roles in feeding the data, generating embeddings, and providing responses in the form of ConversationalRetrievalQA chains [8].
*	chunk_size: In LangChain-based apps, chunk_size determines how much text will be divided into smaller chunks before it is embedded. In addition to ensuring efficient processing of large documents, this parameter controls the granularity of embedding results
*	 fetch_k: This parameter specifies the number of documents to pull from the vector database.
*	 K: k represents the most similar embeddings selected by LangChain-based apps for building the context for the LLM prompt.
*	 max_token: This parameter determines how many documents are returned from the vector store before creating the context to query the large language models.
*	 temperature: It controls the LLM output randomness. Temperatures greater than zero result in greater variation in response, while temperatures less than zero result in deterministic response.

### Text Splitter:
During this project, we were able to compare the results of different LangChain text splitters by using different measures. To demonstrate the results of different text splitters, we compiled the results in a separate Excel file and attached them to the project's final deliverable. Nonetheless, the following diagram summarizes how each of these text splitters performed in response to different questions that were asked through this chatbot interface (Figure 4).

Figure 4: 

<img width="299" height="137" alt="image" src="https://github.com/user-attachments/assets/feca954a-43b9-4ede-b763-ffc986eecd8b" />

### Limitation of Method:
* This app might run into errors due to the prompt length that can be resolved by adjusting the parameters mentioned above. 
*	In some cases, the answers are hallucinatory or do not correlate with the true data content. Changing the temperature may help to overcome such tendencies.  
*	In some cases, the answer may not be relevant, which can be resolved by increasing chunk_size.  

Evaluation of Method 1: 
We evaluated method-1 with the Ultima-2 chatbot using sample questions provided by the sponsor. Our objective was to test the app's ability to retrieve and process financial documents accurately. Test criteria included retrieving specific data points, performing calculations, and comparing values to provide answers to questions. We conducted two types of evaluations: Single Document Question-Answering and Multiple Document Question-Answering.


### References: 

[1] Recursively split by character. Langchain. (n.d.). https://python.langchain.com/docs/modules/data_connection/document_transformers/text_splitters/recursive_text_splitter 

[2] Split by character. Langchain. (n.d.). https://python.langchain.com/docs/modules/data_connection/document_transformers/text_splitters/character_text_splitter 

[3] Split by Token. Langchain. (n.d.). https://python.langchain.com/docs/modules/data_connection/document_transformers/text_splitters/split_by_token

[4] The database for AI by activeloop. Activeloop. (n.d.). https://app.activeloop.ai

[5] Text Embesdding Model (n.d)https://python.langchain.com/docs/modules/data_connection/text_embedding/

[6] Vector Stores (n.d) https://python.langchain.com/docs/modules/data_connection/vectorstores/

[7] Data Connection (n.d) https://python.langchain.com/docs/modules/data_connection/ 

[8] Conversational Retrieval QA. LangChain. (n.d.) https://python.langchain.com/docs/modules/chains/popular/chat_vector_db
