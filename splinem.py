#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 20:57:37 2016

@author: msadegh
"""
#from math import sqrt,exp

from mpmath import mp , mpf
# mpmath Option
mp.dps = 6; mp.pretty = True
import numpy as np


class Spline:
    def __init__(self,x=[0],u=[0]):
        self.x = x
        self.u = u
        self.n = len(x)
        n = len(x)
        fpi = []
        for i in range(1,n-1):
            if (u[i]-u[i-1])==0 or (u[i+1]-u[i])==0:
                fpi += [0]
            else:
                fpi += [2/( ( (x[i+1]-x[i]) / (u[i+1]-u[i]) ) +\
                      ( (x[i]-x[i-1]) / (u[i]-u[i-1]) )  )]
                               
        fp0 = 3/2*(u[1]-u[0])/(x[1]-x[0]) - fpi[0]/2
        fpn = 3/2*(u[-1]-u[-2])/(x[-1]-x[n-2]) - fpi[-1]/2
        
        fp = [fp0] +  fpi + [fpn]
        del fp0 , fpn , fpi
        
        fzp = [-(2*(fp[i]+2*fp[i-1])/(x[i]-x[i-1])) +\
                    (6*(u[i]-u[i-1])/(x[i]-x[i-1])**2) for i in range(1,n)]
        fzn = [(2*(2*fp[i]+fp[i-1])/(x[i]-x[i-1])) -\
                    (6*(u[i]-u[i-1])/(x[i]-x[i-1])**2) for i in range(1,n)]
        
        d = [(fzn[i]-fzp[i])/(6*(x[i+1]-x[i])) for i in range(n-1)]   
        c = [(x[i+1]*fzp[i] - x[i]*fzn[i])/(2*(x[i+1]-x[i])) for i in range(n-1)]
        b = [((u[i+1] - u[i])-\
              c[i]*(x[i+1]**2-x[i]**2)-\
        d[i]*(x[i+1]**3-x[i]**3))/(x[i+1]-x[i]) for i in range(n-1)]
        
        a = [u[i] - b[i]*x[i] - c[i]*x[i]**2 - d[i]*x[i]**3 for i in range(n-1)]      
        
        self._f = [((a[i],b[i],c[i],d[i]),(x[i],x[i+1])) for i in range(n-1)]
 
    def F(self , x):
        l = self._f
        for c , r in l:
            if r[0] <= x <= r[1]:
                px = lambda x: c[0] + c[1]*x + c[2]*x**2 + c[3]*x**3
                return px(x)
                
    def F2(self,x=None):
        l = self._f
        h = .1 ; pr = 0
        i = len(l)
        r , c = l[0]
        st = 'p{i} = lambda x: None\n'.format(i = i)
        for c , r in l:
            pr = h if i == len(l) else 0
            pe = h if i== 1 else 0
            i -= 1
            st += '''p{i} = lambda x: {a} +{b}*x + {c}*x**2 + {d}*x**3 if \
mpf({r0}-{pr}) <= x <= mpf({r1}+{pe}) else p{ip}(x)\n'''.format(a=c[0],
b=c[1],
c=c[2],
d=c[3],
r0=r[0],
r1=r[1],
pr=pr,pe=pe,i=i,ip=i+1)
        f = open('p.py','w')
        f.write('from mpmath import *\n'+st)
        f.close()
        import p
        if x== None:
            return p.p0
        return p.p0(x)
            
        


                
if __name__ == "__main__"                :
    ############ inp 1 ######################
    a = 0
    b = 15
    h = .1
    
    x = [mpf(i)*h for i in range(a,b)]
    sq2 = np.sqrt(2)     
    u = [exp(i/sq2) for i in x]
         
    Fe = lambda x: exp(x/sq2)
    ############# inp 2 #####################
    #x0 = [0 , 10, 30, 50, 70, 90, 100]
    #x = [mpf(i) for i in x0]
    #     
    #u = [30,130,150,150,170,220, 320]
    #####################################
    a = Spline(x,u)  



