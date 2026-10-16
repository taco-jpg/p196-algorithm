import json, sys
sys.setrecursionlimit(100000)
from scope import *
def closure(abcs, k):
    sb = short_back(k)
    def parents(p):
        ps = set(sb.get(p, ()))
        if len(p) == k:
            ps |= prefix_predecessors(p)
        return ps
    height = {}; state = {}
    inits = set()
    for abc in abcs: inits |= initial_words(abc, k)
    for root in inits:
        if root in height: continue
        stack=[(root, iter(sorted(parents(root))))]; state[root]=1
        while stack:
            node,it=stack[-1]; adv=False
            for q in it:
                st=state.get(q)
                if st==1: raise Exception('cycle')
                if st is None:
                    state[q]=1; stack.append((q, iter(sorted(parents(q))))); adv=True; break
            if not adv:
                stack.pop(); ps=parents(node)
                height[node]=0 if not ps else 1+max(height[q] for q in ps); state[node]=2
    return height, inits
if __name__=='__main__':
    k=int(sys.argv[1]); pres=sys.argv[2].split(',')
    h,inits=closure([tuple(int(c) for c in p) for p in pres],k)
    edges=0
    print('k',k,'prefixes',len(pres),'nodes',len(h),'maxrank',max(h.values()))
    for p in pres:
        abc=tuple(int(c) for c in p)
        print(p, 1+max(h[w] for w in initial_words(abc,k)))
