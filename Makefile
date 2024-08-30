AUTH_API_IMAGE_NAME := auth-api:latest
AUTH_API_DOCKERFILE := Dockerfile.auth
BOT_IMAGE_NAME := bot:latest
BOT_DOCKERFILE := Dockerfile.bot
STATIC_CONTENT_IMAGE_NAME := static-content-nginx:latest
STATIC_CONTENT_DOCKERFILE := static-content.Dockerfile
REDIS_IMAGE_NAME := redis:latest
ANSIBLE_OPERATOR_NAME := ansible-operator:latest
ANSIBLE_OPERATOR_DOCKERFILE := Dockerfile.ansible-operator

NAMESPACE := social-ai-profile

all:
	$(MAKE) -C k8s/redis
	docker build --rm -t $(AUTH_API_IMAGE_NAME) -f $(AUTH_API_DOCKERFILE) .
	docker build --rm -t $(BOT_IMAGE_NAME) -f $(BOT_DOCKERFILE) .
	docker build --rm -t $(STATIC_CONTENT_IMAGE_NAME) -f $(STATIC_CONTENT_DOCKERFILE) .
	docker build --rm -t $(ANSIBLE_OPERATOR_NAME) -f $(ANSIBLE_OPERATOR_DOCKERFILE) .
	minikube start
	minikube addons enable ingress
	minikube addons enable ingress-dns
	minikube image load $(AUTH_API_IMAGE_NAME) $(BOT_IMAGE_NAME) $(REDIS_IMAGE_NAME) $(STATIC_CONTENT_IMAGE_NAME) $(ANSIBLE_OPERATOR_NAME)
	kubectl apply -f k8s/namespace.yaml
	kubectl apply -f k8s/service-account.yaml
	kubectl apply -f k8s/redis/configmaps-and-secrets
	kubectl apply -f k8s/redis
	kubectl apply -f k8s/python-apps/configmaps-and-secrets
	kubectl apply -f k8s/static-content/configmaps-and-secrets
	kubectl apply -f k8s/static-content
	kubectl apply -f k8s/ansible-operator/rbac/ansible_operator_service_account.yaml
	kubectl apply -f k8s/ansible-operator/ansible-operator-crd.yaml
	kubectl apply -f k8s/ansible-operator/ansible-operator-cr.yaml
	kubectl apply -f k8s/ansible-operator/operator.yaml
	kubectl apply -f k8s/python-apps
	kubectl apply -f k8s/ingress/app-ingress.yaml


deploy-all:
	kubectl apply -f k8s/namespace.yaml
	kubectl apply -f k8s/service-account.yaml
	kubectl apply -f k8s/redis/configmaps-and-secrets
	kubectl apply -f k8s/redis
	kubectl apply -f k8s/python-apps/configmaps-and-secrets

	kubectl apply -f k8s/static-content/configmaps-and-secrets
	kubectl apply -f k8s/static-content
	kubectl apply -f k8s/ansible-operator/rbac/ansible_operator_service_account.yaml
	kubectl apply -f k8s/ansible-operator/ansible-operator-crd.yaml
	kubectl apply -f k8s/ansible-operator/ansible-operator-cr.yaml
	kubectl apply -f k8s/ansible-operator/operator.yaml
	kubectl apply -f k8s/python-apps
	kubectl apply -f k8s/ingress/app-ingress.yaml

show:
	- kubectl get all -n $(NAMESPACE)
	- kubectl get ingress -n $(NAMESPACE)

remove-all:
	kubectl delete -f k8s/redis/configmaps-and-secrets
	kubectl delete -f k8s/redis
	kubectl delete -f k8s/python-apps/configmaps-and-secrets
	kubectl delete -f k8s/python-apps
	kubectl delete -f k8s/static-content/configmaps-and-secrets
	kubectl delete -f k8s/static-content
	kubectl delete -f k8s/ansible-operator/rbac/ansible_operator_service_account.yaml
	kubectl delete -f k8s/ansible-operator/ansible-operator-crd.yaml
	kubectl delete -f k8s/ansible-operator/ansible-operator-cr.yaml
	kubectl delete -f k8s/ansible-operator/operator.yaml
	kubectl delete -f k8s/ingress/app-ingress.yaml
	kubectl delete -f k8s/service-account.yaml
	kubectl delete -f k8s/namespace.yaml

.PHONY: all deploy-all remove-all show logs