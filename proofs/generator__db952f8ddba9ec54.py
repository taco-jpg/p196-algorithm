"""Exact bounded-period SAT encoding of the phase-padded exterior map.

No exterior length is guessed or trimmed inside the SAT formula. Every row has
width W. The raw (W+1)-st coefficient must equal the next phase, so discarding
it is a legitimate reassignment to the constant tail. Carry bits are computed
by the finite normalization relation, not unconstrained control inputs.
"""
from itertools import combinations


def next_phase(c):
    return 2 * (c - 9 * int(c >= 10))


class CNF:
    def __init__(self):
        self.variables = 0
        self.clauses = []

    def var(self):
        self.variables += 1
        return self.variables

    def add(self, *lits):
        self.clauses.append(tuple(lits))

    def onehot(self, n):
        row = [self.var() for _ in range(n)]
        self.add(*row)
        for a, b in combinations(row, 2):
            self.add(-a, -b)
        return row

    def bit(self, variable, value):
        self.add(variable if value else -variable)

    def decimal_cell(self, coefficient, carry_in, digit, carry_out):
        for a in range(19):
            for e in [0, 1]:
                # Negation of the two input assumptions.
                guard = [-coefficient[a], -carry_in if e else carry_in]
                out = (a + e) // 10
                self.add(*guard, digit[(a + e) % 10])
                self.add(*guard, carry_out if out else -carry_out)

    def exact_count(self, bits, total):
        # Saturating count states 0,...,total,total+1.
        rows = [self.onehot(total + 2) for _ in range(len(bits) + 1)]
        self.add(rows[0][0])
        for t, bit in enumerate(bits):
            for count in range(total + 2):
                self.add(-rows[t][count], bit, rows[t + 1][count])
                self.add(-rows[t][count], -bit,
                         rows[t + 1][min(total + 1, count + 1)])
        self.add(rows[-1][total])

    def text(self):
        return f"p cnf {self.variables} {len(self.clauses)}\n" + "".join(
            " ".join(map(str, clause)) + " 0\n" for clause in self.clauses)


def build(width, period, phase, overflows=None, require_full_width=False,
          cyclic=True, require_overflow=True):
    assert width >= 1 and period >= 1 and phase in range(2, 18, 2)
    phases = [phase]
    for _ in range(period):
        phases.append(next_phase(phases[-1]))
    if cyclic and phases[-1] != phase:
        raise ValueError("The specified phase cannot close after this period")
    cnf = CNF()
    row_count = period if cyclic else period + 1
    B = [[cnf.onehot(19) for _ in range(width)] for _ in range(row_count)]
    low = [[cnf.onehot(10) for _ in range(width)] for _ in range(period)]
    high = [[cnf.onehot(10) for _ in range(width)] for _ in range(period)]
    lc = [[cnf.var() for _ in range(width + 1)] for _ in range(period)]
    rc = [[cnf.var() for _ in range(width + 1)] for _ in range(period)]
    gamma = [rc[t][0] for t in range(period)]
    for t in range(period):
        c, cnext = phases[t], phases[t + 1]
        k, tail_digit = int(c >= 10), c - 9 * int(c >= 10)
        cnf.bit(lc[t][0], 0)
        cnf.bit(rc[t][width], k)
        cnf.add(-B[t][0][0])  # Actual exterior coefficient is positive.
        for j in range(width):
            cnf.decimal_cell(B[t][j], lc[t][j], low[t][j], lc[t][j + 1])
            cnf.decimal_cell(B[t][j], rc[t][j + 1], high[t][j], rc[t][j])
        target = B[(t + 1) % row_count]
        for j in range(width):
            for a in range(10):
                for b in range(10):
                    # gamma=0: low[j]+high[j].
                    cnf.add(gamma[t], -low[t][j][a], -high[t][j][b], target[j][a + b])
                    # gamma=1: low[j]+high[j-1], except exterior low[0]+1.
                    if j:
                        cnf.add(-gamma[t], -low[t][j][a], -high[t][j - 1][b], target[j][a + b])
                if j == 0:
                    cnf.add(-gamma[t], -low[t][0][a], target[0][a + 1])
        # Raw last coefficient must be cnext, for both actual overflow cases.
        for e in [0, 1]:
            neg_e = -lc[t][width] if e else lc[t][width]
            u = c + e - 10 * k
            if u + tail_digit != cnext:
                cnf.add(gamma[t], neg_e)
            for digit in range(10):
                if u + digit != cnext:
                    cnf.add(-gamma[t], neg_e, -high[t][width - 1][digit])
    if require_overflow:
        cnf.add(*gamma)
    if overflows is not None:
        cnf.exact_count(gamma, overflows)
    if require_full_width:
        # At some time the represented canonical exterior really has width W.
        cnf.add(*[-B[t][-1][phases[t]] for t in range(period)])
    metadata = {"width": width, "period": period, "initial_phase": phase,
                "phases": phases[:-1], "exact_overflows": overflows,
                "require_full_width": require_full_width,
                "cyclic": cyclic, "require_overflow": require_overflow,
                "B_variables": B, "overflow_variables": gamma,
                "low_digit_variables": low, "high_digit_variables": high,
                "low_carry_variables": lc, "high_carry_variables": rc,
                "variables": cnf.variables, "clauses": len(cnf.clauses)}
    return cnf, metadata


def normalize(word, incoming):
    digits, carries = [], [incoming]
    for a in word:
        digits.append((a + carries[-1]) % 10)
        carries.append((a + carries[-1]) // 10)
    return digits, carries


def original_outer_step(c, B):
    """Original variable-length map, with actual maximal suffix removal."""
    k = int(c >= 10)
    D, carry = normalize(B, 0)
    R, reverse_carry = normalize(B[::-1], k)
    gamma = reverse_carry[-1]
    u, t = c + carry[-1] - 10 * k, c - 9 * k
    rhs = [1] + R[::-1] if gamma else R[::-1] + [t]
    raw = [a + b for a, b in zip(D + [u], rhs)]
    while raw and raw[-1] == 2 * t:
        raw.pop()
    return 2 * t, raw, gamma


def trim(c, B):
    B = list(B)
    while B and B[-1] == c:
        B.pop()
    return B


def verify_candidate(metadata, positive_literals):
    states, counts = [], []
    B = metadata["B_variables"]
    for c, row in zip(metadata["phases"], B):
        word = []
        for cell in row:
            picked = [a for a, var in enumerate(cell) if var in positive_literals]
            if len(picked) != 1:
                raise AssertionError("invalid one-hot model")
            word.append(picked[0])
        canonical = trim(c, word)
        if canonical and not canonical[0]:
            raise AssertionError("nonpositive exterior")
        states.append((c, canonical))
    for i, state in enumerate(states):
        c, B, g = original_outer_step(*state)
        assert (c, B) == states[(i + 1) % len(states)]
        counts.append(g)
    if metadata["exact_overflows"] is not None:
        assert sum(counts) == metadata["exact_overflows"]
    assert sum(counts) > 0
    return {"states": states, "overflows": counts, "total_overflows": sum(counts),
            "maximum_canonical_width": max(len(B) for _, B in states),
            "original_map_replay": "PASS"}
