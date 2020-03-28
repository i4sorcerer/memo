### jvm篇01_java的运行时内存数据模型

jvm内存中最终要的模型就是队内存，栈内存和常量池，下面针对这几种模型具体分析

#### 运行时数据模型分类

#####  线程私有内存

1. java栈
2. 本地方法栈
3. 程序计数器

##### 线程共享内存

1. 堆内存
2. 方法区（常量池）：jdk1.8之后，该区域被划分到Metaspace元空间中

#### 堆内存模型构成详解Heap

1. 新生代（Young Generation）
   - Eden区
   - From Survivor(S0)
   - To Survivor(S1)
2. 老年代（Old Generation）
   - Tenured区（终身的意思）

##### 图片说明总结

​                                                      图片1.  jvm运行时数据区图解

<img src="D:\sk\learn\git-repo\memo\tech\blogs\images\image-jvm-001.png" alt="image-20200318102554822" style="zoom: 67%;" />



​                                                      图片2.  jvm运行时堆内存jdk7、8版本差异图解

<img src="D:\sk\learn\git-repo\memo\tech\blogs\images\image-jvm-002.png" alt="image-20200318102855299" style="zoom:67%;" />