docker-build:
	docker compose up -d db; docker compose up --build flaskapp

docker-clean:
	docker stop flaskapp; docker rm flaskapp; docker stop `docker ps -a -q`; docker rm `docker ps -a -q`; docker volume prune -f