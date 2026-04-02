from config import load_config
from consumer import Consumer
from indexer import Indexer


def main():
    cfg = load_config("config.yaml")

    indexer = Indexer(cfg.elasticsearch)
    consumer = Consumer(cfg.kafka, indexer)

    try:
        consumer.run()
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        consumer.close()
        indexer.close()


if __name__ == "__main__":
    main()
