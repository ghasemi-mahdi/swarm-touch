# after installing docker on both nodes:

0. set docker permission:
```bash
sudo usermod -aG docker $USER # on both VMs => ⚠️ then reboot 😄
``` 


1. initialize swarm and connect two nodes as manager (⚠️on production we should have 3 or 5 managers)
```bash
docker swarm init # on node1

# Swarm initialized: current node (gdey0em7sbzvna6134yddifff) is now a manager.
# To add a worker to this swarm, run the following command:
#     docker swarm join --token SWMTKN-1-6dn22eu3cyeknai2p885zm8wk3zf1vhyl607c0r5oamzii5qqo-3vt8u55e7kr2x5wah6xqov3ta 192.168.147.132:2377

# To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.

docker swarm join-token manager # on node 1
# To add a manager to this swarm, run the following command:
#     docker swarm join --token SWMTKN-1-6dn22eu3cyeknai2p885zm8wk3zf1vhyl607c0r5oamzii5qqo-3lcqqn795gr90nic82pe6xj3m 192.168.147.132:2377


docker swarm join --token SWMTKN-1-6dn22eu3cyeknai2p885zm8wk3zf1vhyl607c0r5oamzii5qqo-3lcqqn795gr90nic82pe6xj3m 192.168.147.132:2377 # on node2
# This node joined a swarm as a manager. # 🔥
```

```bash
docker node ls # on either nodes
# ID                            HOSTNAME      STATUS    AVAILABILITY   MANAGER STATUS   ENGINE VERSION
# gdey0em7sbzvna6134yddifff     devops-vm-1   Ready     Active         Reachable        29.8.2
# i01ofjtp1wfiizv5uh0awq7on *   devops-vm-2   Ready     Active         Leader           29.8.2
```

2. add worker
in swarm each node can only be `manager` or `worker` and adding a `worker` node is `optional` because, `by default, every manager node is also a worker node`, so because we have only two VMs => they both become manager and we don't need any worker


---
`docker service` vs `docker stack`:
In short,` docker service` manages individual services on swarm (like `docker run` on host), while `docker stack` manages a complete multi-service application defined in a Compose file (like `docker compose` in host)

---

3. copy app to VMs (/apps/swarm-touch/app/app.py...)

4. build custome image on each VM 
> using a registery and pushing to it is best practice and by that we dont need to build on nodes (VMs)

```bash
docker build -t fastapi-redis-api:latest . # on Dockerfile dir # ⚠️ on each node
```

5. deploy stack
```bash
docker stack deploy -c compose.yml swtouch # 💡 only on one manager node


# 🔥 verify
docker stack services swtouch
docker stack ps swtouch
```

💔 there is an error:
while:
```bash
ID             NAME              IMAGE                      NODE          DESIRED STATE   CURRENT STATE            ERROR     PORTS
s95cqwhcb7cw   swtouch_api.1     fastapi-redis-api:latest   devops-vm-2   Running         Running 35 seconds ago             
j03da11v0yc4   swtouch_api.2     fastapi-redis-api:latest   devops-vm-1   Running         Running 41 seconds ago             
62cg8niy6lwa   swtouch_redis.1   redis:7-alpine             devops-vm-1   Running         Running 41 seconds ago 
```

but /counter throw `Internal Server Error`

```bash
docker service logs -f swtouch_api
```

> error resolved by itself (we need wait some time to service complete connection...)

6. update

code change -> puch to nodes -> build app image -> rm previous stack -> deploy new one