## Good QA Pool



#### 主进程fork子进程来实现后台处理额外的任务，主进程不被打断,如何实现的



#### java中存在静态代码块和构造代码块

- **对象一建立就运行构造代码块了，而且优先于构造函数执行**
- 

#### 流的自动关闭

java7之后try(FileOutputStream out = new FileOutputStream("....")) catch(Exception e){}

上述写法，流使用完了后会自动关闭



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



