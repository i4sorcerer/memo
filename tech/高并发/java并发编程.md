## java并发编程

### 基础知识

1. 竞态条件：当某个计算的正确性取决于多线程交替执行的时序时，就会发生竞态条件。

2. 要保证状态的一致性，就需要在单个原子操作中更新所有相关的状态变量。
3. 内置锁：指的是java中的同步代码块（synchronized block）
   同步代码块包含两个部分：
   - 一个作为锁的对象引用
   - 作为这个锁保护的代码块
     内置锁是一种互斥锁，意味着最多只有一个线程能持有这种锁。
     synchronized关键字实现了原子性，可见性，有序性
4. ThreadLocal类
   提供了get和set接口，get方法总是返回当前线程在调用set时设置的最新值

### JMM内存模型

屏蔽了硬件操作系统的差异，提供了统一的规范

- 原子性
- 可见性
- 有序性

CPU高速缓存分类

- L1 ： 处理器私有
- L2 ：处理器私有
- L3 ： 只有此级别的缓存是处理器间共享的。

对于多核心CPU，会出现缓存一致性问题，解决办法

- MESI缓存一致性协议

### Volatile实现原理

禁止指令重排

源码 -》  JVM字节码指令 -》汇编指令 -》机器码

指令重排序

- 编译器的指令重排序
- CPU的指令重排序
- 内存的乱序访问

```java
static int a = 0;
a=a+1;
a=a+2
```

对于上述源码，编译器会进行指令重排序，执行顺序可能有下面2种，导致最终结果不一致（多线程环境下）

```
执行顺序①
a=a+2
a=a+1
执行顺序②
a=a+1
a=a+2
```

1. 保证有序性（加内存屏障）
   - loadload barrier
   - storeload barrier
   - loadstore barrier
   - storestore barrier

2. 如何保证可见性（lock指令）
   - #lock指令，缓存锁，强制CPU缓存失效
3. 复合操作无法保证原子性，单个操作时原子性的

#### 双重检查和延迟初始化

##### 延迟初始化的解决方案一-》双重检查

```java
// 错误实例
public class DoubleCheckedLocking { // 1
private static Instance instance; // 2
public static Instance getInstance() { // 3
if (instance == null) { // 4:第一次检查
synchronized (DoubleCheckedLocking.class) { // 5:加锁
if (instance == null) // 6:第二次检查
instance = new Instance(); // 7:问题的根源出在这里
} // 8
} // 9
return instance; // 10
} // 11
}
```

- 根本原因是由于 instance = new Instance(); // 7:问题的根源出在这里，多线程环境下这里会发生2,3的指令重排序

```java
memory = allocate(); // 1：分配对象的内存空间
ctorInstance(memory); // 2：初始化对象
instance = memory; // 3：设置instance指向刚分配的内存地址
```

```java
// 正确示例
public class DoubleCheckedLocking { // 1
private volatile static Instance instance; // 2将其定义为volatile变量，禁止指令的重排序
public static Instance getInstance() { // 3
if (instance == null) { // 4:第一次检查
synchronized (DoubleCheckedLocking.class) { // 5:加锁
if (instance == null) // 6:第二次检查
instance = new Instance(); // 7:问题的根源出在这里
} // 8
} // 9
return instance; // 10
} // 11
}
```

##### 延迟初始化的解决方案二-》基于类初始化

JVM在类的初始化阶段（即在Class被加载后，且被线程使用之前），会执行类的初始化。在
执行类的初始化期间，JVM会去获取一个锁。这个锁可以同步多个线程对同一个类的初始化。  

```java
public class InstanceFactory {
	private static class InstanceHolder {
		public static Instance instance = new Instance();
	}
    public static Instance getInstance() {
		return InstanceHolder.instance ; // 这里将导致InstanceHolder类被初始化
	}
}
```







### Synchronized实现原理

解决了原子性，可见性，有序性

volatile变量和synchronized内存语义上有相同的地方

- volatile变量的读操作与synchronized的锁的获取有相同内存语义：使线程本地缓存失效，强制从主内存获取数据
- volatile变量的写操作和synchronized的锁释放有相同的内存你语义：使本地缓存刷新到主内存



Synchronized的锁作用域

- 全局锁：锁定整个class
- 对象锁
- 锁代码块

