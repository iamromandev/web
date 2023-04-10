# system
.PHONY: clean
clean:
	docker system prune -a --force
	docker volume prune --force

.PHONY: ps
ps:
	docker compose ps -a

# local
.PHONY: build
build:
	docker-compose -f docker-compose.yml build

.PHONY: up
up:
	docker-compose -f docker-compose.yml up -d

.PHONY: down
down:
	docker-compose -f docker-compose.yml down

.PHONY: restart
restart:
	make down
	make build
	make up

# deploy
.PHONY: deploy
deploy:
	source /home/iamromandev/virtualenv/repositories/web/django/3.9/bin/activate && cd /home/iamromandev/repositories/web/django
#python src/manage.py tailwind install --no-input
