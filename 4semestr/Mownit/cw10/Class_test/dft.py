from numpy import matrix, array, sin, cos, mgrid, arange,real
from numpy.fft import fft
from cmath import exp, pi
from timeit import default_timer as time
from fft import fft as fft2
import matplotlib.pyplot as plt


N = 2**10
#x = matrix([[exp(-2j*pi*(i+1)*(k+1)/N)for i in range(N)] for k in range(N)])
u = mgrid[0:10*pi:0.3]
x=real(10*sin(10*u) + 8*sin(8*u) - 7*cos(7*u))
y = 10*sin(10*u)
y = y.tolist()
y.append((8*sin(8*u)).tolist())
y.append( (7*cos(7*u)).tolist())
#y= array(10*sin(10*u) , 8*sin(8*u) , 7*cos(7*u))
print(x)
#y = array([1 for x in range(N)])
#start = time()
#(list(zip(*x.dot(y).tolist())))
#first = time()
#(fft(y))
#second = time()
plt.plot((fft(y)), u)
plt.show()
end = time()

