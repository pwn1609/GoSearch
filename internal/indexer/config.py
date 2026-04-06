import yaml

class Config:
    
    def __init__(self, filepath):
        self.config_map = self.open_config_file(filepath)
        self.set_config_values()


    def open_config_file(self, filepath):
        
        with open(filepath) as f:
            config = yaml.safe_load(f)
        
        return config

    def set_config_values(self):
        
        self.es_host = self.config_map.get("elasticsearch", "host", fallback=None)
        if self.es_host == None:
            raise ValueError("Config Missing Elastic Search Host")
        
        self.es_index = self.config_map.get("elasticsearch", "index", fallback=None)
        if self.es_index == None:
            raise ValueError("Config Missing Elastic Search Index")
        
        


            