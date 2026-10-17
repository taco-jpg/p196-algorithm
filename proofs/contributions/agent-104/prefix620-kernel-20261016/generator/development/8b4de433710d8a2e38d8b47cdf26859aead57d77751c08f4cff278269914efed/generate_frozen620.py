#!/usr/bin/env python3
"""Instantiate the retained Agent124 code-tree emitter from the frozen 620 table.

The byte-exact Agent124 generator and its scope module are retained in upstream/.
This adapter replaces only its discovery callback by the already-published rank
table, then changes generated instance/module names and adds audit declarations.
Agent124's semantic checker, definitions, and theorem identifiers stay unchanged.
Every finite obligation is checked using `decide +kernel` in the generated Lean.
Python generation is not proof verification.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import io
import itertools
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
EXPECTED_CERT = "e6c447fa7efa26e94d1a8064a9336922d3eeb2e1e55176f8043e1cd9dbe3cea5"
EXPECTED_GEN = "a94f2e4c1b0bf3cbfb82a181ed004a686f767a6eec64f76e2f75d974a4db1433"
EXPECTED_SCOPE = "c51b81cb008e7214a68b65d750ba563f4d912480d326f4c71ea142d60aa51fe2"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def preserve_write(path: Path, data: bytes) -> None:
    if path.exists() and path.read_bytes() != data:
        old = path.read_bytes()
        old_dir = HERE / "development" / hashlib.sha256(old).hexdigest()
        old_dir.mkdir(parents=True, exist_ok=True)
        (old_dir / path.name).write_bytes(old)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=HERE.parents[3])
    parser.add_argument("--leaf", type=int, default=256)
    parser.add_argument("--leaves-per-data", type=int, default=4)
    parser.add_argument("--leaves-per-rows", type=int, default=1)
    parser.add_argument("--finite-batch", type=int, default=100)
    args = parser.parse_args()
    if min(args.leaf, args.leaves_per_data, args.leaves_per_rows, args.finite_batch) <= 0:
        raise ValueError("Batch sizes must be positive")

    src = HERE / "inputs/certificate_620.json"
    gen_path = HERE / "upstream/gen_code.py"
    scope_path = HERE / "upstream/scope.py"
    assert digest(src) == EXPECTED_CERT
    assert digest(gen_path) == EXPECTED_GEN
    assert digest(scope_path) == EXPECTED_SCOPE
    cert = json.loads(src.read_text())
    assert (cert["schema"], cert["prefix"], cert["width"], cert["palindrome_height_bound"]) == (1, "620", 7, 12)
    ranks = {tuple(row["word"]): row["rank"] for row in cert["nodes"]}
    assert len(ranks) == len(cert["nodes"]) == 59189
    assert len({tuple(w) for w in cert["initial"]}) == len(cert["initial"]) == 10002
    assert max(ranks.values()) == 11
    assert max(ranks[tuple(w)] for w in cert["initial"]) == 11

    spec = importlib.util.spec_from_file_location("agent124_retained_gen_code", gen_path)
    upstream = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(upstream)

    def frozen_closure(prefixes, k):
        assert prefixes == [(6, 2, 0)] and k == 7
        return dict(ranks), {(6, 2, 0): 11}

    upstream.closure = frozen_closure
    raw = HERE / f"upstream-output-leaf{args.leaf}"
    raw.mkdir(exist_ok=True)
    saved_argv = sys.argv
    captured = io.StringIO()
    try:
        sys.argv = [str(gen_path), "7", str(raw), "620", "--tag", "Prefix620",
                    "--leaf", str(args.leaf), "--leaves-per-data", str(args.leaves_per_data),
                    "--leaves-per-rows", str(args.leaves_per_rows)]
        with contextlib.redirect_stdout(captured):
            upstream.main()
    finally:
        sys.argv = saved_argv
    (raw / "generation.log").write_text(captured.getvalue())
    old_meta = json.loads((raw / "A124Prefix620-meta.json").read_text())

    def new_name(old: str) -> str:
        tail = old.removeprefix("A124Prefix620")
        tail = {"Tree": "DataTree", "Branch": "RowsBranch", "AllRows": "RowsAll",
                "Short": "ShortAll", "Initial": "InitialAll", "Final": "Final"}.get(tail, tail)
        return "Agent104Prefix620" + tail

    mappings = {old: new_name(old) for old in old_meta["build_order"]}
    emitted = {}
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    for old in old_meta["build_order"]:
        if old.endswith("Final"):
            # Preserve the upstream final reference. The explicitly delegated
            # Agent104 final endpoint is emitted separately below.
            continue
        source = (raw / (old + ".lean")).read_text()
        for before, after in sorted(mappings.items(), key=lambda p: -len(p[0])):
            source = source.replace(before, after)
        source = source.replace("Agent124.CertPrefix620", "Agent104.Prefix620")
        source = source.replace("set_option maxRecDepth 100000\n",
                                "set_option maxRecDepth 100000\nset_option maxHeartbeats 0\n")
        source = source.replace("(by decide)", "(by decide +kernel)")
        source = ("/- Agent #104 concrete 620 instance, emitted from the frozen published certificate.\n"
                  "Retained Agent #124 gen_code.py supplies the tree and checker wiring;\n"
                  "all Agent124 semantic dependencies and attribution are unchanged. -/\n" + source)
        if old.endswith("Initial"):
            marker = "\nend Agent104.Prefix620\n"
            extra = ("\nopen Agent124.PrefixR\n"
                     "theorem initialBounded : InitialBounded 7 6 2 0 11 (R ranks) :=\n"
                     "  initialBounded_of_all init_620\n"
                     "#print axioms init_620\n#print axioms initialBounded\n")
            assert source.count(marker) == 1
            source = source.replace(marker, extra + marker)
        new = mappings[old]
        assert any(new.startswith("Agent104Prefix620" + p) for p in ["Data", "Rows", "Initial", "Short"])
        data = source.encode()
        preserve_write(output / (new + ".lean"), data)
        emitted[new] = {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data),
                        "upstream_generated_module": old, "path": str(output / (new + ".lean"))}

    # The upstream single-module short and initial reductions exceeded the
    # author pilot's memory budget. Keep that exact attempt above and split only
    # its finite lists. Kernel-checked equalities to the original generic lists
    # establish full coverage; the semantic checker and rank tree do not change.
    finite_order = []

    def emit_finite(name, imports, body):
        source = ("/- Agent #104 finite-list partition of the frozen 620 instance.\n"
                  "Agent #124's original semantic checker and enumerations are unchanged. -/\n"
                  + "".join("import " + mod + "\n" for mod in imports)
                  + "\nnamespace Agent104.Prefix620\n"
                  + "open Agent124.CodeCert Agent124.PrefixK Agent124.PrefixR\n"
                  + "set_option maxRecDepth 100000\nset_option maxHeartbeats 0\n\n"
                  + body + "\nend Agent104.Prefix620\n")
        data = source.encode()
        preserve_write(output / (name + ".lean"), data)
        emitted[name] = {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data),
                         "upstream_generated_module": None, "path": str(output / (name + ".lean")),
                         "role": "Agent104 finite partition or endpoint assembly"}
        finite_order.append(name)

    def lean_word(w):
        return "[" + ", ".join(map(str, w)) + "]"

    def lean_words(ws):
        return "[\n  " + ",\n  ".join(lean_word(w) for w in ws) + "\n]"

    def chunks(ws):
        return [ws[i:i + args.finite_batch] for i in range(0, len(ws), args.finite_batch)]

    initial_words = []
    for j in range(5):
        for tail in itertools.product(range(10), repeat=j):
            w = (6, 2, 0) + tail
            if len(w) == 7 or (w == w[::-1] and (len(w) % 2 == 0 or w[len(w) // 2] % 2 == 0)):
                initial_words.append(w)
    assert len(initial_words) == 10002
    assert set(initial_words) == {tuple(w) for w in cert["initial"]}
    initial_blocks = chunks(initial_words)
    initial_names = [f"initial_block{i:03d}" for i in range(len(initial_blocks))]
    emit_finite("Agent104Prefix620DataInitialWords", ["Agent124CodeCert"],
                "\n\n".join(f"noncomputable def {name} : List (List Nat) := {lean_words(block)}"
                              for name, block in zip(initial_names, initial_blocks)))
    emit_finite("Agent104Prefix620InitialCoverage", ["Agent104Prefix620DataInitialWords"],
                "theorem initial_cover : initialWordsK 7 6 2 0 =\n  "
                + " ++\n  ".join(initial_names) + " := by\n  rfl\n")
    initial_modules = []
    initial_checks = []
    for i, name in enumerate(initial_names):
        module = f"Agent104Prefix620Initial{i:03d}"
        check = f"initial_ok{i:03d}"
        emit_finite(module, ["Agent104Prefix620DataTree", "Agent104Prefix620DataInitialWords"],
                    f"theorem {check} : {name}.all (initOKC ranks 11) = true := by\n  decide +kernel\n")
        initial_modules.append(module)
        initial_checks.append(check)
    emit_finite("Agent104Prefix620InitialAll", ["Agent104Prefix620InitialCoverage"] + initial_modules,
                "theorem init_620 : (initialWordsK 7 6 2 0).all (initOKC ranks 11) = true := by\n"
                "  rw [initial_cover]\n"
                "  simp only [List.all_append, " + ", ".join(initial_checks) + ", Bool.and_self]\n\n"
                "theorem initialBounded : InitialBounded 7 6 2 0 11 (R ranks) :=\n"
                "  initialBounded_of_all init_620\n\n"
                "#print axioms init_620\n#print axioms initialBounded\n")

    short_blocks = []
    short_widths = []
    for n in range(7):
        ws = []
        for half in itertools.product(range(19), repeat=(n + 1) // 2):
            w = tuple(half[min(i, n - 1 - i)] for i in range(n))
            if w and w[0] > 0 and (n % 2 == 0 or w[n // 2] % 2 == 0):
                ws.append(w)
        indices = []
        for block in chunks(ws):
            indices.append(len(short_blocks))
            short_blocks.append(block)
        short_widths.append({"width": n, "words": len(ws), "block_indices": indices})
    assert sum(x["words"] for x in short_widths) == 10467
    short_names = [f"short_block{i:03d}" for i in range(len(short_blocks))]
    emit_finite("Agent104Prefix620DataShortWords", ["Agent124CodeCert"],
                "\n\n".join(f"noncomputable def {name} : List (List Nat) := {lean_words(block)}"
                              for name, block in zip(short_names, short_blocks)))
    covers = []
    for item in short_widths:
        n = item["width"]
        rhs = " ++\n  ".join(short_names[i] for i in item["block_indices"]) or "[]"
        covers.append(f"theorem short_cover_w{n} : symWords {n} =\n  {rhs} := by\n  rfl\n")
    emit_finite("Agent104Prefix620ShortCoverage", ["Agent104Prefix620DataShortWords"], "\n".join(covers))
    short_modules = []
    short_checks = []
    for i, name in enumerate(short_names):
        module = f"Agent104Prefix620Short{i:03d}"
        check = f"short_ok{i:03d}"
        emit_finite(module, ["Agent104Prefix620DataTree", "Agent104Prefix620DataShortWords"],
                    f"theorem {check} : {name}.all (shortOKC ranks) = true := by\n  decide +kernel\n")
        short_modules.append(module)
        short_checks.append(check)
    short_proofs = []
    for item in short_widths:
        n = item["width"]
        checks = [short_checks[i] for i in item["block_indices"]]
        proof = f"theorem short_w{n} : (symWords {n}).all (shortOKC ranks) = true := by\n  rw [short_cover_w{n}]\n"
        if not checks:
            proof += "  rfl\n"
        elif len(checks) == 1:
            proof += "  exact " + checks[0] + "\n"
        else:
            proof += "  simp only [List.all_append, " + ", ".join(checks) + ", Bool.and_self]\n"
        short_proofs.append(proof)
    emit_finite("Agent104Prefix620ShortAll", ["Agent104Prefix620ShortCoverage"] + short_modules,
                "\n".join(short_proofs)
                + "\ntheorem short : ShortClosed 7 (R ranks) := shortClosed_of_widths fun n hn => by\n"
                + "  have : n = 0 ∨ n = 1 ∨ n = 2 ∨ n = 3 ∨ n = 4 ∨ n = 5 ∨ n = 6 := by omega\n"
                + "  rcases this with rfl | rfl | rfl | rfl | rfl | rfl | rfl\n"
                + "".join(f"  · exact short_w{n}\n" for n in range(7))
                + "\n#print axioms short\n")

    emit_finite("Agent104Prefix620", ["Agent104Prefix620RowsAll", "Agent104Prefix620ShortAll",
                                     "Agent104Prefix620InitialAll"],
                "/-- Leading decimal digits 620 in the exact canonical numeral. -/\n"
                "abbrev Starts620 (P : Nat) : Prop := Starts3 6 2 0 P\n\n"
                "/-- Decimal palindromes whose leading three digits are 620. -/\n"
                "abbrev PalindromeStarts620 (P : Nat) : Prop := PalStarts3 6 2 0 P\n\n"
                "/-- Expose the numeric meaning of the target predicate. -/\n"
                "theorem palindromeStarts620_iff (P : Nat) :\n"
                "    PalindromeStarts620 P ↔ Lychrel196.Palindrome P ∧\n"
                "      ∃ e W, DecimalDigits.Canonical P e W ∧ 3 ≤ W ∧\n"
                "        e (W - 1) = 6 ∧ e (W - 2) = 2 ∧ e (W - 3) = 0 := Iff.rfl\n\n"
                "/-- Any positive seed reaches a 620-prefix palindrome only within 12 additions.\n"
                "This is the certified upper bound; no optimality claim is made. -/\n"
                "theorem ancestry_bound12 :\n"
                "    ∀ A P t, 0 < A → PalindromeStarts620 P → Lychrel196.orbit A t = P → t ≤ 12 :=\n"
                "  ancestry_bound_of_R 7 6 2 0 11 (by decide +kernel) (by decide +kernel)\n"
                "    (R ranks) allRows short initialBounded\n\n"
                "/-- No iterate from 196 is a decimal palindrome beginning 620. -/\n"
                "theorem no_196_620_palindrome :\n"
                "    ∀ t, ¬ PalindromeStarts620 (Lychrel196.orbit 196 t) :=\n"
                "  no_196_of_R 7 6 2 0 11 (by decide +kernel) (by decide +kernel) (by decide +kernel)\n"
                "    (R ranks) allRows short initialBounded\n\n"
                "#print axioms palindromeStarts620_iff\n"
                "#print axioms ancestry_bound12\n#print axioms no_196_620_palindrome\n")

    meta = {"scope": "Untrusted generated data and concrete kernel obligations; no build claim",
            "owner": "Agent #104", "checker_author": "Agent #124",
            "certificate_sha256": EXPECTED_CERT, "upstream_generator_sha256": EXPECTED_GEN,
            "upstream_scope_sha256": EXPECTED_SCOPE,
            "adapter_sha256": digest(Path(__file__)), "leaf": args.leaf,
            "leaves_per_data": args.leaves_per_data, "leaves_per_rows": args.leaves_per_rows,
            "finite_batch": args.finite_batch,
            "nodes": len(ranks), "initial_words": len(cert["initial"]),
            "width": 7, "max_rank": 11, "ancestry_bound": 12,
            "leaves": old_meta["leaves"], "internal": old_meta["internal"],
            "leaf_sizes": old_meta["leaf_sizes"],
            "build_order": [mappings[m] for m in old_meta["build_order"]
                            if not m.endswith(("Final", "Short", "Initial"))] + finite_order,
            "finite_partition": {"initial_block_sizes": [len(b) for b in initial_blocks],
                                 "short_block_sizes": [len(b) for b in short_blocks],
                                 "short_widths": short_widths,
                                 "coverage": "Kernel equality to original initialWordsK and each symWords enumeration"},
            "finite_pilot_modules": [initial_modules[0], short_modules[short_widths[5]["block_indices"][0]],
                                     short_modules[short_widths[6]["block_indices"][0]],
                                     "Agent104Prefix620InitialCoverage", "Agent104Prefix620ShortCoverage"],
            "sources": emitted,
            "endpoint_interface": {"namespace": "Agent104.Prefix620",
                "rows": "allRows", "short": "short", "initial": "initialBounded",
                "root_module": "Agent104Prefix620", "ancestry": "ancestry_bound12",
                "exclusion": "no_196_620_palindrome"}}
    preserve_write(HERE / "GENERATION_MANIFEST.json", (json.dumps(meta, indent=2) + "\n").encode())
    print(json.dumps({k: meta[k] for k in ["nodes", "initial_words", "max_rank", "ancestry_bound",
                                         "leaves", "internal", "leaf"]}, indent=2))
    print("generated_modules", len(emitted))
    print("manifest", HERE / "GENERATION_MANIFEST.json")


if __name__ == "__main__":
    main()
