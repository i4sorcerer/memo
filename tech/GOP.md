## Good QA Pool



### maven dependencies decorated by optional or provided

首先要理解的是这两个便签针对的目标project

结论：

1. optional指的是对projectB是optinal的。对当前projectA没有影响，如果另一个projectB依赖projectA则，optional的jar不会引入projectB的classpath中。
2. scope为provided指的是，当前jar是被server端提供，典型的就是javax-servlet-api.jar。正常来讲不会被打包进war包里。

- <optional>true</optional> or <scope>provided</scope>
- https://maven.apache.org/guides/introduction/introduction-to-optional-and-excludes-dependencies.html
- https://issues.apache.org/jira/browse/MWAR-351



### java方法中如果包含死循环结果，则可以不必每个分支都包含return 语句

```java
public boolean acquireLoop(Object pred, Object node){
    boolean acquired = false;
    for (;;){
        if (pred == node){
            return true;
        }
    }
}
// 上面代码是没有编译错误的，如果for循环改为有条件循环，则需要添加return语句
// for(inti=0;i<10;i++)
```



