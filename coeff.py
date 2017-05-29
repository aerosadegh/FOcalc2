from mpmath import mp,mpf
# mpmath Option
mp.pretty = True

f = open('df-coeff.txt')
st = f.read().split("\n")

ln = len(st)
i = 0
li = 1
coeff = {}

while i<4:
    i += 1
    li += 1
    if li>=len(st): break
    ls = {}
    while len(st[li])>1:
        tm = st[li].split(' ')
        dm = {int(tm[0]) : [mpf(tm[i])for i in range(1,len(tm)) ]}
        li += 1
        ls.update(dm.copy())
        if li>=len(st): break   
    coeff.update({i : ls})


if __name__ == "__main__":
    for j in range(1,5):
        print(j)
        for k in range(1, 1+len(coeff[j].keys()) ):
            print(coeff[j].get(k)) 
