# seafight

<strong>build the image</strong>
```
docker compose build
```

<strong>run server</strong>
```
docker compose up
```

<strong>stop server</strong>
```
docker compose down
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

<strong>http://localhost:8000/</strong>

to start a game send "start"
shoot: <letter> <number>
