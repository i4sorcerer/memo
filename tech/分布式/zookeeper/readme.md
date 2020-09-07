### 分布式协调服务zookeeper（万能搭配）

#### 解决问题

- 协议地址的维护

- 负载均衡

- 服务上下线的动态感知

- 最初的目的是为了解决资源的共享问题。yahoo开源

- 使用场景

  - 注册中心（上面的几个问题都可以用zookeeper解决）

    其中，/orderservice节点是持久化节点，

    其子节点都是临时节点，没个order服务节点对应一个zk节点（服务节点断开后，临时节点自动删除，从而实现了服务上下线的动态感知）

  <img src=".\注册中心场景.png" alt="image-20200828161825317" style="zoom:80%;" />

  - 实现配置中心

    配置中心统一维护配置（开关之类的配置）

  - 实现负载均衡

  - kafka中实现的leader选举（就是利用zookeeper的有序节点的特性）

  - 实现分布式锁

    

#### 前提知识点

- CAP理论
- 三态（分布式架构里服务会出现三种状态）
  - 可用
  - 不可用
  - 未知

- zookeeper特性

  - 基于key/value的存储

  - zk节点的特性

    - 同级节点的唯一性

    - 临时节点和持久化节点

      临时节点创建：create -e /test/tmp 0000（当前会话断开时，自动删除节点）

    - 有序节点

      有序节点创建：create -s /test/seq 111

      create -s /test/seq 111

      每次创建都会自动按顺序生成节点，编号

    - 临时节点不能创建子节点：Ephemerals cannot have children

  - ACL权限控制（类似于操作系统对于不同操作赋予权限不同）

    CREATE/READ/WRITE/DELETE/ADMIN

#### zookeeper的安装

- 配置文件

  zoo.cfg

- 重要参数
  - dtaDir=where snapshot is stored。should not be /tmp/zookeeper
  - 

#### 数据存储

- log.1

- log.3

- acceptedEpoch

- currentEpoch

  

- 节点znode存储信息

  cZxid = 0x300 创建事务id
  ctime = Fri Aug 28 00:01:54 PDT 2020
  mZxid = 0x300 编辑事务id
  mtime = Fri Aug 28 00:01:54 PDT 2020
  pZxid = 0x300 子节点变更事务id，,子节点增加或删除时会变化，子节点value变更，无变化。

  乐观锁

  cversion = 0 当前节点的子节点的版本号,子节点增加或删除时会变化
  dataVersion = 0 当前节点数据内容的版本号
  aclVersion = 0 当前节点ACL版本号

  临时节点时才会用到

  ephemeralOwner = 0x0：当前节点的会话ID，会话失效后，为了能够删除对应的临时节点

  dataLength = 1：当前数据长度
  numChildren = 0：当前节点的子节点数量



#### 数据同步

#### zookeeper集群

- 修改zoo.cfg配置，添加集群信息

  格式：server.myid=ip:服务端口：leader选举端口

  server.1=ip:2888:3888

  server.2=ip:2888:3888

  server.3=ip:2888:3888

- 创建myid文件

  在每个服务器上创建对应的myid文件 ,目录为dataDIr定义的目录下

  要和配置文件中定义的myid相对应

- 集群角色
  - leader：可以处理事务请求（增删改），读请求
  - follower：可以处理读请求
  - observer：可以处理读请求


#### watch机制

- 客户端可以去watch某个节点的，当节点有发生变更时，会发通知给客户端

- 客户端只会收到一次watcher通知，如果后续节点再次发生变化，之前设置watcher的客户端不会再收到通知

- 如果要持久获取通知，就需要循环监听

- stat /p/sub true :可以设置对某个节点进行监听，节点value发生变化时，会受到WatchedEvent通知

- 通知：WatchedEvent state:SyncConnected type:NodeDataChanged path:/p/sub

- 客户端绑定事件方法：getData,Exists,getChildren三种方式

