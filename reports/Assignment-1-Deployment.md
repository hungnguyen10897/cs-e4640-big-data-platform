# Deployment Guide

## Requirements:
- Docker
- Minikube ([Install Minikube](https://minikube.sigs.k8s.io/docs/start/) - optional)
- Helm v3
- Bash terminal

<br>

## Step 1: Setting Up Minikube cluster (optional)

This step is optional if you already have a Kubernetes cluster

```
minikube start \
-p mysimbdp \
--kubernetes-version=v1.20.7 \
--memory=5g \
--nodes=3 \
--cpus=4 \
--disk-size=10g
```

<br>

## Step 2: Install K8ssandra on Kubernetes and Set up Cassandra

Depends on Kubernetes environment, the installation process is different. You can find more information [here](https://k8ssandra.io/get-started/).
This step shows Installation of k8ssandra on Minikube.

Install appropriate storage class

```
kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/master/deploy/local-path-storage.yaml
```

Add K8ssandra as helm repo
```
helm repo add k8ssandra https://helm.k8ssandra.io/stable
helm repo update
```

Create namespace for **mysimbdp-coredms**
```
kubectl create namespace coredms
```

Install K8ssandra, at `/code/mysimbdp-coredms` run
```
helm install -n coredms -f k8ssandra.yaml k8ssandra k8ssandra/k8ssandra
```

Port-forward K8ssandra Stargate to localhost
```
kubectl port-forward -n coredms svc/k8ssandra-dc1-stargate-service 8080 8081 8082 9042
```

Port-forward Grafana to localhost
```
kubectl port-forward -n coredms svc/k8ssandra-grafana 9090:80
```

<br>

## Step 3: Get Canssandra credentials

Username
```
kubectl get secret k8ssandra-superuser -n coredms -o jsonpath="{.data.username}" | base64 --decode ; echo
```


Password:
```
kubectl get secret k8ssandra-superuser -n coredms -o jsonpath="{.data.password}" | base64 --decode ; echo
```

Change configurations under [credentials.cfg file](/code/mysimbdp-dataingest/credentials.cfg) with these values.

<br>

## Step 4: Set up initial Keyspace and Table

At `/code/mysimbdp-coredms`, replace <USERNAME> and <PASSWORD> and run

```
./cqlsh-astra/bin/cqlsh  -u <USERNAME> -p <PASSWORD> -f setup.cql
```

<br>

## Step 5: Run *mysimbdp-dataingest* service

First configure the number of concurrent producers to run by changing the [dokcer-compose.yaml file](/code/mysimbdp-dataingest/docker-compose.yaml)

```
    deploy:
      replicas: 2
```

At `/code/mysimbdp-dataingest`, run
```
docker-compose up
```

<br>

## Step 6: Clean Up

Simple delete the minikube cluster

```
minikube delete -p mysimbdp
```