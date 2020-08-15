### java基础篇共通

#### java8新特性

1. 接口中可以有默认的方法实现
   - 方法必须带有default

```java
/**
	定义接口
*/
interface DAO {

    default int getInt(){

        return 5;
    }
}
```

