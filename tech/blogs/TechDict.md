#  # TechDict(大全手册20200225)

### failover(作为常见容错机制之一)

Fail-Over的含义为“失效转移”，是一种备份操作模式，当主要组件异常时，其功能转移到备份组件。其要点在于有主有备，且主故障时备可启用，并设置为主。如Mysql的双Master模式，当正在使用的Master出现故障时，可以拿备Master做主使用

### DevOps



### 灰度发布（Gray Release）



### [云原生](https://blog.csdn.net/BtB5e6Nsu1g511Eg5XEg/article/details/102422533)

- 云服务的后半场

### Kubernetes(K8S)

- 是实现云原生的中流砥柱
- 

### 应用容器化

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






