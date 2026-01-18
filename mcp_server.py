from fastmcp import FastMCP
from news_ingester import NewsIngester

# Initialize the MCP server
mcp = FastMCP("Google News Agent")

# Initialize backend (will create DB if not exists)
ingester = NewsIngester()

@mcp.tool()
def ingest_news(topic: str, max_results: int = 5) -> str:
    """
    Fetches news articles from Google News for a given topic, generates vector embeddings,
    and stores them in a local ChromaDB database.
    """
    try:
        count = ingester.fetch_and_index(topic, max_results)
        if count == 0:
            return f"No articles found for topic '{topic}'."
        return f"Successfully ingested {count} articles for topic '{topic}'."
    except Exception as e:
        return f"Error ingesting news: {str(e)}"

@mcp.tool()
def search_news(query: str, n_results: int = 3) -> str:
    """
    Searches the stored news articles using semantic search.
    """
    try:
        results = ingester.query_db(query, n_results)
        
        if not results or not results['documents'] or not results['documents'][0]:
             return "No matching news found."
             
        output = []
        for i, doc in enumerate(results['documents'][0]):
            meta = results['metadatas'][0][i]
            source = meta.get('publisher', 'Unknown')
            date = meta.get('published_date', 'Unknown')
            url = meta.get('url', '#')
            
            # Truncate content for display if too long
            content_preview = doc[:300] + "..." if len(doc) > 300 else doc
            
            output.append(
                f"--- Result {i+1} ---\n"
                f"Title/Content: {content_preview}\n"
                f"Source: {source}\n"
                f"Date: {date}\n"
                f"URL: {url}\n"
            )
            
        return "\n".join(output)
    except Exception as e:
        return f"Error searching news: {str(e)}"

if __name__ == "__main__":
    mcp.run()
