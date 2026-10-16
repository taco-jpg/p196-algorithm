from novel_projective_core import edges
from novel_projective_clock import analyze
import json

def canonical(a):
    a=tuple(a)
    return min(a[i:]+a[:i] for i in range(len(a)))

def enumerate_clocks(p,g):
    out=set()
    def dfs(start,path,h):
        if h>g or h+p-len(path)+1<g:return
        if len(path)==p:
            for v,c in edges(path[-1]):
                if v==start and h+c==g:out.add(canonical(path))
            return
        for v,c in edges(path[-1]):dfs(start,path+(v,),h+c)
    for a in range(1,19):dfs(a,(a,),0)
    return sorted(out)

if __name__=='__main__':
    cs=enumerate_clocks(18,6)
    print('clocks',len(cs),flush=True)
    results=[]
    for i,c in enumerate(cs):
        rs=[]
        for k in (2,3,4):
            r=analyze(c,k);rs.append(r)
            if not r['live']:break
        results.append({'clock':c,'checks':rs})
        if rs[-1]['live']:print('LIVE',c,rs[-1]['live'],flush=True)
    summary={'period':18,'growth':6,'clock_count':len(cs),'live_width3':sum(any(c['width']==3 and c['live']>0 for c in r['checks']) for r in results),'live_width4':sum(any(c['width']==4 and c['live']>0 for c in r['checks']) for r in results),'results':results}
    open('novel_projective_period18_clocks.json','w').write(json.dumps(summary,indent=2))
    print({k:v for k,v in summary.items()if k!='results'},flush=True)
