from coeff import coeff
from mpmath import mp , mpf # , exp,sqrt
from mpmath import diff as mpdiff
mp.pretty = True

try:
    import matplotlib.pyplot as plt
except:
    print('mathplotlib error!!!')

def _g(x):
    return x**4


def diff(s , dx , Ord = 1 , Acc = 6):
    ''' s -> 1D List of ypoints , dx -> Step of xpoint.'''
    ds = []
    n = len(s) - Acc - Ord + 1
    for j in range(n):
        ds += [sum(coeff[Ord].get(Acc)[i] * s[i+j] for i in range(Acc + Ord)) / dx**Ord]
        ds[-1] = round(ds[-1] , 2*Acc)    # Round to 2*Acc digit after point
    if Acc > 1:
        for j in range(n, len(s)-Ord):
    #        ds += [ds[-1]]
            Acc = Acc-1
            ds += [sum(coeff[Ord].get(Acc)[i] * s[i+j] for i in range(Acc + Ord)) / dx**Ord]
            ds[-1] = round(ds[-1] , 2*Acc)
    for j in range(len(s)-Ord,len(s)):
        ds += [ds[-1]]
    return ds


if __name__ == "__main__":        
    h = .1
    s = [mpf((f * h)**4) for f in range(1,20)]
    sd = diff(s, h,2)
    ds = [mpdiff(_g,(f * h),2) for f in range(1,20)]
    xpoints = [(f * h) for f in range(1,20)]
    yp1 = [] ; yp1 += sd
    yp2 = [] ; yp2 += ds
    p1 = plt.plot(xpoints ,yp1,"ro" )
    p2 = plt.plot(xpoints ,yp2 )
    plt.legend((p1[0], p2[0]), ('num', 'exct'),loc="best")
    plt.title("x**4 derivation {:} with accuracy {:}".format(2,5))
    plt.show()
    
##    print("sample f(x)=x^3 :\n", 'num exct err\n',"-----------")
##    for i in range(len(s)):
##        print(sd[i] , ds[i] , round(sd[i] - ds[i],5))
    


