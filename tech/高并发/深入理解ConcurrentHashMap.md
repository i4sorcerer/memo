### 深入理解ConcurrentHashMap

#### 先知（事先知道）

- 线程安全的Map其实很简单，一种实现方式是所有共有方法加Synchronized关键字，其实HashTable就是此种方- 式实现的。
- ConcurrentHashMap是线程安全的同时又是高效的的HashMap，多线程环境下同时保证了并发性和安全性。

#### 为什么要使用ConcurrentHashMap？

- 多线程环境下使用HashMap进行put操作会导致死循环，cpu利用率接近100%
- 使用线程安全的HashTable又会使得效率低下（synchronized导致）

#### 如何提升并发效率的？

- 利用锁分段技术(jdk1.8以前)，数据分段，每个分段分配一把锁，访问不同段的数据时不存在竞争
- **CASE+Synchronized，抛弃了分段技术。**

#### 具体实现(分段锁技术忽略，以jdk1.8的实现为例)

