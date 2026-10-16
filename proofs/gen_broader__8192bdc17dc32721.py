#!/usr/bin/env python3
"""Agent #103: emit the broader-hierarchy finite certificate (jobs 16-30 of the
frozen component certificate) as Lean data, row checks and hierarchy modules.

Data model: same construction as the original scalar generator's `models()`
(read from the pinned certificate, SHA-256 checked), applied to the 15 jobs with
hierarchy 'broader', renumbered 16..30 -> 0..14. Tables use the v2 chunked
representation. Row-check and hierarchy templates follow the original
`generate_checks.py` / `generate_hierarchy.py` verbatim except for module
names (BJobData/BJobChecks), namespaces (BroaderJobData/BroaderHierarchy), the
job links (read from the certificate instead of hard-coded) and the root:
width 2, bound from the certificate. Generated source is not a proof.
"""
import gzip, hashlib, importlib.util, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
CONTRIB = REPO / 'proofs/contributions'
SOURCE = CONTRIB / '2026-10-14-component-specific-bound/component_certificates.json.gz'
EXPECTED = 'ff7a70ee2a6ed677cb9176e212dc0a69acd14eed30425a42b543d7a50823b47e'
OUT = HERE / 'generated'
FIRST = 16

spec = importlib.util.spec_from_file_location('v2', CONTRIB / 'agent-103/scalar-finite-instance/v2/generate_scalar_data_v2.py')
v2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v2)
array = v2.array  # chunked representation, values unchanged


def models():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED
    jobs = [j for j in json.loads(gzip.decompress(raw))['jobs'] if j['hierarchy'] == 'broader']
    assert [j['id'] for j in jobs] == list(range(FIRST, FIRST + 15))
    result = []
    for j in jobs:
        rows = j['vertices']
        local = {r[0]: i for i, r in enumerate(rows)}
        component = [None] * len(rows)
        for c, group in enumerate(j['components']):
            for raw_id in group:
                assert component[local[raw_id]] is None
                component[local[raw_id]] = c
        assert all(c is not None for c in component)
        nxt = [0] * (2 * len(rows))
        for u, v, bit in j['edges']:
            assert bit in (0, 1)
            at = 2 * local[u] + bit
            assert nxt[at] == 0
            nxt[at] = local[v] + 1
        meta = [phase + 7 * last + 133 * low for _, phase, last, low, _ in rows]
        assert all(0 <= phase < 7 and 0 <= last < 19 and low in (0, 1) for _, phase, last, low, _ in rows)
        result.append(dict(job=j, local=local, component=component, next=nxt, meta=meta))
    for p in result:
        for link in p['job']['children']:
            child = result[link['child_job'] - FIRST]
            projection = dict(link['child_to_parent_raw'])
            members = []
            for at in range(0, len(child['job']['vertices']), 19):
                group = child['job']['vertices'][at:at + 19]
                parent = projection[group[0][0]]
                assert [r[2] for r in group] == list(range(19))
                assert all(projection[r[0]] == parent for r in group)
                members.append(p['local'][parent])
            assert set(members) == {p['local'][r] for r in p['job']['components'][link['component']]}
            inverse = [0] * len(p['meta'])
            for i, u in enumerate(members): inverse[u] = i
            child['lift'] = dict(parent=p['job']['id'] - FIRST, selected=link['component'],
                                 members=members, inverse=inverse)
    return result


def checks(mode, identity, count, predicate, unfold, chunk):  # verbatim template
    pieces = []; proofs = []
    for start in range(0, count, chunk):
        size = min(chunk, count - start)
        name = f'{mode}_{identity}_{start//chunk}'
        pieces.append(f'theorem {name} : ∀ i : Fin {size}, {predicate.replace("$u",f"({start}+i.val)")} := by\n  unfold {unfold}\n  decide\n')
        proofs.append((start, start + size, f'(checked_range (fun u => {predicate.replace("$u","u")}) {start} {size} {name})'))
    def join(items):
        if len(items) == 1: return items[0]
        cut = len(items) // 2
        lo, mid, left = join(items[:cut]); mid2, hi, right = join(items[cut:])
        assert mid == mid2
        return lo, hi, f'(join_ranges (fun u => {predicate.replace("$u","u")}) {lo} {mid} {hi} {left} {right})'
    _, _, proof = join(proofs)
    pieces.append(f'theorem {mode}_{identity}_all : ∀ u, 0 ≤ u → u < {count} → {predicate.replace("$u","u")} :=\n  {proof}\n')
    return '\n'.join(pieces)


