
#TODO in order:
#Load config
#INIT elasticsearch connection
#Verify index and map are created
#INIT kafka consumer - subscribe to kafka topic
#Begin consuming data
#Process Data
#Post to elastic search

from config import Config
from elasticsearchclient import ESClient
from processor import Processor
from consumer import Consumer

def main():
    
    #init config
    filepath = "/app/config/indexer_config.yaml"
    config = Config(filepath)
    #init Elasticsearch
    es = ESClient(config.es_host, config.es_index, config.es_username, config.es_password)
    es.ensure_index()

    #init kafka consumer
    kaf = Consumer(config.kfk_brokers, config.kfk_topic)
    
    #init processor
    proc = Processor(es, kaf)
    proc.pull_messages()


if __name__ == "__main__":
    main()