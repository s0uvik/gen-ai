from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()

# loads pdf
file_path = Path(__file__).parent / "nodejs.pdf"
loader = PyPDFLoader(file_path=file_path)

# pdf to normal text
docs = loader.load()

# do text chunking
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400)
split_docs = text_splitter.split_documents(documents=docs)

# do vector embedding of chunked text
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

# store those in vector db
QdrantVectorStore.from_documents(
    documents=split_docs,
    url="http://localhost:6333",
    collection_name="my vector",
    embedding=embedding_model,
)
