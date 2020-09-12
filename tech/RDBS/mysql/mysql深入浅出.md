### Mysql深入浅出之性能优化篇

#### 基础

- 什么是索引

  索引是为了加速对表中数据行的检索而创建的一种分散存储的数据结构

#### 索引使用的数据结构

##### 二叉树

###### 二叉树存在的问题

1. 数据如果是顺序的，则数据结构可能会变为链表，而不是二叉树，时间复杂度增加。

###### 平衡二叉树

- 平衡二叉树存在问题
  - 树太深，数据所处的高度决定IO次数
  - 数据量太小，每个节点/页保存的数据量太小
- 红黑树
  - 红黑树是一种平衡的二叉树

##### B树：多路平衡查找树

- 多路指的是多叉，有几个分叉，就是几路(3)
- 一个节点可以存储的关键字的个数是路数-1(3-1=2)
- 绝对平衡树

<img src="D:\sk\learn\git-repo\memo\tech\RDBS\mysql\多路平衡二叉树.png" alt="image-20200910161735484" style="zoom:80%;" />

##### B+树

- mysql中使用B+树，加强版的B树
- 路数是根据页大小，关键字大小而确定的？？？
- 枝节点不保存任何数据，只保存关键字和引用，所有数据都保存在叶子节点上
- 与B-TREE的区别
  1. B+节点关键字搜索采用闭合区间
  2. B+非叶子节点，不保存数据，只保存关键字和子节点的引用
  3. B+关键字对应的数据保存在叶子节点上
  4. B+叶子节点是顺序排列的，并且相邻节点具有顺序引用关系

#### mysql中索引的具体使用

##### 为什么要使用索引？

- 可以极大的减少存储引擎扫描数据量的大小
- 可以把随机IO变成顺序IO
- 可以帮助我们在分组，排序时使用临时表

- 索引是作用在表上的，可以在定义的时候指定存储引擎（->索引的最终实现者是存储引擎插件）

  show create table user;

  ```sql
  show create table user;
  
  | user  | CREATE TABLE `user` (
    `id` int(13) NOT NULL AUTO_INCREMENT COMMENT '??',
    `name` varchar(33) DEFAULT NULL COMMENT '??',
    `age` int(3) DEFAULT NULL COMMENT '??',
    `money` double DEFAULT NULL COMMENT '????',
    PRIMARY KEY (`id`)
  ) ENGINE=InnoDB AUTO_INCREMENT=525 DEFAULT CHARSET=utf8 | 
  ```

  查看mysql数据存储位置：

  ```sql
  mysql> show variables like 'datadir';
  +---------------+-------------------------------------+
  | Variable_name | Value                               |
  +---------------+-------------------------------------+
  | datadir       | /opt/rh/mysql55/root/var/lib/mysql/ | 
  +---------------+-------------------------------------+
  ```

  

  ##### innodb存储引擎

  - user.frm 文件：数据表的创建语句存储文件

  - user.ibd文件：以主键为索引来组织数据的存储（索引和数据时存储在一起的）

  - 主键是以聚集索引方式存储的
  - 如果没有显示指定主键，则默认创建6byte的隐式主键来存储数据
  - 聚集索引/聚簇索引：数据库表中数据的物理顺序与逻辑顺序一致
  - 辅助索引：存储的也是主键ID，最终还是要通过聚集索引来查询到特定的数据

  <img src="D:\sk\learn\git-repo\memo\tech\RDBS\mysql\innodb中B+树的体现.png" alt="image-20200910170750568" style="zoom:80%;" />





##### MYisam存储引擎

- user.frm文件 
- user.MYI文件 索引文件
- user.MYD文件 数据文件

##### CSV存储引擎

- frm文件
- CSV文件 数据存储，逗号隔开
- 不能建立索引
- 列不能为NULL
- 可以直接编译文件，通过命令flush table user，可以更新文件数据到表。
- 主要场景
  - 数据快速导入导出
  - 表格直接转换成CSV

##### Archive存储引擎

