### ScheduledPoolExecutor运行机制分析



#### DelayedWorkQueue队列

1. 初始化时候使用的是DelayedWorkQueue队列，也是一个无界队列，存储的是ScheduledFutureTask

```java
// ScheduledFutureTask类的主要成员变量
/** Sequence number to break ties FIFO */
private final long sequenceNumber;
/** The time the task is enabled to execute in nanoTime units */
private long time;
```





![image-20200802183714818](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20200802183714818.png)



2. DelayQueue内部同步机制使用的是ReentrantLock和Condition的方式

   take()和add()

   - lock.lock
   - condition.wait















