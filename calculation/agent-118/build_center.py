#!/usr/bin/env python3
"""Build a pinned, guarded P<=48 variant of the existing exact center solver.

Agent 10 identified the original period/segment/packed-key limits in issue #292.
This helper materializes capacity/validation/resource guards in temporary files;
the original transition formulas, state equality, and 120-layer detector remain.
It is an engineering guard, not a proof of the solver's mathematical model.
"""

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import re
import subprocess

SOURCE = Path(__file__).resolve().parents[1] / "neutral_band/structure/cauto_fast.cpp"
SOURCE_SHA256 = "eb2e6b18b09fdfcae0a5b6b818d23291123ed6a76b59fb6e531589e7f6d00fff"

GUARD = r'''
[[noreturn]] void undecided118(const char* reason) {
  throw runtime_error(reason);
}
long long number118(const string& text) {
  size_t n = 0;
  long long value = stoll(text, &n);
  if (text.empty() || n != text.size()) undecided118("invalid_integer");
  return value;
}
void arguments118(int argc, char** argv) {
  if (argc < 6) undecided118("missing_arguments");
  long long base = number118(argv[1]);
  string ee = argv[2], gg = argv[3];
  size_t p = ee.size();
  if (base < 2 || base > 62) undecided118("unsupported_base");
  if (!p || p > 48 || gg.size() != p) undecided118("unsupported_period");
  if (ee.find_first_not_of("01") != string::npos || gg.find_first_not_of("01") != string::npos)
    undecided118("nonbinary_driver");
  long long lo = number118(argv[4]), hi = number118(argv[5]);
  if (lo < 1 || hi < lo || hi > 1000000) undecided118("unsupported_length_range");
  int G = count(gg.begin(), gg.end(), '1');
  if (G % 2) undecided118("odd_total_overflow");
  int K = G / 2;
  if (2 * p + 6 * G + 7 * K > 256) undecided118("legacy_key_exceeds_256_bits");
  bool seenV = false, seenAll = false;
  for (int i = 6; i < argc; ++i) {
    string flag = argv[i];
    if (flag == "-v") {
      if (seenV || i + 1 >= argc) undecided118("invalid_v_option");
      seenV = true; string vv = argv[++i];
      if (vv.size() != p || vv.find_first_not_of("01") != string::npos ||
          count(vv.begin(), vv.end(), '1') != K) undecided118("invalid_trim_schedule");
    } else if (flag == "-vall") {
      if (seenAll) undecided118("duplicate_vall");
      seenAll = true;
    } else if (flag == "-cap") {
      if (i + 1 >= argc) undecided118("missing_cap");
      long long cap = number118(argv[++i]);
      if (cap < 1 || cap > 100000000) undecided118("unsupported_cap");
    } else if (flag == "-w" || flag == "-wlegacy" || flag == "-legacy" ||
               flag == "-sz" || flag == "-allm" || flag == "-q") {
    } else undecided118("unsupported_option");
  }
  if (seenV == seenAll) undecided118("need_exactly_one_v_or_vall");
  if (seenAll) {
    unsigned long long n = 1;
    for (int k = 1; k <= K; ++k) {
      n = n * (p - K + k) / k;
      if (n > 1000000) undecided118("pattern_enumeration_limit_use_single_v");
    }
  }
}
'''


def replace_once(source: str, old: str, new: str) -> str:
    """Fail closed when the pinned edit boundary unexpectedly differs."""
    if source.count(old) != 1:
        raise RuntimeError(f"source patch anchor count != 1: {old[:80]!r}")
    return source.replace(old, new, 1)


