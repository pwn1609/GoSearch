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
kubectl apply -f kafka-cluster.yaml