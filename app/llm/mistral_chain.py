from typing import List
from langchain_community.llms.ollama import Ollama
from langchain_community.embeddings.ollama import OllamaEmbeddings

class MistralLLM:
    """
    Interface to local Mistral LLM via Ollama for embedding generation and Q&A using LangChain.
    """
    def __init__(self, model_name: str = 'mistral'):
        self.model_name = model_name
        self.llm = Ollama(model=model_name)
        self.embedder = OllamaEmbeddings(model=model_name)

    def get_embedding(self, text: str) -> List[float]:
        """
        Generate an embedding for the given text using Ollama.
        Args:
            text (str): Input text.
        Returns:
            List[float]: Embedding vector.
        """
        try:
            return self.embedder.embed_query(text)
        except Exception as e:
            print(f'Error generating embedding: {e}')
            return []

    def answer_question(self, context: str, question: str) -> str:
        """
        Use the LLM to answer a question given some context using Ollama.
        Args:
            context (str): Contextual information (retrieved docs).
            question (str): User's question.
        Returns:
            str: LLM-generated answer.
        """
        try:
            prompt = f"You are an inventory assistant. Use the following context to answer the question.\nContext: {context}\nQuestion: {question}\nAnswer:"
            result = self.llm.invoke(prompt)
            return result.strip()
        except Exception as e:
            print(f'Error generating answer: {e}')
            return "Sorry, I couldn't generate an answer." 