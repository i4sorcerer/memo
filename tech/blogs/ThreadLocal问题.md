

### ThreadLocal问题

Java中ThreadLocal是如何保证线程安全的

#### 结论

1. **ThreadLocal<T>变量通常定义为静态变量 private static final **
2. 每次调用get方法时，如果当前map中不存在当前线程的key，那么就会调用initialValue方法设定一个初始化
3. 

#### 实现多线程安全的关键

1. get方法

```
/**
 * Returns the value in the current thread's copy of this
 * thread-local variable.  If the variable has no value for the
 * current thread, it is first initialized to the value returned
 * by an invocation of the {@link #initialValue} method.
 * 返回当前线程的此ThreadLocal拷贝变量的值
 * @return the current thread's value of this thread-local
 *  返回当前线程的此ThreadLocal实例的值
 */
public T get() {
	// 获取当前调用get方法的线程对象t
    Thread t = Thread.currentThread();
    // 获取当前线程的ThreadLocalMap对象
    // 获取当前线程的所有本地线程变量threadLocals（ThreadLocalMap对象）
    ThreadLocalMap map = getMap(t);
    // 如果当前线程不存在本地线程变量，或者有本地线程变量但从未调用过set方法，则返回null
    if (map != null) {
        // 从当前threadLocals变量中取出当前ThreadLocal对象为key的Entry
        // 此Map是自定义的Map
        ThreadLocalMap.Entry e = map.getEntry(this);
        if (e != null) {
            @SuppressWarnings("unchecked")
            T result = (T)e.value;
            return result;
        }
    }
    // 本地线程变量threadLocals is null时，将初始时值设置到本地变量中，并将此初期值返回
    // 如果当前ThreadLocal的get方法先调用时，entry为null，也是设置初始值，并将其返回。
    return setInitialValue();
}

/**
 * Get the map associated with a ThreadLocal. Overridden in
 * InheritableThreadLocal.
 *
 * @param  t the current thread
 * @return the map
 */
ThreadLocalMap getMap(Thread t) {
    return t.threadLocals;
}
```

2. set方法

```java
/**
 * Sets the current thread's copy of this thread-local variable
 * to the specified value.  Most subclasses will have no need to
 * override this method, relying solely on the {@link #initialValue}
 * method to set the values of thread-locals.
 * 给当前线程的ThreadLocal变量的拷贝设置指定的值
 * @param value the value to be stored in the current thread's copy of
 *        this thread-local.
 */
public void set(T value) {
    // 获取当前线程
    Thread t = Thread.currentThread();
    // 获取当前线程的所有本地线程变量threadLocals（ThreadLocalMap对象）
    ThreadLocalMap map = getMap(t);
    // 如果当前map已经创建不为null，则设置指定的值
    if (map != null)
        map.set(this, value);
    else
        // 如果当前map为null则创建新的map对象，并且赋值给当前线程的threadLocals变量
        createMap(t, value);
}
```

3. remove方法

```java
/**
 * Removes the current thread's value for this thread-local
 * variable.  If this thread-local variable is subsequently
 * {@linkplain #get read} by the current thread, its value will be
 * reinitialized by invoking its {@link #initialValue} method,
 * unless its value is {@linkplain #set set} by the current thread
 * in the interim.  This may result in multiple invocations of the
 * {@code initialValue} method in the current thread.
 * 类似于HashMap的remove方法，将指定的key记录进行删除
 * @since 1.5
 */
 public void remove() {
     ThreadLocalMap m = getMap(Thread.currentThread());
     if (m != null)
         m.remove(this);
 }
```

**那么问题就来了，ThreadLocal变量使用完了之后需要特意调用remove方法吗？**

友情解答: 

- 如果T是基本类型，或者基本类型的集合类型，则一般不用考虑此问题

- 如果是自定义class类型，有可能造成内存泄露

  

4. **ThreadLocal.ThreadLocalMap内部类**

5. Thread类中的两个变量
   当前线程的所有ThreadLocal变量都存储在此threadLocals变量中

```
/* ThreadLocal values pertaining to this thread. This map is maintained
 * by the ThreadLocal class. */
ThreadLocal.ThreadLocalMap threadLocals = null;
```

从父类继承过来的值，在Thread初始化时候进行赋值

```
/*
 * InheritableThreadLocal values pertaining to this thread. This map is
 * maintained by the InheritableThreadLocal class.
 */
ThreadLocal.ThreadLocalMap inheritableThreadLocals = null;
```





以下内容仅供参考：

1. 根源不在ThreadLocal类，而是在于Thread类中的threadLocals成员变量。该变量用来保存线程自己的变量，ThreadLocal.threadLoclMap类型的。
2.ThreadLocal类️是用来操作（get，set，create，remove等）线程的threadLocals成员变量的。️是作为ThreadLocalMap的key来使用。
3.ThreadLocal类型的变量，一定要在使用完后，或者线程结束后调用remove方法来释放threadLocals成员变量。否则在线程池的情况下，因为线程并没有真正销毁，线程的成员变量始终是有效的，不会被gc回收。
2. 

