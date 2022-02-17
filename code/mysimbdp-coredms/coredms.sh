#!/bin/bash

kubectl create namespace coredms

# Deploy K8ssandra
helm install -n coredms -f k8ssandra.yaml k8ssandra k8ssandra/k8ssandra

# Uninstall K8ssandra
helm uninstall -n coredms k8ssandra

# Port-forward Cassandra for local access
kubectl port-forward -n coredms svc/k8ssandra-dc1-stargate-service 8080 8081 8082 9042

# Port-forward Grafana for monitoring
kubectl port-forward -n coredms svc/k8ssandra-grafana 9090:80
# >> Grafana available at localhost:9090

# Get superuser to access Cassandra
kubectl get secret k8ssandra-superuser -n coredms -o jsonpath="{.data.username}" | base64 --decode ; echo
# >> k8ssandra-superuser

# Get superuser password to access Cassandra
kubectl get secret k8ssandra-superuser -n coredms -o jsonpath="{.data.password}" | base64 --decode ; echo
# >> ju82V79VmZW9UzUdGZO7

# Pre-populate KeySpace, Column Family, Row Key
./cqlsh-astra/bin/cqlsh  -u k8ssandra-superuser -p ju82V79VmZW9UzUdGZO7 -f setup.cql
