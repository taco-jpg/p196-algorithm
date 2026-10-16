# Author report: literal carry-free polynomial coordinates

## Source and ownership

Author: Agent #14 / coverage. This is an author report, not independent review.
Root explicitly authorized this second file under the guarded task
agent14-carryfree-residue-saturation-20261016 after the residue interfaces were fixed.

Original mathematical source: Theorem 3 and the fixed-width coordinate definitions
of proofs/research/astra_spectral_carry_quotient.md, source-map commit
2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5, Git blob
eac5b8f61385a615d9cc3e7796a4d698c66b716b.

Intended repository file: proofs/Agent14CarryfreeCoordinates.lean.
Actual authorized working file:
/dev/shm/agent14-carryfree-residues-d43e317f00d9/Agent14CarryfreeCoordinates.lean.

Frozen source SHA256:
5c2b5b72f14b8f002719fa77b54b63aef1a2fa644dd379bdb94dec4b3dbfa519.

The module imports Agent14CarryfreeDigits and uses namespace Agent14.Carryfree.
Root authored the sparse digit definitions and their exact coefficient formulas;
this subagent did not modify those sources.

## Literal definition and exact exported contracts

coefficientEval q L x is the literal finite Int sum, defined by
E(q,0,x)=0 and E(q,L+1,x)=E(q,L,x)+(q L : Int)*x^L.

The module exports one definition and nine theorems:

| Declaration | Exact mathematical content |
|---|---|
| coefficientEval | Literal coefficient evaluation, with Int arithmetic. |
| eval_one | E(q,L,1) = (DecimalMass.wordSum q L : Int), for all words and widths. |
| coefficientEval_congr | Coefficient equality inside the width preserves evaluation. |
| coefficientEval_add | Pointwise natural coefficient addition becomes integer evaluation addition. |
| coefficientEval_spike | A spike contributes a*x^k if k<L, and zero otherwise. |
| neg_one_pow_parity | (-1)^k is 1 for even k and -1 for odd k. |
| columns_eval_one | E(columnSum d L,L,1)=2*(wordSum d L : Int), without digit bounds. |
| canonical_columns_eval_one | For Canonical n d L, E(columnSum d L,L,1)=2*(digitSum n : Int). |
| odd_columns_eval_neg_one | For odd L>=5, E(columnSum(threeDigits a b c L)L,L,-1)=2*((a:Int)-(b:Int)+(c:Int)). |
| even_columns_eval_neg_one | For even L>=2, E(columnSum(oneDigit a L)L,L,-1)=0. |

The ordinary digit-sum bridge reuses the original wordSum_columns and
digitSum_value theorems. The alternating statements reuse root's exact
threeDigits_column_formula and oneDigit_column_formula. Thus the statement
concerns actual mirrored input digits, not an independently postulated
coefficient word.

The width-five central coincidence is preserved: the two c spikes occupy the
same index and both remain in the finite evaluation. No distinct-position
hypothesis was introduced in the evaluation lemmas. The proof subtracts b
over Int; it does not use truncated natural subtraction.

The even theorem concerns Q(-1)=0. It does not say the original input is
zero modulo eleven. The earlier scout correction is therefore part of the
actual checked proposition.

These finite evaluation bridges do not formalize the quotient-ring
isomorphism, carry-defect ideal, universal property, or an orbit conclusion.

## Exact dependency copies

Root's files were copied into this author's isolated dependency directory.
Every copied source and object was checked byte-for-byte by SHA256, with
source/copy paths and sizes recorded in dependency-copy.json.

- LychrelDigitSums source:
  ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57.
- LychrelDigitSums object:
  69dc2ddcd2c17246e2c60ed61195436cc9aefff662f0c49eb769f94baec93978.
- Root's Agent14CarryfreeDigits source:
  ae394c8a19e6fc497c1cf83fdf77943abd3f0b8fd681e59006bc8f7524f4ece9.
- Root's Agent14CarryfreeDigits object:
  d175714ccc1637dd4f98791b82dc5f62706d6d3c07c384a8e0f4116ea8c67cd1.

Copied dependency directory:
/dev/shm/agent14-carryfree-residues-d43e317f00d9/dependencies/coordinates/.

This author build reused these already compiled dependencies. It is not an
independent fresh full-closure rebuild; root coordinates that acceptance gate.

## Actual attempts and audit

Every actual compiler invocation used the existing official runtime
/workspace/scratch/f8aedc6d7adf/runtime-agent6/lean-4.19.0-linux/bin/lean
with --trust=0 -j1 -DElab.async=false.

| Run | Actual exit | Result |
|---|---:|---|
| attempt-001 | 1 | The final even-coordinate proof left the elementary integer goal a+(-a)=0. Complete failed source and log are preserved. |
| attempt-002 | 0 | Adding the explicit arithmetic closure completed all ten declarations. |
| audit-001 | 0 | A separate import file checked all ten exact types and printed all ten axiom dependencies; the parser verified exact name coverage. |

Attempt-001 source SHA256:
3379b96d97a0706e8dd98d310dbf0a94b876a8e0426d9bedc55216c1b0170a95.

The provisional sorryAx emitted for the failed elaboration remains visible
in that failure log. The failed declaration was not accepted. The successful
module and successful import audit have no sorryAx dependency.

Successful object SHA256:
c6f3253ffa590a65764bee22e536a3a9ee4ad58ed58a033aaaad2992b0abd5eb.

The definition coefficientEval has no axioms. eval_one depends only on propext.
Each other theorem depends only on propext and Quot.sound. No Classical.choice,
new mathematical axiom, or compiler-trusted proof shortcut appears in this
module's audited logical dependencies.

The author audit compares the source inventory to ten explicit expected names,
ascribes each intended exact type to its imported declaration, and parses both
the nonempty and empty axiom-output formats. It is separate from implementation
compilation but is not a genuine nonauthor review.

## Evidence and transfer

Each attempt retains its immutable source, exact argv/cwd/environment,
executable/source/dependency hashes, actual stdout/stderr, timestamps, exit
status, and object hash. The audit retains its exact source, driver, raw log,
parsed axiom rows, and result.

Actual evidence directory:
/dev/shm/agent14-carryfree-residues-d43e317f00d9/development/coordinates/.

Intended evidence destination:
proofs/contributions/agent-14/carryfree-residue-saturation-20261016/development/coordinates/.

The full overlay necessitated the explicitly authorized shared-memory path.
No Git writes, remote publication, source edits outside this ownership, or
changes to root's dependency files were performed. Root should publish these
exact source/evidence bytes and the relocation mapping.
