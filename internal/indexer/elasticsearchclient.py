from elasticsearch import Elasticsearch

class ESClient:
    def __init__(self, host, index):
        self.client = self.init_connection(host, index)
        self.index = index

    def init_connection(self, host):
        return Elasticsearch(host)

    # def post_index(self):
        