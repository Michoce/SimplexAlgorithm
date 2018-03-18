import numpy as np

class QTable():
    def __init__(self,cT,A,b,xB):
        self.cT = cT
        self.A = A
        self.b = b
        self.xB = xB
    def getcB(self):
        di = self.xB.shape
        cB = np.zeros(di)
        [rows, cols] = self.xB.shape
        for i in range(rows):
            cB[i,:] = self.cT.T[int(self.xB[i,:]),:]
        return cB
    def get_z(self):
        _z = self.cT - self.getcB().T*self.A
        return _z
    def __str__(self):
        return 'cT:\n'+ str(self.cT)\
                +'\nA:\n' + str(self.A)\
                +'\nb:\n' + str(self.b)\
                +'\nxB:\n'+ str(self.xB+ 1) \
                +'\ncB:\n' + str(self.getcB())\
                +'\n-z:\n' + str(self.get_z())






def AConv(qt,X,Y):
    A_X_Y = qt.A[X,Y]
    qt.A[X,:] = qt.A[X,:]/A_X_Y
    qt.b[X,:] = qt.b[X,:]/A_X_Y
    for i in range(qt.A.shape[0]):
        if i != X:
            A_i_Y = qt.A[i,Y]
            qt.A[i,:] = qt.A[i,:] - qt.A[X,:]*A_i_Y
            qt.b[i,:] = qt.b[i,:] - qt.b[X,:]*A_i_Y
    return qt




def tableMethod(qt):
    #qt = tableMethod_Step(qt)
    #print(qt)


    #zero = np.zeros(qt.get_z().shape)
    while  np.max(qt.get_z()) > 0 :
        qt = tableMethod_Step(qt)
        print(qt)
        print('')
    #print(qt)

def reciprocal(vt):
    MAXNUM = 2**12
    flag = False
    re = np.zeros(vt.shape)
    for i in range(vt.shape[0]):
        if vt[i,:] <= 0:
            re[i,:] = np.array([MAXNUM])
        else:
            re[i,:] = 1/vt[i,:]
            flag = True
    if flag != True:
        print('!!!!!!!!!!!!!!!!!!!!!!!某改!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    return re

def tableMethod_Step(qt):
    cB = qt.getcB()
    #print('cB:\n',cB)
    _z = qt.get_z()
    #print('_z:\n',_z)
    #-z最大的x的数组下标
    maxx = np.argmax(_z)
    #print('maxx:\n',maxx)
    #-z最大的那一列的倒数
    Amaxx_reciprocal =  reciprocal(qt.A[:,maxx])
    #print('Amaxx_reciprocal:\n',Amaxx_reciprocal)
    #最小的要被换的,xb 表格的位置(数组下标)
    xBi = np.argmin(  np.multiply( qt.b,(Amaxx_reciprocal) )  )
    print('xBi:\n',xBi)
    qt.xB[xBi] = maxx
    X = xBi#3-下标2
    Y = maxx#2- 下标1
    qt = AConv(qt,X,Y)
    return qt




if __name__ == '__main__':
    M = 2**16 + 0.
    cT1 = np.mat([0.,0.,0.,0.,0.,0.,-1.])
    cT2 = np.mat([2.,-1.,1.,0.,0.,0.])

    A = np.mat([[1.,1.,-2.,1.,0.,0.,0.]
               ,[4.,-1.,1.,0.,1.,0.,0.]
               ,[2.,3.,-1.,0.,0.,-1.,1.]])
    b = np.mat([[8.]
               ,[2.]
               ,[4.]])
    xB = np.mat([[3]
                ,[4]
                ,[6]])


    qt_1 = QTable(cT1,A,b,xB)
    print('_z:' , qt_1.get_z(), '\n' )
    tableMethod(qt_1)
    print('------------------------------------')
    qt_2 = QTable(cT2,qt_1.A[:,:-1],qt_1.b,qt_1.xB)
    print('_z:' , qt_2.get_z(), '\n' )
    tableMethod(qt_2)



'''
cT = np.mat([1500.,2500.,0.,0.,0.])
A = np.mat([[3.,2.,1.,0.,0.]
           ,[2.,1.,0.,1.,0.]
           ,[0.,3.,0.,0.,1.]])
b = np.mat([[65.]
           ,[40.]
           ,[75.]])
xB = np.mat([[2.]
            ,[3.]
            ,[4.]])
'''
