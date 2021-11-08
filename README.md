# seafight

<strong>build the image</strong>
```
docker compose build
```

<strong>run server</strong>
```
docker compose up
```

<strong>connect to container</strong>
```
docker exec -it socket_fight bash
```
<strong>test</strong>
```
pytest
```
<strong>coverage report</strong>
```
coverage run -m pytest
coverage report
```

<strong>http://localhost:8000/ </strong>

server is accessible from local network at host machine's ip

you can reset game by going <strong>http://localhost:8000/reset </strong>

<strong>stop server</strong>
```
docker compose down
```

