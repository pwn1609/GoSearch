from elasticsearch import Elasticsearch
from dataclasses import dataclass

PAGE_MAPPING = {
    "mappings": {
        "properties": {
            "url":       {"type": "keyword"},
            "title":     {"type": "text"},
            "body":      {"type": "text"},
            "timestamp": {"type": "date"},
        }
    }
}

class ESClient:
    def __init__(self, host, index, username=None, password=None):
        self.client = self.init_connection(host, username, password)
        self.index = index

    def init_connection(self, host, username, password):
        if username and password:
            return Elasticsearch(host, basic_auth=(username, password))
        return Elasticsearch(host)

    def ensure_index(self):
        if not self.client.indices.exists(index=self.index):
            self.client.indices.create(index=self.index, body=PAGE_MAPPING)
            print(f"Created index '{self.index}'")
        else:
            print(f"Index '{self.index}' already exists")
    
    def post_to_index(self, doc) -> bool: #add some sort of retry logic
        print(doc.url)



@dataclass
class Indexed_Page:
    url: str
    title: str
    body: str
    timestamp: str