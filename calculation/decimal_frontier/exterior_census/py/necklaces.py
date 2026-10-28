import sys
def necklaces(p):
    out=[]
    for m in range(1<<p):
        w=format(m,'0%db'%p)[::-1]  # position t = bit t
        # canonical = lexicographically minimal rotation of string w
        if all(w<=w[r:]+w[:r] for r in range(1,p)): out.append(w)
    return out
if __name__=='__main__':
    p=int(sys.argv[1])
    for w in necklaces(p): print(w)
