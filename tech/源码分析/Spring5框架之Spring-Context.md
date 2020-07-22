## Spring5之Spring-Context

- /support
  
  - AbstarctApplicationContext：加载bean的主要过程都在refresh()方法中
  
  - ClassPathXmlApplicationContext : 一种高级IOC容器，除了提供BeanFactory规定的基本功能外，还提供附加功能：
    1. 支持信息源，可以支持国际化（实现MessageSource接口）
    2. 访问资源（实现了ResourcePatternResolver接口）
    3. 支持应用事件（实现了ApplicationEventPublisher接口）





### 基于注解的Context

#### AnnotationConfigApplicationContext  

1. 是专门处理注解方式配置的容器

2. 常用构造函数入口

   2.1 下面是register方式进行载入的入口方法：

```
// 最常用的构造函数， 通过将涉及到的配置类传递给该构造函数， 以实现将相应配置类中的 Bean 自动注册到容器中
public AnnotationConfigApplicationContext(Class<?>... annotatedClasses) {
    this();
    // 通过调用AnnotatedBeanDefinitionReader的register方法向容器注册指定的注解bean
    register(annotatedClasses);
    refresh();
}
```

​    2.2 下面是通过scan方式进行载入的入口方法：

```
/**
 * Create a new AnnotationConfigApplicationContext, scanning for bean definitions
 * in the given packages and automatically refreshing the context.
 * @param basePackages the packages to check for annotated classes
 */
public AnnotationConfigApplicationContext(String... basePackages) {
   this();
   // 根据指定的包名进行扫描，通过容器内部的ClassPathBeanDefinitionScanner进行扫描的
   scan(basePackages);
   // 调用父类AbstractApplicationContext的refresh方法，触发对bean的解析与注册
   refresh();
}

```

3. BeanPostProcessor 是一个接口， 其初始化前的操作方法和初始化后的操作方法均委托其实现子类来
   实现， 在 Spring 中， BeanPostProcessor 的实现子类非常的多， 分别完成不同的操作， 如： AOP 面向
   切面编程的注册通知适配器、 Bean 对象的数据校验、 Bean 继承属性/方法的合并等等， 我们以最简单
   的 AOP 切面织入来简单了解其主要的功能。 

   都是对 Bean 对象使用到的一些特性进行处理， 或者向 IOC 容器中注册， 为创建的 Bean 实例对象做一些自定义的功能增加， 这些操作是容器初始化 Bean
   时自动触发的， 不需要认为的干预。  

扫描给定包及子包的方法doScan

- 还是熟悉的BeanDefinitionHolder来存储解析后的类定义
- 注解BeanDefinition：AnnotatedGenericBeanDefinition 
- 

```
/**
 * Perform a scan within the specified base packages,
 * returning the registered bean definitions.
 * <p>This method does <i>not</i> register an annotation config processor
 * but rather leaves this up to the caller.
 * @param basePackages the packages to check for annotated classes
 * @return set of beans registered if any for tooling registration purposes (never {@code null})
 */
protected Set<BeanDefinitionHolder> doScan(String... basePackages) {
   Set<BeanDefinitionHolder> beanDefinitions = new LinkedHashSet<>();
   for (String basePackage : basePackages) {
   //调用父类 ClassPathScanningCandidateComponentProvider 的方法
//扫描给定类路径， 获取符合条件的 Bean 定义
      Set<BeanDefinition> candidates = findCandidateComponents(basePackage);
      
      for (BeanDefinition candidate : candidates) {
         ScopeMetadata scopeMetadata = this.scopeMetadataResolver.resolveScopeMetadata(candidate);
         candidate.setScope(scopeMetadata.getScopeName());
         String beanName = this.beanNameGenerator.generateBeanName(candidate, this.registry);
         if (candidate instanceof AbstractBeanDefinition) {
            postProcessBeanDefinition((AbstractBeanDefinition) candidate, beanName);
         }
         if (candidate instanceof AnnotatedBeanDefinition) {
            AnnotationConfigUtils.processCommonDefinitionAnnotations((AnnotatedBeanDefinition) candidate);
         }
         if (checkCandidate(beanName, candidate)) {
            BeanDefinitionHolder definitionHolder = new BeanDefinitionHolder(candidate, beanName);
            definitionHolder =
                  AnnotationConfigUtils.applyScopedProxyMode(scopeMetadata, definitionHolder, this.registry);
            beanDefinitions.add(definitionHolder);
            registerBeanDefinition(definitionHolder, this.registry);
         }
      }
}
   return beanDefinitions;
}
```

**ClassPathScanningCandidateComponentProvider 类的 findCandidateComponents 方法具体实现
扫描给定类路径包的功能** 

- **判断是否容器配置的过滤规则是通过ASM读取字节码中的bean定义原信息**

```
ClassPathScanningCandidateComponentProvider class



```







#### AnnotationConfigWebApplicationContext  

1. 专门处理注解方式配置的容器（WEB版本）

2. 注册和扫描基本和非WEB版是一样的，载入过程稍有不同

   







### 附录1 BeanFactory相关类继承关系图(初级IOC容器)

![image-20200613222543735](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20200613222543735.png)

### 附录2 ApplicatinContext相关类关系图（高级IOC容器）

1. XML解析方式

![image-20200613222401691](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20200613222401691.png)

2. 注解方式

   <img src=".\AnnotationConfigApplicationContext.png" />

### 附录3 Spring通用的内部Bean定义相关类结构图

![image-20200702221218989](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20200702221218989.png)