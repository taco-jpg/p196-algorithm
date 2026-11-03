#!/usr/bin/env python3
"""Round 6 queue runner (studio). Runs ./reachdisk (ROT=1, 24 threads, nice 10) on each task of queue.tsv, one at a time.

Files (all under ~/p196_run/r6/):
  queue.tsv         T <tab> clock, in priority order (read at start; re-read each task, so it can be edited)
  r6.jsonl          one row per finished task: status, orbits, height, targets, streams, time, peak RSS, disk
  logs/r6_T{T}_{clock}.log   full reachdisk output
  JOURNAL_R6.md     heartbeat every 30 min (task, height, visited, RSS, disk free)
  T{T}_{clock}/     work directory (manifest.txt is the truth; re-running resumes)

Stops only on a disk-guard TOO_BIG (no point continuing with a full disk) or when the queue is empty. Never asks.
A COMPLETE task deletes its own scratch files (base/delta/front), because the visited set is not needed afterwards and the
disk is the binding resource. Result files and the manifest are kept.
"""
import json, os, re, shutil, subprocess, sys, time, datetime

HOME = os.path.expanduser('~')
R6 = os.path.join(HOME, 'p196_run', 'r6')
EXE = os.path.join(HOME, 'p196_run', 'bands', 'reachdisk')
QUEUE = os.path.join(R6, 'queue.tsv')
RESULTS = os.path.join(R6, 'r6.jsonl')
JOURNAL = os.path.join(R6, 'JOURNAL_R6.md')
CAP = 20000000000          # 2e10 orbits; the disk guard (15% free) is the real limit
HEARTBEAT = 1800

def now():
    return datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

def journal(line):
    with open(JOURNAL, 'a') as f:
        f.write(f'- [{now()}] {line}\n')

def done_tasks():
    # TOO_BIG is final too: its visited/scratch files are deleted after the run (authorized 2026-11-01), so it cannot resume.
    done = set()
    if os.path.exists(RESULTS):
        for l in open(RESULTS):
            r = json.loads(l)
            if r['status'] in ('COMPLETE', 'EMPTY', 'TOO_BIG') and 'T' in r:
                done.add((r['T'], r['clock']))
    return done

def disk_free():
    st = os.statvfs(R6)
    return 100.0 * st.f_bavail / st.f_blocks

def dir_gb(path):
    tot = 0
    for root, _, files in os.walk(path):
        for f in files:
            try: tot += os.path.getsize(os.path.join(root, f))
            except OSError: pass
    return tot / 1e9

def read_queue():
    out = []
    for l in open(QUEUE):
        l = l.strip()
        if not l or l.startswith('#'): continue
        T, clock = l.split('\t')[:2]
        out.append((int(T), clock))
    return out

def rss_of(pid):
    try:
        out = subprocess.run(['ps', '-o', 'rss=', '-p', str(pid)], capture_output=True, text=True).stdout.strip()
        return int(out) / 1e6 if out else 0.0
    except Exception:
        return 0.0

def run_task(T, clock):
    wd = os.path.join(R6, f'T{T}_{clock}')
    os.makedirs(os.path.join(R6, 'logs'), exist_ok=True)
    log = os.path.join(R6, 'logs', f'r6_T{T}_{clock}.log')
    env = dict(os.environ, ROT='1', THREADS='24')
    t0 = time.time(); started = now()
    with open(log, 'a') as f:
        f.write(f'=== {started} T={T} clock={clock} ROT=1 cap={CAP}\n'); f.flush()
        p = subprocess.Popen(['nice', '-n', '10', EXE, '10', str(T), clock, 'ALL', wd, str(CAP), '0.15'],
                             stdout=f, stderr=subprocess.STDOUT, env=env)
        last_hb = time.time()
        while p.poll() is None:
            time.sleep(20)
            if time.time() - last_hb >= HEARTBEAT:
                last_hb = time.time()
                tail = subprocess.run(['tail', '-n', '1', log], capture_output=True, text=True).stdout.strip()
                journal(f'heartbeat T={T} clock={clock} RSS={rss_of(p.pid):.1f} GB disk_free={disk_free():.1f}% last: {tail[:160]}')
    text = open(log).read().split(f'=== {started}')[-1]
    res = [l for l in text.splitlines() if l.startswith('RESULT')]
    status = res[-1].split()[1].rstrip(':') if res else 'CRASH'
    targets = [l.strip() for l in text.splitlines() if 'TARGET' in l]
    streams = [l.split(': ', 1)[1].strip() for l in text.splitlines() if 'NEW STREAM' in l]
    m = re.search(r'(\d+) interfaces reachable', text)
    orbits = int(m.group(1)) if m else None
    hm = re.search(r'after height (\d+)', text)
    if not hm: hm = re.search(r'at height (\d+): \d+ interfaces visited', text)
    height = int(hm.group(1)) if hm else None
    rec = dict(T=T, clock=clock, rot=1, status=status, orbits=orbits, height=height, targets=targets, streams=streams,
               secs=round(time.time() - t0, 1), started=started, ended=now(), result_line=res[-1] if res else '',
               workdir=wd, disk_gb_before_cleanup=round(dir_gb(wd), 2))
    if status in ('COMPLETE', 'TOO_BIG'):  # scratch only (visited/frontier/candidates); manifest, log and result are kept
        for name in os.listdir(wd):
            if name.startswith(('base_', 'delta_', 'front_', 'cand_')) or name.endswith('.tmp'):
                os.remove(os.path.join(wd, name))
        rec['scratch_deleted'] = True
    rec['disk_gb_after'] = round(dir_gb(wd), 2)
    with open(RESULTS, 'a') as f: f.write(json.dumps(rec) + '\n')
    journal(f'finished T={T} clock={clock} status={status} orbits={orbits} height={height} streams={len(streams)} '
            f'targets={len(targets)} secs={rec["secs"]} disk_free={disk_free():.1f}%')
    return rec

def main():
    journal('runner start')
    attempted = set()  # a task that ends TOO_BIG is not retried in this run; a restart resumes it from its manifest
    while True:
        done = done_tasks()
        todo = [t for t in read_queue() if t not in done and t not in attempted]
        if not todo: break
        T, clock = todo[0]
        attempted.add((T, clock))
        while disk_free() < 15.0:   # r6 must not stop: wait for space (a TOO_BIG task deletes its scratch, other jobs end)
            journal(f'waiting before T={T} clock={clock}: disk free {disk_free():.1f}% < 15%'); time.sleep(600)
        rec = run_task(T, clock)
        if 'disk guard' in rec['result_line']:   # scratch was deleted by run_task, so the next task can start
            journal(f'disk guard hit at T={T} clock={clock} (UNDECIDED); scratch deleted, queue continues')
    journal('runner end (queue empty or stopped)')

if __name__ == '__main__':
    main()
