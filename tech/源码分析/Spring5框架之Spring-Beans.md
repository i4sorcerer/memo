## Spring5框架之Spring-Beans

### Spring-Beans

- /annotation

- **/factory** : 此包是重点，Spring基本实现都是在这里
  - /annotation

    - @Autowire
    - **@Autowired**
    - @Lookup
    - @Qulifier
    - **@Value**
    - 
  - **/config**
  - AbstractFactoryBean
    - AutowireCapableBeanFactory
    - ConfigurableBeanFactory
    - ConfigurableListableBeanFactory
    - **BeanDefinition ：Spring中Bean对象的体现就是以BeanDefition来体现的。Spring容器加载过程，就是BeanDefition的Resource定位，载入和注册的过程 **
    - BeanFactoryPostProcessor : 接口
    - BeanPostProcessor: 接口
  - /groovy
    - GroovyBeanDefinitionReader ：groovy方式定义的BeanDefinition读取类
  - /parsing
  - /serviceloader

    - AbstractServiceLoaderBasedFactoryBean
    - ServiceFactoryBean
    - ServiceListFactoryBean
    - ServiceLoaderFactoryBean
  - **/support** ：有一些主要实现类
    - **DefaultListableBeanFactory【重要+++++】** 
      1. 工厂类的最终默认实现类，实现了所有接口。底层IOC容器的最终体现。
      2. BeanDefinition向容器中注册也是通过此类实现的（实现了BeanDefinitionRegistry 接口中的registerBeanDefinition方法）
      3. 
    - AbstractBeanFactory
    - StaticListableBeanFactory
    - BeanDefinitionBuilder
    - **AbstractBeanDefition【重要+++++】 ： BeanDefinition的基本实现类**
    - **BeanDefinitionReader** ：BeanDefinition读取器接口
    - **AbstractBeanDefitionReader** ： BeanDefinition读取器默认实现类
    - PropertiesBeanDefinitionReader：Propery方式定义的BeanDefinition读取类
    - BeanDefinitionResource
    - BeanDefinitionRegisty ： BeanDefinition注册接口
    - BeanNameGenerator ： BeanName生成器
    - AutowireUtils
    - **BeanDefinitionValueResolver** ： 属性处理器
  - /wiring
  - /xml  ： 和xml读写相关包

    - **~~XmlBeanFactory~~ 是最基本IOC容器BeanFactory的实现，读取XML文件的BeanDefinition**，而ClassPathXmlApplicationContext则是高级的容器
    - XmlReaderContext ： Xml方式定义bean时，Bean解析过程中的Context对象
    - **XmlBeanDefitionReader ：XML文件的BeanDefinition读取类**
    - BeanDefinitionDocumentReader ： Document对象转换为BeanDefinition对象的接口
    - **DefaultBeanDefinitionDocumentReader ：Document转换为BeanDefinition实现类**
    - **BeanDefinitionParserDelegate 【重要+++】: 解析xml中的Element元素解析成bean标签类**
  - **BeanFactory【重要+++++】** ：最基本的IOC容器接口
  - ListableBeanFactory
  - BeanFactoryAware
  - BeanFactoryUtils
  - **FactoryBean** ：接口
  - IntializingBean
  - ObjectFactory ：接口
  - InjectionPoint

- /propertyeditors

- /support

- Aware ：接口  a marker superinterface indicating that a bean is eligible to be notified by the Spring container of a particular framework object through a call-back style method.

- BeanUtils

- BeanWrapper

### 附录0-Spring核心组件代码

1. Spring中存储bean定义的map（IOC容器的最终形态）

这些的注册的 Bean 定义信息是 IOC 容器控制反转的基础， 正是有了这些注册的数据， 容器才可以进行依赖注入  

```
/** Map of bean definition objects, keyed by bean name. */
private final Map<String, BeanDefinition> beanDefinitionMap = new ConcurrentHashMap<>(256);
```

从根本上来讲，向容器中注册bean，其实就是向map里添加要注册的BeanDefinition记录

key：beanName

value：BeanDefinition对象

```
this.beanDefinitionMap.put(beanName, beanDefinition);
```

### 附录1-BeanDefinition的类关系图

```
A BeanDefinition describes a bean instance, which has property values, constructor argument values, and further information supplied by concrete implementations.
```

![image-20200617182829780](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20200617182829780.png)

### 附录2（重要）-加载解析重要方法

DefaultBeanDefinitionDocumentReader的parseDefaultElement方法，具体解析每个标签

**注意：这里的解析只是转换成spring内部的bean定义结构而已，并没有对bean生成实例，初始化操作**

(spring配置文件的默认root是beans标签)

- import标签 ：importBeanDefinitionResource() 
- alias标签 ： processAliasRegistration()
- bean标签 ： processBeanDefinition()
- beans标签 (嵌套)： doRegisterBeanDefinitions()

```
private void parseDefaultElement(Element ele, BeanDefinitionParserDelegate delegate) {
   if (delegate.nodeNameEquals(ele, IMPORT_ELEMENT)) {
      importBeanDefinitionResource(ele);
   }
   else if (delegate.nodeNameEquals(ele, ALIAS_ELEMENT)) {
      processAliasRegistration(ele);
   }
   else if (delegate.nodeNameEquals(ele, BEAN_ELEMENT)) {
      processBeanDefinition(ele, delegate);
   }
   else if (delegate.nodeNameEquals(ele, NESTED_BEANS_ELEMENT)) {
      // recurse递归调用
      // 如果是嵌套beans标签，则递归调用
      doRegisterBeanDefinitions(ele);
   }
}
```

解析bean元素标签processBeanDefinition

