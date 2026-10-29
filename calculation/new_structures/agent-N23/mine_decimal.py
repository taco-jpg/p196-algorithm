#!/usr/bin/env python3
"""Infer a one-symbol insertion template from direct decimal orbits only."""
import difflib,sys
def nextn(n):return n+int(str(n)[::-1])
def groups(n):
 s=str(n);return [int(s[max(i-2,0):i]) for i in range(len(s),0,-2)]
def infer(words):
 qs=sorted(words);a=words[0];n=len(a);opts=[]
 for u in range(n):
  v=words[1][u]
  if all(words[q][:u]==a[:u] and words[q][u:u+q]==[v]*q and words[q][u+q:]==a[u:] for q in qs):
   opts.append((u,v))
 if not opts:return None
 u,v=min(opts,key=lambda x:abs(x[0]-n//2))
 return {'parts':[{'digits':a[:u]},{'motif':[v],'slope':1,'offset':0},{'digits':a[u:]}]},(u,v,len(opts))
