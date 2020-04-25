## Java基础篇01_java.lang.Thread类详解

### 基本概念

以下内容摘自官方api文档

注意点：

- Thread类本身就是实现Runnable接口的
- Thread本身有很多Native方法，而且java的Thread实现是依赖于操作系统内核的，因此此类事平台相关的。
- 

```
A thread is a thread of execution in a program. The Java Virtual Machine allows an application to have multiple threads of execution running concurrently.
Every thread has a priority. Threads with higher priority are executed in preference to threads with lower priority. Each thread may or may not also be marked as a daemon. When code running in some thread creates a new Thread object, the new thread has its priority initially set equal to the priority of the creating thread, and is a daemon thread if and only if the creating thread is a daemon.

When a Java Virtual Machine starts up, there is usually a single non-daemon thread (which typically calls the method named main of some designated class). The Java Virtual Machine continues to execute threads until either of the following occurs:

The exit method of class Runtime has been called and the security manager has permitted the exit operation to take place.
All threads that are not daemon threads have died, either by returning from the call to the run method or by throwing an exception that propagates beyond the run method.
There are two ways to create a new thread of execution. 
One is to declare a class to be a subclass of Thread. This subclass should override the run method of class Thread. An instance of the subclass can then be allocated and started. For example, a thread that computes primes larger than a stated value could be written as follows:
```

### 重要方法或变量

#### 7中构造方法的重载(Allocates a new thread object)

- **Thread（）**
- **Thread(Runnable target)**
- Thread(Runnable target, String name)
- **Thread(String name)**

- Thread(ThreadGroup group, Runnable target):

- Thread(ThreadGroup group, Runnable target, String name)

  Allocates a new `Thread` object so that it has `target` as its run object, has the specified `name` as its name, and belongs to the thread group referred to by `group`.

- Thread(ThreadGroup group, Runnable target, String name, long stackSize)

  has the specified stack size

- Thread(ThreadGroup group, String name)

#### public long getId() 方法

Returns the identifier of this Thread. The thread ID is a positive `long` number generated when this thread was created. The thread ID is unique and remains unchanged during its lifetime. When a thread is terminated, **this thread ID may be reused.**

**根据上面API文档内容，线程ID是可能会重复利用的，但是从源码中看，即便是线程终了或销毁了，线程ID也不会重复利用，会继续ID自增。参见方法：nextThreadID方法。**
**nextThreadID()方法是在线程init时候就自动调用并给tid赋值的。**

```java
    /* For generating thread ID */
    private static long threadSeqNumber;
    private static synchronized long nextThreadID() {
        // 这里明明是一直自增，会杀会说线程ID可重复利用呢？？？
        return ++threadSeqNumber;
    }
```

#### 大量使用native方法

```
private static native void registerNatives();

public static native Thread currentThread();
public static native void yield();
public static native void sleep(long millis) throws InterruptedException;
public final native boolean isAlive();
public static native boolean holdsLock(Object obj);

/* Some private helper methods */
private native void start0();
private native boolean isInterrupted(boolean ClearInterrupted);
private native static StackTraceElement[][] dumpThreads(Thread[] threads);
private native static Thread[] getThreads();
private native void setPriority0(int newPriority);
private native void stop0(Object o);
private native void suspend0();
private native void resume0();
private native void interrupt0();
private native void setNativeName(String name);
```



### 创建Thread的两种方法

1. 继承Thread类，实例化对象，调用start方法

```
class PrimeThread extends Thread {
         long minPrime;
         PrimeThread(long minPrime) {
             this.minPrime = minPrime;
         }

         public void run() {
             // compute primes larger than minPrime
              . . .
         }
     }
     
     PrimeThread p = new PrimeThread(143);
     p.start();     
```

2. 实现Runnable接口，作为参数传递给Thread的构造函数，调用实例start方法

```
     class PrimeRun implements Runnable {
         long minPrime;
         PrimeRun(long minPrime) {
             this.minPrime = minPrime;
         }

         public void run() {
             // compute primes larger than minPrime
              . . .
         }
     }
     PrimeRun p = new PrimeRun(143);
     new Thread(p).start();
    
```

### Java线程在虚拟机中是如何实现的

#### 进程与线程的概念

- 进程是资源分配单位（内存资源，文件资源等）
- 线程是操作系统独立调度的单位

#### 线程实现方式有哪些

因为java的线程是映射到操作系统原生线程上的，如果要阻塞或者唤醒一个线程，都需要系统调用，都需要从用户态-核心态的切换，都需要耗费较多的处理器时间，属于重量级操作。

1. 内核线程实现

2. 使用用户线程实现

3. 使用用户线程+轻量级进程LWP（light weight process）混合实现

   UT->LWP->KLT->CPU







