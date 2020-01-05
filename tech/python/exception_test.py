#异常处理
class MyError(BaseException):
    def test():
        print('test error')

#模块内全局变量
#myError='my test error'

def except_test(val):
    print('except test----')

    if val < 0:
        raise MyError
    else:
        print('the value is ' + str(val))

if __name__ == '__main__':
    print('**********异常处理测试开始**************')

    try:
        except_test(-1)
    except MyError:
        print('myError catch successfully.')
    finally:
        print('except_test finally')
    print('**********异常处理测试结束**************')
    
