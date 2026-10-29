#!/usr/bin/env python3
"""Exact arithmetic for the necessary band-phase gate; not an orbit simulator."""
from math import gcd, lcm


def phase_laps(width: int, overflows_per_clock: int) -> int:
    assert width > 0 and overflows_per_clock >= 0
    return width // gcd(width, overflows_per_clock)


def combined_laps(width: int, overflows_per_clock: int, clock_period: int,
                  row_state_period: int) -> int:
    spatial = phase_laps(width, overflows_per_clock)
    temporal = row_state_period // gcd(row_state_period, clock_period)
    return lcm(spatial, temporal)


assert phase_laps(20, 4) == 5       # p8/m20
assert phase_laps(9, 3) == 3        # p12/m9
assert combined_laps(20, 4, 8, 20) == 5
assert combined_laps(4, 8, 16, 48) == 3  # p16/m4 primitive three-cycle
assert 48 * 3 == 144 and 144 // 16 == 9

print("p8/m20: 5 clock laps (40 steps) for phase closure")
print("p12/m9: 3 clock laps (36 steps) for phase closure")
print("p16/m4 three-cycle: row phase closes after 3 clock laps (48 steps)")
print("Existing mod-9 charge excludes 48 and 96; 144 is first not excluded by that charge")
print("No seam/carry closure or infinite-time claim is made.")
