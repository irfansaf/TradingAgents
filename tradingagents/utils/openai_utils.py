"""Utility functions for OpenAI configuration."""

from langchain_openai import ChatOpenAI
from openai import OpenAI
from tradingagents.dataflows.config import get_config


def create_chat_openai(model: str, **kwargs) -> ChatOpenAI:
    """Create a ChatOpenAI instance with proper configuration from environment variables.
    
    Args:
        model: The model name to use
        **kwargs: Additional arguments to pass to ChatOpenAI
        
    Returns:
        Configured ChatOpenAI instance
    """
    config = get_config()
    
    # Build kwargs for ChatOpenAI
    llm_kwargs = {"model": model}
    
    if config.get("openai_base_url"):
        llm_kwargs["base_url"] = config["openai_base_url"]
    
    # Only set api_key if it's explicitly configured
    # If not set, let ChatOpenAI use the default OPENAI_API_KEY environment variable
    if config.get("openai_api_key"):
        llm_kwargs["api_key"] = config["openai_api_key"]
        
    # Merge with any additional kwargs provided
    llm_kwargs.update(kwargs)
    
    return ChatOpenAI(**llm_kwargs)


def create_openai_client() -> OpenAI:
    """Create an OpenAI client with proper configuration from environment variables.
    
    Returns:
        Configured OpenAI client
    """
    config = get_config()
    
    client_kwargs = {}
    if config.get("openai_base_url"):
        client_kwargs["base_url"] = config["openai_base_url"]
    
    # Only set api_key if it's explicitly configured
    # If not set, let OpenAI client use the default OPENAI_API_KEY environment variable
    if config.get("openai_api_key"):
        client_kwargs["api_key"] = config["openai_api_key"]
        
    return OpenAI(**client_kwargs)