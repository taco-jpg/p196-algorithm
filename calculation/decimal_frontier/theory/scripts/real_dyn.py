"""Real-number (h,l) description of exterior B-cycles (limit g->infinity).
X_t = low digit string of N_t (x_0,x_1,...), Y_t = top digit string (y_0 = leading digit).
h = sum y_i b^-i, l = sum x_i b^-i, V = h+l = sum_i P_i b^-i  with P = B ++ (b-1)^inf.
"""
import sys
from fractions import Fraction as F
sys.path.insert(0,'..')
import mirror as m, lib
from parse_bw import parse_bw

def frac_of(b, digits, tail):
    """sum digits[i] b^-i + tail * sum_{i>=len} b^-i"""
    v=F(0)
    for i,d in enumerate(digits): v+=F(d,b**i)
    n=len(digits)
    v+=F(tail,b**n)*F(b,b-1)
    return v

def XY_of_next(b,B):
    """digit strings (finite part, tail digit) of N_{t+1} given B_t: X (low), Y (top first)"""
    e1=m.e1(b,B); e2=1-e1
    DBv=m.DB(b,B); DRv,gm=m.norm(b,B[::-1],e2)
    xd=(b-1)*(1-e1); yd=(b-1)*e1
    X=list(DBv); Y=([1] if gm else [])+DRv[::-1]
    return X,xd,Y,yd,e1,gm

def analyse(b,Bs,verbose=True):
    p=len(Bs); G=0; prod=F(1)
    rows=[]
    for t in range(p):
        X,xd,Y,yd,e1,gm=XY_of_next(b,Bs[t])      # this is N_{t+1}
        l=frac_of(b,X,xd); h=frac_of(b,Y,yd)
        rows.append((t+1,e1,gm,l,h))
    # N_{t+1} has h_{t+1}, l_{t+1}; V_t = h_t + l_t (pair word of N_t = B_t ++ band)
    V=[]
    for t in range(p):
        Bt=Bs[t]
        Vt=sum(F(c,b**i) for i,c in enumerate(Bt))+F(b-1,b**len(Bt))*F(b,b-1)
        V.append(Vt)
    out=[]
    for t in range(p):
        # N_t has (h_t,l_t) = rows[t-1]
        tt,e1p,gmp,lt,ht=rows[(t-1)%p]
        out.append((t,ht,lt,V[t]))
    return out,rows,V

if __name__=="__main__":
    for line in open(sys.argv[1]):
        if 'ACCEPT' not in line: continue
        b,p,g,e,Bs=parse_bw(line)
        out,rows,V=analyse(b,Bs)
        prod=F(1); G=0
        print("b",b,"p",p,"g",g,"e",e)
        for t,(tt,ht,lt,Vt) in enumerate(out):
            gm=int(g[t]); 
            assert ht+lt==Vt,(t,float(ht),float(lt),float(Vt))
            r=Vt/ht
            prod*=r
            # next h
            hn=out[(t+1)%p][1]
            assert hn==Vt/b**gm,(t,float(hn),float(Vt/b**gm))
            print(f"t={t} gam={gm} e1={e[t]} h={float(ht):.5f} l={float(lt):.5f} V={float(Vt):.5f} ratio={float(r):.5f} rho={float(lt/ht):.5f}")
        print("product of ratios",prod,"b^G",b**sum(int(c) for c in g))
