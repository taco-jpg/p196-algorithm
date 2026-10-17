from itertools import product

def decode_pair(u, v, a, b):
    """Literal finite interpretation of Agent105DecoderLocal9df76b.ValidEdge."""
    return [
        (q, low, high)
        for q in range(19)
        for low in range(2)
        for high in range(2)
        if q + a == u + 10 * low and q + high == v + 10 * b
    ]

transitions = {}
for a, b in product(range(2), repeat=2):
    rows = []
    for u in range(10):
        v = 9 - u
        for q, low, high in decode_pair(u, v, a, b):
            rows.append((u, v, q, low, high))
    transitions[(a, b)] = rows

print("Transitions (incoming state -> digit pair, coefficient, outgoing state):")
for state in [(0, 0), (0, 1), (1, 1), (1, 0)]:
    print(state, transitions[state])

state_counts = {(0, 0): 1, (0, 1): 0, (1, 1): 0, (1, 0): 0}
accepted = []
for r in range(12):
    accepted.append(state_counts[(0, 0)] + state_counts[(1, 1)])
    next_counts = {s: 0 for s in state_counts}
    for state, count in state_counts.items():
        for _u, _v, _q, low, high in transitions[state]:
            next_counts[(low, high)] += count
    state_counts = next_counts

print("Accepted path counts for r=0..11:", accepted)
print("Fibonacci recurrence holds:", all(
    accepted[r + 2] == accepted[r + 1] + accepted[r]
    for r in range(len(accepted) - 2)
))
