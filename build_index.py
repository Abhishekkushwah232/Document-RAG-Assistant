from src.loader import load_documents
from src.chunker import chunk_docs
from src.vectorstore import build_index

# replicate the previous behaviour of building an index from the data directory

docs = load_documents()
chunks = chunk_docs(docs)
build_index(chunks)

print("Index built successfully")