```java
public class SynDemo{
    public void add(){
        // 锁定当前实例
        synchronized(this){
        }    
        // 全局锁
        synchronized(SynDemo.class){
            
        }
    }
    // 全局锁
    public synchronized static void proc(){
        
    }
    public void test(){
        synchronized{
            //代码块
        }
    }
}



```



1. Synchronized是如何实现锁的

   偏向锁->轻量级锁->重量级锁，通过对象监视器机制实现的

   支持重入(比如synchronized关键字修饰的递归方法)，非公平锁

   - 自旋锁：避免频繁挂起唤醒而进行的优化

   ```java
   for(;;){
       // 在指定的时间内获取锁，失败则挂起等待
   }
   ```

   - 偏向锁

     绝大部分情况下，锁不仅不存在竞争，而且获得锁的都是同一个线程

   - 轻量级锁

     在没有多线程情况下，避免使用重量级锁

   - 重量级锁

     通过监视器实现ObjectMonitor

     monitorenter-》monitorexit

     CXQ队列：LIFO

     EntryList队列：

   

   通过编译后的字节码指令查看可知:javap -v Demo.class

   - 定义在方法上的synchronized关键字，会在方法的描述符中增加ACC_SYNCHRINIZED
   - 定义在代码块上的synchronized关键字，会在代码块进入前增加指令monitorenter，代码块结束后增加指令monitorexit的方式来实现的

2. 为什么所有对象都可以加锁

3. 锁存在哪个地方

   - 对象头，对应于JVM实现中的oop/oopDesc

### wait/notify

- wait和notify为什么要先获得锁？

wait

1. 释放当前对象锁
2. 是的当前线程进入等待队列（WaitSet）

notify

1. 从等待队列中取出一个等待线程，放到EntryList中，去竞争对象锁
2. notify调用的时候并不是释放锁，只有当monitorexit之后才会释放锁



- wait和sleep的区别？
- 

### CAS

- 使用unsafe类实现，调用的是JVM中的native方法实现的，最终应该是编译器层面指令CMXCHG指令的支持

- 使用锁时，线程获取锁是一种**悲观锁策略**，即假设每一次执行临界区代码都会产生冲突，所以当前线程获取到锁的时候同时也会阻塞其他线程获取该锁。
- 而CAS操作（又称为无锁操作）是一种**乐观锁策略**，它假设所有线程访问共享资源的时候不会出现冲突，既然不会出现冲突自然而然就不会阻塞其他线程的操作。因此，线程就不会出现阻塞停顿的状态。那么，如果出现冲突了怎么办？无锁操作是使用**CAS(compare and swap)**又叫做比较交换来鉴别线程是否出现冲突，出现冲突就重试当前操作直到没有冲突为止。

https://juejin.im/post/5ae6dc04f265da0ba351d3ff#heading-6



### Park&Unpark

是JVM层面提供的工具，也是通过调用unsafe中的native方法来实现par和unpark的

park : LockSupport.park()将线程挂起

unpark：LockSupport.unpark()唤醒线程



### AQS

**ReentrantLock、Semaphore、ReentrantReadWriteLock、**
**CountDownLatch和FutureTask。**





Abstract Queued Synchronizer

```java
Provides a framework for implementing blocking locks and related synchronizers (semaphores, events, etc) that rely on first-in-first-out (FIFO) wait queues.  This class is designed to be a useful basis for most kinds of synchronizers that rely on a single atomic {@code int} value to represent state. Subclasses must define the protected methods that change this state, and which define what that state means in terms of this object being acquired or released.  Given these, the other methods in this class carry out all queuing and blocking mechanics. Subclasses can maintain other state fields, but only the atomically updated {@code int} value manipulated using methods {@link #getState}, {@link #setState} and {@link #compareAndSetState} is tracked with respect to synchronization.

Subclasses should be defined as non-public internal helper classes that are used to implement the synchronization properties of their enclosing class.  Class {@code AbstractQueuedSynchronizer} does not implement any synchronization interface.  Instead it defines methods such as {@link #acquireInterruptibly} that can be invoked as appropriate by concrete locks and related synchronizers to implement their public methods.
	
```

#### 基本特性

- 同步器是用来构建锁和其他同步组件的基础框架，它的实现主要依赖一个int成员变量state来表示同步状态以及通过一个FIFO队列构成等待队列。

