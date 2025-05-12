x.PHONY:

build:
	docker-compose build
build-nc:
	docker-compose build --no-cache
down:
	docker-compose down --volumes
run:
	make down && docker-compose up -d
run-scaled:
	make down && docker-compose up --scale spark-worker=3
submit:
	docker exec da-spark-master spark-submit --master spark://spark-master:7077 --deploy-mode client ./apps/$(app)
