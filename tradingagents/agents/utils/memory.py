import chromadb
from chromadb.config import Settings
from openai import OpenAI
import numpy as np
from tradingagents.dataflows.config import get_config
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False


class FinancialSituationMemory:
    def __init__(self, name, config=None):
        if config is None:
            config = get_config()
        
        self.config = config
        base_url = config.get("openai_base_url", "")
        
        # Determine if we should use OpenAI embeddings or Hugging Face
        self.use_openai_embeddings = (
            not base_url or 
            "openai.com" in base_url or 
            "azure.com" in base_url
        )
        
        if self.use_openai_embeddings:
            # Initialize OpenAI client for embeddings
            client_kwargs = {}
            if config.get("openai_base_url"):
                client_kwargs["base_url"] = config["openai_base_url"]
            
            # Only set api_key if it's explicitly configured
            # If not set, let OpenAI client use the default OPENAI_API_KEY environment variable
            if config.get("openai_api_key"):
                client_kwargs["api_key"] = config["openai_api_key"]
            self.client = OpenAI(**client_kwargs)
            self.embedding_model = config.get("embedding_model", "text-embedding-ada-002")
        else:
            # Use Hugging Face sentence-transformers for non-OpenAI providers
            if not SENTENCE_TRANSFORMERS_AVAILABLE:
                raise ImportError(
                    "sentence-transformers is required for non-OpenAI embedding providers. "
                    "Install it with: pip install sentence-transformers"
                )
            # Use a good general-purpose embedding model
            self.embedding_model = "all-MiniLM-L6-v2"  # Fast and good quality
            self.sentence_transformer = SentenceTransformer(self.embedding_model)
            self.client = None  # No OpenAI client needed for embeddings
        
        self.chroma_client = chromadb.Client(Settings(allow_reset=True))
        self.situation_collection = self.chroma_client.create_collection(name=name)

    def get_embedding(self, text):
        """Get embedding for a text using either OpenAI or Hugging Face"""
        if self.use_openai_embeddings:
            # Use OpenAI embeddings
            response = self.client.embeddings.create(
                model=self.embedding_model, input=text
            )
            return response.data[0].embedding
        else:
            # Use Hugging Face sentence-transformers
            embedding = self.sentence_transformer.encode(text)
            return embedding.tolist()  # Convert numpy array to list for ChromaDB

    def add_situations(self, situations_and_advice):
        """Add financial situations and their corresponding advice. Parameter is a list of tuples (situation, rec)"""

        situations = []
        advice = []
        ids = []
        embeddings = []

        offset = self.situation_collection.count()

        for i, (situation, recommendation) in enumerate(situations_and_advice):
            situations.append(situation)
            advice.append(recommendation)
            ids.append(str(offset + i))
            embeddings.append(self.get_embedding(situation))

        self.situation_collection.add(
            documents=situations,
            metadatas=[{"recommendation": rec} for rec in advice],
            embeddings=embeddings,
            ids=ids,
        )

    def get_memories(self, current_situation, n_matches=1):
        """Find matching recommendations using OpenAI embeddings"""
        query_embedding = self.get_embedding(current_situation)

        results = self.situation_collection.query(
            query_embeddings=[query_embedding],
            n_results=n_matches,
            include=["metadatas", "documents", "distances"],
        )

        matched_results = []
        for i in range(len(results["documents"][0])):
            matched_results.append(
                {
                    "matched_situation": results["documents"][0][i],
                    "recommendation": results["metadatas"][0][i]["recommendation"],
                    "similarity_score": 1 - results["distances"][0][i],
                }
            )

        return matched_results


if __name__ == "__main__":
    # Example usage
    matcher = FinancialSituationMemory()

    # Example data
    example_data = [
        (
            "High inflation rate with rising interest rates and declining consumer spending",
            "Consider defensive sectors like consumer staples and utilities. Review fixed-income portfolio duration.",
        ),
        (
            "Tech sector showing high volatility with increasing institutional selling pressure",
            "Reduce exposure to high-growth tech stocks. Look for value opportunities in established tech companies with strong cash flows.",
        ),
        (
            "Strong dollar affecting emerging markets with increasing forex volatility",
            "Hedge currency exposure in international positions. Consider reducing allocation to emerging market debt.",
        ),
        (
            "Market showing signs of sector rotation with rising yields",
            "Rebalance portfolio to maintain target allocations. Consider increasing exposure to sectors benefiting from higher rates.",
        ),
    ]

    # Add the example situations and recommendations
    matcher.add_situations(example_data)

    # Example query
    current_situation = """
    Market showing increased volatility in tech sector, with institutional investors 
    reducing positions and rising interest rates affecting growth stock valuations
    """

    try:
        recommendations = matcher.get_memories(current_situation, n_matches=2)

        for i, rec in enumerate(recommendations, 1):
            print(f"\nMatch {i}:")
            print(f"Similarity Score: {rec['similarity_score']:.2f}")
            print(f"Matched Situation: {rec['matched_situation']}")
            print(f"Recommendation: {rec['recommendation']}")

    except Exception as e:
        print(f"Error during recommendation: {str(e)}")
