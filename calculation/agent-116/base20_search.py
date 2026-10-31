#!/usr/bin/env python3
"""Guarded base-20 reconstruction using existing exact B/C automata.

No exhausted verdict is inferred from the stock bauto period-level `done`.
A temporary instrumentation prints whether its frontier actually emptied.
Outputs are compact mathematical search records, never a Lean proof.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "calculation/neutral_band/structure/bauto.cpp"
CSOURCE = ROOT / "calculation/neutral_band/structure/cauto_fast.cpp"


def build(directory: Path) -> tuple[Path, Path]:
    source = SOURCE.read_text()
    marker = "      if(!accE.empty()){"
    if source.count(marker) != 1:
        raise RuntimeError("bauto instrumentation anchor changed; review source")
    added = '''      printf("A116_TERMINAL g=%s status=%s states=%zu depth=%d accepts=%zu\\n",
        gs.c_str(), fr.empty()?"EXHAUSTED":(depth>=400?"DEPTH_LIMIT":"STATE_CAP"),
        seen.size(),depth,accE.size()); fflush(stdout);
'''
    instrumented = directory / "bauto_terminal.cpp"
    instrumented.write_text(source.replace(marker, added + marker))
    bbin, cbin = directory / "bauto", directory / "cauto_fast"
    for src, target in ((instrumented, bbin), (CSOURCE, cbin)):
        subprocess.run(["c++", "-O2", "-std=c++17", str(src), "-o", str(target)], check=True)
    return bbin, cbin


def parse_b(text: str) -> tuple[list[dict], list[dict]]:
    terminals, streams = [], []
    for line in text.splitlines():
        if line.startswith("A116_TERMINAL "):
            rec = dict(re.findall(r"(\w+)=(\S+)", line))
            for key in ("states", "depth", "accepts"):
                rec[key] = int(rec[key])
            terminals.append(rec)
        if line.startswith("ACCEPT "):
            head = line.split(" B_t=", 1)[0]
            rec = dict(re.findall(r"(\w+)=(\S+)", head))
            for key in ("b", "p", "depth", "states"):
                rec[key] = int(rec[key])
            rec["B"] = [[int(s) for s in w.split(",") if s] for w in re.findall(r"\[([^\]]*)\]", line)]
            streams.append(rec)
    return terminals, streams


def run_b(binary: Path, base: int, period: int, cap: int, seconds: float,
          word: str | None = None) -> dict:
    command = [str(binary), str(base), str(period), str(period), "-w", "-cap", str(cap)]
    if word is not None:
        command += ["-g", word]
    start = time.monotonic()
    status = "COMPLETE"
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=seconds)
        output, error, rc = result.stdout, result.stderr, result.returncode
        if rc:
            status = "PROCESS_ERROR"
    except subprocess.TimeoutExpired as exc:
        output = (exc.stdout or b"").decode()
        error = (exc.stderr or b"").decode()
        rc, status = None, "TIMEOUT"
    terminal, streams = parse_b(output)
    if "key too long" in error:
        status = "UNSUPPORTED_PACKING"
    return {"base": base, "period": period, "status": status, "returncode": rc,
            "seconds": round(time.monotonic() - start, 3), "terminal": terminal, "streams": streams}


def center(binary: Path, base: int, e: str, g: str, cap: int, seconds: float) -> dict:
    if len(e) != len(g) or len(e) > 32 or len(e) < 1:
        return {"status": "UNSUPPORTED_PERIOD", "e": e, "g": g}
    if g.count("1") % 2:
        return {"status": "ODD_OVERFLOW", "e": e, "g": g}
    if 2*len(e) + 6*g.count("1") + 7*(g.count("1")//2) > 256:
        return {"status": "UNSUPPORTED_PACKING", "e": e, "g": g}
    # Original cauto_fast limits are respected; do not extend fixed arrays here.
    command = [str(binary), str(base), e, g, "1", "1", "-vall", "-allm", "-w",
               "-sym", "-cap", str(cap)]
    start = time.monotonic()
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=seconds)
    except subprocess.TimeoutExpired:
        return {"status": "TIMEOUT", "e": e, "g": g}
    done, hits, feasibility_lines = [], [], 0
    for line in result.stdout.splitlines():
        if line.startswith("DONE "):
            done.append(dict(re.findall(r"(\w+)=(\S+)", line)))
        elif line.startswith(("FEASIBLE ", "FEASIBLE_CLASS ")):
            feasibility_lines += 1
            rec = dict(re.findall(r"(\w+)=(\S+)", line.split(" C0=", 1)[0]))
            rec["C"] = [[int(s) for s in w.split(",") if s] for w in re.findall(r"C\d+=\[([^\]]*)\]", line)]
            if rec["C"]:
                hits.append(rec)
    status = "HIT" if hits else "NONE"
    if not hits and (feasibility_lines or any(x["status"] == "hit" for x in done)):
        status = "FEASIBLE_NO_WITNESS"
    if result.returncode or not done:
        status = "PROCESS_ERROR"
    elif any(x["status"] not in ("none", "hit") for x in done):
        status = "UNDECIDED"
    return {"status": status, "e": e, "g": g, "seconds": round(time.monotonic()-start, 3),
            "done": done, "hits": hits, "returncode": result.returncode}


def reconstruct(bbin: Path, cbin: Path, output: Path | None) -> None:
    """Recover one full base20 cycle from existing solver sources, then replay."""
    import sys
    sys.path.insert(0, str(ROOT / "calculation"))
    import neutral_band_search as mirror
    exterior = run_b(bbin, 20, 8, 1000000, 60, "10001000")
    stream = next((s for s in exterior["streams"] if s["e"] == "10100101"), None)
    if stream is None:
        raise RuntimeError("requested B witness unavailable: " + exterior["status"])
    command = [str(cbin), "20", "10100101", "10001000", "27", "27",
               "-v", "00100000", "-w", "-cap", "3000000"]
    result = subprocess.run(command, capture_output=True, text=True, timeout=60, check=True)
    hit = next((line for line in result.stdout.splitlines() if line.startswith("FEASIBLE ")), None)
    if hit is None:
        raise RuntimeError("requested C witness unavailable; no negative conclusion")
    centers = [[int(s) for s in w.split(",") if s] for w in re.findall(r"C\d+=\[([^\]]*)\]", hit)]
    if len(centers) != 8:
        raise RuntimeError("center feasibility did not provide all eight states")
    status, edges = mirror.run(20, stream["B"][0], centers[0], maxsteps=100, maxlen=2000)
    if status != "cycle" or not mirror.cycleOK(20, edges, edges[0][0], edges[0][1]):
        raise RuntimeError("full mirror replay failed")
    certificate = {"base": 20, "edges": edges, "mirror_cycleOK": True,
                   "source_driver_e": stream["e"], "source_driver_g": stream["g"]}
    if output:
        output.write_text(json.dumps(certificate, indent=2) + "\n")
    print(json.dumps({"status": "MIRROR_ACCEPTED", "base": 20, "period": len(edges),
                      "overflow": sum(mirror.gam(20, edge[0], edge[1]) for edge in edges),
                      "exterior_trim": sum(edge[4] for edge in edges),
                      "center_trim": sum(edge[5] for edge in edges),
                      "max_B": max(len(edge[0]) for edge in edges),
                      "max_C": max(len(edge[1]) for edge in edges)}), flush=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--base", type=int, default=20)
    ap.add_argument("--pmin", type=int, default=1)
    ap.add_argument("--pmax", type=int, default=12)
    ap.add_argument("--cap", type=int, default=1000000)
    ap.add_argument("--seconds", type=float, default=60)
    ap.add_argument("--centers", action="store_true")
    ap.add_argument("--reconstruct", action="store_true",
                    help="recover the explicit period8 base20 certificate directly")
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    if not (2 <= args.base <= 32 and 1 <= args.pmin <= args.pmax <= 12):
        ap.error("supported bounds: base 2..32, periods 1..12")
    records = {"bauto_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
               "cauto_sha256": hashlib.sha256(CSOURCE.read_bytes()).hexdigest(), "B": [], "C": []}
    with tempfile.TemporaryDirectory(prefix="agent116-") as tmp:
        bbin, cbin = build(Path(tmp))
        if args.reconstruct:
            reconstruct(bbin, cbin, args.output)
            return
        for p in range(args.pmin, args.pmax+1):
            rec = run_b(bbin, args.base, p, args.cap, args.seconds)
            records["B"].append(rec)
            counts: dict[str, int] = {}
            for terminal in rec["terminal"]:
                status = terminal["status"]
                counts[status] = counts.get(status, 0) + 1
            print(json.dumps({"period": p, "batch_status": rec["status"], "terminal": counts,
                              "streams": len(rec["streams"]), "seconds": rec["seconds"]}), flush=True)
            if args.centers:
                for st in rec["streams"]:
                    k = 2 if st["g"].count("1") % 2 else 1
                    c = center(cbin, args.base, st["e"]*k, st["g"]*k, args.cap, args.seconds)
                    c["B"] = st["B"] * k
                    records["C"].append(c)
                    print(json.dumps({"period": p, "k": k, "e": st["e"], "g": st["g"],
                                      "center_status": c["status"], "hits": len(c.get("hits", []))}), flush=True)
            if args.output:
                args.output.write_text(json.dumps(records, indent=2) + "\n")


if __name__ == "__main__":
    main()
