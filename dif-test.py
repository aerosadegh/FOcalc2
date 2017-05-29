from coeff import coeff
from mpmath import exp , mp , mpf ,sqrt
mp.pretty = True


from pylab import plot,show,title
from numpy import linspace


h = .1
s = [mpf((f * h)**3) for f in range(1,50)]



#   first diff
Ord = 1; acc = 1 ; 
##j = 19
ds = []
n =  len(s) - acc - Ord + 1
for j in range(n):
    ds += [sum(coeff[Ord].get(acc)[i] * s[i+j] for i in range(acc + Ord))/h**Ord]
    ds[-1] = round(ds[-1] , 2*acc)
##for j in range(n, len(s)-Ord):
##    ds += [ds[-1]]
if acc > 1:
    for j in range(n, len(s)-Ord):
    #   ds += [ds[-1]]
        acc = acc-1
        ds += [sum(coeff[Ord].get(acc)[i] * s[i+j] for i in range(acc + Ord)) / h**Ord]
        ds[-1] = round(ds[-1] , 2*acc)
for j in range(len(s)-Ord,len(s)):
    ds += [ds[-1]]


#mp.dps = 6

print ((s[0])**(1/3) , s[0] , ds[0])


xpoints = []
ypoints = []
ypoints += ds
for x in range(1,len(s)+1):
    xpoints += [x*h]
    
plot(xpoints, ypoints)
title('forward diff ord {:} with accuracy {:}'.format(Ord,acc))
show()
