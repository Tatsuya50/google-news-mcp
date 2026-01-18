import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn
from news_ingester import NewsIngester

# NewsIngesterの初期化（ChromaDB等のバックエンドを準備）
ingester = NewsIngester()

app = FastAPI(
    title="Google News Agent API",
    description="Google Newsのフェッチおよびベクトル検索用インターフェース"
)

# リクエストモデルの定義
class SearchRequest(BaseModel):
    query: str
    n_results: Optional[int] = 3

class IngestRequest(BaseModel):
    topic: str
    max_results: Optional[int] = 5

# APIエンドポイント: 検索
@app.post("/api/search")
async def search(req: SearchRequest):
    """保存されたニュースからベクトル検索を実行します。"""
    try:
        results = ingester.query_db(req.query, req.n_results)
        return results
    except Exception as e:
        print(f"Search Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# APIエンドポイント: ニュース取得
@app.post("/api/ingest")
async def ingest(req: IngestRequest):
    """Google Newsから最新ニュースを取得し、ベクトルDBへ保存します。"""
    try:
        count = ingester.fetch_and_index(req.topic, req.max_results)
        return {"status": "success", "count": count, "message": f"{count}件のニュースを取得しました。"}
    except Exception as e:
        print(f"Ingest Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# 静的ファイルの提供
app.mount("/static", StaticFiles(directory="static"), name="static")

# ルートアクセス時にindex.htmlを返す
@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    # Tailscale経由でアクセスするため、0.0.0.0でホスト
    uvicorn.run(app, host="0.0.0.0", port=8000)