- watcher事件类型

  1. None（-1）：当客户端的状态发生变化时候
  2. NodeCreated（1）：节点创建事件
  3. NodeDeleted（2）：节点删除事件
  4. NodeDataChanged（3）：节点数据变化事件
  5. NodeChildrenChanged（4）：子节点发生变化事件（子节点创建删除）

  



#### 设计思想

1. 防止单点故障：
2. 每个节点数据时一致的：leader/master
3. leader挂了怎么办？数据如何恢复？leader选举？
4. leader选举中使用2PC，必须保证获得过半数节点的投票（因此年集群中的总结点数必须是2n+1，否则会导致选举不成功）





#### ZAB协议

支持崩溃恢复的原子广播协议，主要用于实现数据的一致性

##### 集群中消息广播的过程

1. zk对每个事务请求生成一个zxid（64位的自增ID）
2. 带有zxid的消息作为proposal分发给集群中的每一个follower节点
3. fellower节点把消息写入磁盘，成功则返回ACK。
4. leader节点收到合法数量的ack之后，再发起commit广播消息，同时自己也会commit这条事务消息。
5. 如果此时，leader挂了，会导致部分节点收到commit请求，部分节点没有收到commit请求。zab协议需要保证被处理的消息不能丢失（zab协议保证）。
6. 当收到事务请求，并且还未发起事务投票时，leader挂了，zab要保证被丢弃的消息不会重复出现（zab协议保证）

注1：在此过程中observer节点参与投票，但是必须要和leader节点保持数据同步。



##### 崩溃恢复

下面几种情况下会触发奔溃恢复，集群因此进入崩溃恢复阶段：

1. leader失去过半节点数的联系
2. leader节点挂了

原子广播





#### zab的设计思想

上个朝代（epoch）没有被提交的消息会被丢弃

1. zxid最大，能保证已经提交的事务不会丢失
2. epoch概念，每产生一个新的leader，epoch+1.
   低32位存储自增编号，高32位是epoch编号



#### leader选举

- zxid最大设置为leader（zxid越大数据越新）
- myid越大，leader选举中权重越大
- epoch每一轮投票，都会递增

- 选举状态
  - looking
  - leading
  - following
  - observing



#### 客户端

##### 官方客户端：zookeeper

- 操作比较直接，封装较少，节点操作必须逐级操作

##### curator客户端：curator-framework

- 操作封装比较好，可以操作多级节点
- 需要引入的jar包（模块）
- recipes：http://curator.apache.org/curator-recipes/index.html
- curator 客户端监听：客户端cache例子：https://github.com/apache/curator/tree/master/curator-examples/src/main/java/cache
  - CuratorCache：
  - PathChildCache：监听一个节点的子节点的创建，删除，更新
  - NodeCache：监听一个节点的更新和创建事件
  - TreeCache：综合PathCHildCache和NodeCache的特性，监听所有节点



#### 使用zookeeper实现分布式锁吧

##### 实现方法

- zookeeper：

  实现原理：

  - 多个客户端去/Locks节点下创建有序节点
  - 节点值最小的客户端可以获取锁
  - 每个节点只监听比自己小1的节点的状态，而不是一个节点释放锁之后，其他所有节点去争抢。（避免了惊群效应）

- redis：

  - setnx：如果key不存在才设置，key第一次设置时，获取锁成功

- 数据库

##### 原生api

- 临时有序节点
- watcher机制

##### curator实现分布式锁

curator对于常用的一些场景进行了很好地封装，可以直接拿过来用，比如：分布式锁，分布式读写锁，leader选举，分布式原子类等等

主要在curator-recipes-5.1.0.jar这个jar包里

- InterProcessMutex类实现了分布式锁

##### 惊群效应/羊群效应

当一个节点释放了锁，之后其他所有节点同时去争抢同一个锁，导致的大量通知消息的发生。最终还是只有一个节点可以获取到锁。

#### 实现带注册中心的RPC框架【dubbo思想的简单实现】

如果调用API地址比较多，并且为了实现服务的动态上下线的功能，引入注册中心

