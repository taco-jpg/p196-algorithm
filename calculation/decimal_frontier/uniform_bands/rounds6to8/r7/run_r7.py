#!/usr/bin/env python3
"""Round 7 queue runner (studio): runs backdisk (ROT=1, nice 10, THREADS from the task) one task at a time.

Files under ~/p196_run/r7/:  queue_r7.json (list of tasks, re-read each time), r7.jsonl (one row per finished task),
logs/<name>.log, JOURNAL_R7.md (heartbeat every 30 min: task, layer, visited, RSS, disk), DECISIONS_R7.md (scratch deletions),
wd_<name>/ (manifest.txt is kept; base/delta/front/cand scratch is deleted after the task, and that is logged).
Task: {"name","B","T","clock","specs":[..],"cap","threads"}.  Never asks.  Stops only when the queue is empty.
"""
import json, os, re, subprocess, time, datetime

HOME = os.path.expanduser('~')
R7 = os.path.join(HOME, 'p196_run', 'r7')
EXE = os.path.join(HOME, 'p196_run', 'bands', 'backdisk')
QUEUE = os.path.join(R7, 'queue_r7.json')
RESULTS = os.path.join(R7, 'r7.jsonl')
JOURNAL = os.path.join(R7, 'JOURNAL_R7.md')
DECISIONS = os.path.join(R7, 'DECISIONS_R7.md')
HEARTBEAT = 1800

def now(): return datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
def note(path, line):
    with open(path, 'a') as f: f.write(f'- [{now()}] {line}\n')
def disk_free():
    st = os.statvfs(R7); return 100.0 * st.f_bavail / st.f_blocks
def dir_gb(p):
    tot = 0
    for root, _, files in os.walk(p):
        for f in files:
            try: tot += os.path.getsize(os.path.join(root, f))
            except OSError: pass
    return tot / 1e9
def rss_of(pid):
    try:
        out = subprocess.run(['ps', '-o', 'rss=', '-p', str(pid)], capture_output=True, text=True).stdout.strip()
        return int(out) / 1e6 if out else 0.0
    except Exception: return 0.0
def done_names():
    d = set()
    if os.path.exists(RESULTS):
        for l in open(RESULTS):
            r = json.loads(l)
            if r.get('status') in ('REACHABLE', 'UNREACHABLE', 'TOO_BIG', 'BADTASK'): d.add(r['name'])
    return d

def run_task(t):
    name = t['name']; wd = os.path.join(R7, 'wd_' + name); log = os.path.join(R7, 'logs', name + '.log')
    os.makedirs(os.path.join(R7, 'logs'), exist_ok=True)
    env = dict(os.environ, ROT='1', THREADS=str(t.get('threads', 8)), **t.get('env', {}))
    cmd = ['nice', '-n', '10', EXE, str(t['B']), str(t['T']), t['clock'], wd, str(t.get('cap', 20000000000)), '0.20'] + t['specs']
    t0 = time.time(); started = now()
    with open(log, 'a') as f:
        f.write(f'=== {started} {" ".join(cmd)}\n'); f.flush()
        p = subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT, env=env)
        last = time.time()
        while p.poll() is None:
            time.sleep(15)
            if time.time() - last >= HEARTBEAT:
                last = time.time()
                tail = subprocess.run(['tail', '-n', '1', log], capture_output=True, text=True).stdout.strip()
                note(JOURNAL, f'heartbeat {name} RSS={rss_of(p.pid):.1f} GB disk_free={disk_free():.1f}% last: {tail[:170]}')
    text = open(log).read().split(f'=== {started}')[-1]
    res = [l for l in text.splitlines() if l.startswith('RESULT')]
    line = res[-1] if res else ''
    status = 'REACHABLE' if 'REACHABLE:' in line and 'UNREACHABLE' not in line else 'UNREACHABLE' if 'UNREACHABLE' in line else \
        'TOO_BIG' if 'TOO_BIG' in line else 'BADTASK' if 'BADTASK' in line else 'CRASH'
    hm = re.search(r'at height (\d+)', line); height = int(hm.group(1)) if hm else None
    sm = re.search(r'(\d+) states in the backward cone', line); states = int(sm.group(1)) if sm else None
    lm = re.findall(r'^layer (\d+) \(distance \d+\): \d+ new, (\d+) visited', text, re.M)
    layers = int(lm[-1][0]) if lm else None
    if states is None and lm: states = int(lm[-1][1])
    rec = dict(name=name, task=t, status=status, height=height, layers=layers, states=states, secs=round(time.time() - t0, 1),
               started=started, ended=now(), result_line=line, workdir=wd, disk_gb_before_cleanup=round(dir_gb(wd), 2))
    if status != 'CRASH':   # only this tool's own scratch; the manifest, log and result are kept
        n = 0
        for fn in os.listdir(wd):
            if fn.startswith(('base_', 'delta_', 'front_', 'cand_')) or fn.endswith('.tmp'):
                os.remove(os.path.join(wd, fn)); n += 1
        note(DECISIONS, f'deleted {n} backdisk scratch files of {wd} ({rec["disk_gb_before_cleanup"]} GB) after status {status}; manifest and log kept')
        rec['scratch_deleted'] = n
    with open(RESULTS, 'a') as f: f.write(json.dumps(rec) + '\n')
    note(JOURNAL, f'finished {name} status={status} height={height} layers={layers} states={states} secs={rec["secs"]} disk_free={disk_free():.1f}%')

def main():
    note(JOURNAL, 'runner start')
    attempted = set()
    while True:
        done = done_names() | attempted
        todo = [t for t in json.load(open(QUEUE)) if t['name'] not in done]
        if not todo: break
        attempted.add(todo[0]['name'])
        if disk_free() < 15.0:
            note(JOURNAL, f'STOP before {todo[0]["name"]}: disk free {disk_free():.1f}% < 15%'); break
        run_task(todo[0])
    note(JOURNAL, 'runner end (queue empty or stopped)')

if __name__ == '__main__':
    main()
