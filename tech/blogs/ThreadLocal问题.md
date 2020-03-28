

### ThreadLocal问题

Java中ThreadLocal是如何保证线程安全的
1. 根源不在ThreadLocal类，而是在于Thread类中的threadLocals成员变量。该变量用来保存线程自己的变量，ThreadLocal.threadLoclMap类型的。
2.ThreadLocal类️是用来操作（get，set，create，remove等）线程的threadLocals成员变量的。️是作为ThreadLocalMap的key来使用。
3.ThreadLocal类型的变量，一定要在使用完后，或者线程结束后调用remove方法来释放threadLocals成员变量。否则在线程池的情况下，因为线程并没有真正销毁，线程的成员变量始终是有效的，不会被gc回收。
2. 