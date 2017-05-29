'''Interpoltion Class'''

from mpmath import *
# mpmath Option
#mp.dps = 5;
mp.pretty = True


class Interpoltion:
    def __init__(self, xi , fi):
        """x_i , f_i"""
        self.xi = xi
        self.fi = fi
        self._ls = []

    def _C(s, k):
        s = mpf(s)
        if s-k < 0 and s-int(s) == 0: return 0
        return fac(s) / ( fac(k) * fac(s - k) )
##        return binomial(s,k)

    def _prd(l):
        p = 1
        for c in l:
            p *= c
        return p
##----------------------------------

    def _f(self,x):
        return self.fi[self.xi.index(x)]

    def _L(self,j,x):
        n = len(self.xi) 
        lst = [ mpf(x          - self.xi[i]) for i in range(n)]
        lmj = [ mpf(self.xi[j] - self.xi[i]) for i in range(n)]
        lst.pop(j)
        lmj.pop(j)
        return Interpoltion._prd(lst)/Interpoltion._prd(lmj)

    def _dv(self,l):
        if len(l) == 1 :
            return self._f(l[0])
        rev = ( self._dv(l[1:]) - self._dv(l[:-1]) ) / ( l[-1] - l[0] )
        self._ls += [mpf(rev)]
        return rev

    def _fr(self,l):
        if len(l) == 1 :
            return self._f(l[0])
        rev = ( self._fr(l[1:]) - self._fr(l[:-1]) )
        self._ls += [mpf(rev)]
        return rev

    def _bk(self,l):
        if len(l) == 1 :
            return self._f(l[0])
        rev = -( self._bk(l[:-1]) - self._bk(l[1:]) )
        self._ls += [mpf(rev)]
        return rev

    def Lagrange_Func(self,x=None):  
        '''calculate p(x) function.'''
        n = len(self.xi)
        px = lambda x: sum( self.fi[i] * self._L(i,x) \
                    for i in range(n) )
        if x!=None :
            return px(x)
        return px

    def DifferDivision_Newton_Func(self,x=None):  
        '''calculate p(x) function.'''
        self._ls = []
        self._dv(self.xi)
        fc = [self._f(self.xi[0])] + self._ls[ -(len(self.xi) - 1) :]
        n = len(fc)
        h = abs(self.xi[1] - self.xi[0])
        px = lambda x: sum( fc[i] * \
                            Interpoltion._prd([x - self.xi[j] for j in range(i)] )\
                            for i in range(n) )        
        if x!=None :
            return px(x)
        return px

    def DifferForward_Newton_Func(self,x=None):
        '''calculate p(x) function.'''
        self._ls = []
        self._fr(self.xi)
        fc = [self._f(self.xi[0])] + self._ls[ -(len(self.xi) - 1) :]
        n = len(fc)
        h = abs(self.xi[1] - self.xi[0])
        px = lambda x: sum( fc[i] * \
                            Interpoltion._C((x - self.xi[0]) / h, i) for i in range(n) )        
        if x!=None :
            return px(x)
        return px

    def DifferBackward_Newton_Func(self,x=None):
        '''calculate p(x) function.'''
        self._ls = []
        self._bk(self.xi)
        fc = [self._f(self.xi[-1])] + self._ls[ -(len(self.xi) - 1) :]
        n = len(fc)
        h = abs(self.xi[1] - self.xi[0])
        px = lambda x: sum( (-1)**i * fc[i] * \
                            Interpoltion._C(-(x - self.xi[-1]) / h, i) for i in range(n) )        
        if x!=None :
            return px(x)
        return px

