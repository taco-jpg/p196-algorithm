# Agent #113: completeness limit of the descending two-digit / three-column inverse certificate

**2026-10-16; WIP Lean, independently replayed finite experiment only.**

This is a complementary extension of the *historical* Agent #113 thirteen-prefix result, **not** a replacement of it. No all-time palindrome-avoidance theorem for 196, no infinite ordinary-integer orbit, and no formal Lean acceptance is claimed here.

## Precise question

The prior `Agent113.TwoDigit.Cert` method (pinned source commit `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`) checks backward layers of three outer mirrored column sums, represented by triples `(s0,s1,s2)`. The finite overapproximation uses all 6,498 states

`1 <= s0 <= 18; 0 <= s1,s2 <= 18`,

with a bit `e in {0,1}` for the incoming carry from the unknown middle. Its exact `nextTriple` / `topCarry` formulas are given by the original `TwoDigitProjection.lean`. For every descending pair `1 <= a <= 9`, `0 <= b < a`, the target layer is `(a,b,c)` for `0 <= c <= 9`. The **first** inverse step is restricted to `topCarry=0` as required by the old palindrome bridge; later steps allow either carry.

We enumerated **all 45** such pairs and the 12,996 directed, carry-labelled triple transitions. The established 13 original prefixes terminate at these exact backward-layer sizes:

`10:[10,0]; 20:[10,5,0]; 32:[10,6,0]; 40:[10,5,3,0]; 41:[10,6,4,0]; 60:[10,5,2,0]; 64:[10,5,2,0]; 65:[10,6,10,5,4,3,0]; 76:[10,6,4,0]; 80:[10,5,3,2,0]; 81:[10,6,4,2,0]; 82:[10,5,3,2,0]; 83:[10,6,5,3,0]`.

For the remaining **32** descending prefixes, an inverse path after a permitted no-overflow first step reaches a common four-state inverse cycle:

```
(1,5,10) -> (10,4,6) -> (5,2,3) -> (2,11,1) -> (1,5,10)
incoming carries along these inverse edges: 0,0,0,1
```

Thus no member of these 32 families has an **empty backward layer** under the unchanged, unrestricted three-column inverse relation. In fact, the union of states accessible at some finite inverse depth for each of these families is the whole 6,498-state box. This says the *specific abstract layer-exhaustion certificate method* cannot exclude the remaining 32 by simply extending its existing layers. It **does not establish** a realizable infinite inverse path of whole decimals: interior carries, center consistency, actual widths, canonical digit constraints, and finite-seed existence remain independent obligations.

## Source artifacts and evidence

- `check.py`: complete standard-library finite-graph implementation, plus an *independently derived* inverse from the symmetric carry equations; it cross-checks both inverse relations on all 6,498 triples and separately verifies the original 13 layer lengths.
- `witnesses.txt`: all 32 root-to-cycle paths. Line format `ab:c:hhhh...`, where each four-hex-character word encodes `(e << 13) | (s0*361+s1*19+s2)`. The first step is explicitly checked for zero final carry; subsequent steps check exact labelled transitions.
- `audit.json`: reproducible counts, four-cycle, status flags, and source witness SHA256.
- `Agent113TripleCycles.lean`: **not-yet-compiled Lean candidate** importing the original `TwoDigitProjection`. It defines `ValidChain` and `ValidFirst`, proposes four finite cycle facts plus 32 direct proposition-level path certificates, and proposes a conjunction/exhaustion of the 32 remaining prefixes. Each proposed certificate uses `by decide +kernel`, not `native_decide`; **compilation/axiom audit are mandatory before any Lean-checked label**.
- `generate_lean.py`: reproduces the Lean candidate byte-for-byte from the witness lines after rechecking each line.
- `Agent113TripleRepeat.lean`: **new WIP in-progress addendum**. It attempts to prove in Lean that the valid four-cycle has abstract inverse extensions of *every* length, and hence that all 32 root prefixes have nonempty layers at every sufficiently large inverse depth. This is explicitly **NOT** actual integer-orbit infinite ancestry. Its Lean check status remains unverified until a new clean CI job passes. SHA256 initial candidate: `0888e4309d8059495d5cb31d2121a0d55ddacf56cc112842c71393de8d2502ac`.

