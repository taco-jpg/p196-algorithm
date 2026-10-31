#!/usr/bin/env python3
"""Round 5 driver: decide EXACTLY, for overflow clocks w and left-end periods T (multiples of |w|), whether a periodic
decimal left end of ANY height can carry (a) a uniform absorbing band {0},{18},{6,12},{2,4,8,16,14,10} in any phase
-> 'left end + band + mirror' would be a decimal Lychrel certificate; (b) a 9-wire with some stream (neutral-band
exterior). Tool: reachmt (BFS over interfaces; RESULT COMPLETE = frontier empty = every height checked).

Stages (all resumable; results appended to --out JSONL; per-T counts in *_summary.txt):
  csweep : ALL clocks (binary Lyndon words) and ALL T in [tmin, tmax]; C++ SWEEP shards, single-thread each, small cap.
           Only non-EMPTY tasks are written to the JSONL (EMPTY ones are counted in the summary).
  words  : clocks from --words FILE, every T = k|w| <= tmax (BATCH mode, small cap)
  heavy  : every task in the JSONL whose result is TOO_BIG and whose T is in range: one at a time, multi-threaded, big
           cap, full per-height log results/r5_heavy_T{T}_{w}.log
Any band target -> ALERT_TARGET.txt, then the left end is rebuilt with ./reach and replayed on real big integers.
Band {0} or {18} reached would contradict the Lean result E2ExtremeUniformIsolation -> flagged CONTRADICTION.

usage: sweep.py --stage csweep --tmin 21 --tmax 24 [--shards 64] [--workers 28] [--cap 2000000]
       sweep.py --stage words --words capped_words.txt --tmax 48 [--cap 2000000]
       sweep.py --stage heavy --tmin 1 --tmax 48 [--heavy-cap 8000000000] [--heavy-threads 24] [--heavy-timeout 43200] [--rot 1]
       [--out ../results/r5_sweep.jsonl] [--seed cloud_r5_sweep.jsonl]
"""
import argparse, json, os, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
DECIDED = ('COMPLETE', 'EMPTY')