def patched_source() -> str:
    raw = SOURCE.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != SOURCE_SHA256:
        raise RuntimeError(f"UNDECIDED source_sha256_mismatch: {digest}")
    source = raw.decode()
    patches = [
        ("#include <memory>", "#include <memory>\n#include <stdexcept>\n#include <exception>"),
        ("using namespace std;", "using namespace std;\n" + GUARD),
        ("const int MAXP = 32;", "const int MAXP = 48;"),
        ("const int MAXNS = 16, MAXL = 32;", "const int MAXNS = 16, MAXL = 48;"),
        ("  K128 x = (K128)val;", "  if (w < 1 || w > 63 || sh < 0 || sh + w > 256 || val >= (1ULL << w))\n    undecided118(\"packed_key_capacity\");\n  K128 x = (K128)val;"),
        ("    uint32_t id = S.cfg.size(); S.cfg.push_back(c);", "    if (S.cfg.size() >= UINT32_MAX) undecided118(\"local_config_id_capacity\");\n    uint32_t id = S.cfg.size(); S.cfg.push_back(c);"),
        ("    if (l < 0) { l = S.lidInfo.size();", "    if (l < 0) { if (S.lidInfo.size() >= INT32_MAX) undecided118(\"local_state_id_capacity\"); l = S.lidInfo.size();"),
        ("    NS = ord.size(); ZW = 2 * b; sg.clear(); sg.resize(NS);", "    NS = ord.size();\n    if (NS < 1 || NS > MAXNS) undecided118(\"segment_count_capacity\");\n    for (const auto& segment : ord) if (segment.empty() || segment.size() > MAXL) undecided118(\"segment_length_capacity\");\n    ZW = 2 * b; sg.clear(); sg.resize(NS);"),
        ("    Ent en; en.start = S2.pool.size(); en.cnt = outs.size();", "    if (S2.pool.size() >= UINT32_MAX || outs.size() >= UINT32_MAX || S2.pool.size() + outs.size() >= UINT32_MAX) undecided118(\"local_pool_capacity\");\n    Ent en; en.start = S2.pool.size(); en.cnt = outs.size();"),
        ("        cnt[s] = en.cnt; lst[s] = nullptr; cnt[s] = en.cnt;", "        if (par && en.cnt > 65536) undecided118(\"witness_choice_capacity\");\n        cnt[s] = en.cnt; lst[s] = nullptr; cnt[s] = en.cnt;"),
        ("        if (out.insert(nw) && par) { par->push_back((uint32_t)i); for (int s2 = 0; s2 < NS; s2++) ch->push_back((uint16_t)idx[s2]); }", "        bool fresh = out.insert(nw);\n        if ((long)out.n > cap) { maxStates = max(maxStates, out.n); return false; }\n        if (fresh && par) { par->push_back((uint32_t)i); for (int s2 = 0; s2 < NS; s2++) ch->push_back((uint16_t)idx[s2]); }"),
        ("  vector<size_t> sz; solve_instance(m0, true, g_cap, &Cw, &sz);", "  vector<size_t> sz; int result118 = solve_instance(m0, true, g_cap, &Cw, &sz);\n  if (result118 != 1 || !verify_cycle(Cw)) undecided118(\"witness_reconstruction_failed\");"),
        ("  int mlo = 1;\n  for (int mm = 1;", "  int mlo = -1;\n  for (int mm = 1;"),
        ("  PI.mlo = mlo;", "  if (mlo < 1) undecided118(\"all_length_threshold_not_found\");\n  PI.mlo = mlo;"),
        ("int main(int argc, char** argv) {", "int solver_main118(int argc, char** argv) {"),
        ("  return 0;\n}\n", "  if (g_ncap) { fprintf(stderr, \"UNDECIDED capped_or_noperiod=%ld\\n\", g_ncap); return 2; }\n  return 0;\n}\n"),
    ]
    for old, new in patches:
        source = replace_once(source, old, new)
    source += r'''

int main(int argc, char** argv) {
  try {
    arguments118(argc, argv);
    return solver_main118(argc, argv);
  } catch (const exception& error) {
    fprintf(stderr, "UNDECIDED %s\n", error.what());
    return 2;
  } catch (...) {
    fprintf(stderr, "UNDECIDED unexpected_exception\n");
    return 2;
  }
}
'''
    return source


def build(output_dir: Path, sanitize: bool = False, cxx: str = "c++") -> Path:
    """Return the cauto118 binary, with generated source beside it."""
    output_dir = Path(output_dir).resolve()
    repo = SOURCE.parents[3].resolve()
    if output_dir == repo or repo in output_dir.parents:
        raise ValueError("generated source/binary must be outside the repository")
    output_dir.mkdir(parents=True, exist_ok=True)
    source_path, binary = output_dir / "cauto118.cpp", output_dir / "cauto118"
    source_path.write_text(patched_source())
    flags = ["-O1", "-g", "-fsanitize=address,undefined", "-fno-omit-frame-pointer"] if sanitize else ["-O2"]
    subprocess.run([cxx, "-std=c++17", *flags, str(source_path), "-o", str(binary)], check=True, timeout=180)
    return binary


