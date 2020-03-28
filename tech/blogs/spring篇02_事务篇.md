## Spring篇02_事务篇

参考Spring源码分析第二版第三章内容整理

### 事务基本特点

事务Transaction是访问并可能更新数据库中各项数据的一个程序执行单元。

具有ACID特性：

1. 原子性（Atomicity）：一个事务，不可分割的工作单元，诸操作，要么都做，要么都不做。
2. 一致性（Consistency）：使数据库从一个一致性状态到另一个一致性状态。
3. 隔离性（Isolation）：不被其他事务干扰，事务内部的操作及数据对其他并发执行的事务是隔离的，互不干扰
4. 持久性（Durability）：事务一旦提交，对数据库的改变就是永久的。

### 事务基本原理

1. Spring事务本质是数据库产品对事务的支持，没有数据库事务的支持，Spring

是无法实现事务的。

2. 数据库层真正的事务提交和回滚是通过binlog或者redo log来实现的。
3. 本质上数据库的连接就是Java里的TCP协议的Socket连接的实现。同理，事务的实现也是通过对Socket的操作来实现的。



### Java为实现事务功能提供哪些接口

1. Connection
2. Datasource
3. DefaultTransactionStatus（？）
4. TransactionDefinition（？）
5. 

### Spring实现事务管理类

1. DatasourceTractionManager事务管理类
2. DatasourceTractionManager.DatasourceTractionObject静态内部类（内部的ConnectionHolder类可以获取不同数据库的连接，通过获取的Connection实现类来实现begin，commit，rollback等操作。这些实现类都是由各自数据库厂商实现并提供的。）
3. ChainedTractionManager
4. PlatformTransactionManager
5. 

### Spring中通过注解自动实现事务的支持











