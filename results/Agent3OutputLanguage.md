# Agent3OutputLanguage

**PAPER PROOF (finite-state certificate).** In the base-10 rec2 physical pairword bulk, the no-overflow (`g=0`) map realizes **every admissible finite parity/ascending-carry/descending-carry block**, at arbitrary block length, as the image of a physical cyclic source of period divisible by 48.
The 5776-state output transducer has a 3116-state recurrent SCC and an explicit 14924-pair forward simulation covering all 76 target states.
In contrast, the overflow (`g=1`) image forbids the 11-symbol physical block `(7,1)^5,7`, with labels `P%2+2a+4d`; the ten-symbol prefix is realized by an ordinary 48-periodic source. The forbidden target is itself physical: `P=(1,11)^24`.
**Scope:** arbitrary spatial bulk width and exact physical carries, not finite rooted centre return, boundary phases, all-time decimal orbit, or 196.
Reproduce: `sh calculation/decimal_frontier/lattice_kinks/agent3_output_language/run_checks.sh`.
Standalone primary, independent schoolbook checker, pinned 48-cell witnesses and rec2 controls: `calculation/decimal_frontier/lattice_kinks/agent3_output_language/`.
Proof: `reports/Agent3OutputLanguage.md`. No Lean or repository `verify.py --changed` success claimed.
