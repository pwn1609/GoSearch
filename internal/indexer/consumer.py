from kafka import KafkaConsumer

#upgrade to confluence-kafka in the future

class Consumer:
    def __init__(self, broker, topic):
        self.client = self._init_connection(broker, topic)

    def _init_connection(self, broker, topic) -> KafkaConsumer:
        
        try:
            consumer = KafkaConsumer(
                topic,  # Topic to subscribe to
                bootstrap_servers=broker,
                auto_offset_reset='earliest',  # Start from the beginning if no offset is stored
                group_id='index-group'
            )
            print(consumer.topics())
            return consumer
        except:
            print("Failed to connect to Kafka Broker")
            raise RuntimeError
        
    def __iter__(self):
        return self

    def __next__(self):
        try:
            return next(self.client)
        except Exception as e:
            print(f"Kafka Conn Closing on Exception: {e}")
            self.client.close()
            raise StopIteration