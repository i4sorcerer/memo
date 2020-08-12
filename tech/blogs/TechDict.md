#  # TechDict(技术点手册)

### failover(作为常见容错机制之一)

Fail-Over的含义为“失效转移”，是一种备份操作模式，当主要组件异常时，其功能转移到备份组件。其要点在于有主有备，且主故障时备可启用，并设置为主。如Mysql的双Master模式，当正在使用的Master出现故障时，可以拿备Master做主使用

### DevOps
- 它不是一种工具，DevOps其实要谈的是运维合一
<img src="http://dockone.io/uploads/article/20200228/e50dcb4bfbe7012c608bba0450bfcd96.png" />

### 灰度发布（Gray Release）



### [云原生](https://blog.csdn.net/BtB5e6Nsu1g511Eg5XEg/article/details/102422533)

- 云服务的后半场

### 持续交付Continuous Delivery
- 实际上就是从以前大大步走，改为小步快跑

### 微服务
- 有HA（High Available）的需求需要微服务。
- 有性能调校的需求（例如：图片的呈现或者搜寻）需要微服务。
- 经常变更的需要微服务。

### Kubernetes(K8S)

- 是实现云原生的中流砥柱
- 

### Docker



### Dubbo

- 定义：高性能Java RPC框架(服务治理)
- 主要角色：服务提供方，服务消费方，注册中心，监控中心，服务运行容器
- http://dubbo.apache.org/zh-cn/blog/dubbo-annotation.html

### SPI

- SPI 全称为 Service Provider Interface，是一种服务发现机制。

- SPI 的本质是将接口实现类的全限定名配置在文件中，并由服务加载器读取配置文件，加载实现类。
- 

### 负载均衡

- F5硬件负载均衡（什么是F5硬件负载均衡？其他常用的软件负载有哪些？）
- 

### OSS存储

### Iaas 基础架构即服务
### Paas 平台即服务
### Saas 软件即服务
<img src="https://blogs.bmc.com/wp-content/uploads/2017/09/iaas-paas-saas-comparison-1024x759.jpg" />

### Callable和Runable的区别
- Callable接口是call方法，需要返回值
- Runable接口是run方法，没有返回值
- 两者都可以再Executor框架中通过调用execute方法，或者submit方法来 提交到线程池中




### 疑难杂症问题集
1. mvn clean package 编译时候，出现以下错误信息 unable to find main class的话，原因可能是下面的plugin引入地方不正。
You should have this
```
<build>
    <plugins>
        <plugin>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-maven-plugin</artifactId>
        </plugin>
    </plugins>
</build>
```

only in those modules that you want to run, but not in parent pom.


2. java 中获取地址
https://www.jianshu.com/p/1c9714622a4f