def main():
    data = models(); OUT.mkdir(exist_ok=True)
    N = len(data)
    catalog = 'import RankRows\nnamespace BroaderJobData\nopen ScalarFinite\n'
    catalog += array('bounds', [d['job']['max_path_vertices_bound'] for d in data])
    catalog += array('widths', [d['job']['width'] for d in data])
    catalog += 'def jobBound (j : Nat) : Nat := bounds j\ndef jobWidth (j : Nat) : Nat := widths j\nend BroaderJobData\n'
    (OUT / 'BJobCatalog.lean').write_text(catalog)
    inventory = []
    for identity in range(N):
        d = data[identity]; j = d['job']
        s = 'import BJobCatalog\nnamespace BroaderJobData\nopen ScalarFinite\n'
        for name, values in [('meta', d['meta']), ('components', d['component']),
                             ('nextCodes', d['next']), ('ranks', j['weighted_sink_ranks'])]:
            s += array(f'{name}{identity}', values)
        s += f'def component{identity} (v : Nat) : Nat := components{identity} v\n'
        clauses = ''.join(f'if c={link["component"]} then {link["child_job"]-FIRST+1} else ' for link in j['children'])
        s += f'def childCode{identity} (c : Nat) : Nat := ' + clauses + '0\n'
        s += f'''def data{identity} : Data where
  size := {len(d['meta'])}
  phase v := (meta{identity} v)%7
  last v := (meta{identity} v)/7%19
  low v := (meta{identity} v)/133
  next u bit := nextCodes{identity} (2*u+bit)

def ranking{identity} : Ranking where
  component := component{identity}
  cyclic c := decide (childCode{identity} c ≠ 0)
  weight c := if childCode{identity} c=0 then 1 else jobBound (childCode{identity} c-1)
  rank c := ranks{identity} c
  bound := jobBound {identity}
'''
        if 'lift' in d:
            lift = d['lift']
            s += array(f'members{identity}', lift['members'])
            s += array(f'inverse{identity}', lift['inverse'])
            s += f'def member{identity} (i : Nat) : Nat := members{identity} i\n'
            s += f'def memberIndex{identity} (u : Nat) : Nat := inverse{identity} u\n'
        s += 'end BroaderJobData\n'
        (OUT / f'BJobData{identity}.lean').write_text(s)
        # row checks (template of generate_checks.py)
        n = len(d['meta']); p = d.get('lift', {}).get('parent')
        c = f'import BJobData{identity}\nimport RangeChecks\n'
        if p is not None: c += f'import BJobData{p}\n'
        c += 'namespace BroaderJobData\nopen ScalarFinite\nset_option maxHeartbeats 0\nset_option maxRecDepth 100000\n'
        c += checks('vertex', identity, n, f'VertexRow ranking{identity} $u', 'VertexRow', 128)
        c += checks('edge', identity, n, f'∀ bit : Fin 2, EdgeRow data{identity} ranking{identity} $u bit.val', 'EdgeRow', 128)
        c += f'''theorem checked_rank{identity} : CheckedRank data{identity} ranking{identity} := by
  constructor
  · intro u hu
    exact vertex_{identity}_all u (Nat.zero_le u) hu
  · intro u hu bit hb
    exact edge_{identity}_all u (Nat.zero_le u) hu ⟨bit,by omega⟩
'''
        if p is not None:
            lift = d['lift']; selected = lift['selected']; m = len(lift['members']); pn = len(data[p]['meta'])
            c += checks('coverage', identity, pn, f'CoverageRow data{p} component{p} {selected} {m} member{identity} memberIndex{identity} $u', 'CoverageRow', 128)
            c += checks('field', identity, n, f'FieldRow data{p} data{identity} member{identity} $u', 'FieldRow', 128)
            c += checks('lift', identity, n, f'∀ bit : Fin 2, LiftRow data{p} data{identity} component{p} {selected} member{identity} memberIndex{identity} $u bit.val', 'LiftRow', 128)
            c += f'''def lift_certificate{identity} : LiftCertificate data{p} data{identity} component{p} {selected} where
  members := member{identity}
  memberIndex := memberIndex{identity}
  count := {m}
  size_eq := rfl
  coverage u hu := coverage_{identity}_all u (Nat.zero_le u) hu
  fields u hu := field_{identity}_all u (Nat.zero_le u) hu
  transitions u hu bit hb := lift_{identity}_all u (Nat.zero_le u) hu ⟨bit,by omega⟩

theorem lift_complete{identity} : ActualPrefixLift.Realization
    (bounded (ActualPrefixLift.lift (ActualPrefixLift.select (graph data{p})
      (fun v => component{p} v={selected})))) (graph data{identity})
      (encode lift_certificate{identity}) := lift_realization lift_certificate{identity}
'''
        c += 'end BroaderJobData\n'
        (OUT / f'BJobChecks{identity}.lean').write_text(c)
        inventory.append(dict(job=identity, source_job=identity + FIRST, width=j['width'], vertices=n,
                              edges=len(j['edges']), bound=j['max_path_vertices_bound'],
                              children=[(l['component'], l['child_job'] - FIRST) for l in j['children']]))
    links = {i: [(l['component'], l['child_job'] - FIRST) for l in data[i]['job']['children']] for i in range(N)}
    write_hierarchy(N, links, data)
    (OUT / 'generation.json').write_text(json.dumps(dict(source_sha256=EXPECTED, jobs=inventory,
        generator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        scope='Broader-hierarchy finite data, row checks and hierarchy composition; generated source is not a proof.'), indent=2) + '\n')
    print(json.dumps([(x['job'], x['width'], x['vertices'], x['bound'], x['children']) for x in inventory]))


