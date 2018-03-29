#coding=utf-8
class Base(object):
    def __init__(self,num):
        self.num = num

class Test(Base):
    def __init__(self,num):
        num+=2

        #python3中
        #super().__init__(num)
        #python2/python3都可以
        super(Test,self).__init__(num)
        #python2/python3都可以
        Base.__init__(self,num)


a = Test(100)
print(a.num)
