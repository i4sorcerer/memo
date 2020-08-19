### 了解Fork/Join

参考实例：https://www.cnblogs.com/chenpi/p/5581198.html

#### 什么是Fork/Join

- 是ExecutorService接口的实现（同Executor框架类似，线程池）。
- 帮助开发人员充分利用多核cpu的优势，编写出并行应用，提高程序的性能。
- 处理对象是那些可以被递归拆分的大任务（有点儿类似于Map/Reduce的意思）。

#### 关键的类

- ForkJoinPool类，继承自AbstractExecutorService类：实现了工作窃取算法，可以执行ForkJoinTask任务
- ForkJoinTask抽象类，继承自Future接口
- RecursiveTask继承自ForkJoinTask，有返回结果的任务
- RecursiveAction继承自ForkJoinTask，无返回结果的任务

#### 工作窃取算法

![image-20200815114810268](.\工作窃取算法示意图.png)



#### 常见的使用Fork/Join的例子

- JAVA SE8 中java.util.Arrays 类的parallelSort()方法
- **AVA SE8中的java.util.streams包**

