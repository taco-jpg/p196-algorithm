#!/usr/bin/env python3
"""Guarded period-48 build of the pinned existing center automaton.

The existing algorithm is retained. This module changes only array bounds,
input/representation guards, witness-choice width, and cap enforcement.
It deliberately supports one explicit binary trim schedule per invocation.
Build products use temporary files; the shared C++ source is never edited.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import resource
import subprocess
import tempfile
from typing import Sequence

SOURCE_SHA256 = "eb2e6b18b09fdfcae0a5b6b818d23291123ed6a76b59fb6e531589e7f6d00fff"
SOURCE_RELATIVE = Path("calculation/neutral_band/structure/cauto_fast.cpp")
MAX_PERIOD = 48
MAX_WIDTH_ARGUMENT = 1_000_000
MAX_CAP = 100_000_000
DEFAULT_CAP = 300_000


# This front end is also compiled into the executable: direct calls cannot
# bypass the same input/packing guards used by Python run(). Unsupported input
# terminates with an error, never with a mathematical nonexistence verdict.
CPP_FRONT_END = r'''
static long long a111_number(const char* p, const char* label) {
  if (!p || !*p) throw std::runtime_error(std::string("missing ") + label);
  for (const char* q = p; *q; ++q)
    if (*q < '0' || *q > '9')
      throw std::runtime_error(std::string("invalid integer: ") + label);
  errno = 0; char* end = nullptr;
  long long n = strtoll(p, &end, 10);
  if (errno == ERANGE || !end || *end)
    throw std::runtime_error(std::string("integer range: ") + label);
  return n;
}
static bool a111_bits(const std::string& s) {
  return !s.empty() && s.find_first_not_of("01") == std::string::npos;
}
static void a111_validate(int argc, char** argv) {
  if (argc < 8)
    throw std::runtime_error("usage: binary base e g mlo mhi -v BITS [-allm -cap N -w -sz -legacy -wlegacy -q]");
  long long base = a111_number(argv[1], "base");
  long long lo = a111_number(argv[4], "mlo");
  long long hi = a111_number(argv[5], "mhi");
  if (base < 2 || base > 62) throw std::runtime_error("supported base: 2..62");
  if (lo < 1 || hi < lo || hi > 1000000)
    throw std::runtime_error("require 1 <= mlo <= mhi <= 1000000");
  std::string ee = argv[2], gg = argv[3], vv;
  if (!a111_bits(ee) || !a111_bits(gg) || ee.size() != gg.size() || ee.size() > 48)
    throw std::runtime_error("require equal nonempty binary e/g streams with period <=48");
  long long cap = 4000000; bool saw_v = false, saw_cap = false;
  for (int i = 6; i < argc; ++i) {
    std::string opt = argv[i];
    if (opt == "-v" || opt == "-cap") {
      if (++i == argc) throw std::runtime_error("missing option argument");
      if (opt == "-v") {
        if (saw_v) throw std::runtime_error("duplicate -v");
        saw_v = true; vv = argv[i];
      } else {
        if (saw_cap) throw std::runtime_error("duplicate -cap");
        saw_cap = true; cap = a111_number(argv[i], "cap");
      }
    } else if (opt != "-allm" && opt != "-w" && opt != "-sz" &&
               opt != "-legacy" && opt != "-wlegacy" && opt != "-q") {
      throw std::runtime_error("unsupported option (one explicit -v schedule required): " + opt);
    }
  }
  if (!saw_v || !a111_bits(vv) || vv.size() != ee.size())
    throw std::runtime_error("require one binary -v of the stream length");
  int G = std::count(gg.begin(), gg.end(), '1');
  int K = std::count(vv.begin(), vv.end(), '1');
  if (G % 2 || 2*K != G) throw std::runtime_error("require sum(g)=2*sum(v)");
  int packed_bits = 2*int(ee.size()) + 6*G + 7*K;
  if (packed_bits > 256) throw std::runtime_error("UNSUPPORTED: legacy key needs >256 bits");
  if (K > MAXNS) throw std::runtime_error("UNSUPPORTED: too many segments");
  if (cap < 1 || cap > 100000000) throw std::runtime_error("supported cap: 1..100000000");
}
int main(int argc, char** argv) {
  try { a111_validate(argc, argv); }
  catch (const std::exception& e) {
    fprintf(stderr, "INVALID_OR_UNSUPPORTED: %s\n", e.what()); return 2;
  }
  try { return a111_original_main(argc, argv); }
  catch (const std::bad_alloc&) {
    fprintf(stderr, "UNDECIDED: allocation limit\n"); return 3;
  }
  catch (const std::exception& e) {
    fprintf(stderr, "UNDECIDED: runtime guard: %s\n", e.what()); return 3;
  }
}
'''


def _replace_exact(text: str, old: str, new: str, count: int = 1) -> str:
    actual = text.count(old)
    if actual != count:
        raise ValueError(f"patch anchor count {actual}, expected {count}: {old!r}")
    return text.replace(old, new)


def patched_source(source: str | Path | None = None) -> str:
    """Return the reviewed, source-pinned transformation or refuse to build."""
    source = Path(source) if source else Path(__file__).resolve().parents[2] / SOURCE_RELATIVE
    raw = source.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != SOURCE_SHA256:
        raise ValueError(f"source hash mismatch: {digest}; expected {SOURCE_SHA256}")
    text = raw.decode("utf-8")
    text = _replace_exact(text, "const int MAXP = 32;", "const int MAXP = 48;")
    text = _replace_exact(text, "const int MAXNS = 16, MAXL = 32;", "const int MAXNS = 16, MAXL = 48;")
    text = _replace_exact(text, "int main(int argc, char** argv) {", "int a111_original_main(int argc, char** argv) {")
    text = _replace_exact(text, "vector<uint16_t>", "vector<uint32_t>", count=2)
    text = _replace_exact(text, "(uint16_t)idx[s2]", "(uint32_t)idx[s2]")
    text = _replace_exact(
        text,
        "        int s = NS - 1; while (s >= 0 && ++idx[s] == cnt[s]) { idx[s] = 0; s--; }",
        "        if ((long)out.n > cap) {\n"
        "          maxStates = max(maxStates, out.n);\n"
        "          fprintf(stderr, \"UNDECIDED state_cap frontier=%zu cap=%ld\\n\", out.n, cap);\n"
        "          return false; // stop before expanding more combinations\n"
        "        }\n"
        "        int s = NS - 1; while (s >= 0 && ++idx[s] == cnt[s]) { idx[s] = 0; s--; }",
    )
    text = _replace_exact(
        text,
        "  if ((long)C.out->st.size() > C.cap) C.capped = true;",
        "  if ((long)C.out->st.size() > C.cap) {\n"
        "    fprintf(stderr, \"UNDECIDED state_cap frontier=%zu cap=%ld\\n\", C.out->st.size(), C.cap);\n"
        "    C.capped = true;\n"
        "  }",
    )
    text = _replace_exact(
        text,
        "  K128 x = (K128)val;",
        "  if (w <= 0 || w >= 64 || sh < 0 || sh + w > 256 || val >= (uint64_t(1) << w))\n"
        "    throw std::runtime_error(\"packed-key field exceeds representation\");\n"
        "  K128 x = (K128)val;",
    )
    # Existing index widths are guarded before conversion. These guards are
    # normally unreachable within the address-space budget used by run().
    text = _replace_exact(
        text,
        "    uint32_t id = S.cfg.size(); S.cfg.push_back(c); S.yidMap.emplace(c, id); return id;",
        "    if (S.cfg.size() >= UINT32_MAX) throw std::runtime_error(\"configuration id overflow\");\n"
        "    uint32_t id = S.cfg.size(); S.cfg.push_back(c); S.yidMap.emplace(c, id); return id;",
    )
    text = _replace_exact(
        text,
        "    if (l < 0) { l = S.lidInfo.size(); S.lidInfo.push_back({yid, (int8_t)z}); S.lidOf[ix] = l; }",
        "    if (l < 0) {\n"
        "      if (S.lidInfo.size() >= INT32_MAX) throw std::runtime_error(\"local id overflow\");\n"
        "      l = S.lidInfo.size(); S.lidInfo.push_back({yid, (int8_t)z}); S.lidOf[ix] = l;\n"
        "    }",
    )
    text = _replace_exact(
        text,
        "    Ent en; en.start = S2.pool.size(); en.cnt = outs.size();",
        "    if (S2.pool.size() >= UINT32_MAX || outs.size() >= UINT32_MAX - S2.pool.size())\n"
        "      throw std::runtime_error(\"segment transition id overflow\");\n"
        "    Ent en; en.start = S2.pool.size(); en.cnt = outs.size();",
    )
    text = _replace_exact(
        text,
        "    slots[p] = (uint32_t)(n + 1); data.insert(data.end(), w, w + NS); n++;",
        "    if (n >= UINT32_MAX - 1) throw std::runtime_error(\"frontier id overflow\");\n"
        "    slots[p] = (uint32_t)(n + 1); data.insert(data.end(), w, w + NS); n++;",
    )
    return "#include <cerrno>\n#include <climits>\n#include <stdexcept>\n" + text + CPP_FRONT_END


def build(output: str | Path, sanitize: bool = False, compiler: str = "c++",
          source: str | Path | None = None) -> Path:
    """Compile into output, keeping the generated C++ file outside the repo."""
    output = Path(output).resolve()
    flags = ["-std=c++17", "-O2"]
    if sanitize:
        flags = ["-std=c++17", "-O1", "-g", "-fsanitize=address,undefined",
                 "-fno-omit-frame-pointer", "-fno-pie", "-no-pie"]
    text = patched_source(source)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="agent111-center-") as temp:
        cpp = Path(temp) / "cauto_long.cpp"
        cpp.write_text(text, encoding="utf-8")
        subprocess.run([compiler, *flags, str(cpp), "-o", str(output)], check=True,
                       timeout=120)
    return output


def validate(base: int, e: str, g: str, mlo: int, mhi: int, trim: str,
             cap: int = DEFAULT_CAP) -> dict[str, int]:
    """Check the exact supported domain; rejection means unsupported, not none."""
    if any(type(n) is not int for n in (base, mlo, mhi, cap)):
        raise ValueError("base, widths and cap must be integers")
    if not 2 <= base <= 62:
        raise ValueError("base must be in 2..62")
    if not 1 <= mlo <= mhi <= MAX_WIDTH_ARGUMENT:
        raise ValueError("require 1 <= mlo <= mhi <= 1000000")
    if any(not isinstance(s, str) or not s or set(s) - {"0", "1"} for s in (e, g, trim)):
        raise ValueError("e, g and trim must be nonempty binary strings")
    period = len(e)
    if period > MAX_PERIOD or len(g) != period or len(trim) != period:
        raise ValueError("e, g and trim must have equal lengths in 1..48")
    overflows, trims = g.count("1"), trim.count("1")
    if overflows != 2 * trims:
        raise ValueError("require sum(g)=2*sum(v)")
    bits = 2 * period + 6 * overflows + 7 * trims
    if bits > 256:
        raise ValueError(f"unsupported legacy key: {bits} bits exceeds 256")
    if not 1 <= cap <= MAX_CAP:
        raise ValueError("cap must be in 1..100000000")
    return {"period": period, "overflows": overflows, "trims": trims, "key_bits": bits}


def run(binary: str | Path, base: int, e: str, g: str, mlo: int, mhi: int, trim: str,
        *, all_lengths: bool = False, cap: int = DEFAULT_CAP, timeout: float = 30,
        witness: bool = False, legacy: bool = False, sizes: bool = False,
        memory_mb: int | None = 6144) -> subprocess.CompletedProcess[str]:
    """Execute one schedule. Timeout/error/cap/NOPERIOD never imply absence.

    memory_mb=None is reserved for small sanitizer controls: ASan reserves a
    large virtual address range. Ordinary searches should retain the limit.
    """
    validate(base, e, g, mlo, mhi, trim, cap)
    if not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or not 0 < timeout <= 1800:
        raise ValueError("wall timeout must be in (0,1800] seconds")
    if memory_mb is not None and (type(memory_mb) is not int or not 64 <= memory_mb <= 8192):
        raise ValueError("memory_mb must be in 64..8192, or None for sanitizer controls")
    command = [str(Path(binary).resolve()), str(base), e, g, str(mlo), str(mhi),
               "-v", trim, "-cap", str(cap)]
    command += [flag for enabled, flag in ((all_lengths, "-allm"), (witness, "-w"),
                                           (legacy, "-legacy"), (sizes, "-sz")) if enabled]

    def limits() -> None:
        if memory_mb is not None:
            resource.setrlimit(resource.RLIMIT_AS, (memory_mb * 1024**2,) * 2)
        resource.setrlimit(resource.RLIMIT_CPU, (math.ceil(timeout) + 1, math.ceil(timeout) + 2))

    try:
        return subprocess.run(command, text=True, capture_output=True, timeout=timeout,
                              preexec_fn=limits, check=False)
    except subprocess.TimeoutExpired as err:
        def decoded(value: str | bytes | None) -> str:
            return value.decode(errors="replace") if isinstance(value, bytes) else value or ""
        return subprocess.CompletedProcess(command, 124, decoded(err.stdout),
                                           decoded(err.stderr) + "\nUNDECIDED: wall timeout\n")


def guard_selftest(binary: str | Path) -> dict[str, int | bool]:
    """Reject malformed inputs through the executable's independent front end."""
    command = [str(Path(binary).resolve()), "10", "01", "11", "1", "4", "-v", "10"]
    cases: list[list[str]] = []
    for index, value in ((1, "1"), (1, "63"), (1, "10x"), (2, ""), (2, "02"),
                         (3, "1"), (3, "10"), (4, "0"), (4, "5"), (5, "1000001"),
                         (7, "1"), (7, "20"), (7, "00")):
        bad = command.copy(); bad[index] = value; cases.append(bad)
    cases += [command + ["-cap", n] for n in ("0", "-1", "100000001", "3x", "9999999999999999999999999")]
    cases += [command + ["-cap"], command + ["-v", "10"], command + ["-vall"]]
    cases += [[str(Path(binary).resolve()), "10", "0" * 49, "0" * 49, "1", "1", "-v", "0" * 49],
              [str(Path(binary).resolve()), "10", "01" * 24, "01" * 24, "1", "1", "-v", "1000" * 12]]
    for bad in cases:
        result = subprocess.run(bad, capture_output=True, text=True, timeout=5, check=False)
        if result.returncode != 2 or "INVALID_OR_UNSUPPORTED:" not in result.stderr or "DONE" in result.stdout:
            raise AssertionError((bad, result.returncode, result.stdout, result.stderr))
    try:
        validate(10, "01" * 24, "01" * 24, 1, 1, "1000" * 12)
    except ValueError as err:
        if "324" not in str(err):
            raise AssertionError(str(err)) from err
    else:
        raise AssertionError("oversized 324-bit key accepted")
    with tempfile.TemporaryDirectory(prefix="agent111-pin-check-") as temp:
        bad_source = Path(temp) / "modified.cpp"
        source = Path(__file__).resolve().parents[2] / SOURCE_RELATIVE
        bad_source.write_bytes(source.read_bytes() + b"\n")
        try:
            patched_source(bad_source)
        except ValueError as err:
            if "hash mismatch" not in str(err):
                raise AssertionError(str(err)) from err
        else:
            raise AssertionError("modified upstream source accepted")
    return {"rejected_binary_cases": len(cases), "source_pin_rejected_change": True,
            "key_324_rejected": True}


