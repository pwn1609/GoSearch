import yaml
from dataclasses import dataclass, field


@dataclass
class KafkaConfig:
    brokers: list[str]
    topic: str
    group_id: str


@dataclass
class ElasticsearchConfig:
    host: str
    port: int
    index: str


@dataclass
class Config:
    kafka: KafkaConfig
    elasticsearch: ElasticsearchConfig


def load_config(path: str = "config.yaml") -> Config:
    with open(path, "r") as f:
        raw = yaml.safe_load(f)

    kafka_raw = raw.get("kafka", {})
    es_raw = raw.get("elasticsearch", {})

    missing = []
    if not kafka_raw.get("brokers"):
        missing.append("kafka.brokers")
    if not kafka_raw.get("topic"):
        missing.append("kafka.topic")
    if not kafka_raw.get("group_id"):
        missing.append("kafka.group_id")
    if not es_raw.get("host"):
        missing.append("elasticsearch.host")
    if not es_raw.get("index"):
        missing.append("elasticsearch.index")

    if missing:
        raise ValueError(f"Missing required config fields: {', '.join(missing)}")

    return Config(
        kafka=KafkaConfig(
            brokers=kafka_raw["brokers"],
            topic=kafka_raw["topic"],
            group_id=kafka_raw["group_id"],
        ),
        elasticsearch=ElasticsearchConfig(
            host=es_raw["host"],
            port=es_raw.get("port", 9200),
            index=es_raw["index"],
        ),
    )
