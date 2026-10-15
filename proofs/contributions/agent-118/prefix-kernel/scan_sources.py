#!/usr/bin/env python3
"""Apply check.py's source scans (FORBIDDEN and KERNEL_BYPASS, comments and strings masked) to a directory."""
import hashlib, json, sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import check  # noqa: E402  (module only defines functions and constants at import time)
root = Path(sys.argv[1])
rows = {}
for f in sorted(root.glob('*.lean')):
    code = check.code_only(f.read_text())
    rows[f.name] = {'sha256': hashlib.sha256(f.read_bytes()).hexdigest(),
                    'forbidden': check.FORBIDDEN.findall(code), 'kernel_bypass': check.KERNEL_BYPASS.findall(code)}
bad = {k: v for k, v in rows.items() if v['forbidden'] or v['kernel_bypass']}
print(json.dumps({'files': len(rows), 'flagged': bad}, indent=1))
json.dump({'scanned_dir': str(root), 'files': rows, 'flagged': bad}, open(sys.argv[2], 'w'), indent=1)
sys.exit(1 if bad else 0)
