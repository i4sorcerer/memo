## postgresql深入浅出

### 简介



### 一个事务tx1回滚或者提交之后，事务tx1还存在吗？

使用mq作为消息中间件时，当业务逻辑中事务TX001出现异常回滚之后，消息再次被接收处理的时候，还是使用TX001这个事务？或者说是心创建一个TX002？

- 个人判断应该是倾向TX001，因为根据附录2所表示的问题，第一次执行报错，rollback之后第二次执行时候，后续db操作是可以正常结束的。









### 与mysql相比优缺点
1.postgresql功能强大：
	1）支持所有主流的多表连接查询方式（nest loop，hash join，sort merge join）★★★★
	2）支持绝大多数的sql语法
		①可以使用PL/PGSQL写存储过程，也可以使用Python语言的PL/Python写
	3）性能优化工具和度量信息丰富
		①支持在线建索引（在线DDL），建索引时并不会锁表更新★★
	4）从9.1开始，支持同步复制功能（synchronous replication），
		通过master和slave之间的复制可以实现零数据丢失的高可用方案
	5）支持移动互联网时代的新功能：空间索引 ★★
		地理位置检索需求，附近的景点，附近的店铺等等。

### 附录1
1. 多表之间的连接主要有以上三种方式：（以oracle为例说明）
   https://blog.csdn.net/tianlesoftware/article/details/5826546
   		①Nested loops
   			工作方式是从一张表中读取数据，访问另一张表来做匹配（通常带有索引）
   			使用场合是当一个关联表比较小的时候，效率更高。
   			（小表与另一个带有索引的表结合时使用）
   		②Hash join（大数据连接是常用的方式）
   			工作方式是先将一个表（小表）做hash运算，将列数据存储到hash表中，从另一个表中抽取记录做hash运算，
   			到hash表找相应的值做匹配
   		③Merge join
   			工作方式是将关联表的关联列各自排序，然后从各自的排序表中抽取数据，到另一个排序表中做匹配。
   			需要做更多的排序，因此消耗更多的资源。能够使用merge join的地方，hash join都能发挥很好的性能。



2. postgresql使用时异常信息
   Error：current transaction is aborted, commands is ignored until end of transcation block.
   原因是：在PG数据库中，在关闭了自动提交的情况下，同一个事务中，如果某一个数据库操作出错，那么当前事务的后续任何数据库操作都会报错。这个时候只能是rollback或者commit。





