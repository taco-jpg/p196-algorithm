"""Exact contradictory carry inequalities for sole exceptional masks."""
from fractions import Fraction
EX={'rec0':((23,68,113,158),(0,17,0),(1,9,1)),
    'rec1':((33,78,103,148),(0,7,1),(1,19,0))}
def contradiction(name,mask,U,V,source,D,carry_function):
    wanted,hi,lo=EX[name]
    assert tuple(mask)==wanted
    C=[]
    for row in source:
        a,d=carry_function(row);C.append([list(a),list(d)])
    for z in mask:C[(z%160)//20][z//160][z%20]^=1
    u=list(U);v=list(V)
    def gate(t,j,out):
        cin=C[t][1][j]
        assert C[t][1][(j-1)%20]==out
        if out==0:return D-u[j],-v[j]-D*(1+cin)
        return u[j]-D,v[j]+D*cin
    s,c=gate(*hi)
    assert s<0
    upper=Fraction(c,-s)
    u=[u[j]+u[(j-1)%20]-D*(C[0][0][(j+1)%20]+C[0][1][(j-2)%20]) for j in range(20)]
    v=[v[j]+v[(j-1)%20]+D*(C[0][0][j]+C[0][1][(j-1)%20]) for j in range(20)]
    s,c=gate(*lo)
    assert s>0
    lower=Fraction(-c,s)
    assert upper==Fraction(13986001,4812871)
    assert lower==Fraction(31706572,2202637)
    assert lower>upper
    return True
