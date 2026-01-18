import chromadb
from sentence_transformers import SentenceTransformer
from gnews import GNews
import hashlib
import datetime
import os

class NewsIngester:
    def __init__(self, db_path=None):
        if db_path is None:
            # Default to a folder named 'chroma_db' in the same directory as this script
            base_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(base_dir, "chroma_db")
            
        # print(f"Initializing ChromaDB at: {db_path}")
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name="google_news")
        
        # print("Loading embedding model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.google_news = GNews()

    def fetch_and_index(self, topic, max_results=5):
        # print(f"Fetching news for topic: {topic} (max: {max_results})")
        self.google_news.max_results = max_results
        news_items = self.google_news.get_news(topic)
        
        if not news_items:
            # print("No news items found.")
            return 0

        documents = []
        metadatas = []
        ids = []

        # print(f"Found {len(news_items)} items. Processing...")

        for item in news_items:
            url = item.get('url')
            if not url:
                continue
                
            # Create a deterministic ID based on URL
            doc_id = hashlib.md5(url.encode('utf-8')).hexdigest()
            
            title = item.get('title', '')
            description = item.get('description', '')
            
            # Combine title and description for the embedding content
            text_content = f"{title}\n{description}"
            
            documents.append(text_content)
            ids.append(doc_id)
            
            # Flatten publisher dict for metadata
            publisher_title = item.get('publisher', {}).get('title', 'Unknown')
            
            # Prepare metadata
            meta = {
                'url': url,
                'published_date': item.get('published date', ''),
                'publisher': publisher_title,
                'topic': topic,
                'ingested_at': datetime.datetime.now().isoformat()
            }
            metadatas.append(meta)

        if not documents:
            return 0

        # Generate embeddings
        # print("Generating embeddings...")
        embeddings = self.model.encode(documents).tolist()

        # Upsert to Chroma
        # print("Saving to ChromaDB...")
        self.collection.upsert(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        
        return len(documents)

    def query_db(self, query_text, n_results=3):
        # print(f"Querying for: {query_text}")
        query_embedding = self.model.encode([query_text]).tolist()
        
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        return results

if __name__ == "__main__":
    # Internal test
    ingester = NewsIngester()
    count = ingester.fetch_and_index("Python Programming", max_results=1)
    print(f"Indexed {count} articles.")
