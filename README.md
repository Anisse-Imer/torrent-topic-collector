# Setup
## Start project - docker containers
You will need a linux environment with docker cli installed and make. 
Here are the commands to start and stop the created containers.
```bash
make run
make run-scaled workers=3 # Build Spark docker image
make submit app=spark_job.py # Submit spark job
```
Cleaning your containers after stopping the project is recommended, so you restart it properly.
## Connect and interact
- Spark : Connect to : "http://localhost:9090/".
## License
[MIT](https://choosealicense.com/licenses/mit/)
