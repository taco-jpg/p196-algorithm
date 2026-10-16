#!/usr/bin/env python3
"""Regenerate complete, nonoverlapping kernel-checked cap-three batches.
This generates Lean proof source; Python execution is not proof evidence.
"""
from pathlib import Path

SIZE = 128
TOTAL = 7240
ROOT = Path(__file__).resolve().parent

def generate():
    batches = [(j, start, min(SIZE, TOTAL - start)) for j, start in enumerate(range(0, TOTAL, SIZE))]
    for j, start, count in batches:
        (ROOT / f"Cap3AllBatch{j:03d}.lean").write_text(
            "import Cap3AllBase\nnamespace P196.Agent116.Cap3\n"
            "set_option maxRecDepth 100000\nset_option maxHeartbeats 0\n"
            f"theorem allBatch{j:03d} : AllBatchCheck {start} {count} := by\n  decide +kernel\n"
            f"#print axioms allBatch{j:03d}\nend P196.Agent116.Cap3\n")
    lines = [f"import Cap3AllBatch{j:03d}" for j, _, _ in batches]
    lines += ["", "namespace P196.Agent116.Cap3", "open P196.Agent7.Finite", "set_option maxHeartbeats 0", "",
              "theorem cap3_all_exits_by_ten :", "    ∀ (p : Fin 8) (k : Fin 7240),",
              "      staysWithin 3 10 (encoded3 p k) = false := by",
              "  intro p k", "  change AllExitCheck p k.val"]
    for j, start, count in batches[:-1]:
        lines += [f"  by_cases h{j} : k.val < {start+count}",
                  f"  · exact of_all_batch allBatch{j:03d} p (by omega) (by omega)"]
    j, start, count = batches[-1]
    lines += [f"  exact of_all_batch allBatch{j:03d} p (by omega) (by omega)", "",
              "#print axioms cap3_all_exits_by_ten", "end P196.Agent116.Cap3", ""]
    (ROOT / "Cap3AllFinite.lean").write_text("\n".join(lines))
    print(f"Generated {len(batches)} batches covering {TOTAL} words and 8 phases.")

if __name__ == "__main__":
    generate()
