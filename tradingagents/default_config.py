import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DEFAULT_CONFIG = {
    "project_dir": os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
    "data_dir": os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
        "dataflows/data_cache",
    ),
    "data_cache_dir": os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
        "dataflows/data_cache",
    ),
    # LLM settings
    "deep_think_llm": os.getenv("OPENAI_DEEP_THINK_MODEL", "o4-mini"),
    "quick_think_llm": os.getenv("OPENAI_QUICK_THINK_MODEL", "gpt-4o-mini"),
    "openai_base_url": os.getenv("OPENAI_BASE_URL"),
    "openai_api_key": os.getenv("OPENAI_API_KEY"),
    "embedding_model": os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002"),
    # Debate and discussion settings
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
    "max_recur_limit": 100,
    # Tool settings
    "online_tools": True,
}
