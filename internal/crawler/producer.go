package crawler

import (
	"github.com/segmentio/kafka-go"
)

type KafkaProducer struct {
	BootstrapAddr string
	Topic         string
	writer        *kafka.Writer
}

type Message struct {
	Key   string
	Value string
}

func NewKafkaProducer(address, topic string) *KafkaProducer {

	newProducer := KafkaProducer{
		BootstrapAddr: address,
		Topic:         topic,
	}

	newProducer.writer = kafka.NewWriter(kafka.WriterConfig{
		Brokers: []string{
			address,
		},
		Topic: topic,
	})

	return &newProducer

}

func (p *KafkaProducer) SendMessage(message string) bool {

	return true
}
