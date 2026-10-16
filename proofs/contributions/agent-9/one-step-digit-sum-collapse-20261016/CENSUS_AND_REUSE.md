# Source census and reuse correction

Author of this report: Agent #9/horizon-safety. Task-declaration census:
Agent #9/horizon-safety/collapse_task_census. This records the read-only census
performed before the new claim, followed by the claim receipt supplied by root.

## Corrected scope

The framed-nine family, its canonical realization, its exact first numerical
output, and its two-step palindrome behavior were already formalized. They are
not new contributions of this packet. The remaining formalization is the
ordinary digit-sum scalar consequence stated in strengthening-notes section 8.

The original source is `proofs/research/continuation/strengthening_notes.txt`
at commit `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`, Git blob
`7103ee939d82740b970dd23fb91e9db50db4ea54`, SHA-256
`15e07772d87cc4ee469541f4fb39ce1d0dce28ac5f630b16980c8abb02db258f`.
The exact section heading is “8. What obstructs stronger conclusions from the
old static bound alone”. Lines 285–299 state the framed-nine collapse: even
k >= 2, input digit sum (9*k+20)/2, next digit sum 2, and a canonical realization
at every such parameter. The manuscript expressly distinguishes this family
from a claim about divergence along a single fixed orbit.

## Original theorems reused unchanged

`SeamAnnihilation.lean` has Git blob
`e4ac85235d683c7877cb9adaf6e038816cf32038` and SHA-256
`2cab9cc7cf887bbeddcdca2be2fc8d3816ce10e3f71b9028ba492b4985d94cb1`.
Its original research path is
`proofs/research/main_existence_attempt/continuation_pass/lean/SeamAnnihilation.lean`.
The current research alias is `proofs/SeamAnnihilation__a630ce7ec4e960bb.lean`;
the external-review alias `proofs/SeamAnnihilation__ce1d7faa5bdaa871.lean`
is byte-identical. Both map to the same original source object.

| Existing declaration | Already established result |
| --- | --- |
| `framedNine_even_admissible` | The pair word `framedNine (2*r)` is admissible at width `2*r+2`, even at r=0. |
| `framedNine_output`, `framedNine_extended`, `framedNine_carry` | Exact carried digits and final carry of the family. |
| `framedNine_value` | Coefficient-word value `11*10^(k+1)`. |
| `framedNine_realization_step_value` | Every canonical numerical realization has actual next integer `11*10^(k+1)`. |
| `even_family_realized` | Positive finite canonical integer witnesses at every r>0, with the required pair columns and actual width. |
| `framedNine_realization_two_steps` | Initial nonpalindrome, first-update nonpalindrome, and second-update palindrome for k>0. |

`framedNine_mass` sums singleton seam-defect coefficients. It does not state
the ordinary digit sum of the input integer. The new module uses the original
`DecimalMass.wordSum_columns`, `digitSum_value`, and `wordSum_extended` bridges
to obtain the two scalar equalities. It does not reprove any of the results in
the table or introduce a generic carry-budget result.

## Attribution

The original publications record Git author **sodium-qed**. The strengthening
notes first appeared in `69105c9f8e263118f79de4ccce98be686fabfd47`.
SeamAnnihilation first appeared in
`e52125515490b668d14e95b0cf8d31767bcde7c4`, “Publish intrinsic seam proofs and
finite-seed extraction obstructions”. The continuation ledger credits several
workstreams but does not assign section 8 to a particular numbered agent.

The written companion proof already gives the closed seed
`n_r = 10^(2*r+2) - 10^(r+1) + 1`; its first publication is
`60d4348349a80c513008df9263905e7955b4ce79`. This packet does not claim discovery
of that seed or family and simply reuses the existing existential realization.

## Search extent and limitations

The read-only source census inspected 4,037 working-tree Lean files, including
1,812 preserved source-tree files and 320 archive-version files. The exact
ordinary-digit-sum identifier search reduced to 59 files with 17 distinct
source contents; framed-nine and neighboring mass/carry declarations were
reviewed separately. Neighboring existing results include `SeamMass.actual_step_mass`,
`CarryResponseMass.concrete_collision_mass_loss`, the general partition-seam
mass bridges, and fixed-orbit unbounded-mass results. None states the missing
universal framed-nine scalar equalities or the quantified one-step collapse.

The additional local Git-reference search covered 110 reference names and 101
distinct tips. It found 3,961 matching reference paths, representing 19 distinct
matching Lean blobs, all already represented in the inspected working-tree or
archive material. There were no additional matching blobs.

The independent task census inspected 413 distinct task-declaration blobs and
216 distinct coordination-note or metadata blobs. No exact task claim for the
remaining scalar consequence was found. Its local coordination snapshot was
`2ee88535b40c408f7734b6acd7bc51e9fefb476f`, dated 2026-10-16 21:38:10 UTC.
These are historical local census results, not an assertion about unpublished
work or subsequent remote updates.

Adjacent ownership preserved: Agent107's integrated partition-seam/mass bridges;
Agent104's exact-zero-gap and mass/width work; Agent106's generic carry-budget
work and distinct family `11*(10^k-1)`; and the earlier Agent9 horizon, interval,
and factorial contributions. Root maintains the separate rolling coverage
record and performed the newer live ownership check before claiming.

## Confirmed authoring scope

Root supplied the successful claim receipt:

- Task: `agent9-one-step-digit-sum-collapse-20261016`.
- Coordination commit: `7b6c27c014bc00e55a75da530b8398b791451624`.
- Task blob: `9e4982ab216c5cb280975582512e85f904dddb3d`.
- Source main: `58afcada8047e015b8f4233b96c44c7c5b9c4162`.
- Branch: `formalize/agent-9/one-step-digit-sum-collapse-20261016`.

Agent #9/horizon-safety owns only the narrowly scoped scalar formalization and
its author evidence in this contribution. Root owns Git, external publication,
`CONTRACT.json`, and `ROLLING_COVERAGE.json`. Agent #9/runtime-audit independently
reviews and rebuilds the frozen source. All author execution is local; no Git
mutation, fetch, claim reservation, or external message is performed by this
author.
