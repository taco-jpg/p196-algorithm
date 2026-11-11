import os
import re, glob
ROOT=os.path.expanduser('~/p196_run/r13a')
jobs=[re.search(r'--V ([\d,]+)',l).group(1) for l in open(ROOT+'/jobs_seam1000c2.txt')]
res={}
for f in sorted(glob.glob(ROOT+'/logs/seam1000c/i*.log')):
    txt=open(f).read()
    v=re.search(r'--V ([\d,]+)',txt.splitlines()[0]).group(1)
    l=[x for x in txt.splitlines() if x.startswith('SEAMBAND')]
    e=[x[:90] for x in txt.splitlines() if x.startswith('ERROR')]
    res[v]=(l[0][:95] if l else 'NO SUMMARY LINE (job killed)', len(e))
for v in jobs: print(v, res.get(v,'no log'))
