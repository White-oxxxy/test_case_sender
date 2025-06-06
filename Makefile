DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .dev.env
APP = docker_compose/app.yaml
INFRA = docker_compose/infra.yaml

.PHONY: app
app:
	${DC} -f ${APP} ${ENV} up --build -d

.PHONY: app-down
app-down:
	${DC} -f ${APP} ${ENV} down