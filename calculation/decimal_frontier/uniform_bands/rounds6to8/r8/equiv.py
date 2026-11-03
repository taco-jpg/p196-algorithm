import os, sys, re, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verify_ext as V
def leftend(b, T, clock):
    out = subprocess.run(["./reach_w", str(b), str(T), clock, "WIRE"], capture_output=True, text=True).stdout
    stream = re.search(r"NEW STREAM at height (\d+): ([01]+)", out)
    cells = [list(map(int, l.split(":")[1].split())) for l in out.splitlines() if l.startswith("cell ")]
    ok = "END LEFTEND ok" in out
    return int(stream.group(1)), stream.group(2), cells, ok
def run(b, T, clock):
    h, e, cells, ok = leftend(b, T, clock)
    Bts = []
    for t in range(T):
        B = [cells[k][t] for k in range(len(cells))]
        while B and B[-1] == b - 1: B.pop()
        Bts.append(B)
    res = V.verify(b, clock, e, Bts)
    print(f"b={b} T={T} clock={clock}: reach stream {e} at height {h} (cells {len(cells)}), left end rebuilt={ok}; B-lengths {sorted(set(map(len,Bts)))}; Agent120 mirror replay (Bstep + integer reverse-and-add): {res[0]}", *res[1][:3])
if __name__ == "__main__":
    run(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
