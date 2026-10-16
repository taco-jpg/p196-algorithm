# Author report: carry-free residue parameters

## Scope

Author: Agent #14 / coverage. This is an author report, not an independent review.
Guarded task: agent14-carryfree-residue-saturation-20261016.
Coordination commit: bdfdc25c3158b81e6c6e40109886cdf80c744e57.
Task blob: 8912d279695f7f298e0b1bcde5e612660e13ae5f.

Original source: Theorem 3 of proofs/research/astra_spectral_carry_quotient.md
at source-map commit 2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5,
blob eac5b8f61385a615d9cc3e7796a4d698c66b716b.

Intended repository file: proofs/Agent14CarryfreeResidues.lean.
The overlay reported zero available bytes, so the explicitly authorized
working source is
/dev/shm/agent14-carryfree-residues-d43e317f00d9/Agent14CarryfreeResidues.lean.

Frozen source SHA256:
7785adc325f7ae100cfcde21238f27d06a558c23d74a3fa03464ea356867ece6.

## Exact exported scope and proof

The module imports Std only, uses namespace Agent14.Carryfree, and exports
four explicit theorems:

- residue_parameters: for s < 9 and r < 11, produces 1 <= u <= 10 and b <= 9
  satisfying (u+b)%9=s and (u+10*b)%11=r.
- even_residue_parameters: for s < 9, produces 1 <= a <= 9 and a%9=s.
- ten_pow_mod99: the original AstraModular.ten_pow_mod99 parity formula,
  reproduced with explicit attribution to retain a core-independent helper.
- odd_three_digit_mod99: for odd L >= 5 and arbitrary natural a,b,c, the
  residue of a*10^(L-1)+b*10^(L-2)+c*10^(L-3) is (a+10*b+c)%99.
  This helper does not add digit bounds.

The odd witness is constructive: set t=(55*s+45*r)%99, replace a zero
representative by 99 to obtain x, and use u=(x-1)%10+1 and b=(x-1)/10.
Division with remainder gives u+10*b=x and the required bounds and
congruences. No enumeration of 99 pairs occurs. The even witness is 9
when s=0 and s otherwise.

This file does not assert canonicality, carry vanishing, palindromicity,
a quotient-ring presentation, or an orbit result. Root authors the actual
digit construction and saturation assembly. Polynomial evaluations belong
to the separately authorized coordinates module.

## Actual execution and retention

Runtime:
/workspace/scratch/f8aedc6d7adf/runtime-agent6/lean-4.19.0-linux/bin/lean.

Every compiler call used --trust=0 -j1 -DElab.async=false. Each retained
command.json, compiler.log, and result.json records exact argv, cwd, source
and executable hashes, timestamps, actual exit code, and produced object hash.

| Run | Actual exit | Result |
|---|---:|---|
| attempt-001 | 1 | Recursive modular simplification in the optional positional helper reached the recursion limit. Original source and complete failure log remain retained. |
| attempt-002 | 0 | All four declarations compiled after using separate product congruences. |
| audit-001 | 0 | Imported the successful object, checked all four exact theorem types, and audited all four axiom sets with exact name coverage. |

Attempt-001 source SHA256:
a9017a67a401ad4b84324184b53d6e52706a295025d5bdb9dbd2734b0c3779ec.

The failed elaboration emitted a provisional sorryAx line in its raw log;
that result was not accepted or hidden. The successful module and audit have
no such dependency. Separate functions-level setup parser errors are recorded
in setup-functions-errors.txt; neither executed a nested command.

Successful object SHA256:
5f3a561a736c348a3fb68a1b20369a3c6b1e7614d889baa14a0c7517cd194a0f.

## Author axiom audit and limits

The audit ascribed each exact intended type to its imported theorem.
Its parser matched every complete axiom-output line to the four expected
fully qualified names.

- residue_parameters: propext, Classical.choice, Quot.sound.
- Each other theorem: propext, Quot.sound.

No new mathematical axioms or compiler-trusted proof shortcut was introduced.
This author audit does not replace genuine nonauthor source-semantic review
or an independent fresh full-closure build.

All source versions, failures, logs, actual commands/statuses, audit source,
audit parser, and objects remain under
/dev/shm/agent14-carryfree-residues-d43e317f00d9/development/residues/.

Intended evidence destination:
proofs/contributions/agent-14/carryfree-residue-saturation-20261016/development/residues/.

Root should publish the exact source and retained evidence with this relocation
mapping. No Git writes or remote publication were performed by this subagent.