- user.frm
- user.ARZ 压缩文件方式存储数据
- 占用磁盘空间少
- 主要场景
  - DB备份
  - 日志系统
  - 大量的设备数据采集

##### memory存储引擎

- 生成临时表

#### mysql运行原理讲解

##### 列的离散性

- count(discount col):count(col)
- 离散性越高，选择性越好
- 离散性太差会是优化引擎有可能会选择全表扫描。

##### 最左匹配原则

- 关键字比对与排序规则设定有关

##### 联合索引

- 单列索引是特殊的联合索引
- 联合索引就是多个关键字联合一起，作为一个关键字
  - 经常用的列优先（最左匹配原则）
  - 离散度高的列优先（离散度高优先原则）
  - 宽度小的列优先（最小空间原则）

- 联合索引 indx_name_phonename(name,phonename)①, indx_name(name)② ：②的索引是冗余的，不用创建。根据最左匹配原则①是可以覆盖②的索引的。

##### 覆盖索引

- 如果查询的列可以通过索引关键字直接返回，则称之为覆盖索引
- 减少叶子节点的IO，将随机IO，变为顺序IO，极大提高查询性能
- 这也是禁止使用select *的一个原因，有可能命中覆盖索引。

##### 是否可以命中索引？

- 匹配列前缀可以用到索引 : like 'id99%'. 但是like '%id99%' 和like '%99id'都是不会使用索引的，最左匹配
- where not in 和 <> 无法使用索引
- 匹配范围值，order by 也可以用到索引
- 联合索引中，精确匹配最左列，范围匹配另一列，可以用到索引。
- 联合索引中，精确匹配最右列，范围匹配最左列，不可以用到索引。?????
  - 这里不会命中索引吗？
- in 和 or可以用到索引

#### mysql查询优化及查询执行路径

##### 客户端服务端通信

- 半双工：同一时间只能一方发送给另一方。对讲机

- 全双工：同一时间双方可以通信；打电话

- 连接状态

  show processlist;

  kill {id}可以杀掉连接

##### 查询缓存

- 缓存sql和查询结果（key是sql，必须完全一样）
- 查看是否开启缓存

```
mysql> show variables like 'query_%';
+------------------------------+---------+
| Variable_name                | Value   |
+------------------------------+---------+
| query_alloc_block_size       | 8192    | 
| query_cache_limit            | 1048576 | 
| query_cache_min_res_unit     | 4096    | 
| query_cache_size             | 0       | 
| query_cache_type             | ON      | 
| query_cache_wlock_invalidate | OFF     | 
| query_prealloc_size          | 8192    | 
+------------------------------+---------+
7 rows in set (0.00 sec)

```

- vi /etc/my.conf

  query_cache=0:关闭

  query_cache=1：开启

  query_cache=2：按需开启

- 查询缓存状态

  show status like 'Qcache%';

##### 查询优化处理

###### 解析sql语句，解析成解析树

###### 预处理阶段

###### 查询优化器

- 基于成本计算的原则
- 找到最优的执行计划的规则
  1. 使用等价变化规则
  2. 将可转换的外连接left join 查询转换成内连接inner join查询
  3. 优化count,min max函数
  4. 覆盖索引扫描
  5. 子查询优化：不需要子查询的情况，不使用子查询
  6. 提前终止查询
  7. IN的优化：mysql中in 和or是不一样的
     - or：针对条件中的每个值去比较 O(N)
     - in：先对条件中的值进行排序，再做二分查找O(logN)
  8. 禁止使用属性隐式转换 where phone =123 ;
     - 会导致全表扫描而不使用索引
  9. 禁止在where条件属性上使用表达式或函数，无法命中索引
     - where convert(date,'yyyymmdd')='2020-09-12' :NG
     - where date=convert('2020-09-12','yyyymmdd') :OK可以命中
  10. 禁止使用负向查询
      - NOT，！=，<>, not in not like 等等
      - %开头的会导致全表扫描
  11. 禁止大表使用join，禁止大表使用子查询
      - 会产生临时表，导致性能下降
  12. 禁止使用OR，必须使用IN条件
      - in二分查找优化