```
/**
 * Process the given bean element, parsing the bean definition
 * and registering it with the registry.
 */
protected void processBeanDefinition(Element ele, BeanDefinitionParserDelegate delegate) {
   BeanDefinitionHolder bdHolder = delegate.parseBeanDefinitionElement(ele);
   if (bdHolder != null) {
      // 将xml元素解析成bean对象BeanDefinition
      bdHolder = delegate.decorateBeanDefinitionIfRequired(ele, bdHolder);
      try {
         // Register the final decorated instance.
         // 向IOC容器注册解析得到的bean定义，这是bean定义向IOC容器注册的入口
         BeanDefinitionReaderUtils.registerBeanDefinition(bdHolder, getReaderContext().getRegistry());
      }
      catch (BeanDefinitionStoreException ex) {
         getReaderContext().error("Failed to register bean definition with name '" +
               bdHolder.getBeanName() + "'", ele, ex);
      }
      // Send registration event.
      getReaderContext().fireComponentRegistered(new BeanComponentDefinition(bdHolder));
   }
}
```

bean标签实际解析是由BeanDefinitionParserDelegate的parseBeanDefinitionElement方法实现的

```
/**
 * Parse the bean definition itself, without regard to name or aliases. May return
 * {@code null} if problems occurred during the parsing of the bean definition.
 */
@Nullable
public AbstractBeanDefinition parseBeanDefinitionElement(
      Element ele, String beanName, @Nullable BeanDefinition containingBean) {

   this.parseState.push(new BeanEntry(beanName));

   String className = null;
   if (ele.hasAttribute(CLASS_ATTRIBUTE)) {
      className = ele.getAttribute(CLASS_ATTRIBUTE).trim();
   }
   String parent = null;
   if (ele.hasAttribute(PARENT_ATTRIBUTE)) {
      parent = ele.getAttribute(PARENT_ATTRIBUTE);
   }

   try {
      // 基础的BeanDefinition对象
      AbstractBeanDefinition bd = createBeanDefinition(className, parent);

      parseBeanDefinitionAttributes(ele, beanName, containingBean, bd);
      bd.setDescription(DomUtils.getChildElementValueByTagName(ele, DESCRIPTION_ELEMENT));

      parseMetaElements(ele, bd);
      parseLookupOverrideSubElements(ele, bd.getMethodOverrides());
      parseReplacedMethodSubElements(ele, bd.getMethodOverrides());
      // 设置构造函数元素
      parseConstructorArgElements(ele, bd);
      // 设置属性元素
      parsePropertyElements(ele, bd);
      // 设置qualifier元素
      parseQualifierElements(ele, bd);

      bd.setResource(this.readerContext.getResource());
      bd.setSource(extractSource(ele));

      return bd;
   }
   catch (ClassNotFoundException ex) {
      error("Bean class [" + className + "] not found", ele, ex);
   }
   catch (NoClassDefFoundError err) {
      error("Class that bean class [" + className + "] depends on not found", ele, err);
   }
   catch (Throwable ex) {
      error("Unexpected failure during bean definition parsing", ele, ex);
   }
   finally {
      this.parseState.pop();
   }

   return null;
}
```

以bean标签中的property子元素解析为例，说明bean的子元素解析

