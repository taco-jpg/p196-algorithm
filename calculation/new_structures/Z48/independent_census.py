#!/usr/bin/env python3
"""Independent Python census for rooted p12/m9 U=(10,9,8), phase 0.

The exhaustive pass is a from-scratch pairword recurrence, vectorized across
all raw J words with NumPy and compiled with Numba. Separate controls realize
pairwords as actual decimal integers and compare every step with n+reverse(n).
No mod-11 gate or centre-parity filter is applied.
"""
from __future__ import annotations
import collections, hashlib, json, os, sys, time
import numpy as np
import numba
from numba import njit, prange

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)
numba.set_num_threads(min(8, os.cpu_count() or 1))

B = [10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W = [5,18,4,8,1,15,4,0,5]
U = [10,9,8]
C_DEFAULT = [0,0,0]
G = [1,0,0,0,1,0,0,0,1,0,0,0]
STEPS, Q_REF, K_REF = 120, 14, 100
BAND_START = len(B)
TARGET_END = len(B) + len(W)*Q_REF
SAMPLES = {
    3: [[0,0,0],[18,18,18],[1,2,3],[10,9,8]],
    4: [[0,0,0,0],[18,18,18,18],[0,18,9,1],[10,9,8,7]],
}

def make_template(q, k, junction, center=None):
    if center is None:
        center = C_DEFAULT
    h = B + W*q + junction + U*k
    return h + center + h[::-1]

def pairword_step(pairword):
    digits, carry = [], 0
    for coeff in pairword:
        value = int(coeff) + carry
        digits.append(value % 10)
        carry = value // 10
    overflow = carry
    if carry:
        digits.append(carry)
    return [digits[i] + digits[len(digits)-1-i]
            for i in range(len(digits))], overflow

def pairword_of_int(number):
    digits = [ord(ch)-48 for ch in str(number)[::-1]]
    return [digits[i] + digits[len(digits)-1-i]
            for i in range(len(digits))]

def realize_pairword(pairword):
    assert pairword == pairword[::-1]
    digits = [0]*len(pairword)
    for i in range(len(pairword)//2):
        high = min(9, int(pairword[i]))
        low = int(pairword[i]) - high
        assert 0 <= low <= 9
        digits[i], digits[-1-i] = low, high
    if len(pairword) % 2:
        mid = len(pairword)//2
        assert pairword[mid] % 2 == 0
        digits[mid] = pairword[mid]//2
    assert digits[-1] != 0
    number = int("".join(str(d) for d in digits[::-1]))
    assert pairword_of_int(number) == pairword
    return number

def first_prefix_mismatch(pairword, q):
    target = B + W*q
    for i, expected in enumerate(target):
        if pairword[i] != expected:
            return i
    return None

def bigint_control(q, k, junction, center):
    pairword = make_template(q, k, junction, center)
    number = realize_pairword(pairword)
    assert pairword_of_int(number) == pairword
    initial_digits = len(str(number))
    overflow_bits = []
    for t in range(STEPS):
        old_text = str(number)
        number_next = number + int(old_text[::-1])
        pairword_next, overflow = pairword_step(pairword)
        assert pairword_next == pairword_of_int(number_next), ("pairword/bigint", q,k,junction,center,t)
        actual_overflow = int(len(str(number_next)) > len(old_text))
        assert actual_overflow == overflow, ("overflow/bigint", q,k,junction,center,t)
        overflow_bits.append(overflow)
        number, pairword = number_next, pairword_next
    mismatch = first_prefix_mismatch(pairword, q)
    return {
        "q": q, "k": k, "J": junction, "C": center, "steps": STEPS,
        "initial_decimal_digits": initial_digits,
        "final_decimal_digits": len(str(number)),
        "overflow_count": sum(overflow_bits),
        "clock_exact": overflow_bits == G*10,
        "first_mismatch_absolute": mismatch,
        "first_mismatch_W_offset": None if mismatch is None else mismatch-len(B),
        "full_step_pairword_bigint_equal": True,
    }

def build_matrix(jlen, q, k, center):
    nrows = 19**jlen
    hlen = len(B) + len(W)*q + jlen + len(U)*k
    initial_len = 2*hlen + len(center)
    capacity = initial_len + STEPS + 2
    A = np.empty((nrows, capacity), dtype=np.uint8)
    H = np.empty((nrows, hlen), dtype=np.uint8)
    prefix = np.asarray(B + W*q, dtype=np.uint8)
    H[:, :len(prefix)] = prefix
    codes = np.arange(nrows, dtype=np.int64)
    for pos in range(jlen):
        H[:, len(prefix)+pos] = ((codes // (19**pos)) % 19).astype(np.uint8)
    u_start = len(prefix)+jlen
    H[:, u_start:u_start+len(U)*k] = np.asarray(U*k, dtype=np.uint8)
    A[:, :hlen] = H
    A[:, hlen:hlen+len(center)] = np.asarray(center, dtype=np.uint8)
    A[:, hlen+len(center):initial_len] = H[:, ::-1]
    del H
    D, Q = np.empty_like(A), np.empty_like(A)
    n_init = np.full(nrows, initial_len, dtype=np.int32)
    return A, D, Q, n_init

@njit(parallel=True)
def exhaustive_kernel(A, D, Q, n_init, target, steps, clock):
    nrows = A.shape[0]
    mismatch = np.empty(nrows, dtype=np.int32)
    first_clock_bad = np.empty(nrows, dtype=np.int16)
    final_len = np.empty(nrows, dtype=np.int32)
    for row in prange(nrows):
        n, clock_bad = n_init[row], -1
        for t in range(steps):
            carry = 0
            if (t & 1) == 0:
                for i in range(n):
                    value = int(A[row,i]) + carry
                    D[row,i] = value % 10
                    carry = value // 10
                overflow, n2 = carry, n
                if overflow != 0:
                    D[row,n] = overflow
                    n2 = n+1
                if overflow != int(clock[t % clock.shape[0]]) and clock_bad < 0:
                    clock_bad = t
                for i in range(n2):
                    Q[row,i] = int(D[row,i]) + int(D[row,n2-1-i])
            else:
                for i in range(n):
                    value = int(Q[row,i]) + carry
                    D[row,i] = value % 10
                    carry = value // 10
                overflow, n2 = carry, n
                if overflow != 0:
                    D[row,n] = overflow
                    n2 = n+1
                if overflow != int(clock[t % clock.shape[0]]) and clock_bad < 0:
                    clock_bad = t
                for i in range(n2):
                    A[row,i] = int(D[row,i]) + int(D[row,n2-1-i])
            n = n2
        idx = -1
        for i in range(target.shape[0]):
            if int(A[row,i]) != int(target[i]):
                idx = i
                break
        mismatch[row], first_clock_bad[row], final_len[row] = idx, clock_bad, n
    return mismatch, first_clock_bad, final_len

def run_census(jlen, center):
    A,D,Q,n_init = build_matrix(jlen, Q_REF, K_REF, center)
    target = np.asarray(B + W*Q_REF, dtype=np.uint8)
    started = time.time()
    mismatch, clock_bad, final_len = exhaustive_kernel(A,D,Q,n_init,target,STEPS,np.asarray(G,dtype=np.uint8))
    absolute_hist = collections.Counter(int(x) for x in mismatch)
    offsets = [int(x)-BAND_START for x in mismatch if 0 <= int(x) < TARGET_END]
    offset_hist = collections.Counter(offsets)
    return {
        "junction_length": jlen, "centre": center, "enumerated": int(len(mismatch)),
        "expected_enumeration": 19**jlen,
        "first_mismatch_absolute_histogram": {str(k):int(v) for k,v in sorted(absolute_hist.items())},
        "first_mismatch_W_offset_histogram": {str(k):int(v) for k,v in sorted(offset_hist.items())},
        "first_mismatch_absolute_min": int(mismatch.min()),
        "first_mismatch_absolute_max": int(mismatch.max()),
        "first_mismatch_W_offset_min": min(offsets),
        "first_mismatch_W_offset_max": max(offsets),
        "wrong_clock": int(np.sum(clock_bad >= 0)),
        "root_B_mismatches": sum(1 for x in mismatch if 0 <= int(x) < BAND_START),
        "no_W_prefix_mismatch": int(np.sum(mismatch < 0)),
        "mismatch_after_W_prefix": int(np.sum(mismatch >= TARGET_END)),
        "final_pairword_length_min": int(final_len.min()),
        "final_pairword_length_max": int(final_len.max()),
        "mismatch_index_sha256_le_i32": hashlib.sha256(mismatch.tobytes()).hexdigest(),
        "elapsed_seconds": round(time.time()-started,3),
        "_arrays": (A,D,Q,n_init,mismatch,clock_bad,final_len),
    }

def main():
    started = time.time()
    centres = {"odd_C_000":[0,0,0], "even_C_88":[8,8]}
    census = {}
    for centre_name, center in centres.items():
        c3, c4 = run_census(3,center), run_census(4,center)
        clean3 = {k:v for k,v in c3.items() if k != "_arrays"}
        clean4 = {k:v for k,v in c4.items() if k != "_arrays"}
        offsets = collections.Counter()
        for cell in (c3,c4):
            offsets.update({int(k):int(v) for k,v in cell["first_mismatch_W_offset_histogram"].items()})
        wrong_clock = c3["wrong_clock"] + c4["wrong_clock"]
        root_bad = c3["root_B_mismatches"] + c4["root_B_mismatches"]
        survivors = c3["no_W_prefix_mismatch"] + c4["no_W_prefix_mismatch"]
        combined = {
            "enumerated": c3["enumerated"]+c4["enumerated"],
            "expected_enumeration": 19**3+19**4,
            "wrong_clock": wrong_clock, "root_B_mismatches": root_bad,
            "W9_prefix_survivors": survivors,
            "first_mismatch_W_offset_histogram": {str(k):int(v) for k,v in sorted(offsets.items())},
            "first_mismatch_W_offset_min": min(offsets),
            "first_mismatch_W_offset_max": max(offsets),
            "all_mismatches_inside_W9": root_bad==0 and survivors==0 and c3["mismatch_after_W_prefix"]==0 and c4["mismatch_after_W_prefix"]==0,
            "clock_is_g_repeated_10": wrong_clock==0,
        }
        census[centre_name] = {"centre":center,"length3":clean3,"length4":clean4,"combined":combined}

    controls = []
    for q in (Q_REF,20,40,80,160):
        k = K_REF if q==Q_REF else 5*q
        for center in centres.values():
            for jlen in (3,4):
                for J in SAMPLES[jlen]:
                    controls.append(bigint_control(q,k,J,center))
    output = {
        "label":"COMPUTED independent audit; not an all-time decimal Lychrel proof",
        "template":{"B":B,"W":W,"U":U,"centres_checked":centres,"q_reference":Q_REF,"k_reference":K_REF,
                    "pairword":"P=H ++ C ++ reverse(H), H=B ++ W^q ++ J ++ U^k",
                    "coefficient_order":"least-significant first"},
        "census":census,
        "bigint_controls":{"count":len(controls),"passed":all(c["clock_exact"] and c["full_step_pairword_bigint_equal"] for c in controls),
            "q_values":[14,20,40,80,160],"k_rule":"k=100 at q=14; k=5q at q=20,40,80,160",
            "centres":centres,"steps_each":STEPS,
            "all_clock_exact":all(c["clock_exact"] for c in controls),
            "all_pairword_states_equal":all(c["full_step_pairword_bigint_equal"] for c in controls),
            "cases":controls},
        "elapsed_total_seconds":round(time.time()-started,3),
    }
    print(json.dumps(output,indent=2,sort_keys=True))

if __name__ == "__main__":
    main()
