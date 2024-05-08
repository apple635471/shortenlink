## Run by Docker Compose

1. create .env for your DJANGO_SECRET_KEY_BASE64
```
DJANGO_SECRET_KEY_BASE64=XXXXXXXXXXXXXXXXXXXXXXX
```

2. docker compose run
```
docker compose up 
```

3. create admin to monitor db
```
docker exec -it shortenlink-web-1 /bin/bash
cd shortenlink/
python manage.py createsuperuser
```

4. open browser (user)
```
http://127.0.0.1:8000/
```

5. open browser (admin)
```
http://127.0.0.1:8000/admin/
```