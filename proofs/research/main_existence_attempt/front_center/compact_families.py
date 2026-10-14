"""Exact local cap certificates and conditional finite-family gluing.

Standard-library checker, independent of Domain.step and of the SMT models.
The local identities below do NOT supply the missing finite exterior.
"""
from dataclasses import dataclass
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def carry_into(at, i, direction):
    """Incoming carry is fixed by the nearest non-nine in that direction."""
    j = i + direction
    while at(j) == 9:
        j += direction
    return int(at(j) >= 10)


def output_at(at, h, i):
    low = (at(i) + carry_into(at, i, -1)) % 10
    j = i - h
    high = (at(j) + carry_into(at, j, 1)) % 10
    return low + high


def periodic_step(word, h):
    assert any(q != 9 for q in word)
    at = lambda i: word[i % len(word)]
    return tuple(output_at(at, h, i) for i in range(len(word)))


@dataclass(frozen=True)
class Patch:
    left: tuple
    right: tuple
    start: int
    patch: tuple

    @property
    def end(self):
        return self.start + len(self.patch)

    def at(self, i):
        if i < self.start:
            return self.left[i % len(self.left)]
        if i >= self.end:
            return self.right[i % len(self.right)]
        return self.patch[i - self.start]

    def trim(self):
        a, b = 0, len(self.patch)
        while a < b and self.patch[a] == self.left[(self.start + a) % len(self.left)]:
            a += 1
        while a < b and self.patch[b-1] == self.right[(self.start + b-1) % len(self.right)]:
            b -= 1
        return Patch(self.left, self.right, self.start+a, self.patch[a:b])

    def shifted(self, d):
        left = tuple(self.left[(i-d) % len(self.left)] for i in range(len(self.left)))
        right = tuple(self.right[(i-d) % len(self.right)] for i in range(len(self.right)))
        return Patch(left, right, self.start+d, self.patch)

    def same(self, other):
        return self.left == other.left and self.right == other.right and all(
            self.at(i) == other.at(i)
            for i in range(min(self.start, other.start), max(self.end, other.end)))

    def step(self, h):
        assert h in (0, 1)
        assert any(q != 9 for q in self.left)
        assert any(q != 9 for q in self.right)
        # Beyond this window the nearest non-nine in either direction is
        # reached inside an unchanged periodic tail. Thus all remaining
        # infinitely many columns are exactly the periodic-step residues.
        radius = max(len(self.left), len(self.right)) + 2
        a, b = self.start-radius, self.end+radius
        patch = tuple(output_at(self.at, h, i) for i in range(a, b))
        return Patch(periodic_step(self.left, h), periodic_step(self.right, h),
                     a, patch).trim()

    def serial(self):
        return dict(left=self.left, right=self.right, start=self.start, patch=self.patch)


def symmetric_cap(bulk, core):
    axis2 = len(core) - 1
    right = tuple(bulk[(axis2-i) % len(bulk)] for i in range(len(bulk)))
    return Patch(tuple(bulk), right, 0, tuple(core)).trim()


