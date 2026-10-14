"""Necessary finite constraints for arbitrary-alphabet period-three codes.

Every code motif is fixed by the selected macro clock when repeated forever.
All freely concatenated code words must return to code words.  Necessary
constraints are checked on cyclic AB, AAB, ABB inputs; the alphabet is not
restricted to two letters.  Solver results are discovery only.
"""
from itertools import combinations
from pathlib import Path
import json, time
import z3
from bulk_mixture import macro


def run(name):
    path = Path(__file__).with_name(name+"_mixture.json")
    d = json.loads(path.read_text())
    motifs = tuple(map(tuple, d["candidate_motifs"]))
    index = {a: i for i, a in enumerate(motifs)}
    x = [z3.Bool("m"+str(i)) for i in range(len(motifs))]
    s = z3.Solver()
    s.add(z3.PbGe([(v, 1) for v in x], 2))
    records = []
    started = time.monotonic()
    for i, j in combinations(range(len(motifs)), 2):
        for word in ((i,j), (i,i,j), (i,j,j)):
            source = sum((motifs[k] for k in word), ())
            options = []
            outputs = macro(source, d["clock"])
            for q in outputs:
                blocks = [q[k:k+3] for k in range(0, len(q), 3)]
                if all(b in index for b in blocks):
                    options.append(sorted({index[b] for b in blocks}))
            options = sorted({tuple(a) for a in options})
            records.append([list(word), options])
            s.add(z3.Implies(z3.And(x[i], x[j]),
                            z3.Or(*[z3.And(*[x[k] for k in a]) for a in options])))
    result = s.check()
    doc = {"name": name, "motifs": motifs, "clock": d["clock"],
           "constraints": records, "result": str(result),
           "seconds": time.monotonic()-started}
    if result == z3.sat:
        doc["code"] = [a for a, v in zip(motifs, x) if z3.is_true(s.model().eval(v))]
    Path(__file__).with_name(name+"_alphabet_constraints.json").write_text(json.dumps(doc, indent=2)+"\n")
    print(json.dumps({k: v for k, v in doc.items() if k not in ("motifs", "clock", "constraints")}), flush=True)


if __name__ == "__main__":
    run("clock33_gain12")
    run("clock24_gain12")
