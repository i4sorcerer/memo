## 深入理解Gradle

参照文章(https://www.cnblogs.com/davenkin/p/3417762.html)

### Mavenと区別(特徴)

- Gradle不提供内建的项目生命周期管理，只是java Plugin向Project中添加了许多Task，这些Task依次执行，为我们营造了一种如同Maven般项目构建周期
- Gradle不是采用XML配置方式，领域特定语言Groovy的配置
- 声明式的构建工具
  - 分成2个阶段
    - 配置阶段：Gradle将读取所有build.gradle文件的所有内容来配置Project和Task等
    - 执行阶段

- DSL语句和Groovy的区别
- 理解Gradle中project和task的概念
- 
