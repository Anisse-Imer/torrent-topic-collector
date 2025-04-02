# Setup
## Start project - docker containers
You will need a linux environment with docker cli installed. Here are the commands to start and stop the created containers.
```bash
docker network create nifi
docker compose up -d
docker compose down -v
```
Cleaning your containers after stopping the project is recommended, so you restart it properly.
## Connect and interact
- Nifi : Connect to : "https://localhost:9443/nifi/" and use the credentials set in the docker-compose file.
## License
[MIT](https://choosealicense.com/licenses/mit/)
