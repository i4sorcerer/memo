## Kafka入门

### 安装

### Topic

1. 新建topic

   sh kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 3 --partitions 3 --topic part-topic

2. list当前topic

   sh kafka-topics.sh --list --bootstrap-server 192.168.146.130:9092

### Producer发送消息

sh kafka-console-producer.sh --bootstrap-server localhost:9092 --topic test

sh kafka-console-producer.sh --bootstrap-server 192.168.146.128:9092 --topic demo-topic

### Consumer接收消息

sh  kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning

sh  kafka-console-consumer.sh --bootstrap-server 192.168.146.128:9092 --topic cluster-topic  --from-beginning

sh  kafka-console-consumer.sh --bootstrap-server 192.168.146.128:9093 --topic demo-topic  --from-beginning

### 配置multi-broker cluster（集群环境）

config/server-1.properties:
    broker.id=1
    listeners=PLAINTEXT://:9093
    log.dirs=/tmp/kafka-logs-1

config/server-2.properties:
    broker.id=2
    listeners=PLAINTEXT://:9094
    log.dirs=/tmp/kafka-logs-2

#### 启动

./afka-server-start.sh ../config/server.properties &

./kafka-server-start.sh ../config/server-2.properties &

./kafka-server-start.sh ../config/server-3.properties &



./kafka-server-start.sh -daemon ../config/server.properties

./kafka-server-start.sh -daemon ../config/server-2.properties

./kafka-server-start.sh -daemon ../config/server-3.properties



#### 集群内创建topic

sh kafka-topics.sh --create --bootstrap-server localhost:9093 --replication-factor 3 --partitions 1 --topic demo-topic

#### 查看topic信息

sh kafka-topics.sh --describe --bootstrap-server localhost:9092 --topic cluster-topic

sh kafka-topics.sh --describe --bootstrap-server 192.168.146.128:9092 --topic demo-topic

多个分区：

sh kafka-topics.sh --create --bootstrap-server 192.168.146.128:9092 --topic part-topic --replication-factor 3 --partitions 3

#### 终止leader进程

- 查看占用端口号 lsof -t -i :9092
- kill -9 prossid

#### 查看zk情况

ls /brokers/ids

[2, 3]

leader终止之后，自动选举产生新的leader ：2



### 同步发送和异步发送

kafka1.0版本以后，默认使用的是异步方式发送，会有线程从发送队列去轮训。

- 异步方式，可以自定义CallBack函数

- 同步方式，通过Future的get方法

  





### 服务端参数

1. log.dirs=/tmp/kafka-logs ： A comma separated list of directories under which to store log files

2. **log.segment.bytes=1073741824** 

   每个segment文件最大size，超过此size会创建创建新的segment文件

### **发送端参数**

1. "acks"
   - ProducerConfig.ACKS_CONFIG : "0" : 消息发送给broker后不需要确认（性能高，易丢失数据）
   - ProducerConfig.ACKS_CONFIG : "1" ：消息发送给broker后只需leader节点确认完即可返回
   - ProducerConfig.ACKS_CONFIG : "-1"(all) ： 消息发送给broker后需要ISR中所有的replica节点确认后方可返回。（最完全，但也可能会数据丢失）

2. "batch.size"：针对的是同一个分区的消息

   ```
   批量发送，（16k）,需要和下面的"linger.ms"参数配合使用
   
   "The producer will attempt to batch records together into fewer requests whenever multiple records are being sent to the same partition. This helps performance on both the client and the server. This configuration controls the default batch size in bytes. <p>No attempt will be made to batch records larger than this size. <p>Requests sent to brokers will contain multiple batches, one for each partition with data available to be sent. <p>A small batch size will make batching less common and may reduce throughput (a batch size of zero will disable batching entirely). A very large batch size may use memory a bit more wastefully as we will always allocate a buffer of the specified batch size in anticipation of additional records.";
   ```

3. "linger.ms" ：逗留，徘徊，磨蹭

   ```
   延迟发送毫秒数，默认设置为0，和"batch.size"配合使用
   
   "The producer groups together any records that arrive in between request transmissions into a single batched request. Normally this occurs only under load when records arrive faster than they can be sent out. However in some circumstances the client may want to reduce the number of requests even under moderate load. This setting accomplishes this by adding a small amount of artificial delay&mdash;that is, rather than immediately sending out a record the producer will wait for up to the given delay to allow other records to be sent so that the sends can be batched together. This can be thought of as analogous to Nagle's algorithm in TCP. This setting gives the upper bound on the delay for batching: once we get <code>batch.size</code> worth of records for a partition it will be sent immediately regardless of this setting, however if we have fewer than this many bytes accumulated for this partition we will 'linger' for the specified time waiting for more records to show up. This setting defaults to 0 (i.e. no delay). Setting <code>linger.ms=5</code>, for example, would have the effect of reducing the number of requests sent but would add up to 5ms of latency to records sent in the absence of load."
   ```

4. "max.request.size"

```
单个msg可以发送的最大字节数，默认是1M
"The maximum size of a request in bytes. This setting will limit the number of record batches the producer will send in a single request to avoid sending huge requests. This is also effectively a cap on the maximum uncompressed record batch size. Note that the server has its own cap on the record batch size (after compression if compression is enabled) which may be different from this."
```

