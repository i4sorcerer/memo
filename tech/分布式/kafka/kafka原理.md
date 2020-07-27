## kafka原理相关

### 疑问点

1. 当producer是以批量发送的方式发送时，并且acks设定为1，此时的确认是怎么进行的？如果批量发送的其中一条消息没有被leader确认收到，其他消息会怎样？自己这条消息会怎样？
2. producer设定时候可以指定单个请求可以允许的最大字节数，对于同一producer，可以针对不同的topic设置不同的max.request.size吗？好像不行，此参数是producer级别的
3. 消费端同组内的多个消费者是如何知道自己应该消费的分区的？
   - Coordinator角色
   - leader消费者
   - JoinGroup请求，syncGroup请求
   - SyncGroupResponse响应
   - 

### topic和patition

- topic是存储消息的逻辑概念，具体消息的存储还是通过partition
- 每个topic可以划分为多个partition
- 相同topic下的不同partition，消息是不同的
- 同一个partition上不允许多线程。
- 对同一个partition来讲是可以保证顺序性的（原因是分区内总是append到文件末尾），跨分区不保证顺序性

1. 分区策略可以自定义

   - 默认提供两种分区：

     - Range（范围）默认

       先分区数除以消费者数，除不尽的时候，则前面的消费者需要额外承当分区消费

       partition: 0,1,2,3,4,5,6

       consumer:c0,c1,c2

       分区结果：

       c0:0,1,2

       c1:3,4

       c2:5,6

     - RoundRobin（轮询）

       分解hashcode值进行轮询

   - kafka中一条消息是由key和value组成的，和其他消息组件mq不同之处。

     key是可选项，作用主要是用来决定消息放到哪个分区上。也就是分区策略，默认策略是通过key的hash值取模来实现的。

   - producer在发送的时候，可以自定义分区策略，PARTITIONER_CLASS_CONFIG，实现Partitioner接口
   - consumer在接收的时候，可以指定消费哪些分区，也可以在出发热balance机制时，采用range方式

2. 增减consumer，broker，partition会导致rebalance

   matdata.max.age.ms 10分钟跟新一次

   - 什么时候出发rebalance？
     1. 当consumer group新增消费者时
     2. 消费者离开当前group时
     3. topic中新增分区时
     4. 消费者主动取消订阅topic

   - 谁来执行rebalance以及谁来管理group？

     Coordinator

     1. 

3. **offset是如何存储的？**

   Zookeeper上会默认为 _consumer_offset这个topic默认生成50个分区，去存储已经 被消费掉的offset。

   每个消费group应当存储到哪些分区中，通过下面策略：

   ```
   ("消费group.id"的hashcode值)%分区数50
   得出来的值就是：此消费组消费掉的offset应当存储的分区位置
   _consumer_offset-2
   _consumer_offset-49
   
   
   ```

4. kafka中消息内容是如何存储的？

   1. 消息的保存路径：保存在文件夹part-topic-0,part-topic-1,part-topic-2

   2. broker是如何进行分区分配的：

      **broker-0	broker-1	broker-2**

      par-0	      par-1		  par-2

      par-2	      par-4

   3. 日志文件是分段保存的。logSegment

5. **消息的写入性能**
   - 磁盘顺序写入追加
   
   - 零拷贝：直接从页缓存->网络缓冲区；避免了内核/用户的上下文切换

     在linux中是通过sendfile系统调用来实现的，Java中提供FileChannel.transferTo() API来实现零拷贝
   
   - 页缓存（OS cache）
   
     
   
