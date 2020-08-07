### AQS源码分析

#### 获取同步状态acquire方法

```java
/**
 * Acquires in exclusive mode, ignoring interrupts.  Implemented
 * by invoking at least once {@link #tryAcquire},
 * returning on success.  Otherwise the thread is queued, possibly
 * repeatedly blocking and unblocking, invoking {@link
 * #tryAcquire} until success.  This method can be used
 * to implement method {@link Lock#lock}.
 *
 * @param arg the acquire argument.  This value is conveyed to
 *        {@link #tryAcquire} but is otherwise uninterpreted and
 *        can represent anything you like.
 */
public final void acquire(int arg) {
    if (!tryAcquire(arg) &&
        acquireQueued(addWaiter(Node.EXCLUSIVE), arg))
        selfInterrupt();
}
```



#####  同步获取失败，添加等待节点方法addWaiter

```java
/**
 * Creates and enqueues node for current thread and given mode.
 // 根据当前的线程以及跟定的mode来创建和插入节点
 // AQS提供两种获取同步状态的方式
 1. 独占式：Node.EXCLUSIVE
 2. 共享式：Node.SHARED
 *
 * @param mode Node.EXCLUSIVE for exclusive, Node.SHARED for shared
 // 同步mode
 * @return the new node
 // 返回一个待加入队列中的新节点
 */
private Node addWaiter(Node mode) {
    Node node = new Node(Thread.currentThread(), mode);
    // Try the fast path of enq; backup to full enq on failure
    // 快速尝试在尾部添加
    Node pred = tail;
    if (pred != null) {
        node.prev = pred;
        if (compareAndSetTail(pred, node)) {
            pred.next = node;
            return node;
        }
    }
    enq(node);
    return node;
}

    /**
     * Inserts node into queue, initializing if necessary. See picture above.
     // 向队列中插入新节点，需要初始化则进行初始化操作
     
     * @param node the node to insert
     * @return node's predecessor
     // 返回结果是插入节点的前继节点
     */
    private Node enq(final Node node) {
        for (;;) {
            Node t = tail;
            if (t == null) { // Must initialize
                if (compareAndSetHead(new Node()))
                    tail = head;
            } else {
                node.prev = t;
                if (compareAndSetTail(t, node)) {
                    t.next = node;
                    return t;
                }
            }
        }
    }

```



##### 节点自旋等待的方法acquireQueued

```java
/**
 * Acquires in exclusive uninterruptible mode for thread already in
 * queue. Used by condition wait methods as well as acquire.
 *
 // 对已经进入队列中的线程采用独占式非中断的抢占同步状态。
 // 在condition中的wait方法调用，同时acquire也调用了
 
 * @param node the node
 * @param arg the acquire argument
 * @return {@code true} if interrupted while waiting
 */
final boolean acquireQueued(final Node node, int arg) {
    boolean failed = true;
    try {
        boolean interrupted = false;
        for (;;) {
            // 如果是head节点之后的第一个节点，就去尝试获取同步状态
            final Node p = node.predecessor();
// 这里表明：
            // 1. 只有头结点的下一个节点才有资格去竞争同步状态
            if (p == head && tryAcquire(arg)) {
             // 因为只有一个线程可以成功获取同步状态，因此此处的setHead无需使用CAS操作，即可保证线程安全 
                setHead(node);
                p.next = null; // help GC
                failed = false;
                return interrupted;
            }
            if (shouldParkAfterFailedAcquire(p, node) &&
                parkAndCheckInterrupt())
                // 如果当前节点可以执行park操作，则先park，再返回是否处于中断状态
                interrupted = true;
        }
    } finally {
        if (failed)
            cancelAcquire(node);
    }
}
```



##### 同步状态获取失败之后，判断是否应当park的方法shouldParkAfterFailedAcquire

```java
/**
 * Checks and updates status for a node that failed to acquire.
 * Returns true if thread should block. This is the main signal
 * control in all acquire loops.  Requires that pred == node.prev.
 *
 // 检查并且更新没有成功获得同步状态的节点的waitStatus。
 // 如果线程应当被阻塞则返回true。这个方法是在所有的acquire循环中主要的信号控制环节。
 // 前提条件是传进来的参数pred == node.prev。
 
 * @param pred node's predecessor holding status
 * @param node the node
 * @return {@code true} if thread should block
 */
private static boolean shouldParkAfterFailedAcquire(Node pred, Node node) {
    int ws = pred.waitStatus;
    if (ws == Node.SIGNAL)
        /*
         * This node has already set status asking a release
         * to signal it, so it can safely park.
         */
        return true;
    if (ws > 0) {
        /*
         * Predecessor was cancelled. Skip over predecessors and
         * indicate retry.
         */
// 这里写法精妙绝伦。
        // 前任被取消并且进行retry处理，跳过所有被取消的前任。
        do {
            node.prev = pred = pred.prev;
        } while (pred.waitStatus > 0);
        pred.next = node;

    } else {
        /*
         * waitStatus must be 0 or PROPAGATE.  Indicate that we
         * need a signal, but don't park yet.  Caller will need to
         * retry to make sure it cannot acquire before parking.
         */
        compareAndSetWaitStatus(pred, ws, Node.SIGNAL);
    }
    return false;
}
```