```
/**
 * Parse property sub-elements of the given bean element.
 */
public void parsePropertyElements(Element beanEle, BeanDefinition bd) {
   NodeList nl = beanEle.getChildNodes();
   for (int i = 0; i < nl.getLength(); i++) {
      Node node = nl.item(i);
      if (isCandidateElement(node) && nodeNameEquals(node, PROPERTY_ELEMENT)) {
         parsePropertyElement((Element) node, bd);
      }
   }
}

	/**
	 * Parse a property element.
	 */
	public void parsePropertyElement(Element ele, BeanDefinition bd) {
		String propertyName = ele.getAttribute(NAME_ATTRIBUTE);
		if (!StringUtils.hasLength(propertyName)) {
			error("Tag 'property' must have a 'name' attribute", ele);
			return;
		}
		this.parseState.push(new PropertyEntry(propertyName));
		try {
			if (bd.getPropertyValues().contains(propertyName)) {
				error("Multiple 'property' definitions for property '" + propertyName + "'", ele);
				return;
			}
			Object val = parsePropertyValue(ele, bd, propertyName);
			PropertyValue pv = new PropertyValue(propertyName, val);
			parseMetaElements(ele, pv);
			pv.setSource(extractSource(ele));
			bd.getPropertyValues().addPropertyValue(pv);
		}
		finally {
			this.parseState.pop();
		}
	}

    调用parsePropertyValue方法获取property属性的value值
	/**
	 * Get the value of a property element. May be a list etc.
	 * Also used for constructor arguments, "propertyName" being null in this case.
	 */
	@Nullable
	public Object parsePropertyValue(Element ele, BeanDefinition bd, @Nullable String propertyName) {
		String elementName = (propertyName != null ?
				"<property> element for property '" + propertyName + "'" :
				"<constructor-arg> element");

		// Should only have one child element: ref, value, list, etc.
		NodeList nl = ele.getChildNodes();
		Element subElement = null;
		for (int i = 0; i < nl.getLength(); i++) {
			Node node = nl.item(i);
			if (node instanceof Element && !nodeNameEquals(node, DESCRIPTION_ELEMENT) &&
					!nodeNameEquals(node, META_ELEMENT)) {
				// Child element is what we're looking for.
				if (subElement != null) {
					error(elementName + " must not contain more than one sub-element", ele);
				}
				else {
					subElement = (Element) node;
				}
			}
		}

		boolean hasRefAttribute = ele.hasAttribute(REF_ATTRIBUTE);
		boolean hasValueAttribute = ele.hasAttribute(VALUE_ATTRIBUTE);
		if ((hasRefAttribute && hasValueAttribute) ||
				((hasRefAttribute || hasValueAttribute) && subElement != null)) {
			error(elementName +
					" is only allowed to contain either 'ref' attribute OR 'value' attribute OR sub-element", ele);
		}

		if (hasRefAttribute) {
			String refName = ele.getAttribute(REF_ATTRIBUTE);
			if (!StringUtils.hasText(refName)) {
				error(elementName + " contains empty 'ref' attribute", ele);
			}
			// ref指定其他bean时，spring中对应RuntimeBeanReference
			RuntimeBeanReference ref = new RuntimeBeanReference(refName);
			// 设置ref的引用源
			ref.setSource(extractSource(ele));
			return ref;
		}
		else if (hasValueAttribute) {
			TypedStringValue valueHolder = new TypedStringValue(ele.getAttribute(VALUE_ATTRIBUTE));
			valueHolder.setSource(extractSource(ele));
			return valueHolder;
		}
		else if (subElement != null) {
			return parsePropertySubElement(subElement, bd);
		}
		else {
			// Neither child element nor "ref" or "value" attribute found.
			error(elementName + " must specify a ref or value", ele);
			return null;
		}
	}
调用parsePropertySubElement方法，解析property元素中的子元素标签
	/**
	 * Parse a value, ref or collection sub-element of a property or
	 * constructor-arg element.
	 * @param ele subelement of property element; we don't know which yet
	 * @param bd the current bean definition (if any)
	 * @param defaultValueType the default type (class name) for any
	 * {@code <value>} tag that might be created
	 */
	@Nullable
	public Object parsePropertySubElement(Element ele, @Nullable BeanDefinition bd, @Nullable String defaultValueType) {
		if (!isDefaultNamespace(ele)) {
			return parseNestedCustomElement(ele, bd);
		}
		else if (nodeNameEquals(ele, BEAN_ELEMENT)) {
			BeanDefinitionHolder nestedBd = parseBeanDefinitionElement(ele, bd);
			if (nestedBd != null) {
				nestedBd = decorateBeanDefinitionIfRequired(ele, nestedBd, bd);
			}
			return nestedBd;
		}
		else if (nodeNameEquals(ele, REF_ELEMENT)) {
			// A generic reference to any name of any bean.
			String refName = ele.getAttribute(BEAN_REF_ATTRIBUTE);
			boolean toParent = false;
			if (!StringUtils.hasLength(refName)) {
				// A reference to the id of another bean in a parent context.
				refName = ele.getAttribute(PARENT_REF_ATTRIBUTE);
				toParent = true;
				if (!StringUtils.hasLength(refName)) {
					error("'bean' or 'parent' is required for <ref> element", ele);
					return null;
				}
			}
			if (!StringUtils.hasText(refName)) {
				error("<ref> element contains empty target attribute", ele);
				return null;
			}
			RuntimeBeanReference ref = new RuntimeBeanReference(refName, toParent);
			ref.setSource(extractSource(ele));
			return ref;
		}
		else if (nodeNameEquals(ele, IDREF_ELEMENT)) {
			return parseIdRefElement(ele);
		}
		else if (nodeNameEquals(ele, VALUE_ELEMENT)) {
			return parseValueElement(ele, defaultValueType);
		}
		else if (nodeNameEquals(ele, NULL_ELEMENT)) {
			// It's a distinguished null value. Let's wrap it in a TypedStringValue
			// object in order to preserve the source location.
			TypedStringValue nullHolder = new TypedStringValue(null);
			nullHolder.setSource(extractSource(ele));
			return nullHolder;
		}
		else if (nodeNameEquals(ele, ARRAY_ELEMENT)) {
			return parseArrayElement(ele, bd);
		}
		else if (nodeNameEquals(ele, LIST_ELEMENT)) {
			return parseListElement(ele, bd);
		}
		else if (nodeNameEquals(ele, SET_ELEMENT)) {
			return parseSetElement(ele, bd);
		}
		else if (nodeNameEquals(ele, MAP_ELEMENT)) {
			return parseMapElement(ele, bd);
		}
		else if (nodeNameEquals(ele, PROPS_ELEMENT)) {
			return parsePropsElement(ele);
		}
		else {
			error("Unknown property sub-element: [" + ele.getNodeName() + "]", ele);
			return null;
		}
	}

当子元素是list标签时，调用parseListElement方法解析其值
	/**
	 * Parse a list element.
	 */
	public List<Object> parseListElement(Element collectionEle, @Nullable BeanDefinition bd) {
		String defaultElementType = collectionEle.getAttribute(VALUE_TYPE_ATTRIBUTE);
		NodeList nl = collectionEle.getChildNodes();
		// list标签在spring内部对应的是ManagedList
		ManagedList<Object> target = new ManagedList<>(nl.getLength());
		target.setSource(extractSource(collectionEle));
		target.setElementTypeName(defaultElementType);
		target.setMergeEnabled(parseMergeAttribute(collectionEle));
		parseCollectionElements(nl, target, bd, defaultElementType);
		return target;
	}
```

### 附录3-Bean实例化createBeanInstance  

AbstractAutowireCapableBeanFactory

```
//---------------------------------------------------------------------
// Implementation of relevant AbstractBeanFactory template methods
//---------------------------------------------------------------------

/**
 * Central method of this class: creates a bean instance,
 * populates the bean instance, applies post-processors, etc.
此类的关键方法：创建bean实例，填充bean实例，应用bean后置处理器等等。
mbd指的是mergered BeanDefinition

 * @see #doCreateBean
 */
@Override
protected Object createBean(String beanName, RootBeanDefinition mbd, @Nullable Object[] args)
      throws BeanCreationException {

   if (logger.isTraceEnabled()) {
      logger.trace("Creating instance of bean '" + beanName + "'");
   }
   RootBeanDefinition mbdToUse = mbd;

   // Make sure bean class is actually resolved at this point, and
   // clone the bean definition in case of a dynamically resolved Class
   // which cannot be stored in the shared merged bean definition.
   Class<?> resolvedClass = resolveBeanClass(mbd, beanName);
   if (resolvedClass != null && !mbd.hasBeanClass() && mbd.getBeanClassName() != null) {
      mbdToUse = new RootBeanDefinition(mbd);
      mbdToUse.setBeanClass(resolvedClass);
   }

   // Prepare method overrides.
   校验方法的覆盖
   try {
      mbdToUse.prepareMethodOverrides();
   }
   catch (BeanDefinitionValidationException ex) {
      throw new BeanDefinitionStoreException(mbdToUse.getResourceDescription(),
            beanName, "Validation of method overrides failed", ex);
   }

   try {
      // Give BeanPostProcessors a chance to return a proxy instead of the target bean instance.
      Object bean = resolveBeforeInstantiation(beanName, mbdToUse);
      if (bean != null) {
         return bean;
      }
   }
   catch (Throwable ex) {
      throw new BeanCreationException(mbdToUse.getResourceDescription(), beanName,
            "BeanPostProcessor before instantiation of bean failed", ex);
   }

   try {
      Object beanInstance = doCreateBean(beanName, mbdToUse, args);
      if (logger.isTraceEnabled()) {
         logger.trace("Finished creating instance of bean '" + beanName + "'");
      }
      return beanInstance;
   }
   catch (BeanCreationException | ImplicitlyAppearedSingletonException ex) {
      // A previously detected exception with proper bean creation context already,
      // or illegal singleton state to be communicated up to DefaultSingletonBeanRegistry.
      throw ex;
   }
   catch (Throwable ex) {
      throw new BeanCreationException(
            mbdToUse.getResourceDescription(), beanName, "Unexpected exception during bean creation", ex);
   }
}
```