def write_hierarchy(N, links, data):
    """Template of generate_hierarchy.py with certificate links and a width-2 root."""
    root_bound = data[0]['job']['max_path_vertices_bound']; root_width = data[0]['job']['width']
    J = range(N)
    s = ''.join(f'import BJobChecks{i}\n' for i in J) + 'import ActualJobFamily\n\nnamespace BroaderHierarchy\nopen ScalarFinite BroaderJobData ActualPrefixLift\nset_option maxHeartbeats 0\n\ninductive Job where\n' + ''.join(f'  | j{i}\n' for i in J) + '  deriving DecidableEq\n\n'
    for name, typ, expr in [('data', 'Data', lambda i: f'data{i}'), ('ranking', 'Ranking', lambda i: f'ranking{i}'),
                            ('width', 'Nat', lambda i: f'jobWidth {i}'), ('bound', 'Nat', lambda i: f'jobBound {i}')]:
        s += f'def {name} : Job → {typ}\n' + ''.join(f'  | .j{i} => {expr(i)}\n' for i in J) + '\n'
    s += 'def child : Job → Nat → Job\n'
    for i in J: s += f'  | .j{i}, c => ' + ''.join(f'if c={c} then .j{j} else ' for c, j in links.get(i, [])) + '.j0\n'
    s += '\ndef encode : Job → Nat → Nat × Fin 19 → Nat\n'
    for i in J: s += f'  | .j{i}, c => ' + ''.join(f'if c={c} then ScalarFinite.encode lift_certificate{j} else ' for c, j in links.get(i, [])) + 'fun _ => 0\n'
    s += '''
def graph (j : Job) := ScalarFinite.graph (data j)
def component (j : Job) := (ranking j).component
def cyclic (j : Job) := (ranking j).cyclic
def rank (j : Job) := (ranking j).rank
def height (j : Job) := 14-width j

theorem checked (j : Job) : CheckedRank (data j) (ranking j) := by
  cases j
''' + ''.join(f'  · exact checked_rank{i}\n' for i in J)
    def branches(i, success, fallback, k=0, indent=4):
        ls = links.get(i, [])
        if k == len(ls): return ' ' * indent + fallback + '\n'
        c, ch = ls[k]
        return (' ' * indent + f'by_cases h{k} : c={c}\n' + ' ' * indent + '· subst c\n' +
                '\n'.join(' ' * (indent + 2) + l for l in success(ch).split('\n')) + '\n' +
                ' ' * indent + '· ' + branches(i, success, fallback, k + 1, indent + 2).lstrip())
    s += "\ntheorem weight_eq (j : Job) (c : Nat) :\n    ComponentHierarchy.jobWeight cyclic child bound j c = (ranking j).weight c := by\n  cases j\n"
    for i in J:
        fb = f'simp [ComponentHierarchy.jobWeight, ComponentHierarchy.componentWeight, cyclic, ranking, ranking{i}, childCode{i}, child' + ''.join(f', h{k}' for k in range(len(links.get(i, [])))) + ']'
        s += '  · ' + branches(i, lambda _: 'decide', fb).lstrip()
    for theorem, statement in [
            ('height_decreases', 'height (child j c) < height j'),
            ('width_valid', '1 ≤ width j ∧ width j < L ∧ width (child j c) = width j + 1'),
            ('realizes', 'Realization (BoundedPrefixLift.bounded (ActualPrefixLift.lift (ActualPrefixLift.select (graph j) (fun v => component j v=c)))) (graph (child j c)) (encode j c)')]:
        params = '(L : Nat) (hL : 14 ≤ L) ' if theorem == 'width_valid' else ''
        s += f'\ntheorem {theorem} {params}(j : Job) (c : Nat) (hc : cyclic j c=true) :\n    {statement} := by\n  cases j\n'
        for i in J:
            fb = f'simp [cyclic, ranking, ranking{i}, childCode{i}' + ''.join(f', h{k}' for k in range(len(links.get(i, [])))) + '] at hc'
            def success(ch, theorem=theorem):
                if theorem == 'realizes': return f'exact lift_complete{ch}'
                if theorem == 'height_decreases': return 'decide'
                return 'dsimp [width, child, jobWidth, widths]\nomega'
            s += '  · ' + branches(i, success, fb).lstrip()
    s += f"""
theorem bound_eq (j : Job) : (ranking j).bound = bound j := by
  cases j <;> rfl

theorem vertex_bounds (j : Job) (v : Nat) (hv : (graph j).valid v) :
    ComponentHierarchy.jobWeight cyclic child bound j (component j v) ≤ rank j (component j v) ∧
    rank j (component j v) ≤ bound j := by
  rw [weight_eq, ← bound_eq]
  exact checked_vertex_bounds (checked j) v hv

theorem edge_bounds (j : Job) (u v bit : Nat)
    (hu : (graph j).valid u) (hv : (graph j).valid v)
    (_hb : bit ≤ 1) (he : (graph j).edge u v bit) :
    (cyclic j (component j u)=false → component j u ≠ component j v) ∧
    (component j u ≠ component j v →
      ComponentHierarchy.jobWeight cyclic child bound j (component j u)+rank j (component j v) ≤
      rank j (component j u)) := by
  rw [weight_eq]
  exact checked_edge_bounds (checked j) u v bit hu hv he

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory

theorem finite_root_bound (q : Nat → Nat) (L a s n : Nat) (path : Nat → Nat)
    (ha : Admissible L q) (hL : 14 ≤ L)
    (hp : ActualPath (ScalarFinite.graph data0) q L {root_width} a s path n) : n ≤ {root_bound} := by
  exact ActualJobFamily.actual_path_vertices_le graph width component cyclic child encode
    height bound rank q L ha height_decreases (width_valid L hL) realizes
    vertex_bounds edge_bounds Job.j0 a s path n hp

end BroaderHierarchy
"""
    start = s.index('def encode :'); end = s.index('def graph ', start)
    enc = s[start:end]; s = s[:start] + s[end:]
    start = s.index('theorem checked '); end = s.index('theorem weight_eq ', start)
    checked = s[start:end]; s = s[:start] + s[end:]
    start = s.index('theorem realizes '); end = s.index('theorem bound_eq ', start)
    realizes = s[start:end]; s = s[:start] + s[end:]
    start = s.index('theorem vertex_bounds ')
    endpoints = s[start:]; s = s[:start] + 'end BroaderHierarchy\n'
    s = s.replace('import BJobChecks', 'import BJobData')
    (OUT / 'BroaderHierarchyData.lean').write_text(s)
    final = 'import BroaderHierarchyData\n' + ''.join(f'import BJobChecks{i}\n' for i in J)
    final += 'namespace BroaderHierarchy\nopen ScalarFinite BroaderJobData ActualPrefixLift\nset_option maxHeartbeats 0\n\n'
    (OUT / 'BroaderHierarchy.lean').write_text(final + enc + checked + realizes + endpoints)


if __name__ == '__main__':
    main()
