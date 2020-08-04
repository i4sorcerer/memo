## Spring boot startup 

### @SpringBootConfiguration

1. @Configuration(@SpringBootConfiguration)

2. @ComponentScan

3. @EnableAutoConfiguration (important)

   借助@Import的支持，收集和注册特定场景相关的bean定义。即将所有符合自动配置条件的bean都加载到Ioc容器中。

   看其源码可知，由下面2个比较中要的注解组成

   - @AutoConfigurationPackage:自动配置包
   - @Import(EnableAutoConfigurationImportSelector.class):导入自动配置的组件

   import其他类似使用

   - @EnableScheduling是通过@Import将Spring调度框架相关的bean定义都加载到IoC容器。
   - @EnableMBeanExport是通过@Import将JMX相关的bean定义加载到IoC容器。

下面是连接信息配置错误打出的错误日志信息，通过此可以分析出，Springboot启动时的大概过程

```
2020/06/12 10:26:37.641 [INFO ] Starting VIF120080Controller on ORIX0258 with PID 15972 (C:\Windows\work\release-workspace\janet2_vif120080\target\classes started by AQC in C:\Windows\work\release-workspace\janet2_vif120080)
2020/06/12 10:26:37.672 [INFO ] The following profiles are active: env,janet2,vif120080,fw
2020/06/12 10:26:54.337 [INFO ] Bean 'org.springframework.ws.config.annotation.DelegatingWsConfiguration' of type [org.springframework.ws.config.annotation.DelegatingWsConfiguration$$EnhancerBySpringCGLIB$$8e1b21cc] is not eligible for getting processed by all BeanPostProcessors (for example: not eligible for auto-proxying)
2020/06/12 10:26:54.399 [INFO ] Supporting [WS-Addressing August 2004, WS-Addressing 1.0]
2020/06/12 10:26:54.835 [INFO ] Bean 'org.springframework.transaction.annotation.ProxyTransactionManagementConfiguration' of type [org.springframework.transaction.annotation.ProxyTransactionManagementConfiguration$$EnhancerBySpringCGLIB$$e9835ccd] is not eligible for getting processed by all BeanPostProcessors (for example: not eligible for auto-proxying)
2020/06/12 10:26:57.095 [INFO ] Tomcat initialized with port(s): 8080 (http)
2020/06/12 10:26:57.147 [INFO ] Initializing ProtocolHandler ["http-nio-8080"]
2020/06/12 10:26:57.165 [INFO ] Starting service [Tomcat]
2020/06/12 10:26:57.167 [INFO ] Starting Servlet engine: [Apache Tomcat/9.0.19]
2020/06/12 10:26:57.493 [INFO ] Initializing Spring embedded WebApplicationContext
2020/06/12 10:26:57.494 [INFO ] Root WebApplicationContext: initialization completed in 19741 ms
2020/06/12 10:26:59.757 [WARN ] Exception encountered during context initialization - cancelling refresh attempt: org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'VIF120080BussinessCommon': Unsatisfied dependency expressed through field 'mqUtil'; nested exception is org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'mqUtil': Unsatisfied dependency expressed through field 'jmsTemplate'; nested exception is org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'jmsTemplate' defined in class path resource [biz/jal/crane/jsc/base/util/mq/MQUtilConfig.class]: Unsatisfied dependency expressed through method 'jmsTemplate' parameter 0; nested exception is org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'queueConnectionFactory' defined in class path resource [biz/jal/crane/jsc/base/inf/service/AbstractIFServiceConfig.class]: Bean instantiation via factory method failed; nested exception is org.springframework.beans.BeanInstantiationException: Failed to instantiate [javax.jms.QueueConnectionFactory]: Factory method 'queueConnectionFactory' threw exception; nested exception is javax.naming.NoInitialContextException: Need to specify class name in environment or system property, or as an applet parameter, or in an application resource file:  java.naming.factory.initial
2020/06/12 10:26:59.764 [INFO ] Stopping service [Tomcat]
2020/06/12 10:26:59.791 [INFO ] 

Error starting ApplicationContext. To display the conditions report re-run your application with 'debug' enabled.
2020/06/12 10:26:59.795 [ERROR] Application run failed
org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'VIF120080BussinessCommon': Unsatisfied dependency expressed through field 'mqUtil'; nested exception is org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'mqUtil': Unsatisfied dependency expressed through field 'jmsTemplate'; nested exception is org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'jmsTemplate' defined in class path resource [biz/jal/crane/jsc/base/util/mq/MQUtilConfig.class]: Unsatisfied dependency expressed through method 'jmsTemplate' parameter 0; nested exception is org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'queueConnectionFactory' defined in class path resource [biz/jal/crane/jsc/base/inf/service/AbstractIFServiceConfig.class]: Bean instantiation via factory method failed; nested exception is org.springframework.beans.BeanInstantiationException: Failed to instantiate [javax.jms.QueueConnectionFactory]: Factory method 'queueConnectionFactory' threw exception; nested exception is javax.naming.NoInitialContextException: Need to specify class name in environment or system property, or as an applet parameter, or in an application resource file:  java.naming.factory.initial
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.inject(AutowiredAnnotationBeanPostProcessor.java:596) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.annotation.InjectionMetadata.inject(InjectionMetadata.java:90) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor.postProcessProperties(AutowiredAnnotationBeanPostProcessor.java:374) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.populateBean(AbstractAutowireCapableBeanFactory.java:1411) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:592) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:515) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.lambda$doGetBean$0(AbstractBeanFactory.java:320) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:222) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:318) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:199) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.preInstantiateSingletons(DefaultListableBeanFactory.java:843) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.context.support.AbstractApplicationContext.finishBeanFactoryInitialization(AbstractApplicationContext.java:877) ~[spring-context-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:549) ~[spring-context-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.boot.web.servlet.context.ServletWebServerApplicationContext.refresh(ServletWebServerApplicationContext.java:142) ~[spring-boot-2.1.5.RELEASE.jar:2.1.5.RELEASE]
	at org.springframework.boot.SpringApplication.refresh(SpringApplication.java:775) [spring-boot-2.1.5.RELEASE.jar:2.1.5.RELEASE]
	at org.springframework.boot.SpringApplication.refreshContext(SpringApplication.java:397) [spring-boot-2.1.5.RELEASE.jar:2.1.5.RELEASE]
	at org.springframework.boot.SpringApplication.run(SpringApplication.java:316) [spring-boot-2.1.5.RELEASE.jar:2.1.5.RELEASE]
	at org.springframework.boot.builder.SpringApplicationBuilder.run(SpringApplicationBuilder.java:139) [spring-boot-2.1.5.RELEASE.jar:2.1.5.RELEASE]
	at biz.jal.crane.janet2.inf.VIF120080Controller.main(VIF120080Controller.java:25) [classes/:?]
Caused by: org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'mqUtil': Unsatisfied dependency expressed through field 'jmsTemplate'; nested exception is org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'jmsTemplate' defined in class path resource [biz/jal/crane/jsc/base/util/mq/MQUtilConfig.class]: Unsatisfied dependency expressed through method 'jmsTemplate' parameter 0; nested exception is org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'queueConnectionFactory' defined in class path resource [biz/jal/crane/jsc/base/inf/service/AbstractIFServiceConfig.class]: Bean instantiation via factory method failed; nested exception is org.springframework.beans.BeanInstantiationException: Failed to instantiate [javax.jms.QueueConnectionFactory]: Factory method 'queueConnectionFactory' threw exception; nested exception is javax.naming.NoInitialContextException: Need to specify class name in environment or system property, or as an applet parameter, or in an application resource file:  java.naming.factory.initial
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.inject(AutowiredAnnotationBeanPostProcessor.java:596) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.annotation.InjectionMetadata.inject(InjectionMetadata.java:90) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor.postProcessProperties(AutowiredAnnotationBeanPostProcessor.java:374) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.populateBean(AbstractAutowireCapableBeanFactory.java:1411) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:592) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:515) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.lambda$doGetBean$0(AbstractBeanFactory.java:320) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:222) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:318) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:199) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.config.DependencyDescriptor.resolveCandidate(DependencyDescriptor.java:277) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1248) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1168) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.inject(AutowiredAnnotationBeanPostProcessor.java:593) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	... 18 more
Caused by: org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'jmsTemplate' defined in class path resource [biz/jal/crane/jsc/base/util/mq/MQUtilConfig.class]: Unsatisfied dependency expressed through method 'jmsTemplate' parameter 0; nested exception is org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'queueConnectionFactory' defined in class path resource [biz/jal/crane/jsc/base/inf/service/AbstractIFServiceConfig.class]: Bean instantiation via factory method failed; nested exception is org.springframework.beans.BeanInstantiationException: Failed to instantiate [javax.jms.QueueConnectionFactory]: Factory method 'queueConnectionFactory' threw exception; nested exception is javax.naming.NoInitialContextException: Need to specify class name in environment or system property, or as an applet parameter, or in an application resource file:  java.naming.factory.initial
	at org.springframework.beans.factory.support.ConstructorResolver.createArgumentArray(ConstructorResolver.java:769) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.ConstructorResolver.instantiateUsingFactoryMethod(ConstructorResolver.java:509) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.instantiateUsingFactoryMethod(AbstractAutowireCapableBeanFactory.java:1321) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBeanInstance(AbstractAutowireCapableBeanFactory.java:1160) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:555) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:515) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.lambda$doGetBean$0(AbstractBeanFactory.java:320) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:222) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:318) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:199) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.config.DependencyDescriptor.resolveCandidate(DependencyDescriptor.java:277) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1248) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1168) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.inject(AutowiredAnnotationBeanPostProcessor.java:593) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.annotation.InjectionMetadata.inject(InjectionMetadata.java:90) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor.postProcessProperties(AutowiredAnnotationBeanPostProcessor.java:374) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.populateBean(AbstractAutowireCapableBeanFactory.java:1411) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:592) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:515) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.lambda$doGetBean$0(AbstractBeanFactory.java:320) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:222) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:318) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:199) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.config.DependencyDescriptor.resolveCandidate(DependencyDescriptor.java:277) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1248) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1168) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.inject(AutowiredAnnotationBeanPostProcessor.java:593) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	... 18 more
Caused by: org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'queueConnectionFactory' defined in class path resource [biz/jal/crane/jsc/base/inf/service/AbstractIFServiceConfig.class]: Bean instantiation via factory method failed; nested exception is org.springframework.beans.BeanInstantiationException: Failed to instantiate [javax.jms.QueueConnectionFactory]: Factory method 'queueConnectionFactory' threw exception; nested exception is javax.naming.NoInitialContextException: Need to specify class name in environment or system property, or as an applet parameter, or in an application resource file:  java.naming.factory.initial
	at org.springframework.beans.factory.support.ConstructorResolver.instantiate(ConstructorResolver.java:627) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.ConstructorResolver.instantiateUsingFactoryMethod(ConstructorResolver.java:456) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.instantiateUsingFactoryMethod(AbstractAutowireCapableBeanFactory.java:1321) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBeanInstance(AbstractAutowireCapableBeanFactory.java:1160) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:555) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:515) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.lambda$doGetBean$0(AbstractBeanFactory.java:320) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:222) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:318) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:199) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.config.DependencyDescriptor.resolveCandidate(DependencyDescriptor.java:277) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1248) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1168) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.ConstructorResolver.resolveAutowiredArgument(ConstructorResolver.java:857) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.ConstructorResolver.createArgumentArray(ConstructorResolver.java:760) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.ConstructorResolver.instantiateUsingFactoryMethod(ConstructorResolver.java:509) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.instantiateUsingFactoryMethod(AbstractAutowireCapableBeanFactory.java:1321) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBeanInstance(AbstractAutowireCapableBeanFactory.java:1160) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:555) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:515) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.lambda$doGetBean$0(AbstractBeanFactory.java:320) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:222) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:318) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:199) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.config.DependencyDescriptor.resolveCandidate(DependencyDescriptor.java:277) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1248) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1168) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.inject(AutowiredAnnotationBeanPostProcessor.java:593) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.annotation.InjectionMetadata.inject(InjectionMetadata.java:90) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor.postProcessProperties(AutowiredAnnotationBeanPostProcessor.java:374) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.populateBean(AbstractAutowireCapableBeanFactory.java:1411) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:592) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:515) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.lambda$doGetBean$0(AbstractBeanFactory.java:320) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:222) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:318) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:199) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.config.DependencyDescriptor.resolveCandidate(DependencyDescriptor.java:277) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1248) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1168) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.inject(AutowiredAnnotationBeanPostProcessor.java:593) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	... 18 more
Caused by: org.springframework.beans.BeanInstantiationException: Failed to instantiate [javax.jms.QueueConnectionFactory]: Factory method 'queueConnectionFactory' threw exception; nested exception is javax.naming.NoInitialContextException: Need to specify class name in environment or system property, or as an applet parameter, or in an application resource file:  java.naming.factory.initial
	at org.springframework.beans.factory.support.SimpleInstantiationStrategy.instantiate(SimpleInstantiationStrategy.java:185) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.ConstructorResolver.instantiate(ConstructorResolver.java:622) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.ConstructorResolver.instantiateUsingFactoryMethod(ConstructorResolver.java:456) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.instantiateUsingFactoryMethod(AbstractAutowireCapableBeanFactory.java:1321) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBeanInstance(AbstractAutowireCapableBeanFactory.java:1160) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:555) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:515) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.lambda$doGetBean$0(AbstractBeanFactory.java:320) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:222) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:318) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:199) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.config.DependencyDescriptor.resolveCandidate(DependencyDescriptor.java:277) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1248) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1168) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.ConstructorResolver.resolveAutowiredArgument(ConstructorResolver.java:857) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.ConstructorResolver.createArgumentArray(ConstructorResolver.java:760) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.ConstructorResolver.instantiateUsingFactoryMethod(ConstructorResolver.java:509) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.instantiateUsingFactoryMethod(AbstractAutowireCapableBeanFactory.java:1321) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBeanInstance(AbstractAutowireCapableBeanFactory.java:1160) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:555) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:515) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.lambda$doGetBean$0(AbstractBeanFactory.java:320) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:222) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:318) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:199) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.config.DependencyDescriptor.resolveCandidate(DependencyDescriptor.java:277) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1248) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1168) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.inject(AutowiredAnnotationBeanPostProcessor.java:593) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.annotation.InjectionMetadata.inject(InjectionMetadata.java:90) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor.postProcessProperties(AutowiredAnnotationBeanPostProcessor.java:374) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.populateBean(AbstractAutowireCapableBeanFactory.java:1411) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:592) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:515) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.lambda$doGetBean$0(AbstractBeanFactory.java:320) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:222) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:318) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:199) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.config.DependencyDescriptor.resolveCandidate(DependencyDescriptor.java:277) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1248) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1168) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.inject(AutowiredAnnotationBeanPostProcessor.java:593) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	... 18 more
Caused by: javax.naming.NoInitialContextException: Need to specify class name in environment or system property, or as an applet parameter, or in an application resource file:  java.naming.factory.initial
	at javax.naming.spi.NamingManager.getInitialContext(NamingManager.java:662) ~[?:1.8.0_181]
	at javax.naming.InitialContext.getDefaultInitCtx(InitialContext.java:313) ~[?:1.8.0_181]
	at javax.naming.InitialContext.getURLOrDefaultInitCtx(InitialContext.java:350) ~[?:1.8.0_181]
	at javax.naming.InitialContext.lookup(InitialContext.java:417) ~[?:1.8.0_181]
	at biz.jal.crane.jsc.base.inf.service.AbstractIFServiceConfig.queueConnectionFactory(AbstractIFServiceConfig.java:126) ~[classes/:?]
	at biz.jal.crane.jsc.base.inf.service.AbstractIFServiceConfig$$EnhancerBySpringCGLIB$$65f6b4f4.CGLIB$queueConnectionFactory$8(<generated>) ~[classes/:?]
	at biz.jal.crane.jsc.base.inf.service.AbstractIFServiceConfig$$EnhancerBySpringCGLIB$$65f6b4f4$$FastClassBySpringCGLIB$$b3da9226.invoke(<generated>) ~[classes/:?]
	at org.springframework.cglib.proxy.MethodProxy.invokeSuper(MethodProxy.java:244) ~[spring-core-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.context.annotation.ConfigurationClassEnhancer$BeanMethodInterceptor.intercept(ConfigurationClassEnhancer.java:363) ~[spring-context-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at biz.jal.crane.jsc.base.inf.service.AbstractIFServiceConfig$$EnhancerBySpringCGLIB$$65f6b4f4.queueConnectionFactory(<generated>) ~[classes/:?]
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method) ~[?:1.8.0_181]
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62) ~[?:1.8.0_181]
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43) ~[?:1.8.0_181]
	at java.lang.reflect.Method.invoke(Method.java:498) ~[?:1.8.0_181]
	at org.springframework.beans.factory.support.SimpleInstantiationStrategy.instantiate(SimpleInstantiationStrategy.java:154) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.ConstructorResolver.instantiate(ConstructorResolver.java:622) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.ConstructorResolver.instantiateUsingFactoryMethod(ConstructorResolver.java:456) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.instantiateUsingFactoryMethod(AbstractAutowireCapableBeanFactory.java:1321) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBeanInstance(AbstractAutowireCapableBeanFactory.java:1160) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:555) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:515) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.lambda$doGetBean$0(AbstractBeanFactory.java:320) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:222) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:318) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:199) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.config.DependencyDescriptor.resolveCandidate(DependencyDescriptor.java:277) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1248) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1168) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.ConstructorResolver.resolveAutowiredArgument(ConstructorResolver.java:857) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.ConstructorResolver.createArgumentArray(ConstructorResolver.java:760) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.ConstructorResolver.instantiateUsingFactoryMethod(ConstructorResolver.java:509) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.instantiateUsingFactoryMethod(AbstractAutowireCapableBeanFactory.java:1321) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBeanInstance(AbstractAutowireCapableBeanFactory.java:1160) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:555) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:515) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.lambda$doGetBean$0(AbstractBeanFactory.java:320) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:222) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:318) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:199) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.config.DependencyDescriptor.resolveCandidate(DependencyDescriptor.java:277) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1248) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1168) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.inject(AutowiredAnnotationBeanPostProcessor.java:593) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.annotation.InjectionMetadata.inject(InjectionMetadata.java:90) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor.postProcessProperties(AutowiredAnnotationBeanPostProcessor.java:374) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.populateBean(AbstractAutowireCapableBeanFactory.java:1411) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:592) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:515) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.lambda$doGetBean$0(AbstractBeanFactory.java:320) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:222) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:318) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:199) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.config.DependencyDescriptor.resolveCandidate(DependencyDescriptor.java:277) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1248) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1168) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.inject(AutowiredAnnotationBeanPostProcessor.java:593) ~[spring-beans-5.1.7.RELEASE.jar:5.1.7.RELEASE]
	... 18 more

```











## 其他重要注解继续学习

### @Import 

