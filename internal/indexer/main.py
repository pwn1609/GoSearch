
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

def main():

    #init config
    filepath = "./internal/indexer/config.py"
    config = Config(filepath)
    es = ESClient(config.es_host, config.es_index)

    print(es.info())


if __name__ == "__main__":
    main()