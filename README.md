# GoSearch

*Deployment steps*
If no registry running: docker run -d -p 5000:5000 --name registry registry:2

Crawler:
docker build -t localhost:5000/latest -f ./cmd/crawler/Dockerfile .
docker push localhost:5000/latest
helm install crawler ./charts/crawler

uninstall - helm uninstall crawler

Indexer:
kubectl create configmap indexer-config --from-file=./internal/indexer/indexer_config.yaml
 - kubectl delete configmap indexer-config

docker build -t localhost:5000/indexer:latest -f ./internal/indexer/Dockerfile .
docker push localhost:5000/indexer:latest

helm install indexer ./charts/indexer


kafka:
kubectl create namespace kafka
helm repo add strimzi https://strimzi.io/charts/
helm repo update
helm install strimzi strimzi/strimzi-kafka-operator -n kafka
cd ../charts/kafka
kubectl apply -f kafka-cluster.yaml
kubectl apply -f kafka-nodepool.yaml
kubectl apply -f crawler-topic.yaml

Verify Kafka:
kubectl describe kafka kafka-cluster -n kafka - Should see "strimzi-cluster-operator-xxxx   Running"
kubectl get kafka -n kafka - Should see "kafka-cluster    True"
 - If not: kubectl describe kafka kafka-cluster -n kafka
kubectl get pods -n kafka - Should see:
 - kafka-cluster-dual-role-0      Running
 - kafka-cluster-entity-operator  Running
 - strimzi-cluster-operator       Running
kubectl get svc -n kafka - Should see: 
 - kafka-cluster-kafka-bootstrap
 - kafka-cluster-kafka-brokers

ElasticSearch:
helm repo add elastic https://helm.elastic.co
helm repo update
helm install elastic-operator elastic/eck-operator -n elastic-system --create-namespace
kubectl create namespace elastic-stack
kubectl apply -f ./charts/elasticsearch/elasticsearch.yaml

Verify ElasticSearch:
kubectl get elasticsearch -n elastic-stack
kubectl get pods -n elastic-stack
kubectl get svc -n elastic-stack
kubectl get pvc -n elastic-stack


Indexer should create the index
curl -X PUT http://quickstart-es-http:9200/web-pages \
  -H "Content-Type: application/json" \
  -d '{
    "mappings": {
      "properties": {
        "url":        { "type": "keyword" },
        "domain":     { "type": "keyword" },
        "title":      { "type": "text" },
        "headings": { "type": "text" },
        "content":    { "type": "text" },
        "timestamp":  { "type": "date" },
        "status_code":{ "type": "integer" }
      }
    }
  }'
