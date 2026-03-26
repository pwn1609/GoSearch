# GoSearch

*Deployment steps*
If no registry running: docker run -d -p 5000:5000 --name registry registry:2

docker build -t localhost:5000/crawler:0.1.0 -f ./cmd/crawler/Dockerfile .
docker push localhost:5000/crawler:0.1.0
helm install crawler ./charts/crawler

uninstall - helm uninstall crawler

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