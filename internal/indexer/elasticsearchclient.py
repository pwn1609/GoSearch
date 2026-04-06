from elasticsearch import ElasticSearch

class ESClient:
    def __init__(self, host, index):
        self.client = self.init_connection(host, index)
        self.index = index

    def init_connection(self, host):
        return ElasticSearch(host)

    # def post_index(self):
        