真正执行创建bean操作的方法

```
/**
 * Actually create the specified bean. Pre-creation processing has already happened
 * at this point, e.g. checking {@code postProcessBeforeInstantiation} callbacks.
 * <p>Differentiates between default bean instantiation, use of a
 * factory method, and autowiring a constructor.
 * @param beanName the name of the bean
 * @param mbd the merged bean definition for the bean
 * @param args explicit arguments to use for constructor or factory method invocation
 * @return a new instance of the bean
 * @throws BeanCreationException if the bean could not be created
 * @see #instantiateBean
 * @see #instantiateUsingFactoryMethod
 * @see #autowireConstructor
 */
 根据beanName,merged bean definition和构造函数使用的参数来创建bean
protected Object doCreateBean(final String beanName, final RootBeanDefinition mbd, final @Nullable Object[] args)
      throws BeanCreationException {

   // Instantiate the bean.
   BeanWrapper instanceWrapper = null;
   
   if (mbd.isSingleton()) {
      instanceWrapper = this.factoryBeanInstanceCache.remove(beanName);
   }
   if (instanceWrapper == null) {
      【生成BeanDefinition包含的实例的方法】
      【生成的其实是Object的包装类】
      instanceWrapper = createBeanInstance(beanName, mbd, args);
   }
   final Object bean = instanceWrapper.getWrappedInstance();
   Class<?> beanType = instanceWrapper.getWrappedClass();
   if (beanType != NullBean.class) {
      mbd.resolvedTargetType = beanType;
   }

   // Allow post-processors to modify the merged bean definition.
   synchronized (mbd.postProcessingLock) {
      if (!mbd.postProcessed) {
         try {
            applyMergedBeanDefinitionPostProcessors(mbd, beanType, beanName);
         }
         catch (Throwable ex) {
            throw new BeanCreationException(mbd.getResourceDescription(), beanName,
                  "Post-processing of merged bean definition failed", ex);
         }
         mbd.postProcessed = true;
      }
   }

   // Eagerly cache singletons to be able to resolve circular references
   // even when triggered by lifecycle interfaces like BeanFactoryAware.
   boolean earlySingletonExposure = (mbd.isSingleton() && this.allowCircularReferences &&
         isSingletonCurrentlyInCreation(beanName));
   if (earlySingletonExposure) {
      if (logger.isTraceEnabled()) {
         logger.trace("Eagerly caching bean '" + beanName +
               "' to allow for resolving potential circular references");
      }
      addSingletonFactory(beanName, () -> getEarlyBeanReference(beanName, mbd, bean));
   }

   // Initialize the bean instance.
   Object exposedObject = bean;
   try {
      【对Bean的属性的依赖注入进行处理】
      populateBean(beanName, mbd, instanceWrapper);
      exposedObject = initializeBean(beanName, exposedObject, mbd);
   }
   catch (Throwable ex) {
      if (ex instanceof BeanCreationException && beanName.equals(((BeanCreationException) ex).getBeanName())) {
         throw (BeanCreationException) ex;
      }
      else {
         throw new BeanCreationException(
               mbd.getResourceDescription(), beanName, "Initialization of bean failed", ex);
      }
   }

   if (earlySingletonExposure) {
      Object earlySingletonReference = getSingleton(beanName, false);
      if (earlySingletonReference != null) {
         if (exposedObject == bean) {
            exposedObject = earlySingletonReference;
         }
         else if (!this.allowRawInjectionDespiteWrapping && hasDependentBean(beanName)) {
            String[] dependentBeans = getDependentBeans(beanName);
            Set<String> actualDependentBeans = new LinkedHashSet<>(dependentBeans.length);
            for (String dependentBean : dependentBeans) {
               if (!removeSingletonIfCreatedForTypeCheckOnly(dependentBean)) {
                  actualDependentBeans.add(dependentBean);
               }
            }
            if (!actualDependentBeans.isEmpty()) {
               throw new BeanCurrentlyInCreationException(beanName,
                     "Bean with name '" + beanName + "' has been injected into other beans [" +
                     StringUtils.collectionToCommaDelimitedString(actualDependentBeans) +
                     "] in its raw version as part of a circular reference, but has eventually been " +
                     "wrapped. This means that said other beans do not use the final version of the " +
                     "bean. This is often the result of over-eager type matching - consider using " +
                     "'getBeanNamesOfType' with the 'allowEagerInit' flag turned off, for example.");
            }
         }
      }
   }

   // Register bean as disposable.
   try {
      registerDisposableBeanIfNecessary(beanName, bean, mbd);
   }
   catch (BeanDefinitionValidationException ex) {
      throw new BeanCreationException(
            mbd.getResourceDescription(), beanName, "Invalid destruction signature", ex);
   }

   return exposedObject;
}
```

生成实例对象的方法createBeanInstance：

