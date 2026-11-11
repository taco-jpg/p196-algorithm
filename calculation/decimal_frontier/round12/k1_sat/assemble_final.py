#!/usr/bin/env python3
"""r12d assemble_final.py -- FINAL.md = FINAL_head.md + FINAL_mid.md (tables from final_tables.py) + FINAL_tail.md"""
import os, subprocess, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
out = subprocess.run([sys.executable, 'final_tables.py'], capture_output=True, text=True).stdout
sec = {}; cur = None
for line in out.split('\n'):
    if line.startswith('### '):
        cur = line[4:].strip(); sec[cur] = []
    elif cur is not None:
        sec[cur].append(line)
def get(prefix):
    for k, v in sec.items():
        if k.startswith(prefix): return '\n'.join(v).strip()
    return '(none)'
mid = open('FINAL_mid.md').read()
mid = mid.replace('SCOPE_TABLE', open('scope_table.md').read().strip() if os.path.exists('scope_table.md') else '(see 4.2)')
mid = mid.replace('SAT_TABLE', '**SAT (tsat exact encoding):**\n\n' + get('Fixed centres, SAT'))
mid = mid.replace('ENUM_TABLE', '**Exhaustive enumeration (cen3):**\n\n' + get('Fixed centres, exhaustive'))
mid = mid.replace('WALL_TABLE', get('Walls'))
mid = mid.replace('BAND_TABLE', get('Seams'))
mid = mid.replace('SURV_TABLE', get('Confined'))
txt = open('FINAL_head.md').read().rstrip() + '\n\n' + mid.rstrip() + '\n\n' + open('FINAL_tail.md').read()
open('FINAL.md', 'w').write(txt)
print('FINAL.md', len(txt.split('\n')), 'lines')
