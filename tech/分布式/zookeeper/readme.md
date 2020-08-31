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

- 节点存储信息

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

- stat /p/sub true :可以设置对某个节点进行监听，节点value发生变化时，会受到WatchedEvent通知

- 通知：WatchedEvent state:SyncConnected type:NodeDataChanged path:/p/sub

- watcher事件类型

  1. None（-1）：当客户端的状态发生变化时候
  2. NodeCreated（1）：节点创建事件
  3. NodeDeleted（2）：节点删除事件
  4. NodeDataChanged（3）：节点数据变化事件
  5. NodeChildrenChanged（4）：子节点发生变化事件（子节点创建删除）

  