```
/**
 * Create a new instance for the specified bean, using an appropriate instantiation strategy:
 * factory method, constructor autowiring, or simple instantiation.
 根据指定的策略创建bean对象实例，使用工厂方法策略，构造器自动初始化，或者简单实例化
 * @param beanName the name of the bean
 * @param mbd the bean definition for the bean
 * @param args explicit arguments to use for constructor or factory method invocation
 * @return a BeanWrapper for the new instance
 * @see #obtainFromSupplier
 * @see #instantiateUsingFactoryMethod
 * @see #autowireConstructor
 * @see #instantiateBean
 */
protected BeanWrapper createBeanInstance(String beanName, RootBeanDefinition mbd, @Nullable Object[] args) {
   // Make sure bean class is actually resolved at this point.
   先检查确认bean的class类型是可实例化的
   Class<?> beanClass = resolveBeanClass(mbd, beanName);

   if (beanClass != null && !Modifier.isPublic(beanClass.getModifiers()) && !mbd.isNonPublicAccessAllowed()) {
      throw new BeanCreationException(mbd.getResourceDescription(), beanName,
            "Bean class isn't public, and non-public access not allowed: " + beanClass.getName());
   }

   Supplier<?> instanceSupplier = mbd.getInstanceSupplier();
   if (instanceSupplier != null) {
      return obtainFromSupplier(instanceSupplier, beanName);
   }

   if (mbd.getFactoryMethodName() != null) {
   【使用工厂方法进行实例化】
      return instantiateUsingFactoryMethod(beanName, mbd, args);
   }

   // Shortcut when re-creating the same bean...
   boolean resolved = false;
   boolean autowireNecessary = false;
   if (args == null) {
      synchronized (mbd.constructorArgumentLock) {
         if (mbd.resolvedConstructorOrFactoryMethod != null) {
            resolved = true;
            autowireNecessary = mbd.constructorArgumentsResolved;
         }
      }
   }

   if (resolved) {
      if (autowireNecessary) {
         【使用容器的自动装配】
         【指根据参数类型，自动匹配工构造函数】
         【下面null指的是不是明确指定够参数】
         return autowireConstructor(beanName, mbd, null, null);
      }
      else {
      【使用默认的无参构造函数进行实例化】
         return instantiateBean(beanName, mbd);
      }
   }

   // Candidate constructors for autowiring?
   Constructor<?>[] ctors = determineConstructorsFromBeanPostProcessors(beanClass, beanName);
   if (ctors != null || mbd.getResolvedAutowireMode() == AUTOWIRE_CONSTRUCTOR ||
         mbd.hasConstructorArgumentValues() || !ObjectUtils.isEmpty(args)) {
         【调用和指定参数匹配的构造函数进行实例化】
      return autowireConstructor(beanName, mbd, ctors, args);
   }


   // Preferred constructors for default construction?
   ctors = mbd.getPreferredConstructors();
   【使用偏好构造函数进行默认实例化】
   if (ctors != null) {
      return autowireConstructor(beanName, mbd, ctors, null);
   }

   // No special handling: simply use no-arg constructor.
   【如果没有特殊处理，使用默认无参构造函数进行实例化】
   return instantiateBean(beanName, mbd);
}
```

调用无参构造函数实例化bean

```
/**
 * Instantiate the given bean using its default constructor.
 * @param beanName the name of the bean
 * @param mbd the bean definition for the bean
 * @return a BeanWrapper for the new instance
 */
protected BeanWrapper instantiateBean(final String beanName, final RootBeanDefinition mbd) {
   try {
      Object beanInstance;
      final BeanFactory parent = this;
      if (System.getSecurityManager() != null) {
         beanInstance = AccessController.doPrivileged((PrivilegedAction<Object>) () ->
               getInstantiationStrategy().instantiate(mbd, beanName, parent),
               getAccessControlContext());
      }
      else {
      【根据不同的初始化策略，调用不同的初始化方法】
      【简单实例化测试JDK反射机制 SimpleInstantiationStrategy】
      【CGLIB机制 CglibSubclassingInstantiationStrategy】
         beanInstance = getInstantiationStrategy().instantiate(mbd, beanName, parent);
      }
      // 设置包装类
      BeanWrapper bw = new BeanWrapperImpl(beanInstance);
      initBeanWrapper(bw);
      return bw;
   }
   catch (Throwable ex) {
      throw new BeanCreationException(
            mbd.getResourceDescription(), beanName, "Instantiation of bean failed", ex);
   }
}
```

SimpleInstantiationStrategy的实例化方法（无参构造函数）

```
@Override
public Object instantiate(RootBeanDefinition bd, @Nullable String beanName, BeanFactory owner) {
   // Don't override the class with CGLIB if no overrides.
   【此种实例化策略仅适用于没有方法被覆盖的情况，如果有，应该使用CGLIB策略】
   if (!bd.hasMethodOverrides()) {
      Constructor<?> constructorToUse;
      synchronized (bd.constructorArgumentLock) {
         constructorToUse = (Constructor<?>) bd.resolvedConstructorOrFactoryMethod;
         if (constructorToUse == null) {
            final Class<?> clazz = bd.getBeanClass();
            if (clazz.isInterface()) {
               throw new BeanInstantiationException(clazz, "Specified class is an interface");
            }
            try {
               if (System.getSecurityManager() != null) {
                  constructorToUse = AccessController.doPrivileged(
                        (PrivilegedExceptionAction<Constructor<?>>) clazz::getDeclaredConstructor);
               }
               else {
               【这里使用反射机制，获取默认无参的构造函数】
                  constructorToUse = clazz.getDeclaredConstructor();
               }
               【将构造函数设置回BeanDefinition】
               bd.resolvedConstructorOrFactoryMethod = constructorToUse;
            }
            catch (Throwable ex) {
               throw new BeanInstantiationException(clazz, "No default constructor found", ex);
            }
         }
      }
      【使用 BeanUtils 实例化， 通过反射机制调用”构造方法.newInstance(arg)”来进行实例化】
      return BeanUtils.instantiateClass(constructorToUse);
   }
   else {
      // Must generate CGLIB subclass.
      return instantiateWithMethodInjection(bd, beanName, owner);
   }
}
```

### 附录4-Bean属性依赖注入处理populateBean    

AbstractAutowireCapableBeanFactory

