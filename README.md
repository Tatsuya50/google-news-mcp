# Google News MCP Agent

An MCP (Model Context Protocol) server that fetches news articles from Google News, vectorizes them locally using ChromaDB, and allows for semantic search. This tool enables AI agents (like Claude) to stay updated with specific topics and query stored knowledge effectively.

## Features

- **Ingest News**: Fetch headlines and summaries from Google News by topic.
- **Local Vector Store**: Automatically embeds and stores articles in a local ChromaDB instance (persisted in `chroma_db/`).
- **Semantic Search**: Search through the ingested news using natural language queries to find relevant information.
- **Privacy First**: Runs entirely locally (excluding the initial news fetch). No API keys required for embeddings (uses `sentence-transformers`).

## Prerequisites

- Python 3.10 or higher
- `uv` (recommended) or `pip`

## Installation

### Using uv (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/Tatsuya50/google-news-mcp.git
   cd google-news-mcp
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

### Using pip

1. Clone the repository and navigate to the directory.
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration (Claude Desktop)

To use this with Claude Desktop, add the following configuration to your MCP config file (typically `~/AppData/Roaming/Claude/claude_desktop_config.json` on Windows):

```json
{
  "mcpServers": {
    "google-news": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\Users\\YOUR_USERNAME\\path\\to\\google-news-mcp",
        "run",
        "python",
        "mcp_server.py"
      ]
    }
  }
}
```

*Note: Replace `C:\\Users\\YOUR_USERNAME\\path\\to\\google-news-mcp` with the actual absolute path to this repository.*

## Tools

### `ingest_news`
Fetches and indexes news articles.
- **topic**: The topic to search for (e.g., "Generative AI", "Stock Market").
- **max_results**: (Optional) Number of articles to fetch (default: 5).

### `search_news`
Searches the stored local database.
- **query**: The question or topic to search for (e.g., "What are the latest AI trends?").
- **n_results**: (Optional) Number of results to return (default: 3).

## Development

Run the server locally for testing:

```bash
uv run python mcp_server.py
```

Inspect the database contents:

```bash
uv run python inspect_db.py
```
