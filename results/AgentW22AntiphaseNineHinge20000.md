# AgentW22AntiphaseNineHinge20000
- **COMPUTED:** valid decimal coefficient word 8^14000 9^8000 10^16000 9^8000 8^14000, realized as a 60,000-digit integer, survives 20,000 exact reverse-and-add steps without a palindrome.
- Two independent C++17 implementations: schoolbook decimal integer arithmetic versus full pairword normalization at EVERY step; GMP big-integer accumulator with independently coded decimal updates and exact equality checks every 100th step. Full final integer outputs agree.
- **Full pairword shape at every state 0..20,000:** ordered first-half six-clock bulk A, neutral 9 corridor, antipodal bulk B, with minimum surviving widths 654 / 1198 / 1344.
- Local **PAPER PROOF:** A=(8,16,14,10,2,4) and B=(10,2,4,8,16,14) have opposite carries at each phase, giving a pair coefficient 9 from the two mirrored normalized 9 cells; same-phase controls destroy the corridor immediately.
- Exact decimal length 60,000 -> 68,296; cumulative overflow 8,296; symmetric seam-defect gaps grow from 0 to 10,057.
- Final number SHA-256: 8e111023c78fad5fa2606faf67db5203e2d578964b1ba29b5046f93fa52ccafc.
- Reproduce: sh calculation/new_structures/agent-W22/reproduce.sh; code and compact data therein.
- Full discussion: reports/AgentW22AntiphaseNineHinge20000.md. **No** infinite base-10 orbit, Lean, finite certificate cycle, or 196 claim.
