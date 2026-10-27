#!/usr/bin/env python3
"""Display exact length accounting for the eight existing Lean-source controls.

This is a calibration harness for Agent119NeutralLengthAccounting, not a new
certificate checker or a search. It reuses the unchanged Agent120 Python mirror.
Run from any directory with Python 3; no third-party dependencies are needed.
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import neutral_band_search as mirror


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    controls = mirror._lean_certs()
    require(len(controls) == 8, "Expected the eight existing controls")
    prefix_checks = 0
    edge_count = 0
    for base, edges in controls:
        initial_b, initial_c = edges[0][:2]
        require(mirror.cycleOK(base, edges, initial_b, initial_c),
                f"Existing base-{base} certificate failed the mirror")
        g_total = sum(mirror.gam(base, e[0], e[1]) for e in edges)
        u_total = sum(e[4] for e in edges)
        v_total = sum(e[5] for e in edges)
        require(u_total == g_total == 2 * v_total, "Closed-chain totals differ")
        require(2 * (u_total + v_total) == 3 * g_total, "Gain identity failed")
        edge_count += len(edges)
        for offset in range(len(edges)):
            rotated = edges[offset:] + edges[:offset]
            source_b, source_c = rotated[0][:2]
            current_b, current_c = source_b, source_c
            g_sum = u_sum = v_sum = 0
            for prefix_length in range(len(edges) + 1):
                require(len(current_b) + u_sum == len(source_b) + g_sum,
                        "Exterior prefix telescope failed")
                require(len(current_c) + 2 * v_sum == len(source_c) + g_sum,
                        "Center prefix telescope failed")
                prefix_checks += 1
                if prefix_length == len(edges):
                    break
                edge = rotated[prefix_length]
                b, c, b2, c2, u, v = edge
                require((b, c) == (current_b, current_c), "Chain endpoints differ")
                require(mirror.edgeOK(base, edge), "An existing edge failed")
                gamma = mirror.gam(base, b, c)
                require(len(mirror.nextB(base, b, c)) == len(b) + gamma,
                        "Raw exterior length failed")
                require(len(mirror.nextC(base, b, c)) == len(c) + gamma,
                        "Raw center length failed")
                g_sum += gamma
                u_sum += u
                v_sum += v
                current_b, current_c = b2, c2
        print(f"base={base} edges={len(edges)} G={g_total} U={u_total} "
              f"V={v_total} gain={u_total + v_total} net_gap={v_total}")
    print(f"CALIBRATION PASS controls={len(controls)} edges={edge_count} "
          f"rotated_chain_prefixes={prefix_checks}")


if __name__ == "__main__":
    main()
