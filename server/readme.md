## Setup


## Local development
```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Deploy with docker
```sh
# start container
docker-compose up -d

# restart container
docker-compose restart

# stop container
docker-compose down

# to build Dockerfile
docker-compose rebuild
```
