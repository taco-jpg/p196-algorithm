#!/usr/bin/env python3
"""Emit exact short-boundary kernel checks; generation is not verification."""
from pathlib import Path

here = Path(__file__).resolve().parent
header = ('namespace SevenColumn.Certificate739\nopen Certificate ShortBoundary\n'
          'set_option maxRecDepth 100000\nset_option maxHeartbeats 100000000\n')
for a in range(18):
    text = 'import Rank739\nimport ShortChecksBase\n' + header
    text += f'theorem shortAt{a:02d} : ShortAt ranks {a} := by decide +kernel\n'
    text += f'#print axioms shortAt{a:02d}\nend SevenColumn.Certificate739\n'
    (here / f'Short739_{a:02d}.lean').write_text(text)
text = ''.join(f'import Short739_{a:02d}\n' for a in range(18)) + header
text += ('theorem shortOne : ∀ a : Fin 9, lookup ranks '
         '(nextWord [2*(a.val+1)]) = none := by decide +kernel\n')
text += 'theorem shortRest : ∀ a, a < 18 → ShortAt ranks a := by\n  intro a ha\n'
text += '  have cases : ' + ' ∨ '.join(f'a = {a}' for a in range(18)) + ' := by omega\n'
text += '  rcases cases with ' + ' | '.join('rfl' for _ in range(18)) + '\n'
for a in range(18):
    text += f'  · exact shortAt{a:02d}\n'
text += ('theorem shortChecked : ∀ s ∈ shortWords, lookup ranks (nextWord s) = none :=\n'
         '  shortChecked_of_cases ranks shortOne shortRest\n'
         '#print axioms shortOne\n#print axioms shortChecked\n'
         'end SevenColumn.Certificate739\n')
(here / 'Short739.lean').write_text(text)
