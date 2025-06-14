# OpenAI Configuration

This document explains how to configure OpenAI settings for the TradingAgents project using environment variables.

## Environment Variables

The following environment variables can be set to customize OpenAI behavior:

### Required
- `OPENAI_API_KEY`: Your OpenAI API key (this is the standard OpenAI environment variable)

### Optional
- `OPENAI_BASE_URL`: Custom base URL for OpenAI API (useful for proxies or alternative endpoints)
- `OPENAI_DEEP_THINK_MODEL`: Model to use for deep thinking tasks (default: `o4-mini`)
- `OPENAI_QUICK_THINK_MODEL`: Model to use for quick thinking tasks (default: `gpt-4o-mini`)
- `OPENAI_EMBEDDING_MODEL`: Model to use for embeddings (default: `text-embedding-ada-002`)

### Important Notes

1. **API Key**: The `OPENAI_API_KEY` environment variable is the standard way that OpenAI clients look for API keys. You must set this environment variable for the system to work.

2. **Automatic Embedding Provider Selection**: The system automatically detects your provider and uses the appropriate embedding service:
   - **OpenAI/Azure**: Uses OpenAI's embedding API (e.g., `text-embedding-ada-002`)
   - **Other providers** (DeepSeek, etc.): Automatically uses Hugging Face sentence-transformers (e.g., `all-MiniLM-L6-v2`)
   
   This ensures backward compatibility - when you switch back to OpenAI, embeddings will automatically use OpenAI's service again.

## Setup

1. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and set your values:
   ```bash
   # OpenAI Configuration
   OPENAI_API_KEY=your_api_key_here
   OPENAI_BASE_URL=https://api.openai.com/v1  # Optional
   OPENAI_DEEP_THINK_MODEL=o4-mini
   OPENAI_QUICK_THINK_MODEL=gpt-4o-mini
   OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
   ```

## Usage Examples

### Using Default Configuration
If you don't set any environment variables, the system will use the default models and the standard OpenAI API endpoint.

### Using Custom Models
```bash
OPENAI_DEEP_THINK_MODEL=gpt-4
OPENAI_QUICK_THINK_MODEL=gpt-3.5-turbo
```

### Using Custom Base URL (for proxies or alternative endpoints)
```bash
OPENAI_BASE_URL=https://your-proxy.com/v1
```

### Using Azure OpenAI
```bash
OPENAI_BASE_URL=https://your-resource.openai.azure.com/
OPENAI_API_KEY=your_azure_api_key
```

### Using DeepSeek
```bash
OPENAI_BASE_URL=https://api.deepseek.com/v1
OPENAI_API_KEY=your_deepseek_api_key
OPENAI_DEEP_THINK_MODEL=deepseek-reasoner
OPENAI_QUICK_THINK_MODEL=deepseek-chat
OPENAI_EMBEDDING_MODEL=all-MiniLM-L6-v2
```

**Note**: When using DeepSeek, embeddings will automatically use Hugging Face's `all-MiniLM-L6-v2` model since DeepSeek doesn't provide embedding services. The system will download this model on first use.

## Implementation Details

The configuration is loaded through:
1. `tradingagents/default_config.py` - Defines default values and loads from environment
2. `tradingagents/utils/openai_utils.py` - Utility functions for creating configured clients
3. `tradingagents/agents/utils/memory.py` - Memory system uses configured embedding model
4. `tradingagents/dataflows/interface.py` - API functions use configured clients

All OpenAI clients (both LangChain ChatOpenAI and direct OpenAI clients) will automatically use these environment variables when available.