#### 释放同步状态的release方法

```java
/**
 * Releases in exclusive mode.  Implemented by unblocking one or
 * more threads if {@link #tryRelease} returns true.
 * This method can be used to implement method {@link Lock#unlock}.
 *
 * @param arg the release argument.  This value is conveyed to
 *        {@link #tryRelease} but is otherwise uninterpreted and
 *        can represent anything you like.
 * @return the value returned from {@link #tryRelease}
 */
public final boolean release(int arg) {
    // 调用子类的重写方法尝试获取同步状态
    // 获取成功后，则unpark后记线程
    if (tryRelease(arg)) {
        Node h = head;
        if (h != null && h.waitStatus != 0)
            unparkSuccessor(h);
        return true;
    }
    return false;
}
```



##### 同步状态释放方法tryRelease方法

```java
// 空方法，需要子类重写此方法
protected boolean tryRelease(int arg) {
    throw new UnsupportedOperationException();
}
```



##### 后继线程的唤醒方法unpark

```java
/**
 * Wakes up node's successor, if one exists.
 *
 // 唤醒后继线程，如果存在
 
 * @param node the node
 */
private void unparkSuccessor(Node node) {
    /*
     * If status is negative (i.e., possibly needing signal) try
     * to clear in anticipation of signalling.  It is OK if this
     * fails or if status is changed by waiting thread.
     */
    int ws = node.waitStatus;
    if (ws < 0)
        compareAndSetWaitStatus(node, ws, 0);

    /*
     * Thread to unpark is held in successor, which is normally
     * just the next node.  But if cancelled or apparently null,
     * traverse backwards from tail to find the actual
     * non-cancelled successor.
     */
    Node s = node.next;
    if (s == null || s.waitStatus > 0) {
        s = null;
        for (Node t = tail; t != null && t != node; t = t.prev)
            if (t.waitStatus <= 0)
                s = t;
    }
    // 如果后继线程不为null，则直接调用LockSupport.unpark方法唤醒节点线程
    if (s != null)
        LockSupport.unpark(s.thread);
}
```



#### 获取共享状态的acquireShared方法

- **tryAcquireShared方法返回值<0时表示同步状态获取失败，或当前资源数不足，需自旋等待**
- **tryAcquireShared方法返回值>=0时表示同步状态获取成功，或当前资源数充足，不需自旋等待**

```java
/**
 * Acquires in shared mode, ignoring interrupts.  Implemented by
 * first invoking at least once {@link #tryAcquireShared},
 * returning on success.  Otherwise the thread is queued, possibly
 * repeatedly blocking and unblocking, invoking {@link
 * #tryAcquireShared} until success.
 *
 * @param arg the acquire argument.  This value is conveyed to
 *        {@link #tryAcquireShared} but is otherwise uninterpreted
 *        and can represent anything you like.
 */
public final void acquireShared(int arg) {
    if (tryAcquireShared(arg) < 0)
        doAcquireShared(arg);
}
```



#### 获取共享状态失败，自选等待doAcquireShared方法

```java
/**
 * Acquires in shared uninterruptible mode.
// 以共享的非中断的方式获取同步状态或者资源数

 * @param arg the acquire argument
 */
private void doAcquireShared(int arg) {
    final Node node = addWaiter(Node.SHARED);
    boolean failed = true;
    try {
        boolean interrupted = false;
        for (;;) {
            final Node p = node.predecessor();
            if (p == head) {
                int r = tryAcquireShared(arg);
                if (r >= 0) {
                    setHeadAndPropagate(node, r);
                    p.next = null; // help GC
                    if (interrupted)
                        selfInterrupt();
                    failed = false;
                    return;
                }
            }
            if (shouldParkAfterFailedAcquire(p, node) &&
                parkAndCheckInterrupt())
                interrupted = true;
        }
    } finally {
        if (failed)
            cancelAcquire(node);
    }
}
```



#### 共享同步状态释放releaseShared方法

```java
/**
 * Releases in shared mode.  Implemented by unblocking one or more
 * threads if {@link #tryReleaseShared} returns true.
 *
 * @param arg the release argument.  This value is conveyed to
 *        {@link #tryReleaseShared} but is otherwise uninterpreted
 *        and can represent anything you like.
 * @return the value returned from {@link #tryReleaseShared}
 */
public final boolean releaseShared(int arg) {
// 共享式释放的时候必须保证线程安全的更改同步状态（资源数）
    if (tryReleaseShared(arg)) {
        doReleaseShared();
        return true;
    }
    return false;
}
```

