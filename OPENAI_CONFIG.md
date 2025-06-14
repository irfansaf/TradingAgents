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

### Important Note
The `OPENAI_API_KEY` environment variable is the standard way that OpenAI clients look for API keys. You must set this environment variable for the system to work. The configuration system will use this automatically, or you can override it by setting it in the configuration.

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

## Implementation Details

The configuration is loaded through:
1. `tradingagents/default_config.py` - Defines default values and loads from environment
2. `tradingagents/utils/openai_utils.py` - Utility functions for creating configured clients
3. `tradingagents/agents/utils/memory.py` - Memory system uses configured embedding model
4. `tradingagents/dataflows/interface.py` - API functions use configured clients

All OpenAI clients (both LangChain ChatOpenAI and direct OpenAI clients) will automatically use these environment variables when available.