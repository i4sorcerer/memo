##  ConcurrentHashMap与HashMap使用比较

#### HashMap在多线程环境下的问题

1. 多线程环境下，使用Hashmap进行put操作会引起死循环，导致CPU利用率接近100%，所以在并发情况下不能使用HashMap。虽然已经有一个线程安全的HashTable，但是HashTable容器使用synchronized（他的get和put方法的实现代码如下）来保证线程安全，在线程竞争激烈的情况下HashTable的效率非常低下。因为当一个线程访问HashTable的同步方法时，访问其他同步方法的线程就可能会进入阻塞或者轮训状态。
   如线程1使用put进行添加元素，线程2不但不能使用put方法添加元素，并且也不能使用get方法来获取元素，所以竞争越激烈效率越低。
2. ConcurrentHashMap和普通的hashmap有啥区别。可以在任何场合代替HashMap吗？
   1. 是线程安全的，普通的hashmap不安全。hashtable是线程安全（Synchronized）
   2. 效率要比hashmap高效（多线程扩容等）
   3. 和hashmap一样，当size超过阈值时，会扩容并且结构会变成红黑树
   4. hashmap的key和value都可以设置为null，ConcurrentHashMap和hashtable都是不可以的
   5. 和hashmap一样内部结构使用了数组，链表，红黑树
   结论：在多线程的环境下，应当优先选用线程安全且高效的ConcurrentHashMap。