def audit_cap(name, bulk, core, period=24):
    initial = symmetric_cap(bulk, core)
    row = initial
    rows = [row]
    witnesses = []
    for t in range(period):
        axis2 = len(core)-1 + t//2
        # Check every patch position and each periodic tail residue. The
        # reflected intervals outside this window are both periodic.
        radius = max(len(row.left), len(row.right)) + 2
        lo = min(row.start, axis2-row.end+1)-radius
        hi = max(row.end, axis2-row.start+1)+radius
        for i in range(lo, hi):
            assert row.at(i) == row.at(axis2-i), (name, t, i)
            assert 0 <= row.at(i) <= 18
        if axis2 % 2 == 0:
            assert row.at(axis2//2) % 2 == 0
        witness = next((i, row.at(i)) for i in range(row.start, row.end)
                       if row.at(i) > 9 and row.at(i) != 11)
        witnesses.append(dict(index=witness[0], coefficient=witness[1]))
        row = row.step(t % 2)
        rows.append(row)
    assert rows[4].same(initial.shifted(1)), name
    assert rows[24].same(initial.shifted(6)), name
    assert min(row.start for row in rows) >= 0
    assert all(any(q != 9 for q in row.left) for row in rows)
    return dict(name=name, bulk=bulk, core=core, core_length=len(core),
                period=period, clock=[t % 2 for t in range(period)], shift=6,
                trace=[row.serial() for row in rows], safety_witnesses=witnesses,
                minimum_patch_start=min(row.start for row in rows),
                sufficient_bulk_blocks_each_side=1,
                exact_local_identity=True, finite_exterior_supplied=False,
                decimal_lychrel_existence_proved=False)


def digits(q, incoming):
    result = []
    carry = incoming
    for coefficient in q:
        value = coefficient + carry
        result.append(value % 10)
        carry = value // 10
    return tuple(result), carry


def check_exterior(rows, bulk):
    """Independent finite checker for the remaining exterior obligation.

    rows[t] is a fixed-width prefix followed immediately by bulk_t at phase
    zero. This checks all boundary carries and the overflow seam digit.
    """
    assert len(rows) == 24 and len({len(row) for row in rows}) == 1
    assert len(rows[0]) > 0
    current_bulk = tuple(bulk)
    for t, row in enumerate(rows):
        h = t % 2
        assert all(0 <= q <= 18 for q in row)
        assert row[0] == (8 if h == 0 else 17)
        at = lambda i: current_bulk[i % len(current_bulk)]
        # carry into the periodic tail from the prefix, and the periodic
        # tail's outgoing carry into the prefix when read from the right.
        target_low = carry_into(at, 0, -1)
        target_high = (at(0) + carry_into(at, 0, 1)) // 10
        low, outgoing_low = digits(row, 0)
        high_reversed, outgoing_high = digits(tuple(reversed(row)), target_high)
        high = high_reversed[::-1]
        assert outgoing_low == target_low
        assert outgoing_high == h
        following = tuple(low[i] + (1 if h and i == 0 else high[i-h])
                          for i in range(len(row)))
        assert following == tuple(rows[(t+1) % 24])
        next_bulk = periodic_step(current_bulk, h)
        if h:
            first_low = (at(0) + target_low) % 10
            assert first_low + high[-1] == next_bulk[0]
        current_bulk = next_bulk
    assert current_bulk == tuple(bulk)
    return True


def finite_family_word(prefix, bulk, core, m):
    assert m >= 1
    half = tuple(prefix) + tuple(bulk)*m
    return half + tuple(core) + half[::-1]


def build_records():
    records = []
    cap525 = (7,3,6,9,3,8,10,4,10,8,3,9,6,3,7)
    records.append(audit_cap("525_front_plus_center", (5,2,5), cap525))
    families = [
        ("936_odd", (9,3,6), (9,3,8,10,4,10,8,3,9)),
        ("12159_even", (12,15,9), (12,15,14,8,1,1,8,14,15,12)),
        ("91512_complement_odd", (9,15,12), (9,15,10,8,14,8,10,15,9)),
        ("639_complement_even", (6,3,9), (6,3,4,10,17,17,10,4,3,6)),
    ]
    for name, bulk, core in families:
        for rotation in range(3):
            b = bulk[rotation:]+bulk[:rotation]
            w = core[rotation:len(core)-rotation] if rotation else core
            record = audit_cap(name+f"_rotation{rotation}", b, w)
            record["rotation"] = rotation
            record["inserted_coefficient_mass_per_24_steps"] = 4*sum(b)
            records.append(record)
    # Complement is an exact conjugacy: incoming carries are toggled, so
    # each directional output digit d becomes 9-d, and G_h becomes 18-G_h.
    for source, target in (("936_odd", "91512_complement_odd"),
                           ("12159_even", "639_complement_even")):
        for rotation in range(3):
            original = next(r for r in records if r["name"] == source+f"_rotation{rotation}")
            complement = next(r for r in records if r["name"] == target+f"_rotation{rotation}")
            for x, y in zip(original["trace"], complement["trace"]):
                assert y["start"] == x["start"]
                for part in ("left", "right", "patch"):
                    assert tuple(y[part]) == tuple(18-q for q in x[part])
    return records


def run():
    records = build_records()
    output = dict(
        status="exact_caps_verified_and_exterior_conditional_families_derived",
        checker="nearest_non_nine_carries_in_both_directions; periodic tail residues",
        caps=records,
        family="Q_m = P ++ B^m ++ W ++ reverse(B)^m ++ reverse(P), m >= 1",
        exterior_obligation="24 fixed-width prefix rows accepted by check_exterior(rows,B)",
        conditional_return="F^24(Q_m) = Q_(m+2)",
        gluing_reason=[
            "Each phase has at least one non-nine per three-symbol bulk period.",
            "The center defect starts at a nonnegative local index at every phase.",
            "For m>=1, a complete periodic block separates each exterior from the defect.",
            "This block resets the carry flowing from the center toward the exterior.",
            "The checked exterior supplies the exact periodic incoming carry toward the center.",
            "The overflow seam equality supplies the digit shifted across the prefix cut.",
            "Reflection supplies the right boundary; center symmetry fixes both middle cases.",
            "After 24 phases, the prefix and bulk return, the center shifts six columns, and the finite length increases by twelve.",
        ],
        safety="Every phase contains a coefficient >9 and unequal to11; both exact palindrome-predecessor patterns are excluded.",
        canonical_realization="The finite symmetric q-word has entries0..18, positive outer entry8, and an even middle when odd; split opposed sums into digits0..9 with positive leading digit.",
        conditional_witness="If an exterior is supplied, value(Q_1)=sum_i Q_1[i]*10^i has an entirely nonpalindromic ordinary decimal reverse-and-add orbit.",
        obstruction_525=dict(
            period=24, inserted_positions=12, inserted_coefficient_mass=48,
            mass_increment_mod9=48 % 9, multiplier_mod9=pow(2,24,9),
            exact_reason="For finite canonical rows, sum(F(q))=2*sum(q) modulo9. A24-step return inserting four525 blocks contradicts this.",
            period_24k_necessary_condition="3 divides k",
            smallest_unexcluded_multiple_of_24=72,
            scope="All fixed finite exteriors compatible with this cap and return; not arbitrary Lychrel numbers."),
        finite_exterior_supplied=False, decimal_lychrel_existence_proved=False)
    destination = HERE / "compact_family_certificates.json"
    destination.write_text(json.dumps(output, indent=2)+"\n")
    print(json.dumps(dict(status=output["status"], caps=len(records),
                         destination=str(destination), finite_exterior_supplied=False)))


if __name__ == "__main__":
    run()