```
/**
 * Populate the bean instance in the given BeanWrapper with the property values
 * from the bean definition.
【 将Bean实例化后生成的BeanWrapper进行属性值得填充】
 * @param beanName the name of the bean
 * @param mbd the bean definition for the bean
 * @param bw the BeanWrapper with bean instance
 */
@SuppressWarnings("deprecation")  // for postProcessPropertyValues
protected void populateBean(String beanName, RootBeanDefinition mbd, @Nullable BeanWrapper bw) {
   if (bw == null) {
      if (mbd.hasPropertyValues()) {
         throw new BeanCreationException(
               mbd.getResourceDescription(), beanName, "Cannot apply property values to null instance");
      }
      else {
         // Skip property population phase for null instance.
         return;
      }
   }

   // Give any InstantiationAwareBeanPostProcessors the opportunity to modify the
   // state of the bean before properties are set. This can be used, for example,
   // to support styles of field injection.
   boolean continueWithPropertyPopulation = true;

   if (!mbd.isSynthetic() && hasInstantiationAwareBeanPostProcessors()) {
      for (BeanPostProcessor bp : getBeanPostProcessors()) {
         if (bp instanceof InstantiationAwareBeanPostProcessor) {
            InstantiationAwareBeanPostProcessor ibp = (InstantiationAwareBeanPostProcessor) bp;
            if (!ibp.postProcessAfterInstantiation(bw.getWrappedInstance(), beanName)) {
               continueWithPropertyPopulation = false;
               break;
            }
         }
      }
   }

   if (!continueWithPropertyPopulation) {
      return;
   }
   // 获取容器在解析 Bean 定义资源时为 BeanDefiniton 中设置的属性值
   PropertyValues pvs = (mbd.hasPropertyValues() ? mbd.getPropertyValues() : null);

   【自动注入的mode选择，根据名字注入和针具类型注入】
   int resolvedAutowireMode = mbd.getResolvedAutowireMode();
   if (resolvedAutowireMode == AUTOWIRE_BY_NAME || resolvedAutowireMode == AUTOWIRE_BY_TYPE) {
      MutablePropertyValues newPvs = new MutablePropertyValues(pvs);
      // Add property values based on autowire by name if applicable.
      if (resolvedAutowireMode == AUTOWIRE_BY_NAME) {
         autowireByName(beanName, mbd, bw, newPvs);
      }
      // Add property values based on autowire by type if applicable.
      if (resolvedAutowireMode == AUTOWIRE_BY_TYPE) {
         autowireByType(beanName, mbd, bw, newPvs);
      }
      pvs = newPvs;
   }

   boolean hasInstAwareBpps = hasInstantiationAwareBeanPostProcessors();
   boolean needsDepCheck = (mbd.getDependencyCheck() != AbstractBeanDefinition.DEPENDENCY_CHECK_NONE);

   PropertyDescriptor[] filteredPds = null;
   if (hasInstAwareBpps) {
      if (pvs == null) {
         pvs = mbd.getPropertyValues();
      }
      for (BeanPostProcessor bp : getBeanPostProcessors()) {
         if (bp instanceof InstantiationAwareBeanPostProcessor) {
            InstantiationAwareBeanPostProcessor ibp = (InstantiationAwareBeanPostProcessor) bp;
            PropertyValues pvsToUse = ibp.postProcessProperties(pvs, bw.getWrappedInstance(), beanName);
            if (pvsToUse == null) {
               if (filteredPds == null) {
                  filteredPds = filterPropertyDescriptorsForDependencyCheck(bw, mbd.allowCaching);
               }
               pvsToUse = ibp.postProcessPropertyValues(pvs, filteredPds, bw.getWrappedInstance(), beanName);
               if (pvsToUse == null) {
                  return;
               }
            }
            pvs = pvsToUse;
         }
      }
   }
   if (needsDepCheck) {
      if (filteredPds == null) {
         filteredPds = filterPropertyDescriptorsForDependencyCheck(bw, mbd.allowCaching);
      }
      checkDependencies(beanName, mbd, filteredPds, pvs);
   }

   if (pvs != null) {
      【最终如果属性值不为空，则应用属性值依赖注入】
      【参数依次是beanName，BeanDefinition实例，实例化后的BeanWrapper，属性值】
      applyPropertyValues(beanName, mbd, bw, pvs);
   }
}
```

根据依赖注入mode的不同选择不同方式注入

AUTOWIRE_BY_NAME

AUTOWIRE_BY_TYPE

