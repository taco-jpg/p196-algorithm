"""Focused event discovery for the original Q_m family.

Only the deaths of its first inherited 18 band / 9 band, and the first
loss of the associated complementary center, are recorded. This is not
a balanced-return scan and establishes no all-parameter recurrence.
"""
from pathlib import Path
import json
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "main_existence_attempt" / "constructive"))
from delayed_scale_probe import V, qstep


def anti_radius(q, s):
    left, right = s//2, (s+1)//2
    r = 0
    while left-r >= 0 and right+r < len(q):
        if q[left-r] + q[right+r] != 18:
            break
        r += 1
    return r


def window(q, a, b, padding=8):
    return q[max(0, a-padding):min(len(q), b+padding+1)].tolist()


def probe(m):
    v = V(m)
    q = np.array(v+v[::-1], dtype=np.int16)
    q, pal = qstep(q)
    assert not pal
    a18, b18 = 1, 2*m-1
    a9, b9 = 2*m+2, 4*m
    H = 0
    events = {}
    for t in range(1, 12*m+1):
        s = 6*m+2+H
        r = anti_radius(q, s)
        if r == 0:
            center = (s//2, (s+1)//2)
            events["first_complementary_center_loss"] = {
                "time": t, "overflows": H,
                "center": q[center[0]:center[1]+1].tolist(),
                "window": window(q, *center)}
            break
        out, pal = qstep(q)
        assert not pal  # finite observation only
        h = len(out)-len(q)
        if "inherited_18_death" not in events:
            if h:
                aa18, bb18 = a18+1, b18
            else:
                aa18 = a18+int(out[a18] != 18)
                bb18 = b18-int(out[b18] != 18)
            assert aa18 > bb18 or np.all(out[aa18:bb18+1] == 18)
            if aa18 > bb18:
                events["inherited_18_death"] = {
                    "time": t+1, "overflows": H+h,
                    "collision_window": window(out, aa18, aa18),
                    "surviving_neutral_length_before_step": b9-a9+1,
                    "anti_radius_after_step": anti_radius(out, s+h)}
            a18, b18 = aa18, bb18
        if "inherited_9_event" not in events:
            aa9, bb9 = a9+h, b9
            if aa9 > bb9:
                assert h == 1 and a9 == b9
                x, y = int(q[a9-1]), int(q[b9+1])
                assert x+y == 18 and x != 9
                ox = x+10 if x <= 8 else x-10
                assert out[a9:a9+2].tolist() == [ox, 18-ox]
                events["inherited_9_event"] = {
                    "type": "gap reaches zero on overflow",
                    "time": t+1, "overflows": H+h,
                    "old_front": [x, 9, y],
                    "new_pair": [ox, 18-ox],
                    "anti_radius_after_step": anti_radius(out, s+h)}
            elif not np.all(out[aa9:bb9+1] == 9):
                events["inherited_9_event"] = {
                    "type": "bulk changes before gap reaches zero",
                    "time": t+1, "overflows": H+h,
                    "old_length": b9-a9+1,
                    "new_bulk": out[aa9:bb9+1].tolist(),
                    "old_front": [int(q[a9-1]), int(q[b9+1])],
                    "window": window(out, aa9, bb9)}
            else:
                while aa9 > 0 and out[aa9-1] == 9:
                    aa9 -= 1
                while bb9+1 < len(out) and out[bb9+1] == 9:
                    bb9 += 1
                a9, b9 = aa9, bb9
        H += h
        q = out
    assert len(events) == 3, (m, events)
    return {"m": m, "events": events}


def run():
    rows = [probe(m) for m in (4, 8, 16, 32, 64)]
    result = {"status": "finite event discovery only",
              "family": "Q_m=V_m reverse(V_m)",
              "rows": rows, "all_parameter_return": False}
    Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps([{ "m": row["m"],
                       "18_death": row["events"]["inherited_18_death"]["time"],
                       "9_event": row["events"]["inherited_9_event"],
                       "center_loss": row["events"]["first_complementary_center_loss"]["time"]}
                      for row in rows], indent=2))


if __name__ == "__main__":
    run()
