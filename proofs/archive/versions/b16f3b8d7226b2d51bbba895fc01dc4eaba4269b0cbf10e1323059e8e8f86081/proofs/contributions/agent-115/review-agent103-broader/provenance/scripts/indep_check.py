#!/usr/bin/env python3
"""Agent #115 independent check (does not import any repo code).
usage: python3 -I indep_check.py CERT.json.gz GENERATED_DIR
1. certificate hash; hierarchy/id layout; 2. own Tarjan SCC + weighted longest-path
recomputation of every broader job bound (bottom-up through child links);
3. decode every emitted Lean lookup table (nested `if i < k then A else B` trees,
chunked or not) and compare with values derived directly from the certificate.
"""
import gzip, hashlib, json, re, sys
from pathlib import Path

cert_path, gen = Path(sys.argv[1]), Path(sys.argv[2])
raw = cert_path.read_bytes()
print('cert sha256', hashlib.sha256(raw).hexdigest())
jobs = json.loads(gzip.decompress(raw))['jobs']
print('n jobs', len(jobs), 'ids==0..n-1', [j['id'] for j in jobs] == list(range(len(jobs))))
by_h = {}
for j in jobs: by_h.setdefault(j['hierarchy'], []).append(j['id'])
print('hierarchies', {k: (min(v), max(v), len(v)) for k, v in by_h.items()})
assert by_h['broader'] == list(range(16, 31)) and by_h['scalar'] == list(range(16))
print('status set', {j['status'] for j in jobs})
B = {j['id']: j for j in jobs}

def sccs(n, adj):  # iterative Tarjan
    index = [-1]*n; low = [0]*n; on = [False]*n; st = []; comp = [-1]*n; out = []; c = 0
    for r in range(n):
        if index[r] >= 0: continue
        work = [(r, 0)]; index[r] = low[r] = c; c += 1; st.append(r); on[r] = True
        while work:
            v, k = work[-1]
            if k < len(adj[v]):
                work[-1] = (v, k+1); w = adj[v][k]
                if index[w] < 0:
                    index[w] = low[w] = c; c += 1; st.append(w); on[w] = True; work.append((w, 0))
                elif on[w]: low[v] = min(low[v], index[w])
            else:
                work.pop()
                if work: low[work[-1][0]] = min(low[work[-1][0]], low[v])
                if low[v] == index[v]:
                    grp = []
                    while True:
                        w = st.pop(); on[w] = False; comp[w] = len(out); grp.append(w)
                        if w == v: break
                    out.append(grp)
    return comp, out

bound = {}
def job_bound(jid):  # recompute B(J) from vertices/edges/child links only
    if jid in bound: return bound[jid]
    j = B[jid]; rows = j['vertices']; loc = {r[0]: i for i, r in enumerate(rows)}; n = len(rows)
    adj = [[] for _ in range(n)]; selfloop = [False]*n; seen = set()
    for u, v, bit in j['edges']:
        assert bit in (0, 1) and (u, bit) not in seen; seen.add((u, bit))
        adj[loc[u]].append(loc[v]); selfloop[loc[u]] |= (u == v)
    comp, groups = sccs(n, adj)
    mine = {frozenset(g) for g in groups}
    theirs = {frozenset(loc[x] for x in g) for g in j['components']}
    assert mine == theirs, ('partition mismatch', jid)
    cid = {}  # certificate component index of each vertex
    for c, g in enumerate(j['components']):
        for x in g: cid[loc[x]] = c
    cyc = {cid[g[0]] for g in groups if len(g) > 1 or selfloop[g[0]]}
    assert cyc == set(j['cyclic_components']), ('cyclic mismatch', jid)
    child = {l['component']: l['child_job'] for l in j['children']}
    assert set(child) == cyc, ('children != cyclic comps', jid)
    for c, ch in child.items():
        assert B[ch]['hierarchy'] == j['hierarchy'] and B[ch]['width'] == j['width'] + 1
    w = {c: (job_bound(child[c]) if c in cyc else 1) for c in range(len(j['components']))}
    succ = {c: set() for c in w}
    for u in range(n):
        for v in adj[u]:
            if cid[u] != cid[v]: succ[cid[u]].add(cid[v])
    rank = {}
    def r(c):  # longest weighted path (vertices) starting in component c; DAG
        if c not in rank: rank[c] = w[c] + max((r(d) for d in succ[c]), default=0)
        return rank[c]
    sys.setrecursionlimit(100000)
    ranks = [r(c) for c in range(len(w))]
    assert [w[c] for c in range(len(w))] == j['component_weights'], ('weights', jid)
    assert ranks == j['weighted_sink_ranks'], ('ranks', jid)
    bound[jid] = max(ranks)
    assert bound[jid] == j['max_path_vertices_bound'], ('bound', jid)
    return bound[jid]

root = 16
print('root id 16: hierarchy', B[16]['hierarchy'], 'width', B[16]['width'],
      'max_path_vertices_bound', B[16]['max_path_vertices_bound'],
      'by_start_phase', B[16]['path_vertices_bound_by_start_phase'])
