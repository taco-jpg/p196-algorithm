import subprocess, sys, os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
known=[(2,'10'),(4,'100'),(8,'1000'),(16,'10000'),(32,'100000'),(11,'001'),(11,'001001'),(17,'100001'),(26,'01'),(20,'00010001'),(20,'0001'),(10,'11100010000'),(10,'100010001000'),(3,'11100'),(3,'10')]
def canon(w): return min(w[i:]+w[:i] for i in range(len(w)))
import tempfile
for b,g in known:
    p=len(g); d=tempfile.mkdtemp()
    subprocess.run([os.path.join(ROOT,'bin','fc_enum'),str(b),str(p),str(p),'-list',d],capture_output=True)
    ws=set()
    for f in os.listdir(d):
        for l in open(os.path.join(d,f)): ws.add(l.strip())
    print(b,g,'passes first-coordinate NFA:',canon(g) in ws, ' (#words at p: %d)'%len(ws))
