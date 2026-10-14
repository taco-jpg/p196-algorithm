"""Reproduce finite checks supporting the C12 exterior-graph quotient.

These are exact controls, not an exhaustive graph search or a Lychrel proof.
The general equivariance argument is in c12_quotient_proof.txt.
"""
from pathlib import Path
import json
from exterior_columns import successors, initial


def rotate(state, amount):
    return tuple(a[amount:] + a[:amount] for a in state)


def main():
    here = Path(__file__).resolve().parent
    metadata = json.loads((here / 'exterior_all_chiralities_target_metadata.json').read_text())
    states = {tuple(map(tuple, entry['state'])) for entry in metadata}
    assert all(rotate(s, k) in states for s in states for k in range(12))
    root8 = initial()
    root9 = ((0,) * 12, (1,) * 12, (0,) * 12, (8,) * 12)
    assert all(rotate(root, k) == root for root in (root8, root9) for k in range(12))
    first = successors(root8)
    second = successors(root9)
    assert not second
    checks = 0
    for state in first:
        out = set(successors(state))
        for k in (1, 5):
            assert {rotate(t, k) for t in out} == set(successors(rotate(state, k)))
            checks += 1
    result = dict(
        target_count=len(states),
        target_union_invariant_under_all_twelve_rotations=True,
        initial_states_fixed=True,
        root_8_17_successors=len(first),
        root_9_18_successors=len(second),
        successor_equivariance_control_checks=checks,
        proof_scope='finite target-union check; arbitrary-state equivariance follows from uniform cyclic column equations',
        finite_seed_proved=False,
    )
    (here / 'c12_invariance_checks.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
