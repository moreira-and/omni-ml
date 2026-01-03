.PHONY: build up down clean

build:
	poetry build
	docker compose -f docker/docker-compose.yml build

up: build
	docker compose -f docker/docker-compose.yml up -d

down:
	docker compose -f docker/docker-compose.yml down

clean:
	docker compose -f docker/docker-compose.yml down -v
