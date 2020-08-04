## deep sight in log 

### log4j

### log4j2

- #### [Configuring Loggers](https://logging.apache.org/log4j/2.x/manual/configuration.html#Loggers)

1. An understanding of how loggers work in Log4j is critical before trying to configure them. 

2. Applications using the Log4j 2 API will request a Logger with a specific name from the LogManager. The LogManager will locate the appropriate LoggerContext and then obtain the Logger from it. If the Logger must be created it will be associated with the LoggerConfig that contains either 

   **a) the same name as the Logger,** 
   **b) the name of a parent package, or** 
   **c) the root LoggerConfig. LoggerConfig objects are created from Logger declarations in the configuration.**
    The LoggerConfig is associated with the Appenders that actually deliver the LogEvents.
   [the Architecture of log4j](http://logging.apache.org/log4j/2.x/manual/architecture.html)

1. **The logger element must have a name attribute specified, will usually have a level attribute specified and may also have an additivity attribute specified.** 
2. Capturing location information (the class name, file name, method name, and line number of the caller) can be slow.
3. The LoggerConfig may also be configured with one or more AppenderRef elements. Each appender referenced will become associated with the specified LoggerConfig. If multiple appenders are configured on the LoggerConfig each of them be called when processing logging events.
4. **Every configuration must have a root logger**. If one is not configured the default root LoggerConfig, which has a level of ERROR and has a Console appender attached, will be used. The main differences between the root logger and other loggers are
5. The root logger does not have a name attribute.
6. The root logger does not support the additivity attribute since it has no parent.

### logback



### slf4j

主要是采用此方式，这是API，底层可以灵活采用log4j2或者logback实现

就像java规范了servlet api一样，底层的实现可以是tomcat jboss或者其他web server

步骤如下

1. 配置文件

2. 程序中通过LoggerFactory来获取一个匹配的Logger实例LoggerFactory.getLogger(name);
   通过这个方法获取Logger实际上是在编译时期，内部返回绑定的ILoggerFactory实例，通过此实例来生成对应的Logger对象的。这部分是在各种具体实现类中实现实现的。

   - Log4j implementation of SLF4J ILoggerFactory interface: **Log4jLoggerFactory**
   - logback implemenation of  SLF4J ILoggerFactory interface: **LoggerContext**

   ```
   /**
    * Return a logger named according to the name parameter using the
    * statically bound {@link ILoggerFactory} instance.
    * 
    * @param name
    *            The name of the logger.
    * @return logger
    */
   public static Logger getLogger(String name) {
       ILoggerFactory iLoggerFactory = getILoggerFactory();
       return iLoggerFactory.getLogger(name);
   }
   ```