def selftest(binary: Path) -> dict:
    """Exercise an actual long segment, rejection, and original answers.

    Sanitizer recipe: --sanitize --selftest --out-dir /tmp/a118-center-asan.
    The separate check_center.py owns the eight known-base certificate tests.
    """
    mirror_path = SOURCE.parents[2] / "neutral_band_search.py"
    spec = importlib.util.spec_from_file_location("agent118_control_source", mirror_path)
    mirror = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mirror)
    certificates = dict(mirror._lean_certs())

    def run(args, exe=binary):
        return subprocess.run([str(exe), *args], capture_output=True, text=True, timeout=30)

    def control(base, edges, trims, length):
        ee = "".join(str(mirror.e1(base, edge[0])) for edge in edges)
        gg = "".join(str(mirror.gam(base, edge[0], edge[1])) for edge in edges)
        result = run([str(base), ee, gg, str(length), str(length), "-v", trims, "-w", "-cap", "100000"])
        hits = [line for line in result.stdout.splitlines() if line.startswith("FEASIBLE")]
        if result.returncode or not hits:
            raise RuntimeError(f"positive control failed: base={base}, {result.stderr}, {result.stdout}")
        for line in hits:
            centers = [[int(x) for x in word.split(",")] for word in re.findall(r" C\d+=\[([^\]]*)\]", line)]
            if len(centers) != len(edges):
                raise RuntimeError("incomplete returned witness")
            for t, center in enumerate(centers):
                carry, digits = int(ee[t]), []
                for coefficient in center:
                    carry, digit = divmod(coefficient + carry, base)
                    digits.append(digit)
                if center != center[::-1] or carry != 1 - int(ee[t]):
                    raise RuntimeError("invalid carry/symmetry witness")
                if gg[t] == "1":
                    digits.append((base - 1) * int(ee[t]))
                raw = [x + y for x, y in zip(digits, digits[::-1])]
                pad = [base - 1] * int(trims[t])
                if raw != pad + centers[(t + 1) % len(edges)] + pad:
                    raise RuntimeError("invalid returned transition witness")

    # Four repeats of the base32 positive, moved to a 45-step segment by padding.
    control(32, certificates[32] * 4, "1111" + "0" * 44, 10)
    malformed = [
        ["10", "", "", "1", "1", "-v", ""],
        ["10", "0" * 49, "0" * 49, "1", "1", "-v", "0" * 49],
        ["10", "0020", "1010", "1", "1", "-v", "0001"],
        ["10", "0011", "1010", "1", "1", "-v", "001"],
        ["10", "0011", "1010", "1", "1", "-v", "0002"],
        ["10", "0011", "1010", "1", "1", "-v", "0011"],
        ["10", "0011", "1010", "1", "1", "-v"],
        ["10", "01" * 24, "1" * 48, "1", "1", "-v", "01" * 24],
        ["10", "0011", "1010", "1", "1", "-v", "0001", "-cap", "0"],
        ["10", "101010010101" * 4, "100010001000" * 4, "1", "1", "-vall"],
    ]
    for args in malformed:
        result = run(args)
        if result.returncode != 2 or "UNDECIDED" not in result.stderr or "status=none" in result.stdout:
            raise RuntimeError(f"guard failed: {args}")
    result = run(["11", "011011", "001001", "1", "1", "-v", "000001", "-allm", "-cap", "1"])
    if result.returncode != 2 or "UNDECIDED" not in result.stderr or "status=none" in result.stdout:
        raise RuntimeError("capped computation was not marked undecided")
    original = binary.parent / "cauto-original"
    subprocess.run(["c++", "-O2", "-std=c++17", str(SOURCE), "-o", str(original)], check=True, timeout=180)
    rng, compared = random.Random(118), 0
    for _ in range(60):
        period, base = rng.randrange(3, 8), rng.choice([2, 3, 4, 5, 7, 10])
        gg = "".join(rng.choice("01") for _ in range(period))
        if not gg.count("1") or gg.count("1") % 2:
            continue
        ee, vv = "".join(rng.choice("01") for _ in range(period)), ["0"] * period
        for t in rng.sample(range(period), gg.count("1") // 2):
            vv[t] = "1"
        args = [str(base), ee, gg, "1", "1", "-v", "".join(vv), "-allm", "-cap", "50000"]
        before, after = run(args, original), run(args)
        significant = lambda out: [line for line in out.splitlines() if line.startswith(("FEASIBLE", "CAPPED", "NOPERIOD"))]
        if significant(before.stdout) != significant(after.stdout) or re.findall(r"status=(\w+)", before.stdout) != re.findall(r"status=(\w+)", after.stdout):
            raise RuntimeError(f"original/guarded answer mismatch: {args}")
        compared += 1
    return {"P48_longest_segment_positive": 45,
            "malformed_rejections": len(malformed), "cap_rejection": True,
            "original_differential_cases": compared}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=Path("/tmp/p196-agent118-center"))
    parser.add_argument("--sanitize", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--cxx", default="c++")
    args = parser.parse_args()
    binary = build(args.out_dir, args.sanitize, args.cxx)
    result = {"binary": str(binary), "upstream_sha256": SOURCE_SHA256,
              "generated_sha256": hashlib.sha256(binary.with_suffix(".cpp").read_bytes()).hexdigest(),
              "sanitizers": args.sanitize}
    if args.selftest:
        result["selftest"] = selftest(binary)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
