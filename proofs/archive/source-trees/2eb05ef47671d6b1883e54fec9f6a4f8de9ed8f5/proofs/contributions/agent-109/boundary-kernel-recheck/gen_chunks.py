#!/usr/bin/env python3
"""Agent #109: emit per-chunk kernel-check modules ProjK<g>p<k>.lean (pairs, 45 edges)
and ProjK<g>b<k>.lean (buckets, 180 edges), plus ProjK<g>.lean combining them.
Each module holds one `decide +kernel` theorem (kernel memory is not reclaimed
between declarations of one file)."""
import re, json
src=open('BoundaryDataK.lean').read()
raw={int(m.group(1)):[int(x) for x in m.group(2).split(', ')] for m in re.finditer(r'def graph(\d)K : Graph := \(\[([^\]]*)\] : List Nat\)\.map decodeEdge',src)}
nxt={0:1,1:2,2:3,3:4,4:5,5:6,6:7,7:5}
CP,CB=45,180
H=lambda imp:f"import {imp}\n\nnamespace BoundaryCertificateK\nopen Sofic Sofic.Fast BoundaryCertificate\n\nset_option maxRecDepth 100000\nset_option maxHeartbeats 0\n\n"
def rnest(names):
    return names[0] if len(names)==1 else f"{names[0]} ++ ({rnest(names[1:])})"
mods=[]
for g in range(8):
    n=nxt[g]; codes=raw[g]
    pc=[codes[i:i+CP] for i in range(0,len(codes),CP)]
    bc=[codes[i:i+CB] for i in range(0,len(codes),CB)]
    for k,c in enumerate(pc):
        open(f"ProjK{g}p{k}.lean","w").write(H(f"FastData{g}")+
          f"def g{g}p{k} : Graph := ([{', '.join(map(str,c))}] : List Nat).map decodeEdge\n\n"
          f"theorem pairs{g}_{k} : pairsOK output graph{n}K T{g} B{g} H{g} (rawNodes fiber g{g}p{k}) = true := by\n  decide +kernel\n\nend BoundaryCertificateK\n")
        mods.append(f"ProjK{g}p{k}")
    for k,c in enumerate(bc):
        open(f"ProjK{g}b{k}.lean","w").write(H(f"FastData{g}")+
          f"def g{g}b{k} : Graph := ([{', '.join(map(str,c))}] : List Nat).map decodeEdge\n\n"
          f"theorem buckets{g}_{k} : bucketsOK B{g} (rawNodes fiber g{g}b{k}) = true := by\n  decide +kernel\n\nend BoundaryCertificateK\n")
        mods.append(f"ProjK{g}b{k}")
    def comb(kind,K,k=0):
        if k==K-1: return f"{kind}{g}_{k}"
        lem="pairsOK_graph_append _ _ _ _ _ _ _ _" if kind=="pairs" else "bucketsOK_graph_append _ _ _ _"
        return f"({lem} {kind}{g}_{k} {comb(kind,K,k+1)})"
    imps="\n".join(f"import ProjK{g}p{k}" for k in range(len(pc)))+"\n"+"\n".join(f"import ProjK{g}b{k}" for k in range(len(bc)))
    body=(imps+"\n\n/-! Agent #109: combination of the chunked kernel checks for graph "+str(g)+" → graph "+str(n)+". -/\n\n"
      "namespace BoundaryCertificateK\nopen Sofic Sofic.Fast BoundaryCertificate\n\n"
      "set_option maxRecDepth 100000\nset_option maxHeartbeats 0\n\n"
      f"theorem g{g}_split_p : graph{g}K = {rnest([f'g{g}p{k}' for k in range(len(pc))])} := by rfl\n\n"
      f"theorem g{g}_split_b : graph{g}K = {rnest([f'g{g}b{k}' for k in range(len(bc))])} := by rfl\n\n"
      f"theorem pairs{g}_all : pairsOK output graph{n}K T{g} B{g} H{g} (rawNodes fiber graph{g}K) = true := by\n  exact (congrArg (fun G => pairsOK output graph{n}K T{g} B{g} H{g} (rawNodes fiber G) = true) g{g}_split_p).mpr\n    {comb('pairs',len(pc))}\n\n"
      f"theorem buckets{g}_all : bucketsOK B{g} (rawNodes fiber graph{g}K) = true := by\n  exact (congrArg (fun G => bucketsOK B{g} (rawNodes fiber G) = true) g{g}_split_b).mpr\n    {comb('buckets',len(bc))}\n\n"
      f"theorem projection{g}_fast :\n    Projection fiber output graph{g}K graph{n}K (rankT T{g}) (projT T{g}) :=\n  fast_sound buckets{g}_all pairs{g}_all\n\n"
      "end BoundaryCertificateK\n\n"+f"#print axioms BoundaryCertificateK.projection{g}_fast\n")
    open(f"ProjK{g}.lean","w").write(body)
json.dump(mods,open("chunk_modules.json","w"))
print(len(mods),"chunk modules")
