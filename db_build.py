from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, DirectoryLoader, Docx2txtLoader, TextLoader, CSVLoader
from langchain.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                model_kwargs={'device': 'cpu'})

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                                chunk_overlap=50)

def load_data(directory):
    pdf_loader = DirectoryLoader(directory,
                                glob='*.pdf',
                                loader_cls=PyPDFLoader)
    docx_loader = DirectoryLoader(directory,
                                glob='*.docx',
                                loader_cls=Docx2txtLoader)
    spotify_loader = CSVLoader(file_path=f'{directory}spotify.csv')
    pdf_documents = pdf_loader.load()
    docx_documents = docx_loader.load()
    spotify_documents = spotify_loader.load()

    corpus = pdf_documents
    corpus.extend(docx_documents)
    corpus.extend(spotify_documents)

    corpus_processed = text_splitter.split_documents(corpus)
    return corpus_processed

def vectordb_store(corpus_processed):
    vectorstore = FAISS.from_documents(corpus_processed, embeddings)
    vectorstore.save_local('vectorstore/db_faiss')

if __name__=="__main__":
    vectordb_store = load_data('data/')