#!/usr/bin/env python3
"""Independent, GMP-free red-team counterexamples to X11's written edge theorem.

The report's numbered edge obligations omit c[n] = gamma. This script
checks every enumerated obligation for two false ordinary-decimal edges
and tests the corrected boundary against all two-digit source numbers.
"""

def val(ds):
    return sum(d * (10 ** i) for i, d in enumerate(ds))

def columns(ds):
    carry = [0]
    outs = []
    for i, d in enumerate(ds):
        total = d + ds[-1-i] + carry[-1]
        outs.append(total % 10)
        carry.append(total // 10)
    return outs, carry

def written_conditions(source, target):
    n = len(source)
    gamma = len(target) - n
    outs, carry = columns(source)
    return (gamma in (0, 1)
            and source[-1] > 0 and target[-1] > 0
            and source != source[::-1]
            and target[:n] == outs
            and (gamma == 0 or target[n] == 1)), gamma, carry[-1]

def test_false_edges():
    # LSD-first: 98 + 89 = 187, not claimed 87.
    # LSD-first: 21 + 12 = 33, not claimed 133.
    bad = [([8, 9], [7, 8]), ([1, 2], [3, 3, 1])]
    for source, target in bad:
        accepted, gamma, c_last = written_conditions(source, target)
        actual = val(source) + int(str(val(source))[::-1])
        assert accepted and source != source[::-1] and target != target[::-1]
        assert gamma != c_last and val(target) != actual
        print(f"FALSE EDGE: {val(source)} -> {val(target)}; actual={actual}; "
              f"gamma={gamma}; final_carry={c_last}; written_conditions=True")

def test_corrected_boundary():
    for n in range(10, 100):
        source = [int(z) for z in str(n)[::-1]]
        outputs, carries = columns(source)
        true_sum = n + int(str(n)[::-1])
        gamma = int(carries[-1] == 1)
        target = outputs + ([1] if gamma else [])
        assert val(target) == true_sum
        assert len(str(true_sum)) == len(source) + gamma
        passed, recorded_gamma, last = written_conditions(source, target)
        # The witness requirement is irrelevant for palindromic inputs.
        if source != source[::-1]:
            assert passed and recorded_gamma == last
    print("CORRECTED ENDPOINT CHECK: 90 two-digit source additions PASS")

if __name__ == '__main__':
    test_false_edges()
    test_corrected_boundary()
