import subprocess, resource, time, sys, os
tests = {
 "fibers": 'theorem x : ((List.range 88).all fun l => (fiber l).all (fun i => i < 164) && (List.range 164).all (fun i => (fiber l).contains i == permitted l opts[i]!)) = true := by decide +kernel',
}
for i,(a,b) in enumerate([(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,5)]):
    tests[f"p{a}"] = f'theorem x : checkProjection fiber output graph{a}K graph{b}K ranks{a}K maps{a}K = true := by decide +kernel'
tests["root7"]='theorem x : checkRoot graph7K 41 rootRanks7K = true := by decide +kernel'
env=dict(os.environ, LEAN_PATH=".")
for name in sys.argv[1:]:
    open("Tk.lean","w").write("import BoundaryDataK\nopen Sofic BoundaryCertificate\nset_option maxRecDepth 100000\nset_option maxHeartbeats 0\n"+tests[name]+"\n")
    t=time.time()
    p=subprocess.Popen(["bash","-c","ulimit -v 6000000; exec lean Tk.lean"],env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    try: out,_=p.communicate(timeout=900)
    except subprocess.TimeoutExpired: p.kill(); out=b"TIMEOUT"
    ru=resource.getrusage(resource.RUSAGE_CHILDREN)
    print(name, round(time.time()-t,1),"s rc",p.returncode,"maxrss_children_KB",ru.ru_maxrss, out.decode()[:200].replace("\n"," "), flush=True)
