## ThreadPoolExector源码分析



#### ThreadPoolExecutor的execute方法：

```java
/**
 * Executes the given task sometime in the future.  The task
 * may execute in a new thread or in an existing pooled thread.
 这里注释写的很清楚，在未来的某个时刻执行指定的任务，而不是立即执行
任务可能是创建新的线程来执行，也可能是通过已经在池中的线程来执行。
 
 * If the task cannot be submitted for execution, either because this
 * executor has been shutdown or because its capacity has been reached,
 * the task is handled by the current {@code RejectedExecutionHandler}.
 如果任务不能被提交来执行，因executor已经被shutdown，或者因达到最大容量，或者因任务被reject了
 
 * @param command the task to execute 即将执行的task，就是一个实现了Runnable接口的实现类
 
 * @throws RejectedExecutionException at discretion of
 *         {@code RejectedExecutionHandler}, if the task
 *         cannot be accepted for execution
 如果线程被reject会抛出RejectedExecutionException
 * @throws NullPointerException if {@code command} is null
 如果task为null，抛出空指针异常NPE
 */
public void execute(Runnable command) {
    if (command == null)
        throw new NullPointerException();
    /*
     * Proceed in 3 steps:
     *
     * 1. If fewer than corePoolSize threads are running, try to
     * start a new thread with the given command as its first
     * task.  The call to addWorker atomically checks runState and
     * workerCount, and so prevents false alarms that would add
     * threads when it shouldn't, by returning false.
     *
     * 2. If a task can be successfully queued, then we still need
     * to double-check whether we should have added a thread
     * (because existing ones died since last checking) or that
     * the pool shut down since entry into this method. So we
     * recheck state and if necessary roll back the enqueuing if
     * stopped, or start a new thread if there are none.
     *
     * 3. If we cannot queue task, then we try to add a new
     * thread.  If it fails, we know we are shut down or saturated
     * and so reject the task.
     */
执行过程分为3个步骤
	1. 如果正在运行的线程数小于核心线程数，尝试创建新的线程，并将当前任务作为firstTask。其中在调用addWorker的时候，会自动check runState和workerCount
    
    
    int c = ctl.get();
    if (workerCountOf(c) < corePoolSize) {
        if (addWorker(command, true))
            return;
        c = ctl.get();
    }
    if (isRunning(c) && workQueue.offer(command)) {
        int recheck = ctl.get();
        if (! isRunning(recheck) && remove(command))
            reject(command);
        else if (workerCountOf(recheck) == 0)
            addWorker(null, false);
    }
    else if (!addWorker(command, false))
        reject(command);
}
```

#### 重要->线程池的runState:32位Integer的前29位存储

- RUNNING ：可接收新任务，可处理已经进入队列的任务
- SHUTDOWN ：不可接收新任务，可处理已经进入队列的任务
- STOP：不可接收新任务，不可处理已经进入队列的任务，中断正在执行中的任务
- TIDYING：所有任务都已经被终结，并且workCount是0
- TERMINATIED：终结完成的状态

#### 重要->工作队列的workCount：32位Integer的后3位存储

workCount也就是工作队列中当前的线程数



Worker内部类

```java
/**
 * Class Worker mainly maintains interrupt control state for
 * threads running tasks, along with other minor bookkeeping.
 * This class opportunistically extends AbstractQueuedSynchronizer
 * to simplify acquiring and releasing a lock surrounding each
 * task execution.  This protects against interrupts that are
 * intended to wake up a worker thread waiting for a task from
 * instead interrupting a task being run.  We implement a simple
 * non-reentrant mutual exclusion lock rather than use
 * ReentrantLock because we do not want worker tasks to be able to
 * reacquire the lock when they invoke pool control methods like
 * setCorePoolSize.  Additionally, to suppress interrupts until
 * the thread actually starts running tasks, we initialize lock
 * state to a negative value, and clear it upon start (in
 * runWorker).
 */
private final class Worker
    extends AbstractQueuedSynchronizer
    implements Runnable
{
```

