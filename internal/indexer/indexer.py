from datetime import datetime, timezone

from elasticsearch import Elasticsearch

from config import ElasticsearchConfig
from parser import ParsedPage

INDEX_MAPPING = {
    "mappings": {
        "properties": {
            "url":         {"type": "keyword"},
            "title":       {"type": "text"},
            "description": {"type": "text"},
            "body_text":   {"type": "text"},
            "indexed_at":  {"type": "date"},
        }
    }
}


class Indexer:
    def __init__(self, cfg: ElasticsearchConfig):
        self._index = cfg.index
        self._client = Elasticsearch(f"http://{cfg.host}:{cfg.port}")
        self._ensure_index()

    def _ensure_index(self):
        if not self._client.indices.exists(index=self._index):
            self._client.indices.create(index=self._index, body=INDEX_MAPPING)
            print(f"Created index '{self._index}'")

    def upsert(self, page: ParsedPage):
        doc = {
            "url":         page.url,
            "title":       page.title,
            "description": page.description,
            "body_text":   page.body_text,
            "indexed_at":  datetime.now(timezone.utc).isoformat(),
        }
        self._client.index(index=self._index, id=page.url, document=doc)

    def close(self):
        self._client.close()
