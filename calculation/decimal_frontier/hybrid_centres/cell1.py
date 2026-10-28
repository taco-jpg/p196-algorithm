from runsat import stream
import sys
def cell1(b, gam, e1):
    p=len(gam); N=b-1; R=2*b-1
    edges={}
    for ph in range(p):
        a=e1[ph]
        for v in range(R):
            for din in (0,1):
                if ((v+din)>=b)!=bool(1-a): continue
                da=(v+a)%b; dd=(v+din)%b
                vn=da+(N*a if gam[ph] else dd)
                if vn>2*b-2: continue
                edges.setdefault((v,ph),set()).add((vn,(ph+1)%p))
    return edges
def analyze(name):
    cyc=stream(name); p=len(cyc); b=10
    gam=[cyc[t][1] for t in range(p)]; e1=[cyc[t][2] for t in range(p)]
    E=cell1(b,gam,e1)
    nodes=set(E)|{w for s in E.values() for w in s}
    # backward reach to v==9
    rev={}
    for u,s in E.items():
        for w in s: rev.setdefault(w,set()).add(u)
    target={n for n in nodes if n[0]==9}
    seen=set(target); st=list(target)
    while st:
        x=st.pop()
        for y in rev.get(x,()):
            if y not in seen: seen.add(y); st.append(y)
    # nodes that are on infinite paths avoiding... 
    print(name,'gam',gam,'e1',e1)
    print(' nodes',len(nodes),' can-reach-9:',len(seen),' (incl. 9 nodes', len(target),')')
    for ph in range(p):
        pop=sorted(n[0] for n in seen if n[1]==ph and n[0]!=9)
        allv=sorted(n[0] for n in nodes if n[1]==ph)
        print('  phase',ph,'gam',gam[ph],'e1',e1[ph],'poppers(non9):',pop,' all consistent v:',allv)
analyze('p11'); analyze('p12')