- 它的**子类必须重写AQS的几个protected修饰的用来改变同步状态的方法**，其他方法主要是实现了排队和阻塞机制。**状态的更新使用getState,setState以及compareAndSetState这三个方法**。

- 子类被**推荐定义为自定义同步组件的静态内部类**，同步器自身没有实现任何同步接口，它仅仅是定义了若干同步状态的获取和释放方法来供自定义同步组件的使用，同步器既支持独占式获取同步状态，也可以支持共享式获取同步状态，这样就可以方便的实现不同类型的同步组件。

- 同步器是实现锁（也可以是任意同步组件）的关键，在锁的实现中聚合同步器，利用同步器实现锁的语义。可以这样理解二者的关系：**锁是面向使用者，它定义了使用者与锁交互的接口，隐藏了实现细节；同步器是面向锁的实现者，它简化了锁的实现方式，屏蔽了同步状态的管理，线程的排队，等待和唤醒等底层操作**。锁和同步器很好的隔离了使用者和实现者所需关注的领域。

https://juejin.im/post/5aeb07ab6fb9a07ac36350c8

- 独占锁ReentrantLock
- 共享锁ReentrantWriteReadLock

#### 公平锁和非公平锁

- 默认构造是非公平锁，公平锁构造的时候，构造函数参数传递true
- 公平锁，在调用lock的时候，是直接调用acquire方法。
- 非公平锁是先调用compareAndSetState方法尝试去设置锁状态，成功则lock成功，当前线程设置锁独占线程，失败则会继续调用acquire方法（同公平锁）



#### AQS队列数据结构

- Node
- head node
- tail node
- enq方法
- compareAndSetHead方法
- compareAndSetTail方法



#### AQS同步器可重写的方法

```java
	@Override
// 独占式获取同步状态，实现该方法需要查询当前状态并判断同步状态是否符合预期，然后进行CAS操作设置同步状态
    protected boolean tryAcquire(int arg) {
        return super.tryAcquire(arg);
    }
    @Override
// 独占式释放同步状态，等待获取同步状态的线程将有机会获取同步状态
    protected boolean tryRelease(int arg) {
        return super.tryRelease(arg);
    }
// 共享式获取同步状态，返回大于等于0的值，表示获取成功，负责获取失败
	@Override
    protected int tryAcquireShared(int arg) {
        return super.tryAcquireShared(arg);
    }
// 共享式释放同步状态
    @Override
    protected boolean tryReleaseShared(int arg) {
        return super.tryReleaseShared(arg);
    }
// 表示是否被当前线程所独占
    @Override
    protected boolean isHeldExclusively() {
        return super.isHeldExclusively();
    }
```



#### AQS同步器已经实现的模板方法

```
void acquire(int arg);
void acquireInterruptibly(int arg);
boolean tryAcquireNanos(int arg, long nanos);
void acquireShared(int arg);
void acquireSharedInterruptibly(int arg);
boolean tryAcquireSharedNanos(int arg, long nanos);
boolean release(int arg);
Colletion<Thread> getQueuedThreads();

```





### Unsafe

提供的大量native方法。

### J.U.C并发包java.util.concurrent包

#### Atomic

- AtomicInteger

#### Lock接口的使用

- LockSupport

  - 提供了基本的操作线程的静态方法

    park() : 阻塞当前线程

    unpark(Thread thread) ：唤醒处于阻塞状态的线程

- ReentrantLock：可重入锁，独占锁

