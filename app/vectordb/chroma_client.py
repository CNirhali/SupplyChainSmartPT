import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any

class ChromaClient:
    """
    Client for interacting with a local ChromaDB instance for document storage and semantic search.
    """
    def __init__(self, persist_directory: str = 'chroma_db'):
        self.client = chromadb.Client(Settings(persist_directory=persist_directory))
        self.collection = self.client.get_or_create_collection('inventory_docs')

    def add_documents(self, docs: List[str], embeddings: List[List[float]], metadatas: List[Dict[str, Any]] = None):
        """
        Add documents and their embeddings to the collection.
        Args:
            docs (List[str]): List of document texts.
            embeddings (List[List[float]]): List of embedding vectors.
            metadatas (List[Dict[str, Any]], optional): Metadata for each document.
        """
        try:
            self.collection.add(
                documents=docs,
                embeddings=embeddings,
                metadatas=metadatas or [{} for _ in docs]
            )
        except Exception as e:
            print(f'Error adding documents to ChromaDB: {e}')

    def similarity_search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Perform a similarity search using a query embedding.
        Args:
            query_embedding (List[float]): Embedding vector for the query.
            top_k (int): Number of top results to return.
        Returns:
            List[Dict[str, Any]]: List of matching documents and metadata.
        """
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            return results
        except Exception as e:
            print(f'Error querying ChromaDB: {e}')
            return [] 