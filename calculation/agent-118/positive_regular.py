#!/usr/bin/env python3
"""One known-positive finite-tail control for the frozen regular-language code.

This is a test harness, not a generalized solver or a new search.  It compiles
an exact copy of center_regular.cpp with only its bottom CLI main renamed, then
uses the unchanged Engine image/normalization/finite-frontier comparison methods
on the known base-26 certificate repeated three times.  The decimal-only carry
mask optimization is disabled through its existing flag.  The emitted 12-edge
witness is replayed independently with integer arithmetic in check_center.py.

Generated C++ and its binary live in a temporary directory outside the repo.
The complete compile-and-run control has a 120-second wall limit and each child
has a 4-GiB address-space limit.  Failure or a cap prints UNDECIDED and exits 2.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import resource
import subprocess
import tempfile
import time

from build_center import SOURCE_SHA256, patched_source
from check_center import parse_witness, source_certificates, source_stream, verify_centers


HARNESS = r'''

int main() {
  try {
    REG118::Engine engine;
    engine.prune = false;  // Existing decimal-only mask is outside this control.
    engine.compare = true;
    engine.compareCap = 1000000;
    engine.budget.states = 200000;
    engine.budget.edges = 3000000;
    engine.budget.operations = 100000000;
    b = 26; P = 12;
    es_ = "010101010101"; gs_ = es_;
    const string trims = "000100010001";
    e.clear(); g.clear(); v.clear();
    for (char x : es_) e.push_back(x - '0');
    for (char x : gs_) g.push_back(x - '0');
    for (char x : trims) v.push_back(x - '0');
    if (!setup_instance(4) || nseg != 3 || noV)
      undecided118("positive_control_setup");
    for (const auto& segment : order) if (segment.size() != 4)
      undecided118("positive_control_segment_length");
    engine.fast.init(order);
    engine.fast.cap = engine.compareCap; g_cap = engine.compareCap;
    const int layerCount = Jall;
    REG118::DFA current = engine.initial();
    for (int j = 0; j < layerCount; ++j) {
      REG118::ImageStats stats;
      current = engine.step(current, j, false, stats);
    }
    const auto word = engine.acceptedWord(current);
    if (word.size() != 3) undecided118("positive_control_missing_three_segment_word");
    for (size_t k = 0; k < word.size(); ++k)
      if (REG118::typeOf(word[k]) != int(k)) undecided118("positive_control_phase");
    const auto finalRows = REG118::decodeThree(current, engine.compareCap, engine.budget);
    if (finalRows.empty() || engine.comparisons != uint64_t(layerCount))
      undecided118("positive_control_incomplete_frontiers");
    vector<vector<int>> centers;
    get_witness(&engine.fast, 4, centers);
    if (centers.size() != 12 || !verify_cycle(centers))
      undecided118("positive_control_invalid_witness");
    printf("FEASIBLE b=%d e=%s g=%s v=%s m0=4", b, es_.c_str(), gs_.c_str(), trims.c_str());
    for (size_t t = 0; t < centers.size(); ++t) {
      printf(" C%zu=[", t);
      for (size_t k = 0; k < centers[t].size(); ++k)
        printf("%s%d", k ? "," : "", centers[t][k]);
      printf("]");
    }
    printf("\nREG_POSITIVE base=26 period=12 width=4 layers=%d comparisons=%llu "
           "word_length=%zu final_tuples=%zu dfa=%zu ops=%llu\n",
           layerCount, (unsigned long long)engine.comparisons, word.size(), finalRows.size(),
           current.q.size(), (unsigned long long)engine.budget.used);
    return 0;
  } catch (const exception& error) {
    fprintf(stderr, "UNDECIDED %s\n", error.what()); return 2;
  } catch (...) {
    fprintf(stderr, "UNDECIDED unexpected_positive_control_exception\n"); return 2;
  }
}
'''


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def fields(line):
    return dict(re.findall(r"(\w+)=([^ ]+)", line))


def child_limits():
    memory = 4 * 1024**3
    resource.setrlimit(resource.RLIMIT_AS, (memory, memory))
    resource.setrlimit(resource.RLIMIT_CPU, (120, 120))


def control(cxx):
    start = time.monotonic()
    e, g, trims, centers = source_stream(26, source_certificates()[26])
    require(e == g == (0, 1, 0, 1) and trims == (0, 0, 0, 1)
            and len(centers[0]) == 4, "known base-26 source profile changed")
    require(verify_centers(26, e * 3, g * 3, trims * 3, centers * 3),
            "known repeated source witness failed independent replay")
    original = Path(__file__).with_name("center_regular.cpp").read_bytes()
    source_hash = hashlib.sha256(original).hexdigest()
    text = original.decode()
    anchor = "int main(int argc, char** argv) {"
    require(text.count(anchor) == 1, "bottom CLI main anchor is not unique")
    combined = text.replace(anchor, "int regular_cli118(int argc, char** argv) {", 1) + HARNESS

    def run(command, limit):
        remaining = 120 - (time.monotonic() - start)
        require(remaining > 0, "positive control wall budget exhausted")
        result = subprocess.run(command, text=True, capture_output=True,
                                timeout=min(limit, remaining), preexec_fn=child_limits)
        require(result.returncode == 0,
                f"positive control subprocess exited {result.returncode}: {result.stderr[-4000:]}")
        return result

    with tempfile.TemporaryDirectory(prefix="p196-agent118-positive-", dir="/tmp") as temp:
        folder = Path(temp)
        (folder / "cauto118_core.hpp").write_text(patched_source())
        combined_path = folder / "positive_regular.cpp"
        combined_path.write_text(combined)
        binary = folder / "positive_regular"
        run([cxx, "-std=c++17", "-O2", "-I", str(folder), str(combined_path),
             "-o", str(binary)], 90)
        result = run([str(binary)], 30)
    require("UNDECIDED" not in result.stdout + result.stderr, "positive control incomplete")
    lines = result.stdout.splitlines()
    witnesses = [line for line in lines if line.startswith("FEASIBLE ")]
    done = [fields(line) for line in lines if line.startswith("REG_POSITIVE ")]
    comparisons = [fields(line) for line in lines if line.startswith("REG_COMPARE ")]
    require(len(witnesses) == len(done) == 1, "missing unique positive witness/completion")
    require(parse_witness(witnesses[0]) == (26, 12, 4), "returned positive witness profile differs")
    require(done[0]["layers"] == done[0]["comparisons"] == "3"
            and done[0]["word_length"] == "3" and int(done[0]["final_tuples"]) > 0,
            "positive automata result missing or wrong")
    require(len(comparisons) == 3, "complete positive-frontier comparisons missing")
    for j, item in enumerate(comparisons):
        require(int(item["j"]) == j and item["generic"] == "0"
                and int(item["comparisons"]) == j + 1, "finite-layer comparison order differs")
        require(int(item["input"]) > 0 and int(item["output"]) > 0,
                "known positive frontier was reported empty")
    require(comparisons[-1]["output"] == done[0]["final_tuples"], "final positive counts differ")
    print(result.stdout, end="")
    print(json.dumps({"status": "COMPUTED_POSITIVE_CONTROL_PASSED", "base": 26,
                      "period": 12, "width": 4, "frontier_comparisons": 3,
                      "source_witness_edges_replayed": 12, "returned_witness_edges_replayed": 12,
                      "final_tuples": int(done[0]["final_tuples"]),
                      "regular_sha256": source_hash, "upstream_sha256": SOURCE_SHA256,
                      "wall_seconds": round(time.monotonic() - start, 6),
                      "peak_child_rss_kib": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss},
                     sort_keys=True))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cxx", default="c++")
    args = parser.parse_args()
    try:
        control(args.cxx)
    except (RuntimeError, OSError, subprocess.TimeoutExpired) as error:
        print("UNDECIDED", str(error))
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
