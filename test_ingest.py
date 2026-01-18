from news_ingester import NewsIngester

def test_ingestion():
    ingester = NewsIngester()
    print("Ingesting news about 'Artificial Intelligence'...")
    count = ingester.fetch_and_index("Artificial Intelligence", max_results=2)
    print(f"Ingested {count} articles.")
    
    print("Searching for 'Neural Networks'...")
    results = ingester.query_db("Neural Networks", n_results=1)
    if results['documents'] and results['documents'][0]:
        print("Found result:", results['documents'][0][0][:100])
    else:
        print("No results found.")

if __name__ == "__main__":
    test_ingestion()
