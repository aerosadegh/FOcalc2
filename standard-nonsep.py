from diff import diff

#import click
from time import time
from mpmath import mp,exp,factorial,cos,pi
# mpmath Option
mp.dps = 6; mp.pretty = True

from datetime import datetime

def um(x,t):
    return exp(-x) * exp(-.1*t) # exact

def mul(a,b,Acc = 5):
    r =[]
    if type(b) != type(list):
        for i in range(len(a)):
            r += [round(a[i]*b,Acc+1)]
        return r
    if len(a) != len(b):
        raise "len of list is'nt same."
    
    for i in range(len(a)):
        r += [round(a[i]*b[i],Acc+1)]
    return r

def add(a,b,Acc = 5):
    r =[]
    for i in range(len(a)):
        r += [round(a[i]+b[i],Acc+1)]
    return r

def fltr(l):
    g = [l[0]]
    for i in range(1,len(l)-1):
        g += [(2*l[i] + l[i-1] + l[i+1])/4]
    g += [l[-1]]
    return g
####  Input

a = 0
b = 30
h = .1
dt = .01 * h


n = 4   # Term {i}


x = [i*h for i in range(a,b)]
T0=1
p0 = [x[i]/(x[i]**2 + T0) for i in range(len(x))]

t = 1
U0 = [x[i]/(x[i]**2 + T0+t) for i in range(len(x))]


####  Calc.
t1 = time()
nt = (round(t/dt) if t>dt else 1)
#with click.progressbar(range(nt),label=' Step(s) to arrive t:',show_pos=True,fill_char="█") as bar:
for j in range(nt):
    p = [] ; U2 = []
    p += [p0]
    U2 += p0
    tt = T0+j*dt
    for i in range(1,n+1):
        A = -x[i] / (x[i]**2-tt)
        B = (x[i]**2+tt)/(x[i]**2 - 3*tt)
        p1 = p[i-1]
        p += [add( mul(diff(p1,h),A) , mul(diff(p1,h,2),B) )]
        U2 = add( U2, mul(p[-1] , (dt**i)/factorial(i) ) )
    p0 = []
    p0 += U2

t2 = time()
    
print("pass: t = {:}, \nTook: {:8.1f}".format(round(nt*dt,4), t2-t1))

U0[0]=U2[0]
prn1 = '{:^5.2f}   |{:^8.4f}|{:^8.4f}|%{:<8.2f}'
for i in range(len(U0)):
    print(prn1.format(x[i], U0[i], U2[i] , (U2[i]-U0[i])/U0[i]*100))


import matplotlib.pyplot as plt
fig = plt.figure()
P1 = plt.plot(x[5:], U0[5:], 'ro')
P2 = plt.plot(x[5:], U2[5:])
plt.show()
fig.savefig("Results/{:}-{:}-({:}-{:}).JPG".format(a,b,T0,T0+round(nt*dt,4)),dpi=200)

############   write in file
f = open("Results/{:}-{:}-({:}-{:}).out".format(a,b,T0,T0+round(nt*dt,4)),"w")
#f.write(prn.format('Xpoint',"0.Exact","1.Interp.","2.Discrt." , "Err_1,0_" ,"Err_2,0_" ,"Err_1,2_" , w = 13))
#f.write('-'*105+"\n")
for i in range(len(U0)):
    f.write(prn1.format(x[i],
                        U0[i],
                        U2[i],
                        round((U2[i]-U0[i])/U0[i]*100,2)))
    f.write('\n')
f.write('-'*45+"\n")
f.write("Time took:"+" "*18+'| {:^{w}.5}(s)| '.format(t2-t1,w=10))
f.close()