def canon(w):
    """minimal rotation of the primitive root of w ((10)^8 -> 01)"""
    for d in range(1, len(w) + 1):
        if len(w) % d == 0 and w == w[:d] * (len(w) // d):
            w = w[:d]; break
    return min(w[i:] + w[:i] for i in range(len(w)))

def parse_block(lines):
    rec = {'targets': [], 'streams': []}
    for l in lines:
        m = re.match(r'\s*TARGET (\S+) phase (\d+) REACHED at height (\d+)\s+\(BAND=\'([^\']*)\' PH=(\d+)\)', l)
        if m:
            rec['targets'].append(dict(band=m.group(1), phase=int(m.group(2)), height=int(m.group(3)), spec=m.group(4)))
        m = re.match(r'\s*NEW STREAM at height (\d+): ([01]+)', l)
        if m:
            rec['streams'].append(dict(height=int(m.group(1)), stream=m.group(2)))
        if l.startswith('RESULT'):
            rec['result'] = l.split()[1].rstrip(':'); rec['detail'] = l.strip()
            m = re.search(r'(\d+) interfaces (reachable|visited)', l)
            if m:
                rec['interfaces'] = int(m.group(1))
    rec.setdefault('result', 'CRASH')
    return rec

def parse_tasks(text):
    out, cur, task = [], [], None
    for l in text.splitlines():
        if l.startswith('TASK '):
            _, T, w = l.split(); task = (int(T), w); cur = []
        elif l.startswith('ENDTASK') and task:
            r = parse_block(cur); r.update(word=task[1], T=task[0]); out.append(r); task = None
        elif task:
            cur.append(l)
    return out

def better(new, old):
    if old is None: return True
    if old['result'] in DECIDED: return False
    return new['result'] in DECIDED or new.get('cap', 0) >= old.get('cap', 0)

class Store:
    def __init__(self, out, seeds):
        self.out = out; self.best = {}
        for fn in seeds + [out]:
            if fn and os.path.exists(fn):
                for l in open(fn):
                    r = json.loads(l); k = (r['T'], r['word'])
                    if better(r, self.best.get(k)): self.best[k] = r
        self.f = open(out, 'a'); self.outdir = os.path.dirname(os.path.abspath(out))
    def add(self, r):
        self.f.write(json.dumps(r) + '\n'); self.f.flush()
        k = (r['T'], r['word'])
        if better(r, self.best.get(k)): self.best[k] = r
        if r.get('targets'):
            alert(r, self.outdir); self.f.write(json.dumps(dict(r, stage=r.get('stage', '') + '+replay')) + '\n'); self.f.flush()

def alert(rec, outdir):
    with open(os.path.join(outdir, 'ALERT_TARGET.txt'), 'a') as a:
        a.write(json.dumps(rec) + '\n')
        for tg in rec['targets']:
            if tg['band'] in ('band[0]', 'band[18]'):
                a.write('CONTRADICTION with Lean E2ExtremeUniformIsolation (check the tool first): ' + json.dumps(tg) + '\n')
    print('!!! BAND TARGET REACHED', json.dumps(rec), flush=True)
    for tg in rec['targets']:
        fn = os.path.join(outdir, f"fit_T{rec['T']}_{rec['word']}_{tg['band']}_ph{tg['phase']}.log")
        env = dict(os.environ, BAND=tg['spec'], PH=str(tg['phase']))
        with open(fn, 'w') as f:
            subprocess.run([os.path.join(HERE, 'reach'), '10', str(rec['T']), rec['word'], 'BAND', '4000000000'], env=env, stdout=f)
        rp = subprocess.run([sys.executable, os.path.join(HERE, 'replay_band.py'), fn, '--periods', '20'], capture_output=True, text=True)
        open(fn + '.replay', 'w').write(rp.stdout + rp.stderr)
        tg['fit_log'] = fn; tg['replay'] = 'PASS' if rp.returncode == 0 else 'FAIL'
        print('    rebuilt with reach + big-int replay:', tg['replay'], fn, flush=True)

def stage_csweep(a, st):
    tag = f'r5_csweep_T{a.tmin}-{a.tmax}_cap{a.cap}'
    files = [os.path.join(st.outdir, f'{tag}_s{k}of{a.shards}.txt') for k in range(a.shards)]
    def done(fn):
        return os.path.exists(fn) and 'SWEEP DONE' in open(fn).read()[-300:]
    todo = [k for k in range(a.shards) if not done(files[k])]
    print(f'csweep T={a.tmin}..{a.tmax}: {a.shards} shards, {len(todo)} to run, cap {a.cap}', flush=True)
    def run(k):
        with open(files[k], 'w') as f:
            subprocess.run([os.path.join(HERE, 'reachmt'), 'SWEEP', '10', str(a.tmin), str(a.tmax), str(a.cap), str(k), str(a.shards)], stdout=f)
        return k
    t0 = time.time()
    with ThreadPoolExecutor(a.workers) as ex:
        for i, fu in enumerate(as_completed([ex.submit(run, k) for k in todo])):
            fu.result(); print(f'  shard done ({i + 1}/{len(todo)}), {time.time() - t0:.0f} s', flush=True)
    tot = {}
    for fn in files:
        txt = open(fn).read()
        if 'SWEEP DONE' not in txt[-300:]:
            print('  INCOMPLETE shard file', fn, flush=True); continue
        for r in parse_tasks(txt):
            r.update(cap=a.cap, stage='csweep')
            if st.best.get((r['T'], r['word']), {}).get('result') not in DECIDED or r.get('targets'):
                st.add(r)
        for l in txt.splitlines():
            if l.startswith('SWEEP SUMMARY'):
                f = l.split(); T = int(f[2][2:])
                for kv in f[3:]:
                    k, v = kv.split('='); tot.setdefault(T, {}); tot[T][k] = tot[T].get(k, 0) + int(v)
    with open(os.path.join(st.outdir, tag + '_summary.txt'), 'w') as sf:
        for T in sorted(tot):
            line = f'T={T} ' + ' '.join(f'{k}={v}' for k, v in tot[T].items()); sf.write(line + '\n'); print('  ' + line, flush=True)

def stage_words(a, st):
    words = list(dict.fromkeys(canon(l.split()[0]) for l in open(a.words) if l.strip() and not l.startswith('#')))
    tasks = [(k * len(w), w) for w in words for k in range(1, a.tmax // len(w) + 1) if k * len(w) >= a.tmin]
    tasks = [t for t in tasks if st.best.get(t, {}).get('result') not in DECIDED and st.best.get(t, {}).get('cap', 0) < a.cap]
    print(f'words: {len(words)} clocks, {len(tasks)} tasks to run, cap {a.cap}', flush=True)
    def run(chunk):
        inp = ''.join(f'{T} {w}\n' for T, w in chunk)
        out = subprocess.run([os.path.join(HERE, 'reachmt'), 'BATCH', '10', 'ALL', str(a.cap)], input=inp, capture_output=True,
                             text=True, env=dict(os.environ, THREADS='1')).stdout
        return parse_tasks(out)
    chunks = [tasks[i:i + 50] for i in range(0, len(tasks), 50)]
    with ThreadPoolExecutor(a.workers) as ex:
        for fu in as_completed([ex.submit(run, c) for c in chunks]):
            for r in fu.result():
                r.update(cap=a.cap, stage='words'); st.add(r)

def stage_heavy(a, st):
    todo = sorted(k for k, r in st.best.items() if r['result'] not in DECIDED and a.tmin <= k[0] <= a.tmax and r.get('cap', 0) < a.heavy_cap)
    print(f'heavy: {len(todo)} tasks, cap {a.heavy_cap}, {a.heavy_threads} threads, one at a time: {todo}', flush=True)
    for T, w in todo:
        log = os.path.join(st.outdir, f'r5_heavy_T{T}_{w}.log'); t0 = time.time()
        env = dict(os.environ, THREADS=str(a.heavy_threads), ROT='1' if a.rot else '0')
        try:
            with open(log, 'w') as lf:
                subprocess.run([os.path.join(HERE, 'reachmt'), '10', str(T), w, 'ALL', str(a.heavy_cap)], env=env, stdout=lf,
                               stderr=subprocess.STDOUT, timeout=a.heavy_timeout)
            r = parse_block(open(log).read().splitlines())
        except subprocess.TimeoutExpired:
            r = parse_block(open(log).read().splitlines()); r['result'] = 'TIMEOUT'
        r.update(word=w, T=T, cap=a.heavy_cap, stage='heavy', rot=a.rot, secs=round(time.time() - t0, 1), log=log)
        st.add(r); print('  heavy', T, w, r['result'], r.get('detail', ''), flush=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--stage', required=True, choices=['csweep', 'words', 'heavy'])
    ap.add_argument('--tmin', type=int, default=1); ap.add_argument('--tmax', type=int, default=24)
    ap.add_argument('--shards', type=int, default=64); ap.add_argument('--workers', type=int, default=28)
    ap.add_argument('--cap', type=int, default=2000000); ap.add_argument('--words')
    ap.add_argument('--heavy-cap', type=int, default=4000000000); ap.add_argument('--heavy-threads', type=int, default=24)
    ap.add_argument('--heavy-timeout', type=int, default=43200)
    ap.add_argument('--rot', type=int, default=1, help='heavy stage: 1 = store one interface per orbit of the clock shift (exact, saves memory by T/p)')
    ap.add_argument('--out', default=os.path.join(HERE, '..', 'results', 'r5_sweep.jsonl'))
    ap.add_argument('--seed', action='append', default=[])
    a = ap.parse_args()
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    st = Store(a.out, a.seed)
    {'csweep': stage_csweep, 'words': stage_words, 'heavy': stage_heavy}[a.stage](a, st)
    und = sorted(k for k, r in st.best.items() if r['result'] not in DECIDED)
    print(f'ALL DONE. undecided tasks in the store: {len(und)} {und[:20]}', flush=True)

if __name__ == '__main__':
    main()
