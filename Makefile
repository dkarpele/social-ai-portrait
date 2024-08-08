AUTH_API_IMAGE_NAME := auth-api:latest
AUTH_API_DOCKERFILE := auth.Dockerfile
BOT_IMAGE_NAME := bot:latest
BOT_DOCKERFILE := bot.Dockerfile
STATIC_CONTENT_IMAGE_NAME := static-content-nginx:latest
STATIC_CONTENT_DOCKERFILE := static-content.Dockerfile
REDIS_IMAGE_NAME := redis:latest
NAMESPACE := default

all:
	$(MAKE) -C k8s/redis
	docker build --rm -t $(AUTH_API_IMAGE_NAME) -f $(AUTH_API_DOCKERFILE) .
	docker build --rm -t $(BOT_IMAGE_NAME) -f $(BOT_DOCKERFILE) .
	docker build --rm -t $(STATIC_CONTENT_IMAGE_NAME) -f $(STATIC_CONTENT_DOCKERFILE) .
	minikube start
	minikube addons enable ingress
	minikube addons enable ingress-dns
	minikube image load $(AUTH_API_IMAGE_NAME) $(BOT_IMAGE_NAME) $(REDIS_IMAGE_NAME) $(STATIC_CONTENT_IMAGE_NAME)
	kubectl apply -f k8s/redis/redis-config.yaml
	kubectl apply -f k8s/redis/redis-pvc.yaml
	kubectl apply -f k8s/redis/redis-service.yaml
	kubectl apply -f k8s/auth_api/auth-api-deployment.yaml
	kubectl apply -f k8s/bot/bot-deployment.yaml
	kubectl apply -f k8s/static-content/static-content-configmap.yaml
	kubectl apply -f k8s/static-content/static-content-service.yaml
	kubectl apply -f k8s/static-content/static-content-deployment.yaml
	kubectl apply -f k8s/ingress/app-ingress.yaml


deploy-all:
	kubectl apply -f k8s/redis/redis-config.yaml
	kubectl apply -f k8s/redis/redis-pvc.yaml
	kubectl apply -f k8s/redis/redis-service.yaml
	kubectl apply -f k8s/auth_api/auth-api-deployment.yaml
	kubectl apply -f k8s/bot/bot-deployment.yaml
	kubectl apply -f k8s/static-content/static-content-configmap.yaml
	kubectl apply -f k8s/static-content/static-content-service.yaml
	kubectl apply -f k8s/static-content/static-content-deployment.yaml
	kubectl apply -f k8s/ingress/app-ingress.yaml

show:
	- kubectl get all
	- kubectl get ingress

remove-all:
	- kubectl delete -f k8s/redis/redis-config.yaml
	- kubectl delete -f k8s/redis/redis-pvc.yaml
	- kubectl delete -f k8s/redis/redis-service.yaml
	- kubectl delete -f k8s/auth_api/auth-api-deployment.yaml
	- kubectl delete -f k8s/bot/bot-deployment.yaml
	- kubectl delete -f k8s/static-content/static-content-configmap.yaml
	- kubectl delete -f k8s/static-content/static-content-service.yaml
	- kubectl delete -f k8s/static-content/static-content-deployment.yaml
	- kubectl delete -f k8s/ingress/app-ingress.yaml

.PHONY: all deploy-all remove-all show logs