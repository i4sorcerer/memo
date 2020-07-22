## Spring5框架之Spring-tx

参考链接：http://www.codeceo.com/article/spring-transactions.html

- Spring 事务的本质其实就是数据库对事务的支持， 没有数据库的事务支持， spring 是无法提供事务功
  能的。   

### 事务的基本特性ACID

- 原子性
- 一致性
- 隔离性
- 持久性

### Spring事务的传播属性

- **PROPAGATION_REQUIRED**
- **PROPAGATION_REQUIRES_NEW**
- **PROPAGATION_SUPPORTS**
- PROPAGATION_MANDATORY
- PROPAGATION_NOT_SUPPORTED
- PROPAGATION_NEVER
- **PROPAGATION_NESTED**

```
问题1：
上面的NEW和NESTED最终结果不一样吗？
//外层事务
1 methodA(){
try{
// 内层事务
2  methodB();
}catch(Exception){
 //处理
}
}
NEW：
	2commit，1也可能回滚，不影响1的commit结果
	2rollback,1也可commit，也可rollback
NESTED：
	2commit，1也可能回滚，不影响1的commit结果？？？？
	2rollback,1也可commit，也可rollback

```



### Spring事务的隔离级别

- ISOLATION_DEFAULT
- ISOLATION_READ_UNCOMMITTED
- ISOLATION_READ_COMMITTED
- ISOLATION_REPEATABLE_READ
- ISOLATION_SERIALIZABLE



### Spring中的@Transaction





### 浅谈分布式事务

特定在分布式系统中的事务，区别于传统的单机事务。一般做法是满足分区容错性，牺牲一部分的一致性，来换区系统过的高可用性，保证最终一致性。

#### CAP定律

- C: 一致性Consistency  
- A:可用性Availability  
- P:分区容错性Partition Tolerance  

#### 一致性方案

- 强一致性：当更新操作完成之后， 任何多个后续进程或者线程的访问都会返回最新的更新过的值。   
- 弱一致性：系统并不保证后续进程或者线程的访问都会返回最新的更新过的值。系统在数据写入成功之
  后， 不承诺立即可以读到最新写入的值， 也不会具体的承诺多久之后可以读到。牺牲掉一部分一致性，来换取系统的高可用性，只需保证最终一致性
- 最终一致性：弱一致性的一种形式。系统保证在没有后续更新的前提下， 系统最终返回上一次更新操作
  的值。   





### 