def boundary_smoke(binary: str | Path, sanitizer: bool = False) -> dict[str, object]:
    """Exercise period-33/48 arrays with a cap of one, not a negative search.

    With a sanitizer build, use ASAN_OPTIONS=detect_leaks=0 on environments
    where LeakSanitizer cannot inspect processes. Address/UB checks remain on.
    """
    results = []
    for e, g, trim in (("10100110011" * 3, "11100010000" * 3, "1" * 6 + "0" * 27),
                       ("101010010101" * 4, "100010001000" * 4, "1" * 6 + "0" * 42)):
        for legacy in (False, True):
            result = run(binary, 10, e, g, 1, 1, trim, all_lengths=True, cap=1,
                         timeout=10, memory_mb=None if sanitizer else 6144, legacy=legacy)
            if (result.returncode or "AddressSanitizer" in result.stderr or
                    "runtime error:" in result.stderr or "status=noperiod" not in result.stdout or
                    "UNDECIDED state_cap frontier=2 cap=1" not in result.stderr):
                raise AssertionError((result.returncode, result.stdout, result.stderr))
            metadata = validate(10, e, g, 1, 1, trim, 1)
            results.append({**metadata, "longest_segment": len(e) - 5,
                            "legacy": legacy, "status": "noperiod", "reason": "state_cap"})
    return {"boundary_runs": results, "sanitizer": sanitizer, "passed": True}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p_build = sub.add_parser("build", help="compile the guarded source-pinned engine")
    p_build.add_argument("output", type=Path)
    p_build.add_argument("--sanitize", action="store_true")
    p_build.add_argument("--compiler", default="c++")
    p_guard = sub.add_parser("guard-selftest", help="check direct-binary rejection and source pinning")
    p_guard.add_argument("binary", type=Path)
    p_smoke = sub.add_parser("boundary-smoke", help="tiny capped period-33/48 array checks")
    p_smoke.add_argument("binary", type=Path)
    p_smoke.add_argument("--sanitizer", action="store_true")
    p_run = sub.add_parser("run", help="run one explicit trim schedule under process limits")
    p_run.add_argument("binary", type=Path)
    p_run.add_argument("base", type=int)
    p_run.add_argument("e")
    p_run.add_argument("g")
    p_run.add_argument("trim")
    p_run.add_argument("--mlo", type=int, default=1)
    p_run.add_argument("--mhi", type=int, default=1)
    p_run.add_argument("--all-lengths", action="store_true")
    p_run.add_argument("--cap", type=int, default=DEFAULT_CAP)
    p_run.add_argument("--timeout", type=float, default=30)
    p_run.add_argument("--memory-mb", type=int, default=6144)
    p_run.add_argument("--witness", action="store_true")
    p_run.add_argument("--legacy", action="store_true")
    p_run.add_argument("--sizes", action="store_true")
    args = parser.parse_args(argv)
    if args.command == "build":
        output = build(args.output, args.sanitize, args.compiler)
        print(json.dumps({"binary": str(output), "source_sha256": SOURCE_SHA256,
                          "generated_sha256": hashlib.sha256(patched_source().encode()).hexdigest(),
                          "sanitize": args.sanitize}, sort_keys=True))
        return 0
    if args.command == "guard-selftest":
        print(json.dumps(guard_selftest(args.binary), sort_keys=True))
        return 0
    if args.command == "boundary-smoke":
        print(json.dumps(boundary_smoke(args.binary, args.sanitizer), sort_keys=True))
        return 0
    result = run(args.binary, args.base, args.e, args.g, args.mlo, args.mhi, args.trim,
                 all_lengths=args.all_lengths, cap=args.cap, timeout=args.timeout,
                 memory_mb=args.memory_mb, witness=args.witness, legacy=args.legacy,
                 sizes=args.sizes)
    print(result.stdout, end="")
    if result.stderr:
        import sys
        print(result.stderr, end="", file=sys.stderr)
    if result.returncode:
        print(f"UNDECIDED process_returncode={result.returncode}")
    return result.returncode if result.returncode >= 0 else 128 - result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
