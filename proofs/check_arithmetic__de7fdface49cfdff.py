"""Independent ordinary-integer checks of the explicit shorter candidates."""
import json
from pathlib import Path


def main():
    states = 0
    for horizon in range(129):
        length = 7 * horizon // 4 + 1
        assert length <= 2 * horizon + 1
        if horizon:
            assert length < 2 * horizon + 1
        n = 2 * (10 ** length - 1)
        for t in range(horizon + 1):
            digits = str(n)
            assert digits != digits[::-1], (horizon, t, n)
            states += 1
            n += int(digits[::-1])
    result = {
        "status": "PASS",
        "horizon_min": 0,
        "horizon_max": 128,
        "candidates": 129,
        "states_checked_including_initial": states,
        "scope": "Finite ordinary-integer controls; the unrestricted theorem is in Lean.",
    }
    Path(__file__).with_name("arithmetic.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