- ReentrantReadWriteLock：重入读写锁，读锁共享，写锁独占

  - 特性

  1. 公平性选择：支持公平和非公平两种，吞吐量还是非公平优于公平
  2. 重进入：读线程获取读锁之后能够继续获取读锁，写线程获取写锁之后能够再次获取写锁，也能获取读锁
  3. 降级性：遵循获取写锁，获取读锁，释放写锁，释放读锁顺序。写锁能够降级为读锁。

  - 读写状态的设计

  1. 一个32位int变量，高16位表示读状态，低16位表示写状态。
  2. 写状态获取：S&0x0000FFFF（高位抹去），写状态自增：直接S+1就可以
  3. 读状态获取：S>>>16位，读状态自增：S+(1<<<16)S加上1左移16位的值
  4. 写锁的获取：
     - 如果当前读锁存在，获取失败：为了保证写锁的操作对读锁可见
     - 如果当前写锁存在，并且获取锁的线程不是当前线程，获取失败

  5. 读锁的获取：

     - 读状态保存的是所有线程读锁次数总和。
     - 获取当前线程读锁次数方法getHoldCount，每个线程各自获取读锁的次数维护在ThreadLocal中。

     ```java
             /**
              * ThreadLocal subclass. Easiest to explicitly define for sake
              * of deserialization mechanics.
              */
             static final class ThreadLocalHoldCounter
                 extends ThreadLocal<HoldCounter> {
                 public HoldCounter initialValue() {
                     return new HoldCounter();
                 }
             }
             /**
              * The number of reentrant read locks held by current thread.
              * Initialized only in constructor and readObject.
              * Removed whenever a thread's read hold count drops to 0.
              */
             private transient ThreadLocalHoldCounter readHolds;
     ```

  6. 锁降级

     - 写锁降级为读锁。如果当前线程用有写锁，释放写锁，再拥有读锁，这个过程不是锁降级。降级指的是当前线程获得写锁，再获取读锁，释放写锁，再释放读锁的过程。

     - 为什么第二次的读锁要获取？

       如果不获取则不能保证数据的可见性，别的写线程更新的数据，对当前读线程不可见

     - 为什么第一次的写锁不再最后释放呢？

       写操作执行完后立即释放，可以最大限度的保证吞吐量，提高读的并发量。

#### lock和Condition

##### 需要和Lock搭配一起使用

- 本质上是提供的JDK层面的wait/notify工具，可以由程序去控制
- 和synchronized和wait+notify没有太大区别，只不过这种方式是JVM层面提供的，无法自行控制lock和unlock

##### Object的监视器方法实现(synchronized wait notify)/Condition(lock await signal)接口实现

<img src=".\object-monitor-codition.png" alt="object-monitor-condition" style="zoom:80%;" />

##### Condition的实现分析

- 每个ConditionObject都市AQS的一个内部类
- 每个conditionObject对象都包含一个等待队列，是实现等待/通知的关键
- 和AQS共用节点结构AQS.Node
- 等待队列是一个FIFO队列，拥有首节点firstWaiter和尾节点lastWaiter
- 同步队列与等待队列

<img src=".\同步队列与等待队列.png" alt="同步队列与等待队列" style="zoom:80%;" />

- await过程

<img src=".\condition的await过程.png" alt="condition的await过程" style="zoom:80%;" />

- signal过程

<img src=".\condition的signal过程.png" alt="condition的signal过程" style="zoom:80%;" />

#### CountDownLatch

是通过AQS实现的

会比较经常使用的工具，计数倒计时



#### Semaphore：信号量

主要应用是限流，和CountDownLath类似，也是使用AQS



### 阻塞队列

- LinkedBlockingQueue

- SynchronousQueue



### Fork/Join操作





### java中的线程池及Exector框架

避免线程的重复创建，有限流作用

#### 为什么要使用线程池？

1. 降低资源的消耗：通过重复利用已经创建的线程，降低线程创建和销毁带来的消耗
2. 提高响应速度：当任务到达时，不需要等待线程创建就能立即执行
3. 提高线程的可管理性：线程是稀缺资源，可以统一分配，调优和监控

#### 任务task和线程thread有什么区别



#### Exectors提供的静态方法

- newFixedThreadPool ： 创建固定线程数的线程池

队列使用的是无界队列LinkedBlockingQuue

```
return new ThreadPoolExecutor(nThreads, nThreads,
                              0L, TimeUnit.MILLISECONDS,
                              new LinkedBlockingQueue<Runnable>());
```

- newCachedThreadPool ： 核心线程数0，最大线程数整型最大值

1. 大小无界的线程池，适用于很多的短期异步任务的小程序
2. 空线程等待任务最长时间为60s，超过将会被终止
3. 主线程的offer必须有与之对应的空线程进行poll操作时才会成功，反之亦然。如果没有空线程则创建新线程执行poll操作
4. SynchronousQueue是没有容量的队列:一个不存储元素的阻塞队列

```
return new ThreadPoolExecutor(0, Integer.MAX_VALUE,
                              60L, TimeUnit.SECONDS,
                              new SynchronousQueue<Runnable>());
```

