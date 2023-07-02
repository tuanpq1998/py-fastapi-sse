# py-fastapi-sse

## Docker
- Build:
```bash
$ docker build -t my-fastapi-app .
```
- Run:
```bash
$ docker run --name fastapi-app -d -p 8000:8000 my-fastapi-app 
```
- Add to network
```bash
$ $ docker network connect milvus fastapi-app
```