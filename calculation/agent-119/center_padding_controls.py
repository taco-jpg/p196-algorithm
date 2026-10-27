#!/usr/bin/env python3
"""Calibrate the Lean local-padding theorem on existing source certificates.

This does not search for certificates or replace the unchanged Python checker.
The general covariance and edge-transport proofs live in the registered Lean
project Agent119NeutralCenterPadding; these are finite positive controls only.
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import neutral_band_search as mirror


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pad(base, amount, center):
    return [base - 1] * amount + center + [base - 1] * amount


def main():
    controls = mirror._lean_certs()
    local_edges = uniform_cycles = original_edges = 0
    for base, edges in controls:
        require(mirror.cycleOK(base, edges, edges[0][0], edges[0][1]),
                "An existing control failed the original mirror")
        original_edges += len(edges)
        for b, c, b2, c2, u, v in edges:
            for source_padding in range(5):
                padded_c = pad(base, source_padding, c)
                require(mirror.hyp(base, b, padded_c), "Source Hyp changed")
                require(mirror.nextB(base, b, padded_c) == mirror.nextB(base, b, c),
                        "Exterior successor changed")
                require(mirror.nextC(base, b, padded_c) ==
                        pad(base, source_padding, mirror.nextC(base, b, c)),
                        "Center covariance failed")
                require(mirror.e2(base, b, padded_c) == mirror.e2(base, b, c),
                        "Center carry changed")
                require(mirror.gam(base, b, padded_c) == mirror.gam(base, b, c),
                        "Overflow changed")
                for target_padding in range(source_padding + v + 1):
                    new_trim = source_padding + v - target_padding
                    transported = (b, padded_c, b2, pad(base, target_padding, c2),
                                   u, new_trim)
                    require(mirror.edgeOK(base, transported), "Edge transport failed")
                    local_edges += 1
        for amount in range(5):
            transported = [(b, pad(base, amount, c), b2, pad(base, amount, c2), u, v)
                           for b, c, b2, c2, u, v in edges]
            require(mirror.cycleOK(base, transported, transported[0][0], transported[0][1]),
                    "Uniformly padded positive control did not close")
            uniform_cycles += 1
    print(f"PADDING CALIBRATION PASS bases={len(controls)} original_edges={original_edges} "
          f"local_transports={local_edges} uniform_cycles={uniform_cycles}")


if __name__ == "__main__":
    main()
