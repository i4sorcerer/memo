### 深入浅出之MyBatis

mybatis的处理流程



mybatis中关键类/接口

- SqlSessionFactoryBuilder

- SqlSessionFactory

- SqlSession

- Mapper



#### 配置文件

- mybatis-config.xml文件
  - https://www.cnblogs.com/lujiango/p/8630154.html#_label1
  - 
- Configuration下的配置
  - properties 属性
  - settings 设置
    These are extremely important tweaks that modify the way that MyBatis behaves at runtime
  - typeAliases 类型别名
  - typeHandlers 类型处理器
  - objectFactory 对象工厂
    MyBatis uses an ObjectFactory to create all needed new Objects.
  - plugins 插件
  - environments 环境
  - environment 环境变量
  - transactionManager 事务管理器
  - dataSource 数据源
  - databaseIdProvider 数据库厂商标识
  - mappers 映射器

##### TypeHandler

- mybatis默认提供的类型处理：https://mybatis.org/mybatis-3/configuration.html#typeHandlers
- 是可以自定义类型处理的，集成BaseTypeHandler或者实现TypeHandler接口

##### plugin

- 分页插件 pageHelper
- 手写一个拦截器【todo】

可以定义拦截器

MyBatis allows you to intercept calls to at certain points within the execution of a mapped statement. By default, MyBatis allows plug-ins to intercept method calls of:

- Executor (update, query, flushStatements, commit, rollback, getTransaction, close, isClosed)
- ParameterHandler (getParameterObject, setParameters)
- ResultSetHandler (handleResultSets, handleOutputParameters)
- StatementHandler (prepare, parameterize, batch, update, query)

#### 日志实现

jdbc方式：使用动态代理方式，对各自对象进行代理，添加logging功能

- BaseJdbcLogging
- ConnectionLogger
- PreparedStatementLogger
- ResultSetLogger
- StatementLogger

#### 开闭原则

对修改开放，对扩展关闭

#### Mapper

1. 使用方式

   - XML形式

   - 注解形式

2. 文件详解

   - namespace

   - resultMap、resultType

   - sql

   - CRUD

   - 动态sql

   - 缓存

     1. 一级缓存：

        - 减少数据库压力，有可能出现脏数据
        - 默认开启一级缓存，指的是session级别的缓存，同一个session内，相同的查询会命中缓存。

        - 清除策略：遇到update，delete操作时，缓存被清除
        - sql语句中强制刷新缓存：flushCache="true"，默认false

     2. 二级缓存

        - 默认关闭，不建议使用。
        - 一般使用redis等代替
        - 对于各个Mapper的缓存，不同session访问同一个mapper时，会命中缓存（以namespace区分，mapper文件）。
        - 问题：
          1. 很容易出现在脏数据
          2. 清除的时候，会将同一个namespace下的缓存全部失效
          3. N+1问题：

3. 使用场景
   - 分页
   - 批量操作
   - 联合查询



#### 与spring框架继承

#### mybatis类加载进spring

```java
	ImportBeanDefinitionRegistrar spring容器在处理@Configuration注解时，会调用第三方实现类
    MapperScannerRegistrar implements ImportBeanDefinitionRegistrar注册MapperScan注解到spring容器中
    
```

- xml方式和注解方式互补

  - 注解方式开启(简单增删改查)

  ```
  // 添加注解，扫描mapper接口
  @MapperScan("kafka.demo.domain.dao")
  定义UserMapper接口，使用@Select@Result等等注解，定义方法
  
  ```

  - 同时，又可以开启xml的默认方式（定义的method是惟一的，任意method来说，只能是xml方式或者注解方式）

  复杂的查询或者条件查询可以使用这个。sql更容易编写

  ```
  mybatis.config-location=classpath:mybatis-config.xml
  注1：mybatis.mapper-locations=classpath:mapping/*.xml
  
  注1：或者此处不写，mapper文件的引入，写在mybatis-config.xml中
      <mappers>
  <!--        <mapper resource="mapping/UserMapper.xml"/>-->
          <!--package的方式未验证成功-->
  <!--        <package name="kafka.demo.domain.dao"/>-->
      </mappers>
  
  ```



#### 问题集

- 为什么mybatis是通过mapper接口来调用方法的？如何实现的？

```
通过动态代理实现的，最终调用的是代理类的方法。此方法和xml文件中的sql文关联起来
```



