from diff import *
from percise1 import um , Up
import click
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
b = 15
h = .1
dt = .01 * h

A = 1/20
B = -1/20

n = 4   # Term {i}


x = [i*h for i in range(a,b)]
p0 = [exp(-x[i]) for i in range(len(x))]

t = 0.5

####  Calc.
t1 = time()
nt = (round(t/dt) if t>dt else 1)
with click.progressbar(range(nt),label=' Step(s) to arrive t:',show_pos=True,fill_char="█") as bar:
    for j in bar:
        p = [] ; U2 = []
        p += [p0]
        U2 += p0
        for i in range(1,n+1):
            p1 = p[i-1]
            p += [add( mul(diff(p1,h),A) , mul(diff(p1,h,2),B) )]
            U2 = add( U2, mul(p[-1] , (dt**i)/factorial(i) ) )
        p0 = []
        p0 += U2    
t2 = time()
    
print("pass: t = {:}".format(round(nt*dt,4)))
    

U1 = []
U0 = []
with click.progressbar(range(len(x)),label=' Calc U(x_i, t) i-th:',show_pos=True,fill_char="█") as bar:
    for i in bar:
        U1 += [Up(x[i],round(nt*dt,4))]
        #print(c)
        U0 += [um(x[i],round(nt*dt,4))]

t3 = time()
U1 = fltr(U1)
U2 = fltr(U2)

##########  print in consol

prn = "{:^{w}}| "*7
prn1 = '{!s:^{w}}| {!s:^{w}}| {!s:^{w}}| {!s:^{w}}| %{:<{w1}}| %{:<{w1}}| %{:<{w1}}|'
print(prn.format('Xpoint',"0.Exact","1.Interp.","2.Discrt." , "Err_1,0_" ,"Err_2,0_" ,"Err_1,2_" , w = 13,w1 = 8))
print('-'*105)

for i in range(len(U0)):
    print(prn1.format(mpf(x[i]),
                    U0[i],
                    U1[i],
                    U2[i],
                    round((U1[i]-U0[i])/U0[i]*100,2),
                    round((U2[i]-U0[i])/U0[i]*100,2),
                    round((U1[i]-U2[i])/U0[i]*100,2),
                    w =13,w1=12))
    
print('-'*105)
print("Time took:"+" "*18+'| {:^{w}.5}(s)| {:^{w}.5}(s)|'.format(t3-t2,t2-t1,w=10))
print('Program took {:.5} s.'.format(t3-t1))


############   write in file
prn = prn + "\n"
prn1= prn1+ "\n"
f = open("R ({:},{:},{:}) & t={:}.out".format(a,b,h,round(nt*dt,4)),"w")
f.write(prn.format('Xpoint',"0.Exact","1.Interp.","2.Discrt." , "Err_1,0_" ,"Err_2,0_" ,"Err_1,2_" , w = 13))
f.write('-'*105+"\n")
for i in range(len(U0)):
    f.write(prn1.format(mpf(x[i]),
                        U0[i],
                        U1[i],
                        U2[i],
                        round((U1[i]-U0[i])/U0[i]*100,2),
                        round((U2[i]-U0[i])/U0[i]*100,2),
                        round((U1[i]-U2[i])/U0[i]*100,2),
                        w =13,w1=12))
f.write('-'*105+"\n")
f.write("Time took:"+" "*18+'| {:^{w}.5}(s)| {:^{w}.5}(s)|'.format(t3-t2,t2-t1,w=10))
