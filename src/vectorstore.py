from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
INDEX_PATH = "medical_index"


# Create embedding model ONCE at module load
_embeddings = HuggingFaceEmbeddings(
    model_name=EMBED_MODEL,
    model_kwargs={"device": "cpu"}
)


def build_index(chunks, index_path: str = INDEX_PATH):

    db = FAISS.from_documents(chunks, _embeddings)

    db.save_local(index_path)

    print("✅ Vector index built and saved.")


def rebuild_index_from_dir(data_dir: str = "data", index_path: str = INDEX_PATH):
    """Convenience wrapper that rebuilds the vector store from a directory.

    This mirrors the logic in ``build_index.py`` but is callable from the
    web UI when users upload new documents.
    """
    from src.loader import load_documents
    from src.chunker import chunk_docs

    docs = load_documents(path=data_dir)
    chunks = chunk_docs(docs)
    build_index(chunks, index_path=index_path)


def load_index():
    """Load existing FAISS index from disk.

    Raises a RuntimeError with instructions if the index directory
    doesn't exist or the .faiss file is missing. This helps newcomers
    avoid the opaque faiss exception seen when the file is absent.
    """

    try:
        db = FAISS.load_local(
            INDEX_PATH,
            _embeddings,
            allow_dangerous_deserialization=True
        )
    except Exception as exc:
        # faiss throws a low-level runtime error when it can't find the
        # file; wrap it to make the recovery step clear.
        raise RuntimeError(
            "Vector index not found. Please run `python build_index.py` "
            "to generate the embedding index before starting the app."
        ) from exc

    return db