### 接收端参数

1. "group.id"

```
接收端最重要的参数，消费组。
"A unique string that identifies the consumer group this consumer belongs to. This property is required if the consumer uses either the group management functionality by using <code>subscribe(topic)</code> or the Kafka-based offset management strategy."
```

- 同一消费组竞争关系，不能消费同一条消息
- 不同消费组不存在竞争关系，可以消费相同消息
- 同一个消费组内的消费者在协调者的统筹下一起消费订阅主题的所有分区

2. "auto.offset.reset"

```
对于新创建的消费组来说，如何设置offset（偏移量）
"earliest" : 重置offset为最早的offset
"latest" : 重置为最近的offset
"none" : 如果在当前组内没有找到前一次的offset，则消费者报错
报错信息：org.apache.kafka.clients.consumer.NoOffsetForPartitionException: Undefined offset with no reset policy for partitions: [demo-topic-0]

"What to do when there is no initial offset in Kafka or if the current offset does not exist any more on the server (e.g. because that data has been deleted): 
<ul>
<li>earliest: automatically reset the offset to the earliest offset
<li>latest: automatically reset the offset to the latest offset</li>
<li>none: throw exception to the consumer if no previous offset is found for the consumer's group</li>
<li>anything else: throw exception to the consumer.</li>
</ul>"
```

3. "enable.auto.commit"

```
是否自动提交，也可以手动提交（consumer.commitAsync();）
消息不提交，就可以被继续消费，其实就是offset没有commit
"If true the consumer's offset will be periodically committed in the background."
```

4. "auto.commit.interval.ms"

```
自动提交为true时，offset的提交频率，毫秒
"The frequency in milliseconds that the consumer offsets are auto-committed to Kafka if <code>enable.auto.commit</code> is set to <code>true</code>."
```



### Spring中整合使用kafka

1. 容易混淆的几个类

```
//接口，封装原生KafkaConsumer，一个container封装一个consumer
interface MessageListenerContainer;
//单线程container实现，只启动一个consumer
class KafkaMessageListenerContainer implemets MessageListenerContainer;
//多线程container实现，负责创建多个KafkaMessageListenerContainer
class ConcurrentMessageListenerContainer implemets MessageListenerContainer;

//接口，工厂模式，container工厂，负责创建container，当使用@KafkaListener时需要提供
interface KafkaListenerContainerFactory<C extends MessageListenerContainer>;
//container工厂的唯一实现，且参数为多线程container，如果需要单线程，setConsurrency(null)即可，这也是默认参数
class KafkaListenerContainerFactory<ConcurrentMessageListenerContainer<K, V>>
```



### 优质参考资源

- [Kafka System Tool](https://cwiki.apache.org/confluence/display/KAFKA/System+Tools#SystemTools-DumpLogSegment)
- 

### 问题集

1. 使用提供的生产者和消费者工具可以正常的处理消息，但使用java client api的时候，总是无法和server通信上，并且没有任何错误信息。

原因是我listeners=PLAINTEXT://:9094中未指定IP地址，并且advertised.listeners也没有指定，导致api客户端无法成功发送到192.168.146.128这个ip地址，也无法从这个ip地址接收消息

解决办法：

- 在listeners属性上加上hostname
- 放开advertised.listeners属性，并且配置上hostname

```
需要修改配置文件中下面属性，指定hostname（ip地址）
############################# Socket Server Settings #############################

# The address the socket server listens on. It will get the value returned from
# java.net.InetAddress.getCanonicalHostName() if not configured.
#   FORMAT:
#     listeners = listener_name://host_name:port
#   EXAMPLE:
#     listeners = PLAINTEXT://your.host.name:9092
listeners=PLAINTEXT://192.168.146.128:9094

# Hostname and port the broker will advertise to producers and consumers. If not set,
# it uses the value for "listeners" if configured.  Otherwise, it will use the value
# returned from java.net.InetAddress.getCanonicalHostName().
#advertised.listeners=PLAINTEXT://your.host.name:9092

```



2. kafka集群搭建好了之后，使用提供的stop脚本无法关闭server，提示 ``` no kafka server to stop ```

   ```
   手动修改官方的server-stop脚本后可以停止
   PIDS=$(ps ax | grep -i 'kafka\.Kafka' | grep java | grep -v grep | awk '{print $1}')
   修改为：
   PIDS=$(jps -lm | grep -i 'kafka\.Kafka' | awk '{print $1}')
   
   ```

3. Spring中使用kafka启动时候，经常会遇到下面的错误

Caused by: java.lang.NoClassDefFoundError: org/apache/kafka/common/requests/IsolationLevel

原因如下：

```
因为我kafka使用的2.5版本的，因此spring-boot必须是2.3以上版本才可以
This is a breaking change in Kafka 2.5 and Spring Boot 2.3 is required. We released RC1 last week and GA is around the corner.
```

4. Sring boot中如果要想使用xml方式进行配置要注意一下的问题

   - 文件名不能是applicattion开头的，否则加载时会报错

   - 需添加引入资源文件的注解，否则不会自动加载xml资源：

     ```java
     @ImportResource(locations = "kafkaConsumer.xml")
     ```

     