- 服务端
  - 服务地址的注册
  - 服务配置集群，并实现简单的负载均衡（随机负载，权重负载）
  - 实现服务的多版本发布（通过version去控制）
- 客户端
  - 服务地址的发现
  - 服务调用地址是动态获取的

- 手写实现RPC+注册中心案例

  场景：

  

#### 问题集

- 因为System.in.read()方法没有写在cache.start();所在的方法中个，导致监听器始终获取不到通知消息

  暂停当前的进程必须写在cache.start所在的方法中，否则会接收不到通知消息？？？？？？

  

- 【未解之谜】使用curator-framework创建listener的时候，客户端可以连接成功，但是始终有下面的错误信息：**Invalid config event received**

  参考jira上的记录，v4.0.1版本尚未解决https://issues.apache.org/jira/browse/CURATOR-526

```java
org.apache.zookeeper.server.quorum.QuorumPeer
 public static class QuorumServer
查看对应源码可知，直接原因是zk返回的config属性里，没有客户端的连接信息，导致报错
     
private static final String wrongFormat = " does not have the form server_config or server_config;client_config where server_config is the pipe separated list of host:port:port or host:port:port:type and client_config is port or host:port";

```



```
[14:17:00:251] [INFO] - org.apache.curator.framework.imps.EnsembleTracker.processConfigData(EnsembleTracker.java:201) - New config event received: {server.1=localhost:2888:3888:participant, version=0, server.3=localhost:2890:3890:participant, server.2=localhost:2889:3889:participant}
[14:17:00:259] [ERROR] - org.apache.curator.framework.imps.EnsembleTracker.processConfigData(EnsembleTracker.java:214) - Invalid config event received: {server.1=localhost:2888:3888:participant, version=0, server.3=localhost:2890:3890:participant, server.2=localhost:2889:3889:participant}
[14:17:00:278] [INFO] - org.apache.curator.framework.imps.EnsembleTracker.processConfigData(EnsembleTracker.java:201) - New config event received: {server.1=localhost:2888:3888:participant, version=0, server.3=localhost:2890:3890:participant, server.2=localhost:2889:3889:participant}
[14:17:00:279] [ERROR] - org.apache.curator.framework.imps.EnsembleTracker.processConfigData(EnsembleTracker.java:214) - Invalid config event received: {server.1=localhost:2888:3888:participant, version=0, server.3=localhost:2890:3890:participant, server.2=localhost:2889:3889:participant}

```

- 使用curator时，即便是了调用getData也出现了异常的报错信息：节点不存在

```
先判断节点是否存在，如果节点不存在，然后创建节点。
在getData操作的时候就出现下面错误：
Exception in thread "main" org.apache.zookeeper.KeeperException$NoNodeException: KeeperErrorCode = NoNode for /sk
	at org.apache.zookeeper.KeeperException.create(KeeperException.java:118)
	at org.apache.zookeeper.KeeperException.create(KeeperException.java:54)
	at org.apache.zookeeper.ZooKeeper.getData(ZooKeeper.java:2348)
	at org.apache.curator.framework.imps.GetDataBuilderImpl$4.call(GetDataBuilderImpl.java:327)
	at org.apache.curator.framework.imps.GetDataBuilderImpl$4.call(GetDataBuilderImpl.java:316)
	at org.apache.curator.RetryLoop.callWithRetry(RetryLoop.java:93)
	at org.apache.curator.framework.imps.GetDataBuilderImpl.pathInForeground(GetDataBuilderImpl.java:313)
	at org.apache.curator.framework.imps.GetDataBuilderImpl.forPath(GetDataBuilderImpl.java:304)
	at org.apache.curator.framework.imps.GetDataBuilderImpl$2.forPath(GetDataBuilderImpl.java:145)
	at org.apache.curator.framework.imps.GetDataBuilderImpl$2.forPath(GetDataBuilderImpl.java:141)
	at kafka.demo.util.ZookeeperUtil.main(ZookeeperUtil.java:52)
```











