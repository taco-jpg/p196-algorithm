"""Extract Lean-verified prefix entry lists (pre, bound) from Agent124FourDigit,
prefix-k45 branch files if present, and Agent124PrefixFiveSix; print per-file
width and entries.  Used to cross-check the forward/core computation:
every backward-certified prefix at width k must be NOT hit by F_k."""
import re, glob, sys, json
pat = re.compile(r'\(\[([0-9, ]+)\],\s*(\d+)\)')
out = {}
for f in sorted(glob.glob(sys.argv[1] + '/**/*.lean', recursive=True)):
    txt = open(f).read()
    ents = [([int(x) for x in a.split(',')], int(b)) for a, b in pat.findall(txt)]
    if ents:
        # width: look for 'entryOK <k>' or 'no_196_of_entries <k>'
        m = re.findall(r'(?:entryOK|no_196_of_entries|ancestry_of_entries)\s+(\d+)', txt)
        out[f] = {'width_hint': sorted(set(m)), 'entries': ents}
json.dump(out, open(sys.argv[2], 'w'))
for f, v in out.items():
    print(f.split('lean/P196/')[-1], 'n=', len(v['entries']), 'widths', v['width_hint'],
          'lens', sorted(set(len(e[0]) for e in v['entries'])), 'maxbound', max(e[1] for e in v['entries']))
