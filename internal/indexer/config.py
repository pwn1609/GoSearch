import os
import yaml

class Config:
    
    def __init__(self, filepath):
        self.config_map = self.open_config_file(filepath)
        self.set_config_values()

    def open_config_file(self, filepath):
        with open(filepath) as f:
            return yaml.safe_load(f)

    def set_config_values(self):
        es_config = self.config_map.get("elasticsearch", {})
        kfk_config = self.config_map.get("kafka", {})

        self.es_host = es_config.get("host")
        if self.es_host is None:
            raise ValueError("Config Missing Elastic Search Host")

        self.es_index = es_config.get("index")
        if self.es_index is None:
            raise ValueError("Config Missing Elastic Search Index")

        self.es_username = os.environ.get("ES_USERNAME")
        self.es_password = os.environ.get("ES_PASSWORD")

        self.kfk_brokers = kfk_config.get("brokers")
        if not self.kfk_brokers:
            raise ValueError("Config Missing Kafka Brokers")
         
        self.kfk_topic = kfk_config.get("topic")
        if self.kfk_topic is None:
            raise ValueError("Config Missing Kafka Topic") 