# ================================================================================
# This script is run only once when loading all the data and 
# creating the vector database.
# ================================================================================


from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import (PyPDFLoader, 
                                        DirectoryLoader, 
                                         Docx2txtLoader, CSVLoader)
from langchain.embeddings import HuggingFaceEmbeddings

# Embedding model loading
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                model_kwargs={'device': 'cpu'})

# Recursive text splitting
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                                chunk_overlap=50)


def load_data(directory):
    """ This function loads and splits the files

    Parameters:
    `directory (str): Path where data is located`

    Returns:
    List: Returns a list of processed Langchain Document objects
   """
    #Inititating all loaders
    pdf_loader = DirectoryLoader(directory,
                                glob='*.pdf',
                                loader_cls=PyPDFLoader)
    docx_loader = DirectoryLoader(directory,
                                glob='*.docx',
                                loader_cls=Docx2txtLoader)
    spotify_loader = CSVLoader(file_path=f'{directory}spotify.csv')

    insta_following_loader = CSVLoader(file_path=f'{directory}insta_following.csv')
    insta_followers_loader = CSVLoader(file_path=f'{directory}insta_followers.csv')

    # Loading all documents
    pdf_documents = pdf_loader.load()
    docx_documents = docx_loader.load()
    spotify_documents = spotify_loader.load()
    insta_following_documents = insta_following_loader.load()
    insta_followers_documents = insta_followers_loader.load()

    # Adding all loaded documents to one single list of Documents
    corpus = pdf_documents
    corpus.extend(docx_documents)
    corpus.extend(spotify_documents)
    corpus.extend(insta_following_documents)
    corpus.extend(insta_followers_documents)

    # Splitting all documents
    corpus_processed = text_splitter.split_documents(corpus)
    return corpus_processed


def vectordb_store(corpus_processed):
    """ This function takes in the split documents,
    creates vector embeddings, indexes with the help
    of FAISS and stores them locally.

    Parameters:
    corpus_processed (List): List of Langchain Document objects

    Returns: None
   """
    vectorstore = FAISS.from_documents(corpus_processed, embeddings)
    vectorstore.save_local('vectorstore/db_faiss')

if __name__=="__main__":
    vectordb_store(load_data('data/'))