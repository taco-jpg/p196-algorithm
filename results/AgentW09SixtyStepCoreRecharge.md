# W09 60-step delayed core recharge
- **COMPUTED:** an explicit decimal N_k=A++4^(2k)++B with k=22000 and 44120 digits, A=116306872642729707615958232967841904794691524521087889888578, B=864887887780025415096487409047668232759515706816235167603511.
- Two independent actual-integer engines verify all 20000 reverse-and-add steps with zero palindromes, an exact nonempty six-phase 8,16,14,10,2,4 central pairword at all 20001 stages.
- Width w0=44000, w36=44004, w60=44006, w20000=30891; final 52329 digits, LSD-first FNV64 262683335058ed77.
- **PAPER PROOF:** universal centre-insertion lemma from AgentW09TransientCoreReplenishment gives for every k>=80 a 60-step sequence with k-independent caps and central width 2k+beta_t, beta60=+6; finite caps and odd safety guards independently checked using genuine Python big integers for k=80,81,100,150.
- Non-recurrent: cap grows from 60 to 69 cells over 60 steps, so positive temporary credit is NOT an infinite certificate.
- Source/controls/expected data: calculation/new_structures/agent-W09/renew60/ ; reproduce with sh calculation/new_structures/agent-W09/renew60/reproduce.sh.
- Full scope: reports/AgentW09SixtyStepCoreRecharge.md. **UNDECIDED** infinite base-10 Lychrel or Lean verification.
