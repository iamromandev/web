# system
.PHONY: clean-system
clean-system:
	docker system prune -a --force

.PHONY: clean-db
clean-db:
	docker volume prune --all --force

.PHONY: clean
clean:
	make clean-system
	make clean-db

.PHONY: ps
ps:
	docker compose ps -a

# local
.PHONY: build
build:
	COMPOSE_BAKE=true docker compose -f docker-compose.yml build

.PHONY: up
up:
	docker compose -f docker-compose.yml up -d

.PHONY: stop
stop:
	docker compose -f docker-compose.yml stop

.PHONY: down
down:
	docker compose -f docker-compose.yml down

.PHONY: restart
restart:
	make stop
	make build
	make up

.PHONY: poetry install
install:
	poetry lock
	poetry update
	poetry install

.PHONY: ruff
ruff:
	make install
	poetry run ruff format
