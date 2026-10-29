#!/usr/bin/env python3
"""Fail-closed finite-width audit for claimed decimal two-epoch template returns.

This tool checks the physical base-10 orbit with two independent engines:
(1) Python's unbounded integer plus decimal-string reversal, and (2) an LSD-first
schoolbook digit-array reverse-and-add. At t=120 and t=240, the complete folded
pair-coefficient word must equal the claimed template with the specified gains.

JSON claims supply either a lattice path or explicit B/W arrays, plus J/U/C.
Use samples: [[q,k], ...] or q_values with k_values/k_scale; the default widths
are q=k=20,40,80,160. The default epoch clock is 1000 repeated 30 times.
For phase-changing seam families, endpoint_templates (two objects) or each
sample's targets can override B/W/J/U/C and the q/k offsets at t=120 and t=240.

A PASS is a finite differential replay only. It is not an all-width lemma or an
all-time Lychrel proof. For an all-width claim, use a symbolic checker too.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if not __debug__:
    raise RuntimeError("alert_check requires assertions enabled; do not run python -O")
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_Q_VALUES = (20, 40, 80, 160)
DEFAULT_CLOCK = [1, 0, 0, 0] * 30


class CheckError(ValueError):
    pass


def need(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


def parse_coefficients(value: Any, label: str) -> list[int]:
    if isinstance(value, str):
        try:
            values = [int(part.strip()) for part in value.split(",") if part.strip()]
        except ValueError as exc:
            raise CheckError(f"{label} must be comma-separated integers") from exc
    elif isinstance(value, list):
        values = value
    else:
        raise CheckError(f"{label} must be a list or comma-separated string")
    need(all(type(x) is int and 0 <= x <= 18 for x in values),
         f"{label} coefficients must be integers in [0,18]")
    return list(values)


def read_lattice(path: Path) -> tuple[list[int], list[int]]:
    try:
        lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        header = [int(x) for x in lines[0].split()]
        need(len(header) == 4, f"{path}: bad lattice header")
        period, b_len, w_len, base = header
        need((period, b_len, w_len, base) == (12, 34, 9, 10),
             f"{path}: expected rooted decimal p12/m9 lattice header (12,34,9,10)")
        need(len(lines) >= 2 + 2 * period + period, f"{path}: truncated lattice file")
        # Format: header, gamma, 12 W rows, 12 auxiliary rows, 12 B rows.
        w_rows = [[int(x) for x in lines[2 + i].split()] for i in range(period)]
        b_rows = [[int(x) for x in lines[2 + 2 * period + i].split()] for i in range(period)]
        need(all(len(row) == w_len for row in w_rows), f"{path}: malformed W rows")
        need(all(len(row) == b_len for row in b_rows), f"{path}: malformed B rows")
        b, w = b_rows[0], w_rows[0]
        need(all(0 <= x <= 18 for x in b + w), f"{path}: invalid pair coefficients")
        return b, w
    except (OSError, IndexError, ValueError) as exc:
        if isinstance(exc, CheckError):
            raise
        raise CheckError(f"cannot read lattice {path}: {exc}") from exc


def resolve_path(raw: str, claim_path: Path) -> Path:
    p = Path(raw)
    if p.is_absolute():
        return p
    candidates = (ROOT / p, claim_path.parent / p, Path.cwd() / p)
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    return (ROOT / p).resolve()


def build_template(B: list[int], W: list[int], J: list[int], U: list[int],
                   C: list[int], q: int, k: int) -> list[int]:
    need(type(q) is int and q >= 1, "q must be a positive integer")
    need(type(k) is int and k >= 1, "k must be a positive integer")
    H = B + W * q + J + U * k
    P = H + C + H[::-1]
    need(P == P[::-1], "template pairword is not symmetric")
    need(P and P[0] > 0, "template pairword must have a positive outer coefficient")
    need(all(type(x) is int and 0 <= x <= 18 for x in P), "template has invalid coefficients")
    if len(P) % 2:
        need(P[len(P) // 2] % 2 == 0, "odd-length pairword has an odd midpoint coefficient")
    return P


def realize_pairword(P: list[int]) -> list[int]:
    """Produce an LSD-first canonical decimal numeral with pairword P."""
    need(P == P[::-1] and bool(P), "cannot realize a nonsymmetric/empty pairword")
    d = [0] * len(P)
    for i in range(len(P) // 2):
        high = min(P[i], 9)
        low = P[i] - high
        need(0 <= low <= 9 and 0 <= high <= 9, f"pair coefficient {P[i]} is not realizable")
        d[i] = low
        d[len(P) - 1 - i] = high
    if len(P) % 2:
        need(P[len(P) // 2] % 2 == 0, "unrealizable odd midpoint")
        d[len(P) // 2] = P[len(P) // 2] // 2
    need(d[-1] != 0, "source numeral is not canonical")
    need(pairword_digits(d) == P, "internal realization cross-check failed")
    return d


def digits_to_int(d: list[int]) -> int:
    n = 0
    for x in reversed(d):
        n = n * 10 + x
    return n


def bigint_digits(n: int) -> list[int]:
    need(n > 0, "decimal state must be positive")
    return [ord(ch) - 48 for ch in reversed(str(n))]


def pairword_digits(d: list[int]) -> list[int]:
    return [d[i] + d[len(d) - 1 - i] for i in range(len(d))]


def pairword_bigint(n: int) -> list[int]:
    s = str(n)
    return [ord(s[-1 - i]) - 48 + ord(s[i]) - 48 for i in range(len(s))]


def bigint_step(n: int) -> int:
    # Engine A: independent unbounded-integer arithmetic and string reversal.
    return n + int(str(n)[::-1])


def digit_array_step(d: list[int]) -> list[int]:
    # Engine B: schoolbook decimal addition, no integer/string reversal.
    out: list[int] = []
    carry = 0
    n = len(d)
    for i in range(n):
        total = d[i] + d[n - 1 - i] + carry
        out.append(total % 10)
        carry = total // 10
    if carry:
        out.append(carry)
    need(out and out[-1] != 0, "digit-array engine produced a noncanonical numeral")
    return out


def normalize_target_spec(spec: dict[str, Any], *, B: list[int], W: list[int],
                         J: list[int], U: list[int], C: list[int],
                         q: int, k: int, epoch: int,
                         q_gain: int, k_gain: int) -> dict[str, Any]:
    need(isinstance(spec, dict), f"endpoint template {epoch} must be a JSON object")
    if "B" in spec or "W" in spec:
        need("B" in spec and "W" in spec, f"endpoint template {epoch} must provide both B and W")
        target_B = parse_coefficients(spec["B"], f"endpoint_templates[{epoch-1}].B")
        target_W = parse_coefficients(spec["W"], f"endpoint_templates[{epoch-1}].W")
    else:
        target_B, target_W = B, W
    target_J = parse_coefficients(spec["J"], f"endpoint_templates[{epoch-1}].J") if "J" in spec else J
    target_U = parse_coefficients(spec["U"], f"endpoint_templates[{epoch-1}].U") if "U" in spec else U
    target_C = parse_coefficients(spec["C"], f"endpoint_templates[{epoch-1}].C") if "C" in spec else C
    q_offset = spec.get("q_offset", epoch * q_gain)
    k_offset = spec.get("k_offset", epoch * k_gain)
    need(type(q_offset) is int and q_offset >= 0, f"endpoint template {epoch} q_offset must be nonnegative")
    need(type(k_offset) is int and k_offset >= 0, f"endpoint template {epoch} k_offset must be nonnegative")
    need(len(target_B) == 34 and len(target_W) == 9 and len(target_U) == 3,
         f"endpoint template {epoch} must use B34/W9/U3")
    need(target_C == target_C[::-1], f"endpoint template {epoch} C must be a palindrome")
    build_template(target_B, target_W, target_J, target_U, target_C, q + q_offset, k + k_offset)
    return {"B": target_B, "W": target_W, "J": target_J, "U": target_U, "C": target_C,
            "q_offset": q_offset, "k_offset": k_offset}


def normalize_claim(raw: dict[str, Any], claim_path: Path) -> dict[str, Any]:
    need(isinstance(raw, dict), "claim must be a JSON object")
    need(raw.get("base", 10) == 10, "this alert checker is for base 10 only")
    if "B" in raw and "W" in raw:
        B = parse_coefficients(raw["B"], "B")
        W = parse_coefficients(raw["W"], "W")
        if raw.get("lattice"):
            file_B, file_W = read_lattice(resolve_path(str(raw["lattice"]), claim_path))
            need(B == file_B and W == file_W, "explicit B/W disagree with lattice file")
    else:
        need(bool(raw.get("lattice")), "provide B and W, or a lattice path plus J/U/C")
        B, W = read_lattice(resolve_path(str(raw["lattice"]), claim_path))
    J = parse_coefficients(raw.get("J", []), "J")
    U = parse_coefficients(raw.get("U"), "U")
    C = parse_coefficients(raw.get("C", []), "C")
    need(B and W and U, "B, W, and U must be nonempty")
    need(C == C[::-1], "C must be a palindrome")
    need(len(B) == 34 and len(W) == 9 and len(U) == 3,
         "T* schema requires rooted p12/m9 B34, W9, and U3 blocks")
    q_gain = raw.get("q_gain", 0)
    k_gain = raw.get("k_gain", 5)
    epoch_steps = raw.get("epoch_steps", 120)
    epochs = raw.get("epochs", 2)
    need(type(q_gain) is int and q_gain >= 0, "q_gain must be a nonnegative integer")
    need(type(k_gain) is int and k_gain > 0, "k_gain must be a positive integer")
    need(type(epoch_steps) is int and epoch_steps == 120,
         "T* alert checks require exactly 120 ordinary steps per epoch")
    need(type(epochs) is int and epochs == 2,
         "alert_check is specifically a two-epoch (240-step) checker")
    if "overflow_clock" not in raw:
        clock = DEFAULT_CLOCK[:]
    else:
        value = raw["overflow_clock"]
        if isinstance(value, str):
            need(value and set(value) <= {"0", "1"}, "overflow_clock string must contain only 0/1")
            clock = [int(ch) for ch in value]
        else:
            need(isinstance(value, list) and all(type(x) is int and x in (0, 1) for x in value),
                 "overflow_clock must be a 0/1 string or list")
            clock = list(value)
    repeats = raw.get("overflow_repeats")
    if repeats is not None:
        need(type(repeats) is int and repeats >= 1, "overflow_repeats must be a positive integer")
        need(len(clock) * repeats == epoch_steps,
             f"overflow_clock pattern length × overflow_repeats must equal {epoch_steps}")
        clock = clock * repeats
    need(len(clock) == epoch_steps,
         f"overflow_clock must contain exactly {epoch_steps} bits (or a pattern with overflow_repeats)")
    global_targets = raw.get("endpoint_templates")
    if global_targets is not None:
        need(isinstance(global_targets, list) and len(global_targets) == 2,
             "endpoint_templates must contain exactly two endpoint objects (t=120 and t=240)")
    samples = raw.get("samples")
    if samples is None:
        q_values = raw.get("q_values", list(DEFAULT_Q_VALUES))
        need(isinstance(q_values, list) and q_values, "q_values must be a nonempty list")
        if "k_values" in raw:
            k_values = raw["k_values"]
            need(isinstance(k_values, list) and len(k_values) == len(q_values),
                 "k_values must have the same length as q_values")
        else:
            k_scale = raw.get("k_scale", 1)
            k_offset = raw.get("k_offset", 0)
            need(type(k_scale) is int and k_scale > 0 and type(k_offset) is int and k_offset >= 0,
                 "k_scale must be positive and k_offset nonnegative")
            k_values = [q * k_scale + k_offset for q in q_values]
        samples = [{"q": q, "k": k} for q, k in zip(q_values, k_values)]
    need(isinstance(samples, list) and samples, "samples must be a nonempty list")
    normalized_samples = []
    seen_samples = set()
    for i, sample in enumerate(samples):
        if isinstance(sample, list) and len(sample) == 2:
            q, k = sample
            sample_targets = None
        elif isinstance(sample, dict):
            q, k = sample.get("q"), sample.get("k")
            sample_targets = sample.get("targets")
        else:
            raise CheckError(f"samples[{i}] must be [q,k] or an object with q,k and optional targets")
        need(type(q) is int and q >= 20 and type(k) is int and k >= 20,
             f"samples[{i}] requires q,k >= 20")
        need((q, k) not in seen_samples, "duplicate q,k samples")
        seen_samples.add((q, k))
        if sample_targets is not None:
            need(isinstance(sample_targets, list) and len(sample_targets) == 2,
                 f"samples[{i}].targets must contain exactly two endpoint objects")
            target_raws = sample_targets
        elif global_targets is not None:
            target_raws = global_targets
        else:
            target_raws = [{}, {}]
        targets = [
            normalize_target_spec(target_raws[epoch - 1], B=B, W=W, J=J, U=U, C=C,
                                  q=q, k=k, epoch=epoch, q_gain=q_gain, k_gain=k_gain)
            for epoch in (1, 2)
        ]
        # Reject malformed/noncanonical source and endpoint families before replay.
        build_template(B, W, J, U, C, q, k)
        normalized_samples.append({"q": q, "k": k, "targets": targets})
    odd_guard = raw.get("require_odd_pair_guard", True)
    need(type(odd_guard) is bool, "require_odd_pair_guard must be a JSON boolean")
    return {
        "name": str(raw.get("name", claim_path.stem)), "B": B, "W": W, "J": J, "U": U, "C": C,
        "samples": normalized_samples, "q_gain": q_gain, "k_gain": k_gain,
        "epoch_steps": epoch_steps, "epochs": epochs, "clock": clock,
        "require_odd_pair_guard": odd_guard,
    }


def first_difference(got: list[int], expected: list[int]) -> int | None:
    limit = min(len(got), len(expected))
    for i in range(limit):
        if got[i] != expected[i]:
            return i
    return None if len(got) == len(expected) else limit


def run_sample(claim: dict[str, Any], q: int, k: int,
               targets: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    B, W, J, U, C = (claim[name] for name in ("B", "W", "J", "U", "C"))
    if targets is None:
        sample = next((item for item in claim["samples"] if item["q"] == q and item["k"] == k), None)
        if sample is not None:
            targets = sample["targets"]
        else:
            targets = [
                normalize_target_spec({}, B=B, W=W, J=J, U=U, C=C, q=q, k=k,
                                      epoch=epoch, q_gain=claim["q_gain"], k_gain=claim["k_gain"])
                for epoch in (1, 2)
            ]
    source_pair = build_template(B, W, J, U, C, q, k)
    digits = realize_pairword(source_pair)
    number = int("".join(str(x) for x in reversed(digits)))
    need(bigint_digits(number) == digits, "initial bigint/digit-array realization mismatch")
    issues: list[str] = []
    issue_count = 0
    endpoint_results: list[dict[str, Any]] = []
    overflow: list[int] = []
    palindrome_times: list[int] = []
    odd_guard_missing: list[int] = []
    engine_mismatch_times: list[int] = []
    clock_mismatch_times: list[int] = []
    total_steps = claim["epoch_steps"] * claim["epochs"]

    def fail(message: str) -> None:
        nonlocal issue_count
        issue_count += 1
        if len(issues) < 24:
            issues.append(message)

    for t in range(total_steps + 1):
        try:
            d_from_big = bigint_digits(number)
            pw_digits = pairword_digits(digits)
            pw_big = pairword_bigint(number)
            if digits != d_from_big or digits_to_int(digits) != number or pw_digits != pw_big:
                engine_mismatch_times.append(t)
                fail(f"t={t}: bigint and digit-array states/pairwords disagree")
            if digits == digits[::-1]:
                palindrome_times.append(t)
                fail(f"t={t}: actual decimal state is palindromic")
            if not any(x & 1 for x in pw_digits):
                odd_guard_missing.append(t)
                if claim["require_odd_pair_guard"]:
                    fail(f"t={t}: no odd pair-coefficient witness for the non-palindrome guard")
            if t > 0 and t % claim["epoch_steps"] == 0:
                epoch = t // claim["epoch_steps"]
                target_spec = targets[epoch - 1]
                target_q = q + target_spec["q_offset"]
                target_k = k + target_spec["k_offset"]
                expected = build_template(target_spec["B"], target_spec["W"], target_spec["J"],
                                          target_spec["U"], target_spec["C"], target_q, target_k)
                diff = first_difference(pw_digits, expected)
                result = {
                    "step": t, "target_q": target_q, "target_k": target_k,
                    "target_J_length": len(target_spec["J"]), "target_C_length": len(target_spec["C"]),
                    "return": diff is None, "actual_pairword_length": len(pw_digits),
                    "expected_pairword_length": len(expected), "first_mismatch": diff,
                }
                endpoint_results.append(result)
                if diff is not None:
                    observed = pw_digits[diff] if diff < len(pw_digits) else None
                    wanted = expected[diff] if diff < len(expected) else None
                    fail(f"t={t}: full template mismatch at coefficient {diff} (observed={observed}, expected={wanted})")
        except CheckError as exc:
            fail(f"t={t}: {exc}")
            break
        if t == total_steps:
            break
        try:
            next_number = bigint_step(number)
            next_digits = digit_array_step(digits)
            big_overflow = len(str(next_number)) - len(str(number))
            digit_overflow = len(next_digits) - len(digits)
            expected_bit = claim["clock"][t % claim["epoch_steps"]]
            if big_overflow != digit_overflow:
                engine_mismatch_times.append(t + 1)
                fail(f"t={t + 1}: engines disagree on digit-length overflow")
            if digit_overflow != expected_bit:
                clock_mismatch_times.append(t + 1)
                fail(f"t={t + 1}: overflow bit {digit_overflow}, expected {expected_bit}")
            if digits_to_int(next_digits) != next_number or bigint_digits(next_number) != next_digits:
                engine_mismatch_times.append(t + 1)
                fail(f"t={t + 1}: engines disagree on successor digits")
            number, digits = next_number, next_digits
            overflow.append(digit_overflow)
        except (CheckError, ValueError) as exc:
            fail(f"step {t}->{t + 1}: {exc}")
            break

    passed = issue_count == 0 and len(endpoint_results) == 2 and all(x["return"] for x in endpoint_results)
    return {
        "status": "PASS_FINITE_TWO_EPOCH_REPLAY_ONLY" if passed else "FAIL",
        "q": q, "k": k, "steps": len(overflow), "epochs": len(endpoint_results),
        "overflow_count": sum(overflow), "overflow_clock_matches": not clock_mismatch_times,
        "endpoint_returns": endpoint_results, "palindrome_times": palindrome_times,
        "odd_guard_missing_times": odd_guard_missing,
        "engine_mismatch_times": sorted(set(engine_mismatch_times)),
        "clock_mismatch_times": clock_mismatch_times,
        "failure_count": issue_count, "failures": issues,
        "scope_warning": "Finite-width replay only; not an all-width or all-time proof.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("claim", type=Path, help="JSON claim file describing B/W/J/U/C and expected gains")
    args = parser.parse_args()
    try:
        raw = json.loads(args.claim.read_text(encoding="utf-8"))
        claim = normalize_claim(raw, args.claim.resolve())
    except (OSError, json.JSONDecodeError, CheckError) as exc:
        print(json.dumps({"name": str(args.claim), "status": "FAIL", "error": str(exc)}, sort_keys=True))
        return 2

    print(json.dumps({"name": claim["name"], "status": "START",
                      "samples": len(claim["samples"]), "steps_per_sample": claim["epoch_steps"] * claim["epochs"],
                      "engines": ["python-bigint-string-reversal", "schoolbook-decimal-digit-array"],
                      "q_gain_per_epoch": claim["q_gain"], "k_gain_per_epoch": claim["k_gain"]}, sort_keys=True), flush=True)
    all_pass = True
    results = []
    for sample in claim["samples"]:
        q, k = sample["q"], sample["k"]
        try:
            result = run_sample(claim, q, k, sample["targets"])
        except CheckError as exc:
            result = {"status": "FAIL", "q": q, "k": k, "failure_count": 1, "failures": [str(exc)],
                      "scope_warning": "Finite-width replay only; not an all-width or all-time proof."}
        print(json.dumps(result, sort_keys=True), flush=True)
        results.append(result)
        all_pass = all_pass and result["status"] == "PASS_FINITE_TWO_EPOCH_REPLAY_ONLY"
    print(json.dumps({"name": claim["name"], "status": "PASS" if all_pass else "FAIL",
                      "samples_passed": sum(1 for result in results if result["status"] == "PASS_FINITE_TWO_EPOCH_REPLAY_ONLY"),
                      "interpretation": "PASS means all listed widths passed only; it does not establish a symbolic/all-time return."}, sort_keys=True))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
