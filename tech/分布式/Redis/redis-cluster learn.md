## learn redis-cluster

### Playing with the cluster

#### lack of the client libraries implementation

- The most used Java client, [Jedis](https://github.com/xetorthio/jedis) recently added support for Redis Cluster, see the *Jedis Cluster* section in the project README.
- [redis-py-cluster](https://github.com/Grokzen/redis-py-cluster) A port of redis-rb-cluster to Python. Supports majority of *redis-py* functionality. Is in active development.
- The popular [Predis](https://github.com/nrk/predis) has support for Redis Cluster, the support was recently updated and is in active development.
- The `redis-cli` utility implements basic cluster support when started with the `-c` switch.

#### Resharding the cluster

- ```
  redis-cli --cluster reshard 127.0.0.1:7000
  ```

- ```
  $ redis-cli -p 7000 cluster nodes | grep myself
  97a3a64667477371c4479320d683e4c8db5858b1 :0 myself,master - 0 0 0 connected 0-5460
  ```

- While the resharding is in progress you should be able to see your example program running unaffected. You can stop and restart it multiple times during the resharding if you want.

- At the end of the resharding, you can test the health of the cluster with the following command:

  ```
  redis-cli --cluster check 127.0.0.1:7000
  ```

####  Manual failover

ometimes it is useful to force a failover without actually causing any problem on a master. For example in order to upgrade the Redis process of one of the master nodes it is a good idea to failover it in order to turn it into a slave with minimal impact on availability.

Manual failovers are special and are safer compared to failovers resulting from actual master failures, since they occur in a way that avoid data loss in the process, by switching clients from the original master to the new master only when the system is sure that the new master processed all the replication stream from the old one.

```
redis-cli  -p 7005 cluster failover
I'm not sure...

```

#### Adding a new node as master

Adding a new node is basically the process of adding an empty node and then moving some data into it, in case it is a new master, or telling it to setup as a replica of a known node, in case it is a slave.

- In both cases the first step to perform is **adding an empty node**.

- start the server with `../redis-server ./redis.conf`

- ```
  redis-cli --cluster add-node 127.0.0.1:7006 127.0.0.1:7000
  ```

#### Adding a new node as a replica

- Note that the command line here is exactly like the one we used to add a new master, so we are not specifying to which master we want to add the replica. In this case what happens is that redis-cli will add the new node as replica of a random master among the masters with less replicas.

- ```
  redis-cli --cluster add-node 127.0.0.1:7006 127.0.0.1:7000 --cluster-slave
  ```

- However you can specify exactly what master you want to target with your new replica with the following command line:

  ```
  redis-cli --cluster add-node 127.0.0.1:7006 127.0.0.1:7000 --cluster-slave --cluster-master-id 3c3a0c74aae0b56170ccb03a76b60cfe7dc1912e
  ```

2. A more manual way to add a replica to a specific master is to add the new node as an empty master, and then turn it into a replica using the [CLUSTER REPLICATE](https://redis.io/commands/cluster-replicate) command. This also works if the node was added as a slave but you want to move it as a replica of a different master.

   - ```
     redis 127.0.0.1:7006> cluster replicate 3c3a0c74aae0b56170ccb03a76b60cfe7dc1912e
     ```

#### Removing a node

- ```
  redis-cli --cluster del-node 127.0.0.1:7000 `<node-id>`
  ```

  The first argument is just a random node in the cluster, the second argument is the ID of the node you want to remove.

#### Replicas migration

