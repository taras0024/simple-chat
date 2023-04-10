# Simple Chat (Technical Task)

## Dependencies

- [poetry](https://python-poetry.org/docs/#installing-manually)
- [docker](https://docs.docker.com/get-docker/)

### Create requirements.txt from poetry

```shell
 poetry export -f requirements.txt --output requirements.txt --without-hashes
```

### Build images

```shell
docker build -f .\docker\django\Dockerfile -t chat-app:dev .
```

### Run containers

```shell
docker-compose -f .\docker\compose\docker-compose.local.yml -p chat up -d
```
