import subprocess, time, json, os, sys
tests=json.load(open('tests2.json')); env=dict(os.environ, LEAN_PATH=".")
for name,(imp,thm) in tests.items():
    open("Tk2.lean","w").write(imp+"namespace BoundaryCertificateK\nopen Sofic BoundaryCertificate\nset_option maxRecDepth 100000\nset_option maxHeartbeats 0\n"+thm.replace('theorem ','theorem k_',1)+"\nend BoundaryCertificateK\n")
    t=time.time()
    p=subprocess.Popen(["bash","-c","ulimit -v 6000000; exec lean Tk2.lean"],env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    try: out,_=p.communicate(timeout=900)
    except subprocess.TimeoutExpired: p.kill(); out=b"TIMEOUT"
    print(name, round(time.time()-t,1),"s rc",p.returncode, out.decode()[:300].replace("\n"," "), flush=True)
