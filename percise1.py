from splinem import Spline as _Spline
from Interpoltion_Class import Interpoltion as _ic
from mpmath import diff,mp,mpf,exp,factorial,cos,pi
# mpmath Option
mp.dps = 6; mp.pretty = True

from datetime import datetime

####  Inp_ut

_a = 0
_b = 15

_A = lambda x: 1/20
_B = lambda x: -1/20

_n = 4   # Term {i}
_h = .1

_x = [i*_h for i in range(_a,_b)]
_ux = [exp(-_x[i]) for i in range(_a,_b)]


####  Calc.


def Dif(f, x, n=1, Acc= 6):
    h = 1/10**Acc
    if mpf(x) in _x or x in _x:
        return diff(f,x-h,n)/2+diff(f,x+h,n)/2
    return diff(f,x,n)
    

#_p0 = _Spline(_x,_ux).F2()
_p0 = _ic(_x, _ux).Lagrange_Func()

_k0 = lambda t: 1

for i in range(1,_n+1):
    exec('''_k{ii} = lambda t: (t**{ii})/factorial({ii}) '''.format(ii = i))
    exec('''_p{ii} = lambda x: (_A(x)*{diff}(_p{ji},x) + _B(x)*{diff}(_p{ji},x,2))'''.format(ii = i,
         ji = i-1,diff = 'diff'))
    

def um(x,t):
    return exp(-x) * exp(-.1*t) # exact

def Up(x , t):
    global _n
    y =[]
    for i in range(_n+1):
        y += [eval("_p{ii}({x})*_k{ii}({t})" .format(ii = i,x=x,t=t))]
    return sum(y)
