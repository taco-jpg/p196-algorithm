"""Discovery only: variable-time return search through complete collisions.

No finite time bound is extrapolated. The known family is scanned after its
ninth-step loss of balance, rather than discarded at that failure.  A return
would have to supply a symbolic equation before yielding an all-time claim.
"""
from pathlib import Path
import json, time
import numpy as np


def V(m):
    return ((1,)+(9,)*(2*m-1)+(8,2)+(9,)*(2*m-1)
            +(16,10)+(9,)*(2*m-1)+(17,))


def qstep(q):
    last = np.maximum.accumulate(np.where(q != 9, np.arange(len(q)), -1))
    out = ((last >= 0) & (q[np.maximum(last, 0)] >= 10)).astype(np.int16)
    d = q + np.r_[np.int16(0), out[:-1]] - 10*out
    if out[-1]:
        d = np.r_[d, np.int16(1)]
    palindrome = bool(np.array_equal(d, d[::-1]))
    return d+d[::-1], palindrome


def balance(q):
    mass = int(q.sum())
    if mass % 18:
        return None
    c = mass//18
    if c < 1 or c > len(q):
        return None
    budgets = np.bincount(np.arange(len(q)) % c, weights=q, minlength=c)
    return c if np.all(budgets == 18) else None


def run():
    started = time.monotonic()
    rows = []
    for m in list(range(1,65))+[96,128,192,256]:
        v = V(m)
        q = np.array(v+v[::-1], dtype=np.int16)
        was_balanced = True
        returns = []
        collisions = []
        horizon = 24*m+128
        palindrome_at = None
        for t in range(1, horizon+1):
            q, pal = qstep(q)
            c = balance(q)
            if c is not None and not was_balanced:
                returns.append({"step": t, "C": c, "width": len(q),
                                "q": q.tolist()})
            if was_balanced and c is None:
                collisions.append(t)
            was_balanced = c is not None
            if pal:
                palindrome_at = t
                break
        rows.append({"m": m, "initial_C": 6*m+3, "horizon": horizon,
                     "executed_steps": t, "palindrome_at": palindrome_at,
                     "balance_loss_steps": collisions, "delayed_returns": returns,
                     "last_width": len(q), "last_digit_sum": int(q.sum())//2})
    result = {"status": "bounded discovery; no all-time claim",
              "family": "V_m reverse(V_m)", "horizon": "24*m+128",
              "rows": rows, "seconds": time.monotonic()-started}
    Path(__file__).with_name("delayed_scale_probe.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"tested_parameters": len(rows),
                      "total_steps": sum(r["executed_steps"] for r in rows),
                      "palindromes": [[r["m"],r["palindrome_at"]] for r in rows if r["palindrome_at"]],
                      "delayed_return_parameters": [r["m"] for r in rows if r["delayed_returns"]],
                      "seconds": result["seconds"]}), flush=True)


if __name__ == "__main__":
    run()
