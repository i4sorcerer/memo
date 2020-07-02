## Spring5之Spring-Context

- /support
  
  - AbstarctApplicationContext：加载bean的主要过程都在refresh()方法中
  
  - ClassPathXmlApplicationContext : 一种高级IOC容器，除了提供BeanFactory规定的基本功能外，还提供附加功能：
    1. 支持信息源，可以支持国际化（实现MessageSource接口）
    2. 访问资源（实现了ResourcePatternResolver接口）
    3. 支持应用事件（实现了ApplicationEventPublisher接口）









### 附录1 BeanFactory相关类继承关系图(初级IOC容器)

![image-20200613222543735](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20200613222543735.png)

### 附录2 ApplicatinContext相关类关系图（高级IOC容器）

![image-20200613222401691](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20200613222401691.png)



