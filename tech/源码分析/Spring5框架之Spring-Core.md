## Spring5框架之Spring-Core

### Spring-Core

主要是asm包和cglib等操作字节码相关的包；对象生成技术包objenesis;各种常用Utils类

- asm
- cglib
- core ：提供各种核心操作支持
  - env
  
  - convert
  
  - io
  
    - /support
      - ResourcePatternResolver：继承自ResourceLoader 的资源匹配接口
  
    - ResourceLoader : Spring内部资源加载器接口
    - DefaultResourceLoader : Spring内部的资源加载器
  
  - serializer
- lang
- objenesis ：对象生成技术（针对无法通过无参构造函数生成的时候）
- util ： 大量共通类

### Spring的Util中写了大量的Util列，虽然不是专门提供给我们用的，但有些常用的可以直接拿来用

下面挑选如下20个以供参考使用：

1. **Asset**
2. Base64Utils
3. CollectionUtils
4. DigestUtils
5. FileCopyUtils
6. IdGenerator
7. NumberUtils
8. **ObjectUtils** ：对象相关的常见操作
9. RefectionUtils
10. ResourceUtils
11. SerializationUtils
12. SimpleIdGenerator
13. SocketUtils
14. StopWatch
15. StreamUtils
16. **StringUtils** ：字符串相关的常见操作
17. SystemPropertyUtils
18. TypeUtils
19. MethodInvoke
20. MimeTypeUtils

