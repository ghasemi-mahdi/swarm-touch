import os
from fastapi import FastAPI
from redis import Redis

app = FastAPI()

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
NODE_HOSTNAME = os.getenv("NODE_HOSTNAME", "unknown")

redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


@app.get("/health")
def health():
    try:
        redis_client.ping()
        redis_ok = True
    except Exception:
        redis_ok = False
    return {"status": "ok" if redis_ok else "degraded", "redis": redis_ok}


@app.get("/counter")
def counter():
    total_count = redis_client.incr("hits")
    node_count = redis_client.incr(f"{NODE_HOSTNAME}-hits")
    return {
        "hostname": NODE_HOSTNAME,
        "total_count": total_count,
        "node_count": node_count,
    }