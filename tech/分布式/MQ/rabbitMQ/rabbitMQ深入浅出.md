### RabbitMQ深入浅出

官方文件RabbitMQ Tutorials：https://www.rabbitmq.com/getstarted.html

官方文档Doc：https://www.rabbitmq.com/documentation.html

#### 安装

windows安装

- 安装手册

https://www.rabbitmq.com/install-windows.html#installer

- Erlang安装下载

https://www.erlang-solutions.com/resources/download.html

- rabbitMQ-server安装下载
- Erlang与rabbitMQ兼容版本对照

https://www.rabbitmq.com/which-erlang.html

#### MQ消息队列应用场景

- 异步
- 解耦
- 削峰

#### 协议

- AMQP

#### 主要组成

- 生产者

- broker

  - exchange

    交换机和队列的绑定方式：

    - DirectExchange：固定路由key方式（路由key=test）
    - TopicExchange：带通配符的路由key方式（路由key=test.*,路由key=test.#）
    - FanoutExchange：广播（不指定路由key）

  - queue队列

  - virtual host

  - connection

    - channel
    
      - 服务端确认Transaction模式
    
        channel.txSelect()
    
        channel.txCommit();
    
        channel.txRollback();
    
      - 服务端确认Confirm模式:异步确认
    
        channel.confirmSelect();
    
        if(channel.waitForConfirms()){
    
        }

- 消费者

- UI管理客户端：http://127.0.0.1:15672/

#### 过期时间ttl

- 队列的过期时间设置属性x-message-ttl
- 单个消息的ttl



#### 死信队列

当消息在一个队列中变成死信 `(dead message)` 之后，它能被重新publish到另一个Exchange，这个Exchange就是DLX

- 什么时候会变成死信？
  1. 消息被客户端拒绝reject
  2. 消息设置了过期时间，并且未被消费
  3. 队列设置了`x-max-length`最大消息数量且当前队列中的消息已经达到了这个数量，再次投递，消息将被挤掉，被挤掉的是最靠近被消费那一端的消息。

- 如何设置

  - 业务队列添加属性

    x-dead-letter-exchange=xxxx

    x-dead-letter-routing-key=a.b.c 

    **死信消息会自动发送到xxxx交换机上，路由key不是初识的key，而是变成了指定的a.b.c**

#### 优先队列

- 设置优先级

#### 延迟队列

- 延迟队列插件
- TTL+DLX

#### 消息存储机制

- 队列持久化
- 交换机持久化
- 消息持久化

#### cookie机制



#### 死信队列的设置

#### 集群

- 网络分区：只能是局域网，不支持wlan
- 必须存在一个磁盘节点，其他可以是内存节点



#### RabbitMQ和其他消息中间件相比的特性

- **可靠性**
  - 路由保证
    1. 发送端设置ReturnListener
    2. 本分交换机
- **灵活的路由**
- 消息集群
- **高可用**
- 多种协议
- 多语言客户端
- 管理界面
- 插件机制
- 消息幂等性(防止重复消费问题)
  - 可以通过设置全局messageID，消费端进行判断
- 消息顺序性
  - 一个queue一个消费者的时候，可以保证消息的顺序性（prefetchcount=1）





#### 问题集

- 注意不同项目中（或者多个生产者如果都创建同一个exchange,queue时，queue，exchange相关配置应该是一样的），否则会报如下错误：

  inequivalent arg 'x-dead-lett

  解决办法：在UI客户端删除，再重新运行即可

  ```
  [10:34:01:346] [ERROR] - org.springframework.amqp.rabbit.connection.CachingConnectionFactory$DefaultChannelCloseLogger.log(CachingConnectionFactory.java:1566) - Channel shutdown: channel error; protocol method: #method<channel.close>(reply-code=406, reply-text=PRECONDITION_FAILED - inequivalent arg 'x-message-ttl' for queue 'TEST-DX-QUEUE' in vhost '/': received the value '5000' of type 'signedint' but current is none, class-id=50, method-id=10)
  ```

  