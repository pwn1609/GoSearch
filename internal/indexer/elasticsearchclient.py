from elasticsearch import Elasticsearch

class ESClient:
    def __init__(self, host, index, username=None, password=None):
        self.client = self.init_connection(host, username, password)
        self.index = index

    def init_connection(self, host, username, password):
        if username and password:
            return Elasticsearch(host, basic_auth=(username, password))
        return Elasticsearch(host)

    # def post_index(self):
        