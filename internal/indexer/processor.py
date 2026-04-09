from elasticsearchclient import ESClient, Indexed_Page
from consumer import Consumer
from kafka import ConsumerRecord

class Processor:
    def __init__(self, elasticsearch: ESClient, kafka: Consumer) -> None:
        self.es_client = elasticsearch
        self.kfk_client = kafka

    def pull_messages(self) -> None:
        for msg in self.kfk_client:
            self.process_message(msg)

    def process_message(self, msg: ConsumerRecord) -> None:
        normalized_url = self.normalize_url(msg.key)
        page_title = self.get_title(msg.value)
        cleaned_text = self.process_html(msg.value)

        page = Indexed_Page(url=normalized_url, title=page_title, body=cleaned_text, timestamp=msg.time)
        self.es_client.post_to_index(page)

    def normalize_url(self, url: str) -> str:
        pass

    def get_title(self, htlm_body: str) -> str:
        pass

    def process_html(self, html_body: str) -> str:
        pass