x.PHONY: build-workers launch-workers stop-workers down

build:
	docker-compose build
build-nc:
	docker-compose build --no-cache

build-workers:
	docker build -f ./workers/app/Dockerfile -t worker-magnet ./workers/app
launch-workers:
	python3 ./workers/build_workers.py
stop-workers:
	python3 ./workers/stop_workers.py

down: stop-workers
	docker-compose down --volumes

run: down build-workers
	docker-compose up -d
	make launch-workers

run-submit: run submit app=$(app)

run-scaled: down build-workers
	docker-compose up --scale spark-worker=$(workers) -d
	make launch-workers

submit:
	docker exec da-spark-master spark-submit \
	--master spark://spark-master:7077 \
	--deploy-mode client \
	--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 \
	./apps/$(app)

kafka-test:
	(python3 kafka_apps/consumer.py &) && python3 kafka_apps/producer.py

view:
	docker compose logs -f
