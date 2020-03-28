### @Scope的使用注意

在spring中可以通过注解@Scope，来指定对象bean的初始化方式。spring中默认是Singleton即单例模式。单例模式指的是在spring容器范围内实例只有一个。支持方式有以下4种：

```java
@Target({ElementType.TYPE, ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface Scope {
    @AliasFor("scopeName")
    String value() default "";

    @AliasFor("value")
    String scopeName() default "";

    ScopedProxyMode proxyMode() default ScopedProxyMode.DEFAULT;
}
```

#### singleton单例(默认方式)

#### prototype拷贝

#### request请求（是不是只适用于web请求）

#### session 会话（是不是只适用于web请求）

1. 不是只要加上@Scope("prototype")的注解就能实现的。

   Scope的范围是具有传递性的，或者说在多个Bean的依赖链中，有一个需要做成多例时，上述注解可能会失效或者说达不到想要的效果。问题可参考：https://www.jianshu.com/p/54b0711a8ec8

   场景：类A中注入类B

   1. 类A单例，类B原型：类B中的@Scope("prototype")注解失效
      失效的原因还需要再探讨，主要和spring原理相关，和容器中是何时初始化bean，创建bean有关？？？
   2. 类A原型，类B原型：类B中的@Scope("prototype")注解有效









