The cluster:
- 2 Managers
- 2 Workers

Workers APIs:
- /health:
```json
{
    "worker": "wrk1",
    "status": true
}
```

- /counter:
```json
{
    "worker": "wrk1",
    "worker_hits": 6,
    "total_hits": 14
}
```



