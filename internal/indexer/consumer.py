from kafka import KafkaConsumer

from config import KafkaConfig
from indexer import Indexer
from parser import parse_page


class Consumer:
    def __init__(self, cfg: KafkaConfig, indexer: Indexer):
        self._indexer = indexer
        self._consumer = KafkaConsumer(
            cfg.topic,
            bootstrap_servers=cfg.brokers,
            group_id=cfg.group_id,
            auto_offset_reset="earliest",
            enable_auto_commit=False,
        )

    def run(self):
        print("Consumer started, waiting for messages...")
        for message in self._consumer:
            url = message.key.decode("utf-8") if message.key else ""
            html = message.value.decode("utf-8") if message.value else ""

            print(f"Processing: {url}")
            page = parse_page(url, html)
            self._indexer.upsert(page)
            self._consumer.commit()
            print(f"Indexed: {url} | title={page.title!r}")

    def close(self):
        self._consumer.close()
