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
        (ROOT / f"Cap3Batch{j:03d}.lean").write_text(
            "import Cap3Base\nnamespace P196.Agent116.Cap3\n"
            "set_option maxRecDepth 100000\nset_option maxHeartbeats 0\n"
            f"theorem batch{j:03d} : BatchCheck {start} {count} := by\n  decide +kernel\n"
            f"#print axioms batch{j:03d}\nend P196.Agent116.Cap3\n")
    lines = [f"import Cap3Batch{j:03d}" for j, _, _ in batches]
    lines += ["", "namespace P196.Agent116.Cap3", "open P196.Agent7.Finite", "set_option maxHeartbeats 0", "",
              "theorem cap3_exits_by_nine :", "    ∀ (p : Fin 8) (k : Fin 7240),",
              "      validOuter (encoded3 p k) = true →", "      staysWithin 3 9 (encoded3 p k) = false := by",
              "  intro p k", "  change ExitCheck p k.val"]
    for j, start, count in batches[:-1]:
        lines += [f"  by_cases h{j} : k.val < {start+count}",
                  f"  · exact of_batch batch{j:03d} p (by omega) (by omega)"]
    j, start, count = batches[-1]
    lines += [f"  exact of_batch batch{j:03d} p (by omega) (by omega)", "",
              "#print axioms cap3_exits_by_nine", "end P196.Agent116.Cap3", ""]
    (ROOT / "Cap3Finite.lean").write_text("\n".join(lines))
    print(f"Generated {len(batches)} batches covering {TOTAL} words and 8 phases.")

if __name__ == "__main__":
    generate()