- newSingleThreadScheduledExecutor：单个周期任务

适用于1个后台线程执行周期任务，同时需要保证顺序的执行各个任务的场景

- newScheduledThreadPool ： 创建周期任务的线程池

1. 适用于多个后台线程执行周期任务，同时需要限制后天线程数量的场景

2. 在给定的延迟之后执行任务或者定期执行任务

```java
return new ThreadPoolExecutor(corePoolSize, Integer.MAX_VALUE, 0, NANOSECONDS,
      new DelayedWorkQueue());
```

3. ScheduledThreadPool运行机制
   - 

生成**ThreadPoolExecutor**实例的构造方法参数：

```
   public ThreadPoolExecutor(
	   int corePoolSize,--核心线程数
       int maximumPoolSize,--最大线程数
       long keepAliveTime,--超出核心线程以外的其余空闲线程的最大存活时间
       TimeUnit unit,--存活时间单位
       BlockingQueue<Runnable> workQueue,--阻塞队列
       ThreadFactory threadFactory,--指定线程工厂类
       RejectedExecutionHandler handler--被reject之后的handler，涉及到reject policy
   ) {}
```



#### 主要类接口关系

- Executor接口：顶层可执行接口，只有一个方法：execute()方法

  

- ExecutorService接口，继承自Executor接口，扩展了常用的方法

- ScheduledExecutorService接口，继承ExecutorService，扩展了定时计划的功能，添加了schedule相关方法

- AbstractExecutorService实现类，实现了ExecutorService接口主要方法



- **ThreadPoolExecutor**实现类，继承了AbstractExecutorService
- ScheduledThreadPoolExecutor实现了ScheduledExecutorService接口，基础的线程池的功能继承自ThreadPoolExecutor实现类
  1. 利用场景有dubbo中的心跳实现

- Executors类，juc提供的用于生成常用线程池的工厂类，通过调用静态方法



#### 异步计算的结果

- Future接口
- Future接口的实现类FutureTask

1. FutureTask即实现了Future接口，也实现了Runnable接口，包含的状态如下

   - 未启动状态
   - 已启动
   - 已完成（正常结束，取消而结束，异常而结束）

   

2. get方法的调用

   - 当FutureTask处于未启动或者已启动状态时，调用get方法将导致调用线程阻塞
   - 当FutureTask处于已完成状态时，执行get方法将会立即返回结果或抛出异常
   - ScheduledFutureTask与FutureTask





#### 线程拒绝策略

- AbortPolicy ：抛出异常给主线程
- CallerRunsPolicy ：只用调用者所在的线程处理
- DiscardOldestPolicy ：丢弃最老的线程
- DiscardPolicy ：直接丢弃

#### 线程池的设置需考虑问题

- 任务属于那种类型
  - CPU密集型 ： 线程数尽量小
  - IO密集型 ： 按照CPU核心数的倍数去设置
  - 混合型

- 任务执行时间 ：
- 队列的选择和队列大小

#### 线程池的监控

默认没有提供监控工具，但是提供了对应的API，可以自行扩展（重写对应方法，调用相关API、获取线程信息，上传到DB中作为监控分析的数据源）



#### 常见问题集

- synchronized个lock方式有啥不同？
  1. synchronized是jvm层面的关键字，lock是jdk层面提供的api
  2. synchronized是自动加锁和释放锁，程序不可控制；lock可以控制何时加锁lock，释放锁unlock
  3. synchronized是非公平锁，lock可以自由选择使用公平锁或者非公平锁

- ReentrantLock重入读写锁的使用？

- 在都多写少的场景下，读写锁的性能要好于排它锁。一般的锁都是排它锁
  1. 是共享锁，同一时刻可以存在多个锁。
  2. 存在读锁和写锁，

- 同步队列有哪些？

  - synchronized+wait+notify：cxq/entrylist队列，waitset队列

  - lock+condition：

    AQS队列：

    （lock->将当前线程封装成node，加入到AQS队列中）

    （await->将节点放入到condition队列，调用park，阻塞当前线程，释放锁）

    condition队列：

    （新的线程lock->将当前线程封装成node，加入到AQS队列中）

    (新的线程调用signal->从等待队列进入AQS队列，可以抢锁)



