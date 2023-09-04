# ================================================================================
# This script instantiates the RetreivalQA object and 
# creates the PromptTemplate object. It is called everytime the main script
# is run
# ================================================================================

from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Milvus
from prompts import qa_template
from llm import llm
from pymilvus import connections
from dbconfig import CONNECTION_HOST, CONNECTION_PORT, COLLECTION_NAME

def set_qa_prompt():
    """ This function wraps the prompt template in a PromptTemplate object

    Parameters:
    
    Returns:
    PromptTemplate Object: Returns the prompt template object
   """
    prompt = PromptTemplate(template=qa_template,
                            input_variables=['context', 'question'])
    return prompt

def build_retrieval_qa(llm, prompt, vectordb):
    """ This function builds the RetreivalQA object

    Parameters:
    llm (Object): The llm object
    prompt (Object): The prompt template
    vectordb (Object): The vector store

    Returns:
    RetreivalQA Object: Returns the best result
   """
    # Only retreiving the first best result
    dbqa = RetrievalQA.from_chain_type(llm=llm,
                                       chain_type='stuff',
                                       retriever=vectordb.as_retriever(search_kwargs={'k':1}),
                                       return_source_documents=True,
                                       chain_type_kwargs={'prompt': prompt})
    return dbqa

def setup_dbqa():
    """ This function instantiates the RetreivalQA object

    Parameters:
    llm (Object): The llm object
    prompt (Object): The prompt template
    vectordb (Object): The vector store

    Returns:
    RetreivalQA Object: Returns created object
   """
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                       model_kwargs={'device': 'cpu'})
    
    connections.connect("default", host="localhost", port="19530")

    vector_db: Milvus = Milvus(
    embedding_function=embeddings,
    connection_args={"host": CONNECTION_HOST, "port": CONNECTION_PORT},
    collection_name=COLLECTION_NAME
    )

    qa_prompt = set_qa_prompt()
    dbqa = build_retrieval_qa(llm, qa_prompt, vector_db)
    return dbqa