##### 查询执行引擎

###### 执行计划

- expain 查询语句 \G 可以查看sql的执行计划

- 每个指标含义
  1. id
     - id 表示执行顺序
     - id值大的先执行
  2. select _type
     - 查询类型，用来区分，普通查询、联合查询、子查询
  3. table
     - 查询作用在哪个表，子查询别名
  4. type（执行计划好坏的关键）
     下面的访问类型，是从好到坏
     - system :系统表，表中只有一行记录，可以忽略
     - const：通过索引一次就可以找到，用于比较主键和唯一键索引
     - eq_ref：对于每个索引键，表中只有一行记录预制匹配，用于比较主键和唯一键索引
     - ref：非唯一性索引，匹配某个值得所有行
     - range：只检索指定范围的行，使用一个索引来选择行
     - index：full index scan ,索引全表扫描。
     - all：full table scan,遍历全表找到匹配行
  5. possiable_key
     - 可能使用的key
  6. key
     - 实际执行时使用的key
  7. extra：十分重要的额外信息
     - Using  filesort :  使用了外部的文件排序，而不是使用表内的索引进行排序的；比较耗费性能
     - Using temporary:对查询结果进行排序时，使用了临时表。
     - Using index : 表明了使用覆盖索引covering index，避免访问了数据行，效率比较高
     - Using where :对于where条件进行过滤
     - Select tables optimized away :在查询执行计划生成阶段即可完优化。

##### 返回结果

- 增量的返回结果：开始生成第一条结果时，mysql就开始向请求方逐步返回数据。

#### 事务

##### 什么是事务

- 是数据库操作的做小单元，不可分割的操作集合

##### 满足ACID特性：

- A：原子性

- C：一致性

- I：隔离性

  - sql标准定义的几种隔离级别 select @@tx_isolation

    1. read uncommited 未提交度读（未做任何并发控制）

    2. read commited 提交读（解决脏读问题）

    3. repeatable read 重复读（innerdb引擎默认级别）（解决了不可重复读问题）

       innodb中同时也解决了幻读问题

    4. serializable 串行化，解决所有并发问题

  - 事务并发带来的问题？
    1. 脏读：
    2. 不可重复读
    3. 幻读

- D：持久性



##### 事务实现方式：锁

- 并发情况下，对共享资源的并发访问限制
- 表锁，行锁
  - 锁定粒度：表>行
  - 加锁效率：表>行
  - 冲突概率：表>行
  - 并发性能：表<行


###### 锁的类型

- 共享锁
  - 又称读锁，S锁，多个事务可以同时读取同一个数据，但是不能修改数据
  - 加锁方式：select * from user where id =5 LOCK IN SHARE MODE;
- 排它锁
  - 又称写锁，X锁：排它锁不能与其他锁并存，一个事务获取了排他锁，其他事务不能对改行获取任何锁（排它锁，共享锁），只有获取了该锁的事务才可以读取，修改
  - CUD操作自动加锁
  - select * from user where id =6 for update;

- 自增锁AUTO-INC lock
  - 针对自增列自增长的一个特殊的表级别锁
  - show variables like '%autoinc%';
  - 默认值时1，代表事务即使未提交ID也是永久丢弃的

- 意向共享锁（IS）表锁：
  - 加共享锁前会对表自动加IS锁，用户无需干预
  - 类似是否可以进行表锁的标记
  - 存在IS锁，则立即返回无法进行表锁
- 意向排它锁（IX）表锁：
  - 加排他锁前会对表自动加IX锁，用户无需干预
  - 类似是否可以进行表锁的标记
  - 存在IX锁，则立即返回无法进行表锁

- 锁的实现算法
  - 临键锁Next-key lock
    1. innodb行级锁的默认算法，为了解决幻读的问题。
    2. 划分区间，左开右闭(]
    3. Next-key lock=record lock + gap lock锁住当前索引记录和下一个区间

