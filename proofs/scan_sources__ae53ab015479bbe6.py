#!/usr/bin/env python3
"""Secondary source-token scan. Kernel transitive axiom reports remain authoritative."""
from __future__ import annotations
import argparse,hashlib,json,re
from pathlib import Path

def active_text(text: str) -> str:
    out=[]; i=0; depth=0; quoted=False
    while i<len(text):
        if depth:
            if text.startswith('/-',i): depth+=1; i+=2
            elif text.startswith('-/',i): depth-=1; i+=2
            else: out.append('\n' if text[i]=='\n' else ' '); i+=1
        elif quoted:
            if text[i]=='\\': i+=2
            elif text[i]=='"': quoted=False; i+=1
            else: out.append('\n' if text[i]=='\n' else ' '); i+=1
        elif text.startswith('/-',i): depth=1; i+=2
        elif text.startswith('--',i):
            j=text.find('\n',i); i=len(text) if j<0 else j
        elif text[i]=='"': quoted=True; i+=1
        else: out.append(text[i]); i+=1
    if depth or quoted: raise RuntimeError('Unterminated comment or string')
    return ''.join(out)

def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('--repo',type=Path,required=True)
    args=ap.parse_args(); here=Path(__file__).parent
    pins=json.loads((here/'source-pins.json').read_text())['sources']
    paths=[args.repo/r['path'] for r in pins]+[here/'Agent121ScopeRegression.lean']
    rows=[]
    for p in paths:
        hits=re.findall(r'\b(sorry|admit|sorryAx|native_decide|ofReduceBool|axiom|unsafe|implemented_by|extern)\b',active_text(p.read_text()))
        rows.append({'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'active_forbidden_tokens':hits})
    ok=not any(r['active_forbidden_tokens'] for r in rows)
    print(json.dumps({'agent':121,'status':'PASS' if ok else 'FAIL',
        'scope':'seven upstream modules and one new review module; source scan is secondary to transitive axiom audits',
        'files':rows},indent=2))
    if not ok: raise SystemExit(1)
if __name__=='__main__': main()