```
/**
 * Fill in any missing property values with references to
 * other beans in this factory if autowire is set to "byName".
 * @param beanName the name of the bean we're wiring up.
 * Useful for debugging messages; not used functionally.
 * @param mbd bean definition to update through autowiring
 * @param bw the BeanWrapper from which we can obtain information about the bean
 * @param pvs the PropertyValues to register wired objects with
 */
protected void autowireByName(
      String beanName, AbstractBeanDefinition mbd, BeanWrapper bw, MutablePropertyValues pvs) {

   String[] propertyNames = unsatisfiedNonSimpleProperties(mbd, bw);
   for (String propertyName : propertyNames) {
      if (containsBean(propertyName)) {
         Object bean = getBean(propertyName);
         pvs.add(propertyName, bean);
         registerDependentBean(propertyName, beanName);
         if (logger.isTraceEnabled()) {
            logger.trace("Added autowiring by name from bean name '" + beanName +
                  "' via property '" + propertyName + "' to bean named '" + propertyName + "'");
         }
      }
      else {
         if (logger.isTraceEnabled()) {
            logger.trace("Not autowiring property '" + propertyName + "' of bean '" + beanName +
                  "' by name: no matching bean found");
         }
      }
   }
}

/**
 * Abstract method defining "autowire by type" (bean properties by type) behavior.
 * <p>This is like PicoContainer default, in which there must be exactly one bean
 * of the property type in the bean factory. This makes bean factories simple to
 * configure for small namespaces, but doesn't work as well as standard Spring
 * behavior for bigger applications.
 * @param beanName the name of the bean to autowire by type
 * @param mbd the merged bean definition to update through autowiring
 * @param bw the BeanWrapper from which we can obtain information about the bean
 * @param pvs the PropertyValues to register wired objects with
 */
protected void autowireByType(
      String beanName, AbstractBeanDefinition mbd, BeanWrapper bw, MutablePropertyValues pvs) {

   TypeConverter converter = getCustomTypeConverter();
   if (converter == null) {
      converter = bw;
   }

   Set<String> autowiredBeanNames = new LinkedHashSet<>(4);
   String[] propertyNames = unsatisfiedNonSimpleProperties(mbd, bw);
   for (String propertyName : propertyNames) {
      try {
         PropertyDescriptor pd = bw.getPropertyDescriptor(propertyName);
         // Don't try autowiring by type for type Object: never makes sense,
         // even if it technically is a unsatisfied, non-simple property.
         if (Object.class != pd.getPropertyType()) {
            MethodParameter methodParam = BeanUtils.getWriteMethodParameter(pd);
            // Do not allow eager init for type matching in case of a prioritized post-processor.
            boolean eager = !PriorityOrdered.class.isInstance(bw.getWrappedInstance());
            DependencyDescriptor desc = new AutowireByTypeDependencyDescriptor(methodParam, eager);
            Object autowiredArgument = resolveDependency(desc, beanName, autowiredBeanNames, converter);
            if (autowiredArgument != null) {
               pvs.add(propertyName, autowiredArgument);
            }
            for (String autowiredBeanName : autowiredBeanNames) {
               registerDependentBean(autowiredBeanName, beanName);
               if (logger.isTraceEnabled()) {
                  logger.trace("Autowiring by type from bean name '" + beanName + "' via property '" +
                        propertyName + "' to bean named '" + autowiredBeanName + "'");
               }
            }
            autowiredBeanNames.clear();
         }
      }
      catch (BeansException ex) {
         throw new UnsatisfiedDependencyException(mbd.getResourceDescription(), beanName, propertyName, ex);
      }
   }
}
```

进行属性值依赖处理的方法applyPropertyValues

(1).属性值类型不需要转换时， 不需要解析属性值， 直接准备进行依赖注入。
(2).属性值需要进行类型转换时， 如对其他对象的引用等， 首先需要解析属性值， 然后对解析后的属性
值进行依赖注入。  

```
/**
 * Apply the given property values, resolving any runtime references
 * to other beans in this bean factory. Must use deep copy, so we
 * don't permanently modify this property.
 * @param beanName the bean name passed for better exception information
 * @param mbd the merged bean definition
 * @param bw the BeanWrapper wrapping the target object
 * @param pvs the new property values
 */
protected void applyPropertyValues(String beanName, BeanDefinition mbd, BeanWrapper bw, PropertyValues pvs) {
   if (pvs.isEmpty()) {
      return;
   }

   if (System.getSecurityManager() != null && bw instanceof BeanWrapperImpl) {
      ((BeanWrapperImpl) bw).setSecurityContext(getAccessControlContext());
   }

   MutablePropertyValues mpvs = null;
   List<PropertyValue> original;

   if (pvs instanceof MutablePropertyValues) {
      mpvs = (MutablePropertyValues) pvs;
      if (mpvs.isConverted()) {
         // Shortcut: use the pre-converted values as-is.
         try {
            bw.setPropertyValues(mpvs);
            return;
         }
         catch (BeansException ex) {
            throw new BeanCreationException(
                  mbd.getResourceDescription(), beanName, "Error setting property values", ex);
         }
      }
      original = mpvs.getPropertyValueList();
   }
   else {
      original = Arrays.asList(pvs.getPropertyValues());
   }

   TypeConverter converter = getCustomTypeConverter();
   if (converter == null) {
      converter = bw;
   }
   BeanDefinitionValueResolver valueResolver = new BeanDefinitionValueResolver(this, beanName, mbd, converter);

   // Create a deep copy, resolving any references for values.
   List<PropertyValue> deepCopy = new ArrayList<>(original.size());
   boolean resolveNecessary = false;
   for (PropertyValue pv : original) {
      if (pv.isConverted()) {
         deepCopy.add(pv);
      }
      else {
         String propertyName = pv.getName();
         Object originalValue = pv.getValue();
         if (originalValue == AutowiredPropertyMarker.INSTANCE) {
            Method writeMethod = bw.getPropertyDescriptor(propertyName).getWriteMethod();
            if (writeMethod == null) {
               throw new IllegalArgumentException("Autowire marker for property without write method: " + pv);
            }
            originalValue = new DependencyDescriptor(new MethodParameter(writeMethod, 0), true);
         }
         【当容器在对属性进行依赖注入时， 如果发现属性值需要进行类型转换， 如属性值是容器中另一个 Bean
实例对象的引用， 则容器首先需要根据属性值解析出所引用的对象， 然后才能将该引用对象注入到目标
实例对象的属性上去】
         Object resolvedValue = valueResolver.resolveValueIfNecessary(pv, originalValue);
         Object convertedValue = resolvedValue;
         boolean convertible = bw.isWritableProperty(propertyName) &&
               !PropertyAccessorUtils.isNestedOrIndexedProperty(propertyName);
         if (convertible) {
            convertedValue = convertForProperty(resolvedValue, propertyName, bw, converter);
         }
         // Possibly store converted value in merged bean definition,
         // in order to avoid re-conversion for every created bean instance.
         if (resolvedValue == originalValue) {
            if (convertible) {
               pv.setConvertedValue(convertedValue);
            }
            deepCopy.add(pv);
         }
         else if (convertible && originalValue instanceof TypedStringValue &&
               !((TypedStringValue) originalValue).isDynamic() &&
               !(convertedValue instanceof Collection || ObjectUtils.isArray(convertedValue))) {
            pv.setConvertedValue(convertedValue);
            deepCopy.add(pv);
         }
         else {
            resolveNecessary = true;
            deepCopy.add(new PropertyValue(pv, convertedValue));
         }
      }
   }
   if (mpvs != null && !resolveNecessary) {
      mpvs.setConverted();
   }

   // Set our (possibly massaged) deep copy.
   try {
      【设置属性依赖注入】
      bw.setPropertyValues(new MutablePropertyValues(deepCopy));
   }
   catch (BeansException ex) {
      throw new BeanCreationException(
            mbd.getResourceDescription(), beanName, "Error setting property values", ex);
   }
}
```

