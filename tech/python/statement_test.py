#各种常用语句测试

#全局作用域
str_x='global str'


def if_test():
    print('-----if test-----')
    a=[1,2,4,5]
    b=[1,2,3]
    #if满足的情况
    if a == b:
        print('a==b')
    #else if的情况
    elif len(a)==len(b):
        print('a!=b but len(a)==len(b)')
    #以上条件都不满足的情况
    else:
        print('a!=b and len(a)!=len(b)')
    str_x = 'block str'
    global str_y
    str_y = 'block if_test str y'
    print('str_x:' + str_x)
    print('str_y:' + str_y)
def loop_while_test():
    #while test
    print('----------while test-------------')
    condition = 'strtest'
    idnexCnt=1
    while len(condition) > 0:
        print('index:' + str(idnexCnt) + condition)
        condition=condition[:-1]
        idnexCnt+=1
    else:
        #while else`语句是可选的
        print('while else statemnt exec.')
    str_y = 'block loop_while_test str y'
    print('str_y:' + str_y)
def map_test():
    print('------map test-------')
    a=[1,210,100]
    map((lambda x:print(x+1)),a)
    print(a)
    
          
if __name__ == '__main__':
    print('****************this is main start*************')

    map_test()
    #if_test()
    #loop_while_test()
    print('****************this is main end***************')
    