print('recomputed B(root16) =', job_bound(16), '; scalar root B(0) =', job_bound(0))
reach = set(); todo = [16]
while todo:
    x = todo.pop(); reach.add(x); todo += [l['child_job'] for l in B[x]['children']]
print('jobs reachable from 16 via child links:', sorted(reach))
print('per-job (id,width,|V|,|E|,B):', [(i, B[i]['width'], len(B[i]['vertices']), len(B[i]['edges']), bound[i]) for i in sorted(reach)])
print('R bound from 7R+1<=636:', (636-1)//7)

# ---- decode emitted Lean tables ----
TOK = re.compile(r'\(|\)|<|[A-Za-z_][A-Za-z_0-9]*|\d+')
defs = {}
for f in sorted(gen.glob('BJob*.lean')):
    for m in re.finditer(r'^def (\w+) \(i : Nat\) : Nat := (.*)$', f.read_text(), re.M):
        defs[m.group(1)] = m.group(2)

def parse(toks, p):
    t = toks[p]
    if t == '(':
        e, p = parse(toks, p+1); assert toks[p] == ')'; return e, p+1
    if t == 'if':
        assert toks[p+1] == 'i' and toks[p+2] == '<'
        k = int(toks[p+3]); assert toks[p+4] == 'then'
        a, p = parse(toks, p+5); assert toks[p] == 'else'
        b, p = parse(toks, p+1); return ('if', k, a, b), p
    if t.isdigit(): return int(t), p+1
    assert toks[p+1] == 'i'; return ('call', t), p+2

def table(name, n):
    """values at 0..n+5 (checks the default 0 past the end too)"""
    memo = {}
    def ev(e, i):
        while True:
            if isinstance(e, int): return e
            if e[0] == 'if': e = e[2] if i < e[1] else e[3]; continue
            nm = e[1]
            if nm not in memo:
                toks = TOK.findall(defs[nm]); memo[nm], end = parse(toks, 0); assert end == len(toks)
            e = memo[nm]
    top = name
    return [ev(('call', top), i) for i in range(n + 5)]

def expect(name, vals):
    got = table(name, len(vals))
    ok = got[:len(vals)] == list(vals) and all(x == 0 for x in got[len(vals):])
    if not ok: print('TABLE MISMATCH', name)
    return ok

allok = True
ids = list(range(16, 31))
allok &= expect('bounds', [B[i]['max_path_vertices_bound'] for i in ids])
allok &= expect('widths', [B[i]['width'] for i in ids])
for k, i in enumerate(ids):
    j = B[i]; rows = j['vertices']; loc = {r[0]: t for t, r in enumerate(rows)}
    # meta encodes phase,last,low as in FiniteGraph field projections (%7, /7%19, /133)
    allok &= expect(f'meta{k}', [r[1] + 7*r[2] + 133*r[3] for r in rows])
    assert all(0 <= r[1] < 7 and 0 <= r[2] < 19 and r[3] in (0, 1) for r in rows)
    cmap = [None]*len(rows)
    for c, g in enumerate(j['components']):
        for x in g: cmap[loc[x]] = c
    allok &= expect(f'components{k}', cmap)
    nxt = [0]*(2*len(rows))
    for u, v, bit in j['edges']: nxt[2*loc[u]+bit] = loc[v]+1
    allok &= expect(f'nextCodes{k}', nxt)
    allok &= expect(f'ranks{k}', j['weighted_sink_ranks'])
    txt = (gen / f'BJobData{k}.lean').read_text()
    cc = re.search(rf'^def childCode{k} \(c : Nat\) : Nat := (.*)$', txt, re.M).group(1)
    want = ''.join(f'if c={l["component"]} then {l["child_job"]-16+1} else ' for l in j['children']) + '0'
    if cc != want: print('CHILDCODE MISMATCH', k); allok = False
    assert f'size := {len(rows)}\n' in txt
    # lift tables for children: parent component members ordered by child 19-blocks
    for l in j['children']:
        ch = B[l['child_job']]; kc = l['child_job'] - 16; proj = dict(l['child_to_parent_raw'])
        mem = []
        for a in range(0, len(ch['vertices']), 19):
            grp = ch['vertices'][a:a+19]
            assert [r[2] for r in grp] == list(range(19)) and len({proj[r[0]] for r in grp}) == 1
            mem.append(loc[proj[grp[0][0]]])
        assert sorted(mem) == sorted(loc[x] for x in j['components'][l['component']])
        inv = [0]*len(rows)
        for t, u in enumerate(mem): inv[u] = t
        allok &= expect(f'members{kc}', mem); allok &= expect(f'inverse{kc}', inv)
print('all emitted tables match certificate-derived values:', allok)
h = (gen / 'BroaderHierarchy.lean').read_text()
m = re.search(r'theorem finite_root_bound.*?:= by', h, re.S)
print('finite_root_bound statement:\n' + m.group(0))
