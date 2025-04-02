# Setup
## Start project - docker containers
You will need a linux environment with docker cli installed and make. 
Here are the commands to start and stop the created containers.
```bash
docker network create nifi # Nifi network
make run-scaled # Build Spark docker image
docker compose up -d # Build all containers
docker compose down -v # Stop all containers
```
Cleaning your containers after stopping the project is recommended, so you restart it properly.
## Connect and interact
- Nifi : Connect to : "https://localhost:9443/nifi/" and use the credentials set in the docker-compose file.
- Spark : Connect to : "http://localhost:9090/".
## License
[MIT](https://choosealicense.com/licenses/mit/)
