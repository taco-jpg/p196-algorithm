"""Independent standard-library LRAT checker; only positive RUP hints.

The checker does not import the CNF generator or a SAT library. Every added
clause is checked by literal-level unit propagation along explicit hints.
Deletion is honored for memory use; attempts to reuse deleted clauses fail.
"""
from pathlib import Path
import argparse, gzip, hashlib, json, time


def read(path):
    return gzip.open(path, 'rt') if str(path).endswith('.gz') else path.open()


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def check(cnf, proof):
    start = time.monotonic()
    clauses = {}
    with read(cnf) as source:
        for line in source:
            if not line.strip() or line.startswith('c'):
                continue
            if line.startswith('p'):
                _, kind, n, m = line.split()
                assert kind == 'cnf'
                n, m = int(n), int(m)
                continue
            row = [int(x) for x in line.split()]
            assert row[-1] == 0 and all(1 <= abs(x) <= n for x in row[:-1])
            clauses[len(clauses)+1] = tuple(row[:-1])
    assert len(clauses) == m
    assignment = [0] * (n+1)
    added = deleted = hint_count = 0
    empty = False
    last = m
    with read(proof) as source:
        for lineno, line in enumerate(source, 1):
            tok = line.split()
            if not tok or tok[0] == 'c':
                continue
            if tok[1] == 'd':
                assert tok[-1] == '0'
                for cid in map(int, tok[2:-1]):
                    clauses.pop(cid, None)
                    deleted += 1
                continue
            row = [int(x) for x in tok]
            cid = row[0]
            sep = row.index(0, 1)
            new = tuple(row[1:sep])
            hints = row[sep+1:-1]
            assert row[-1] == 0 and cid > last
            assert all(1 <= abs(x) <= n for x in new)
            assert all(x > 0 for x in hints), ('non-RUP hint', lineno)
            last = cid
            touched = []
            conflict = False
            for lit in new:
                var, value = abs(lit), -1 if lit > 0 else 1
                if assignment[var] and assignment[var] != value:
                    conflict = True
                    break
                if not assignment[var]:
                    assignment[var] = value
                    touched.append(var)
            if not conflict:
                for hint in hints:
                    assert hint in clauses, ('missing clause', lineno, hint)
                    hint_count += 1
                    unassigned = 0
                    count = 0
                    for lit in clauses[hint]:
                        val = assignment[abs(lit)]
                        assert not (val and val == (1 if lit > 0 else -1)), ('satisfied hint', lineno, hint)
                        if not val:
                            unassigned = lit
                            count += 1
                    assert count <= 1, ('nonunit hint', lineno, hint)
                    if count == 0:
                        conflict = True
                        break
                    var = abs(unassigned)
                    assignment[var] = 1 if unassigned > 0 else -1
                    touched.append(var)
            assert conflict, ('not RUP', lineno, cid)
            for var in touched:
                assignment[var] = 0
            clauses[cid] = new
            added += 1
            if not new:
                empty = True
    assert empty
    return dict(verified=True, cnf_variables=n, cnf_clauses=m,
                checked_additions=added, checked_hints=hint_count,
                deletion_ids=deleted, empty_clause_proved=True,
                seconds=time.monotonic()-start,
                cnf_sha256=sha(cnf), proof_sha256=sha(proof),
                claim='UNSAT of supplied CNF; semantics require separate encoding audit',
                positive_lychrel_proof=False)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('stem')
    p.add_argument('--gzip-proof', action='store_true')
    args = p.parse_args()
    stem = Path(args.stem)
    out = check(stem.with_suffix('.cnf'), Path(str(stem)+'.lrat'+('.gz' if args.gzip_proof else '')))
    Path(str(stem)+'.lrat_check.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))
