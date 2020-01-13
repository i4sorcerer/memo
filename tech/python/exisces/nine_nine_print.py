#打印9*9乘法表
def print9x9Table():
    for row in range(1,10,1):
        for col in range(1,row+1,1):
            print(str(row) + '*' + str(col) + '=' + str(row*col),end='\t')
        print('')
if __name__=='__main__':
    print('#########9*9乘法表打印############')
    print9x9Table()
    