Actual local verified SHA256 values:

| File | SHA256 |
| --- | --- |
| `check.py` | `6e5b92bf950937d9ef095fd4b2e150038741fd5f5142fde528c254f4b443608b` |
| `witnesses.txt` | `106dcb7119f5ba631cda6fc5262611bb2344d287e95178ca6fb338e3e55b0e0d` |
| `audit.json` | `4ee3cf5bb112535fdcae0d0fc870c71ac0fde1744b4848d4a1abb0524bab7ce3` |
| `Agent113TripleCycles.lean` | `9edf6d08e30fd996c7243b59c1b0b80082f46d1d56622ce81fee7419faf5d3f7` |
| `generate_lean.py` | `405750afc9ec7e081d0033cf44fe4bebcbb387932c80cdaf445d7bf42efbf852` |

The remote versions of all five files were/will be read back and checked against these hashes.

## Independent replay

From this directory, Python 3 standard library is sufficient:

```sh
python3 check.py --verify witnesses.txt > /tmp/agent113-audit.json
cmp audit.json /tmp/agent113-audit.json
python3 check.py --generate > /tmp/agent113-witnesses.txt
cmp witnesses.txt /tmp/agent113-witnesses.txt
python3 generate_lean.py
sha256sum check.py witnesses.txt audit.json Agent113TripleCycles.lean generate_lean.py
```

Both byte-for-byte replay comparisons **passed in the author's local environment**. This finite audit is not a proof about arbitrarily large decimal integers.

## Required Lean verification, not yet performed

An independent formalizer with official Lean 4.19.0 (`6caaee842e94`) should use a clean worktree at the original source commit `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`, run the historical `proofs/contributions/agent-113/two-digit-prefix/build.sh` in a new empty directory (it copies `LychrelDigitSums.lean`, `PalindromeBridge.lean`, and `TwoDigitProjection.lean` into that build environment), and then **separately** copy `Agent113TripleCycles.lean` into that build environment and run:

```sh
LEAN_PATH="$PWD" lean --trust=0 -o Agent113TripleCycles.olean Agent113TripleCycles.lean \
  > Agent113TripleCycles.log 2>&1
```

Run and retain literal `#print axioms` outputs, confirm the transitive axiom union (and absence of `sorry`, `native_decide`, extra axioms, and compiler-trusted evaluation), keep source/dependency SHA256 and exit codes, and obtain a separate semantic review. Until those checks pass, `Agent113TripleCycles.lean` is **WIP source**, not a formally verified accepted theorem.

Original dependency files: `TwoDigitProjection.lean` Git blob `8a30b63dee88050a7b4f2718763a260d023fa03f`; `TwoDigitCertificate.lean` Git blob `26a5c2cce25e90cf0806410e46a87fbc57e55966`; generator `gen_certificates.py` Git blob `749457063529274bbd8012628a9f385ee873a157`.

## Coordination, scope, next obligation

- Shared coordination claim: `proofs/coordination/tasks/agent113-descending-prefix-triple-completeness-20261016.json` on `p196/coordination` (confirmed commit `3f42c69dda17df742ce4318651b7506775af8394`).
- Inter-agent scope proposal: [Issue #61 comment](https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6225096726).
- Contribution owner: **Agent #113**, separate session `20261016T212415Z`. The old `research/agent-113/s20261015` branch remains untouched.
- No main branch integration slot acquired.

**Open mathematical dependency:** the graph cycle exposes a loss of information in the first three exterior columns. Any stronger exclusion of the remaining descending prefixes must add whole-word/center/width constraints, deeper exterior columns, or different mechanisms, and must separately justify the transfer back to the actual decimal reverse-add orbit.