6. 日志文件存储的分段原理

   - logsegment

     1. 参数The maximum size of a single log file：log.segment.bytes=xxxxxxx

     2. 文件命名：是上一个log文件中最后一条消息的offset+1

     3. 每条消息中都会有一个position值，这是此消息存储在物理文件中的偏移量

     4. **索引文件采用的是稀疏索引**

     5. **查看日志文件命令：**
        ./kafka-run-class.sh kafka.tools.DumpLogSegments --files 0000000.index --print-data-log

        ./kafka-run-class.sh kafka.tools.DumpLogSegments --files 0000000.log--print-data-log
     
     00000000000000000003.snapshot 
     
     leader-epoch-checkpoint
     
     00000000000000000000.index 文件
     
     ```
     offset: 0 position: 0
     ```
     
     00000000000000000000.timeindex 
     
     ```
     timestamp: 1595132887779 offset: 2
     ```
     
     00000000000000000000.log 文件
     
     ```
     Starting offset: 0
     baseOffset: 0 lastOffset: 0 count: 1 baseSequence: -1 lastSequence: -1 producerId: -1 producerEpoch: -1 partitionLeaderEpoch: 0 isTransactional: false isControl: false position: 0 CreateTime: 1595131852617 size: 81 magic: 2 compresscodec: NONE crc: 3296762030 isvalid: true
     | offset: 0 CreateTime: 1595131852617 keysize: -1 valuesize: 13 sequence: -1 headerKeys: [] payload: test : sk1006
     baseOffset: 1 lastOffset: 1 count: 1 baseSequence: -1 lastSequence: -1 producerId: -1 producerEpoch: -1 partitionLeaderEpoch: 0 isTransactional: false isControl: false position: 81 CreateTime: 1595132079721 size: 100 magic: 2 compresscodec: NONE crc: 202350941 isvalid: true
     | offset: 1 CreateTime: 1595132079721 keysize: 16 valuesize: 16 sequence: -1 headerKeys: [] key: test : sk1000007 payload: test : sk1000007
     baseOffset: 2 lastOffset: 2 count: 1 baseSequence: -1 lastSequence: -1 producerId: -1 producerEpoch: -1 partitionLeaderEpoch: 0 isTransactional: false isControl: false position: 181 CreateTime: 1595132887779 size: 94 magic: 2 compresscodec: NONE crc: 3997261980 isvalid: true
     | offset: 2 CreateTime: 1595132887779 keysize: 13 valuesize: 13 sequence: -1 headerKeys: [] key: test : 123434 payload: test : 123434
     ```
     
     

   1. 成对出现的日志文件

      - 0000000.index文件 索引文件

        索引文件内容：

        offset:522 position:1000（物理偏移量）

        offset:600 position:2000

      - 0000000.log文件 

        日志文件内容：

        offset:....... position:........

        offset:522 position:1000

        offset:....... position:........

        offset:600 position:2000

        offset:....... position:........

      - 0000000.timeindex文件 时间索引文件

      - leader-epoch-checkpoint 

   2. 日志的清理策略
      - 根据时间log.retention.hours=168 默认保存7天
      - 根据大小**log.segment.bytes=1073741824**：默认1G

   3. 日志压缩
      
      - 相同key的消息，offset小的将会被合并

7. **partition的副本机制**

   - kafka-topics.sh --create --zookeeper192.168.146.128:2181--replication-factor 3 --partitions 3 --topic test-topic

   - 相同partition的副本也是存在leader和follower，会均匀分散在集群的每个broker上

   - ISR：in sync replicas d当前分区的所有副本集

     - 其中的followers副本集必须要和leader副本的数据在阈值范围内保持一致，否则被踢出ISR
     - 如果ISR为空怎么办？（follower全被踢出，leader也挂机）：
       1. 等待ISR中任意一个leader活过来，重新选举leader
       2. 选择一个活过来的replica作为leader

   - 查看副本的状态zookeeper

     get /brokers/topics/topic_name/partition/partition_num/state

     part-topic-0:{"controller_epoch":6,"leader":3,"version":1,"leader_epoch":0,"isr":[3,0,2]}

     part-topic-1:{"controller_epoch":6,"leader":0,"version":1,"leader_epoch":0,"isr":[0,2,3]}

     part-topic-2:{"controller_epoch":6,"leader":2,"version":1,"leader_epoch":0,"isr":[2,3,0]}

     

   - leader副本：负责客户端消息的写入和读取

   - follower副本：负责从leader副本读取消息（不接收客户端请求）

   - LEO : log end offset. 

   - HW : high watermark没有此HW标记的副本不能被消费

   - acks ： 0,1，-1

8. 监控方案

   github上有几种监控工具可供使用

   - kafka-manager 

9. 分区大小如何选择
   1. 分区大小的选择大致要看下面的几个要素
      - 硬件资源
      - 消息大小
      - 目标吞吐量

