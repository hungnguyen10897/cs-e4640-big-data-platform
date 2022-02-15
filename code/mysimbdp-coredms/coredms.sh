#!/bin/bash

kubectl create namespace coredms

# Deploy K8ssandra
helm install -n coredms -f k8ssandra.yaml k8ssandra k8ssandra/k8ssandra