- 锁的实现方式
  - **innodb的行锁是通过给索引上的索引项加锁来实现的**
  - 如果未使用索引 执行计划类型是all，则锁表
  - 如果命中索引，则锁定命中的所有索引项，索引项以外的记录不就锁。
  - 通过辅助索引命中的锁，会自动对对应的主键索引上也加锁

- 常见场景
  - delete语句中没有使用索引进行删除操作，会导致整个表被锁住。

- 死锁的避免
  1. 类似业务以固定顺序访问表和行
  2. 大事务拆小，大事务更容易死锁
  3. 在同一个事务中尽可能做到一次锁定所需的所有资源。
  4. 为表添加合理的索引，如果不走索引，将会为表的每一行添加索引（表锁）

- MVCC multiversion concurrency control 多版本并发控制

  - 避免写操作的堵塞引发读操作的并发问题
  - 隐藏列：数据行版本号DB_TRX_ID，删除版本号DB_ROOLL_PT
  - insert时：数据行版本号：插入时事务ID，删除版本号：NULL
  - deletet时：数据版本号：不变，删除版本号：删除时事务ID
  - update时（delete，insert）
    - 先copy新记录：数据版本号：update时事务ID，删除版本号：NULL
    - 原数据删除：数据版本号：不变，删除版本号：update时事务ID

  - select时，查询同时满足下述条件的记录
    - 数据版本号小于当前事务ID
    - 删除版本号为NULL，或者大于当前的事务ID（排除掉select之前已经被删除的记录）


#### undo log（操作老数据）

- 为撤销操作为目的，事务开始之前，在操作任何数据之前，首先将需操作的数据备份到undo log中。
- 为了实现事务的原子性（rollback之后，可以利用undo log的备份将数据恢复到事务开始前的状态）
- undo中的数据可作为数据旧版本提供其他并发事务进行快照读
- undo buffer
- 正式场景
  1. 事务1修改id=1的数据，未提交（X锁，排它锁）。
  2. 事务2查询id=1的数据，按正常逻辑（S锁，共享锁），因为有X锁的存在，无法读取。结果是可以读到修改前的数据。此处就是快照读，读取的是undo log中备份数据。
- 快照读
  1. 普通的select就是快照读，是历史版本
  2. 解决了幻读的问题
- 当前读
  1. 最新版本的读，通过锁机制保证数据无法被其他事务修改

#### redo log（操作新数据）

- 重做，恢复操作为目的，重现操作。

- 是为了实现事务的持久性而出现的

- 事务中操作的任何数据，都会讲最新的数据备份到redo 中（redo buffer -> redo log）

- redo buffer写入redo log是顺序IO

  redo buffer写入磁盘

  - show VARIABLES like '%innodb_flush_log_at_trx_commit%';
  - 默认1，最安全，每次事务提交都执行redo buffer -> redo log os cache -> flush cache to disk
  - 取值2：每次事务提交都执行redo buffer -> redo log os cache ,再每秒执行redo log os cache -> flush cache to disk.

#### 服务器参数设定优化

https://www.cnblogs.com/wyy123/p/6092976.html

- 全局参数 set global autocommit  =off
- 会话参数 set session autocommit =off
- 查询服务器参数配置地址：mysql --help|grep -A 1 'following files'
- 最大连接数 show variables like 'max_%';
  - linux 系统根据句柄数：ulimit -a
  - mysql句柄数配置：

#### 内存参数配置

- sort_buffer_size 连接排序缓冲区大小:默认256K~2M之内
  - 当查询语句需要文件排序时，马上为connection分配的内存(执行计划extra项 Using filesort)
- join_buffer_size 连接的关联查询缓冲区大小：默认256K~1M之间
  - 使用到关联查询时，马上分配的内存大小
  - 可能分配多个
- wait_timeout 服务器非关闭交互连接之前等待的秒数

#### 其他

##### 慢查询sql定位

- mysqdumpslow工具