根据属性值类型的不同，进行解析resolveValueIfNecessary

```
/**
 * Given a PropertyValue, return a value, resolving any references to other
 * beans in the factory if necessary. The value could be:
 * <li>A BeanDefinition, which leads to the creation of a corresponding
 * new bean instance. Singleton flags and names of such "inner beans"
 * are always ignored: Inner beans are anonymous prototypes.
 * <li>A RuntimeBeanReference, which must be resolved.
 * <li>A ManagedList. This is a special collection that may contain
 * RuntimeBeanReferences or Collections that will need to be resolved.
 * <li>A ManagedSet. May also contain RuntimeBeanReferences or
 * Collections that will need to be resolved.
 * <li>A ManagedMap. In this case the value may be a RuntimeBeanReference
 * or Collection that will need to be resolved.
 * <li>An ordinary object or {@code null}, in which case it's left alone.
 * @param argName the name of the argument that the value is defined for
 * @param value the value object to resolve
 * @return the resolved object
 */
@Nullable
public Object resolveValueIfNecessary(Object argName, @Nullable Object value) {
   // We must check each value to see whether it requires a runtime reference
   // to another bean to be resolved.
   if (value instanceof RuntimeBeanReference) {
      RuntimeBeanReference ref = (RuntimeBeanReference) value;
      return resolveReference(argName, ref);
   }
   else if (value instanceof RuntimeBeanNameReference) {
      String refName = ((RuntimeBeanNameReference) value).getBeanName();
      refName = String.valueOf(doEvaluate(refName));
      if (!this.beanFactory.containsBean(refName)) {
         throw new BeanDefinitionStoreException(
               "Invalid bean name '" + refName + "' in bean reference for " + argName);
      }
      return refName;
   }
   else if (value instanceof BeanDefinitionHolder) {
      // Resolve BeanDefinitionHolder: contains BeanDefinition with name and aliases.
      BeanDefinitionHolder bdHolder = (BeanDefinitionHolder) value;
      return resolveInnerBean(argName, bdHolder.getBeanName(), bdHolder.getBeanDefinition());
   }
   else if (value instanceof BeanDefinition) {
      // Resolve plain BeanDefinition, without contained name: use dummy name.
      BeanDefinition bd = (BeanDefinition) value;
      String innerBeanName = "(inner bean)" + BeanFactoryUtils.GENERATED_BEAN_NAME_SEPARATOR +
            ObjectUtils.getIdentityHexString(bd);
      return resolveInnerBean(argName, innerBeanName, bd);
   }
   else if (value instanceof DependencyDescriptor) {
      Set<String> autowiredBeanNames = new LinkedHashSet<>(4);
      Object result = this.beanFactory.resolveDependency(
            (DependencyDescriptor) value, this.beanName, autowiredBeanNames, this.typeConverter);
      for (String autowiredBeanName : autowiredBeanNames) {
         if (this.beanFactory.containsBean(autowiredBeanName)) {
            this.beanFactory.registerDependentBean(autowiredBeanName, this.beanName);
         }
      }
      return result;
   }
   else if (value instanceof ManagedArray) {
      // May need to resolve contained runtime references.
      ManagedArray array = (ManagedArray) value;
      Class<?> elementType = array.resolvedElementType;
      if (elementType == null) {
         String elementTypeName = array.getElementTypeName();
         if (StringUtils.hasText(elementTypeName)) {
            try {
               elementType = ClassUtils.forName(elementTypeName, this.beanFactory.getBeanClassLoader());
               array.resolvedElementType = elementType;
            }
            catch (Throwable ex) {
               // Improve the message by showing the context.
               throw new BeanCreationException(
                     this.beanDefinition.getResourceDescription(), this.beanName,
                     "Error resolving array type for " + argName, ex);
            }
         }
         else {
            elementType = Object.class;
         }
      }
      return resolveManagedArray(argName, (List<?>) value, elementType);
   }
   else if (value instanceof ManagedList) {
      // May need to resolve contained runtime references.
      return resolveManagedList(argName, (List<?>) value);
   }
   else if (value instanceof ManagedSet) {
      // May need to resolve contained runtime references.
      return resolveManagedSet(argName, (Set<?>) value);
   }
   else if (value instanceof ManagedMap) {
      // May need to resolve contained runtime references.
      return resolveManagedMap(argName, (Map<?, ?>) value);
   }
   else if (value instanceof ManagedProperties) {
      Properties original = (Properties) value;
      Properties copy = new Properties();
      original.forEach((propKey, propValue) -> {
         if (propKey instanceof TypedStringValue) {
            propKey = evaluate((TypedStringValue) propKey);
         }
         if (propValue instanceof TypedStringValue) {
            propValue = evaluate((TypedStringValue) propValue);
         }
         if (propKey == null || propValue == null) {
            throw new BeanCreationException(
                  this.beanDefinition.getResourceDescription(), this.beanName,
                  "Error converting Properties key/value pair for " + argName + ": resolved to null");
         }
         copy.put(propKey, propValue);
      });
      return copy;
   }
   else if (value instanceof TypedStringValue) {
      // Convert value to target type here.
      TypedStringValue typedStringValue = (TypedStringValue) value;
      Object valueObject = evaluate(typedStringValue);
      try {
         Class<?> resolvedTargetType = resolveTargetType(typedStringValue);
         if (resolvedTargetType != null) {
            return this.typeConverter.convertIfNecessary(valueObject, resolvedTargetType);
         }
         else {
            return valueObject;
         }
      }
      catch (Throwable ex) {
         // Improve the message by showing the context.
         throw new BeanCreationException(
               this.beanDefinition.getResourceDescription(), this.beanName,
               "Error converting typed String value for " + argName, ex);
      }
   }
   else if (value instanceof NullBean) {
      return null;
   }
   else {
      return evaluate(value);
   }
}
```