## Spring Resources

[Spring Framework Tutorials](https://www.logicbig.com/tutorials/spring-framework.html)

### [Spring - Dependency injection in @Bean method parameters](https://www.logicbig.com/tutorials/spring-framework/spring-core/javaconfig-methods-inter-dependency.html)

### Spring boot中完美的诠释了约定优于配置这一规则

#### 默认配置文件application.properties

- Spring boot中默认的配置文件是不用配置（路径，名字等），默认加载src/main/resources/下的application.properties

- 如果想改变这一默认配置文件的路径可以通过环境变量进行指定**spring.config.location**

  ```
  java -jar app.jar --spring.config.location=classpath:/another-location.properties
  ```

#### 环境相关的配置文件

- application-env.properties

- application-dev.properties

- application-staging.properties

- application-prept.properties

- application-prod.properties

- 通过环境变量JAVA_OPTS指定profile，```-Dspring.profiles.active=staging,jboss```

  



### Spring boot中属性文件加载顺序

- spring.profiles.include=test1,test2 按照test1,test2的顺序进行加载
- 无论key定义在哪个文件中，最终生效的总是最后一次加载的key的值

### Spring boot 中message文件加载顺序

- spring.messages.basename=messages1,messages2按照messages1，messages2的顺序进行文件加载
- 定义在同一个文件中的相同messageId，总是后加载的有效（覆盖）
- 定义在不同文件中的相同messageId，总是先加载的有效（之前property文件已存在则后续相同key不加载）

### [www.logicbig.com](www.logicbig.com)





