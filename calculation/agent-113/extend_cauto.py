#!/usr/bin/env python3
"""Build/run a guarded P<=48 variant of the existing exact center automaton.

The upstream source stays unchanged. Every source replacement is anchored and
the input digest is checked. This is runtime hardening, not a new automaton or
a proof of a decimal result. A fixed -v schedule is mandatory; no implicit
enumeration or unverified skip files are accepted. Native and wrapper guards
both reject malformed inputs. CAPPED/NOPERIOD/timeouts remain UNDECIDED.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import shlex
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "calculation/neutral_band/structure/cauto_fast.cpp"
SOURCE_SHA256 = "eb2e6b18b09fdfcae0a5b6b818d23291123ed6a76b59fb6e531589e7f6d00fff"

KEY = r'''// Agent113: nine words hold all 2P+6G+7K <=552 bits at P<=48.
struct LKey {
  array<uint64_t, 9> w{};
  bool operator==(const LKey& o) const { return w == o.w; }
  bool operator<(const LKey& o) const {
    return lexicographical_compare(w.rbegin(), w.rend(), o.w.rbegin(), o.w.rend());
  }
};
struct LKH {
  size_t operator()(const LKey& k) const {
    uint64_t h = 0x9E3779B97F4A7C15ULL;
    for (uint64_t x : k.w) {
      h ^= x + 0x9E3779B97F4A7C15ULL + (h << 6) + (h >> 2);
    }
    return static_cast<size_t>(h);
  }
};
'''

PUTBITS = r'''static inline void putbits(LKey& k, int& sh, uint64_t val, int w) {
  if (w < 1 || w > 7 || sh < 0 || sh + w > 576 || val >= (1ULL << w))
    throw runtime_error("invalid packed field");
  const int word = sh / 64, bit = sh % 64;
  k.w[word] |= val << bit;
  if (bit + w > 64) k.w[word + 1] |= val >> (64 - bit);
  sh += w;
}
'''

GUARDED_MAIN = r'''
// Validation also protects the native binary when invoked without Python.
static bool a113_number(const char* s, long long lo, long long hi) {
  if (!s || !*s) return false;
  for (const char* p = s; *p; ++p) if (*p < '0' || *p > '9') return false;
  errno = 0; char* end = nullptr;
  const long long x = strtoll(s, &end, 10);
  return errno == 0 && *end == 0 && lo <= x && x <= hi;
}
static bool a113_bits(const string& s, size_t n) {
  return s.size() == n && s.find_first_not_of("01") == string::npos;
}
static bool a113_args(int argc, char** argv) {
  if (argc < 8 || !a113_number(argv[1], 2, 62) ||
      !a113_number(argv[4], 1, 1000000) || !a113_number(argv[5], 1, 1000000) ||
      strtoll(argv[4], nullptr, 10) > strtoll(argv[5], nullptr, 10)) return false;
  const string E = argv[2], G = argv[3];
  if (E.empty() || E.size() > MAXP || !a113_bits(E,E.size()) ||
      !a113_bits(G,E.size())) return false;
  const int ng = count(G.begin(), G.end(), '1');
  if (ng % 2 || 2*E.size()+6*ng+7*(ng/2)>576) return false;
  bool have_v = false;
  for (int i = 6; i < argc; ++i) {
    const string opt = argv[i];
    if (opt == "-v") {
      if (have_v || i+1 >= argc) return false;
      const string V = argv[++i];
      if (!a113_bits(V,E.size()) || 2*count(V.begin(),V.end(),'1') != ng)
        return false;
      have_v = true;
    } else if (opt == "-cap" || opt == "-jgen") {
      if (i+1 >= argc || !a113_number(argv[i+1],1,opt=="-cap"?100000000:1000000))
        return false;
      ++i;
    } else if (opt != "-w" && opt != "-allm" && opt != "-legacy" &&
               opt != "-wlegacy" && opt != "-sz" && opt != "-q") return false;
  }
  return have_v;
}
int main(int argc, char** argv) {
  if (!a113_args(argc,argv)) {
    fprintf(stderr,"INVALID: base2..62, binary equal streams P1..48, positive widths, "
                   "one binary -v with 2sum(v)=sum(g), and supported options required\n");
    return 2;
  }
  try {
    return a113_original_main(argc,argv);
  } catch (const bad_alloc&) {
    fprintf(stderr,"UNDECIDED: memory allocation limit\n"); return 3;
  } catch (const exception& ex) {
    fprintf(stderr,"UNDECIDED: %s\n",ex.what()); return 3;
  }
}
'''


def extended_source() -> str:
    raw = SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError("upstream cauto_fast.cpp changed; review replacements before rebuilding")
    src = raw.decode()

    def replace(old: str, new: str, n: int = 1) -> None:
        nonlocal src
        if src.count(old) != n:
            raise ValueError(f"source anchor count mismatch: {old[:100]!r}")
        src = src.replace(old, new)

    replace("#include <cstdio>", "#include <array>\n#include <cerrno>\n#include <stdexcept>\n#include <cstdio>")
    start, end = src.index("struct LKey {"), src.index("const int MAXP")
    src = src[:start] + KEY + src[end:]
    replace("const int MAXP = 32;", "const int MAXP = 48;\nint g_jgen = 120;")
    start, end = src.index("static inline void putbits("), src.index("LKey pack(")
    src = src[:start] + PUTBITS + src[end:]
    replace("LKey k; k.lo = 0; k.hi = 0; int sh = 0;", "LKey k; int sh = 0;")
    replace("return a.hi != c.hi ? a.hi < c.hi : a.lo < c.lo;", "return a < c;")
    replace("const int MAXNS = 16, MAXL = 32;", "const int MAXNS = 24, MAXL = 48;")
    # The successor choice is an index into a local transition list.
    replace("vector<uint16_t>", "vector<uint32_t>", 2)
    replace("(uint16_t)idx[s2]", "(uint32_t)idx[s2]")
    # Enforce the existing global cap while forming a Cartesian product.
    needle = "        int s = NS - 1; while (s >= 0 && ++idx[s] == cnt[s])"
    replace(needle, "        if (out.n > maxStates) maxStates = out.n;\n"
                    "        if (out.n > (size_t)cap) return false;\n" + needle)
    # Cached local relations also need finite index and allocation guards.
    replace("    uint32_t id = S.cfg.size();", "    if (S.cfg.size() >= (size_t)cap) throw runtime_error(\"local configuration cap\");\n"
                                                "    uint32_t id = S.cfg.size();")
    replace("    if (l < 0) { l = S.lidInfo.size();", "    if (l < 0) { if (S.lidInfo.size() >= (size_t)cap) throw runtime_error(\"local state cap\"); l = S.lidInfo.size();")
    replace("          X.res->emplace(make_pair(cfg, X.c0), cs);", "          X.res->emplace(make_pair(cfg, X.c0), cs);\n"
               "          if (X.res->size() > (size_t)cap) throw runtime_error(\"local transition cap\");")
    replace("    Ent en; en.start = S2.pool.size(); en.cnt = outs.size();",
            "    if (S2.pool.size() + outs.size() >= UNSET) throw runtime_error(\"local transition index limit\");\n"
            "    Ent en; en.start = S2.pool.size(); en.cnt = outs.size();")
    replace("    NS = ord.size(); ZW = 2 * b; sg.clear(); sg.resize(NS);",
            "    NS = ord.size();\n"
            "    if (NS < 1 || NS > MAXNS) throw runtime_error(\"segment-count limit\");\n"
            "    for (const auto& seg : ord) if (seg.empty() || seg.size() > MAXL) throw runtime_error(\"segment-length limit\");\n"
            "    ZW = 2 * b; sg.clear(); sg.resize(NS);")
    # A fallback failure must not print an unverified witness as FEASIBLE.
    replace("  vector<size_t> sz; solve_instance(m0, true, g_cap, &Cw, &sz);",
            "  vector<size_t> sz; const int r = solve_instance(m0, true, g_cap, &Cw, &sz);\n"
            "  if (r != 1 || !verify_cycle(Cw)) throw runtime_error(\"legacy witness failed verification\");")
    replace("long g_count = 0, g_ninst = 0, g_ncap = 0;",
            "bool verify_cycle(const vector<vector<int>>& Cw);\n"
            "long g_count = 0, g_ninst = 0, g_ncap = 0;")
    replace("  if (r == 1) {\n    g_count++;",
            "  if (r == 1) {\n"
            "    if (g_wit && (Cw.empty() || !verify_cycle(Cw))) throw runtime_error(\"reported witness failed verification\");\n"
            "    g_count++;")
    # Adjustable finite generic-layer budget: still UNDECIDED if unfinished.
    replace("2 * (120 + 2 * P + 8)", "2 * (g_jgen + 2 * P + 8)", 2)
    replace("f->detect(120,", "f->detect(g_jgen,")
    replace("detect_period_legacy(120,", "detect_period_legacy(g_jgen,")
    replace("(frontier not periodic within 120 layers or capped)", "(generic layer budget or state cap reached)")
    # Exact replacement for the former arbitrary mlo<100000 scan.
    replace("  int mlo = 1;\n  for (int mm = 1; mm < 100000; mm++) { if (!setup_instance(mm)) continue; int j0 = *min_element(J.begin(), J.end()) - 1; if (j0 >= jstar && mm > 2 * P) { mlo = mm; break; } }",
            "  int delta = 0, mindelta = 0;\n"
            "  for (int t = 0; t < P; ++t) { mindelta = min(mindelta, delta); delta += g[t] - 2*v[t]; }\n"
            "  const int mlo = max(2*P+1, 2*jstar+1-mindelta);")
    replace("int main(int argc, char** argv) {", "int a113_original_main(int argc, char** argv) {")
    replace('    else if (a == "-q") {}', '    else if (a == "-jgen") g_jgen = atoi(argv[++i]);\n    else if (a == "-q") {}')
    return src + GUARDED_MAIN


def build(*, sanitize: bool = False, emit: Path | None = None) -> Path:
    src = extended_source()
    compiler = shlex.split(os.environ.get("CXX", "c++"))
    flags = ["-std=c++17", "-O1" if sanitize else "-O2", "-g"]
    if sanitize:
        flags += ["-fsanitize=address,undefined", "-fno-omit-frame-pointer", "-fno-sanitize-recover=all"]
    digest = hashlib.sha256((src + repr(compiler + flags)).encode()).hexdigest()[:24]
    directory = Path(tempfile.gettempdir()) / ("p196-agent113-cauto-" + digest)
    directory.mkdir(exist_ok=True)
    source, binary = directory / "cauto_p48.cpp", directory / "cauto_p48"
    if emit is not None:
        emit.write_text(src)
    if not binary.exists():
        source.write_text(src)
        temporary = directory / ("cauto_p48.tmp." + str(os.getpid()))
        subprocess.run(compiler + flags + [str(source), "-o", str(temporary)], check=True, timeout=120)
        temporary.replace(binary)
    return binary


def run(binary: Path, args: list[str], seconds: float, memory_mib: int, sanitize: bool) -> dict:
    """Run one explicitly specified pattern; a missing DONE is never negative."""
    def limits() -> None:
        # ASan reserves a large virtual address space; do not use RLIMIT_AS then.
        if not sanitize:
            resource.setrlimit(resource.RLIMIT_AS, (memory_mib << 20, memory_mib << 20))
        cpu = math.ceil(seconds) + 1
        resource.setrlimit(resource.RLIMIT_CPU, (cpu, cpu + 1))

    result: dict = {"status": "UNDECIDED", "reason": "no completion", "source_sha256": SOURCE_SHA256}
    try:
        child = subprocess.run([str(binary)] + args, capture_output=True, text=True,
                               timeout=seconds, preexec_fn=limits)
    except subprocess.TimeoutExpired as exc:
        for value, target in ((exc.stdout, sys.stdout), (exc.stderr, sys.stderr)):
            if value:
                target.write(value.decode(errors="replace") if isinstance(value, bytes) else value)
        result["reason"] = "wall timeout"
        return result
    except (OSError, subprocess.SubprocessError) as exc:
        result.update(reason="process startup failed", detail=str(exc))
        return result
    sys.stdout.write(child.stdout)
    sys.stderr.write(child.stderr)
    result["exit_code"] = child.returncode
    dones = [line for line in child.stdout.splitlines() if line.startswith("DONE ")]
    scope = "all positive center lengths for this schedule" if "-allm" in args else "requested initial lengths for this schedule"
    result["scope"] = scope
    if child.returncode == 2:
        result.update(status="INVALID", reason="argument guard")
    elif child.returncode != 0:
        result["reason"] = "native error or resource limit"
        reasons = [line for line in child.stderr.splitlines() if line.startswith("UNDECIDED:")]
        if reasons:
            result["native_reason"] = reasons[-1]
    elif len(dones) == 1 and " status=none " in dones[0]:
        result.update(status="EXHAUSTED", reason="completed exact supplied-schedule decision")
    elif len(dones) == 1 and " status=hit " in dones[0] and "-w" in args:
        result.update(status="FEASIBLE", reason="completed decision with internally rechecked witness")
    elif len(dones) == 1 and " status=hit " in dones[0]:
        result.update(status="FEASIBLE", reason="completed decision; witness not requested")
    elif len(dones) == 1:
        result["reason"] = "state cap or unfinished generic frontier"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-only", action="store_true")
    parser.add_argument("--sanitize", action="store_true")
    parser.add_argument("--emit-source", type=Path)
    parser.add_argument("--seconds", type=float, default=120)
    parser.add_argument("--memory-mib", type=int, default=2048)
    parser.add_argument("native", nargs=argparse.REMAINDER)
    opts = parser.parse_args()
    if not 0 < opts.seconds <= 1800 or not 64 <= opts.memory_mib <= 153600:
        parser.error("seconds must be in (0,1800], memory-mib in 64..153600")
    try:
        binary = build(sanitize=opts.sanitize, emit=opts.emit_source)
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print(json.dumps({"status": "UNDECIDED", "reason": "build failed", "detail": str(exc)}))
        return 3
    if opts.build_only:
        print(binary)
        return 0
    native = opts.native[1:] if opts.native[:1] == ["--"] else opts.native
    result = run(binary, native, opts.seconds, opts.memory_mib, opts.sanitize)
    print("A113_RESULT " + json.dumps(result, sort_keys=True))
    return 0 if result["status"] in ("EXHAUSTED", "FEASIBLE") else 2 if result["status"] == "INVALID" else 3


if __name__ == "__main__":
    raise SystemExit(main())
