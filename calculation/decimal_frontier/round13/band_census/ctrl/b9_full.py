import os
import json,subprocess,sys
d=json.load(open(os.path.expanduser('~/p196_run/r12d/ctrl/cert_b9_rec0.json')))
X=d['B_t'][0]; Xs=','.join(map(str,X))
PY=os.path.expanduser('~/p196_run/venv/bin/python')
cmd=[PY,os.path.expanduser('~/p196_run/r13a/fullreplay.py'),'--b','9','--X',Xs,'--Vtau','1,1,15,15','--re','0','--rc','1','--N','20','--j','1','--mstart','30','--returns','3','--clock','1100011000']
out=subprocess.run(cmd,capture_output=True,text=True)
print(out.stdout[-600:]); print(out.stderr[-300:])
