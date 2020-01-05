#python中的类使用
#计算器类
class Calculator:
    def setData(self,x):
        self.data=x
    def toString(self):
        print(self.data)

#类的继承 父类于子类
#方法的继承，方法的重载，多态？？？
#面向对象编程的三大特点：继承，多态，封装

class Calculator2(Calculator):

    def toString(self):
        print("second " + str(self.data))    
    
if __name__=='__main__':
    c1=Calculator()
    c1.setData(11)
    c1.toString()

    c2=Calculator2()
    c2.setData(4444)
    c2.toString()
