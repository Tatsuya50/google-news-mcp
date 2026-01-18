import chromadb
import os

def inspect_chroma():
    # ChromaDBの保存先パスを設定
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "chroma_db")
    
    print(f"Connecting to ChromaDB at: {db_path}")
    client = chromadb.PersistentClient(path=db_path)
    
    # コレクションの一覧を表示
    collections = client.list_collections()
    print(f"Available Collections: {[c.name for c in collections]}")
    
    if not collections:
        print("No collections found.")
        return

    # 'google_news' コレクションを取得
    collection = client.get_collection(name="google_news")
    
    # 登録件数を確認
    count = collection.count()
    print(f"\nTotal items in 'google_news': {count}")
    
    if count == 0:
        return

    # 全て（または一部）のデータを取得
    # get() を使うと、ids, documents, metadatas が返ってきます
    data = collection.get(
        include=["documents", "metadatas"]
    )
    
    print("\n--- Items Overview ---")
    for i in range(min(count, 10)):  # 最初の10件を表示
        doc = data['documents'][i]
        meta = data['metadatas'][i]
        item_id = data['ids'][i]
        
        print(f"\n[ID: {item_id}]")
        print(f"Topic: {meta.get('topic')}")
        print(f"Publisher: {meta.get('publisher')}")
        print(f"Date: {meta.get('published_date')}")
        print(f"URL: {meta.get('url')}")
        print(f"Content Outline: {doc[:100]}...")

if __name__ == "__main__":
    inspect_chroma()
