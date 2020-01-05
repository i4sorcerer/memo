
#设置常数
CONST_STR2='方法参数默认值'
CONST_STRIP_STR=';'
CONST_STRIP_STR_SPACE=' '
CONST_STR_CHAR_AT='@'


def number_test(a,b):
    #数字类型
    print('hello world python.')
    c=a+b
    print("a + b :" + str(c))

def string_test(str1, str2=CONST_STR2):
    #测试是否支持默认值
    print('测试字符串操作')
    #从指定字符串的前后替换指定的字符
    str=str1.strip(CONST_STRIP_STR_SPACE)+str2.strip(CONST_STRIP_STR_SPACE)

    str_3quote="""this is test 三个引号的字符串
这是同一个字符串"""
    print('['+str_3quote+']')

    #字符串重复
    str_repeat=CONST_STR_CHAR_AT*10
    print(str_repeat)

    #字符串索引
    str_index='test123index456='
    print(str_index[0])
    print(str_index[1])
    print(str_index[len(str_index)-1])
    #字符串分片
    str_split='this is test for python split.'
    print(str_split[1:4])
    #格式化字符串
    str_format="a %s people" %'dying'
    print(str_format)

    #迭代关系
    for x in str_repeat[0:2]:
        print(x,end='\t')

    #in操作符
    if '@' in str_repeat:
        print ('@ in str_repeat')

    #分片提取片段
    str_divid_test='zaq12wsxcde34rfvbgt5'
    print('str_divid_test[0:4]'+str_divid_test[0:4])
    print('str_divid_test[10:]'+str_divid_test[10:])
    print('str_divid_test[:-1]'+str_divid_test[:-1])
    
    #字符串输出
    print(str)

#字典使用测试
def hash_test():
    print('hash test')
    lang={'java':'java language','python':'python language','C#':'C#language'}
    str_lang='python'
    print(lang[str_lang])
    print('----遍历所有的key-----:')
    for k in lang.keys():
        print('key:'+ k + ',value:' + lang[k])
    
#当前module的主函数
if __name__ == '__main__':
    number_test(1,999.999)
    string_test(';hello;', ';自定义参数;')
    hash_test()

    print('module name:' +__name__)



