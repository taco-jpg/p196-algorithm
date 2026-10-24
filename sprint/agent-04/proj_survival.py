#!/usr/bin/env python3
"""|pi(I_{k+1})| versus |I_k|, where pi drops the innermost column (code mod 19^k).
By Agent117.forwardAdmitted_project, pi maps cycles to closed walks, so pi(I_{k+1}) is a subset of I_k.
Also: how many of the 19 one-column extensions of a word of I_k lie in I_{k+1} (histogram)."""
import sys
import numpy as np
D = sys.argv[1]
def load(k):
    b = np.fromfile(f"{D}/inf_{k}.bits", dtype=np.uint64)
    bits = np.unpackbits(b.view(np.uint8), bitorder="little")[: 19 ** k]
    return bits.astype(bool)
prev = load(4)
for k in range(4, 7):
    nxt = load(k + 1)
    codes = np.nonzero(nxt)[0]
    proj = np.unique(codes % (19 ** k))
    inside = prev[proj].all()
    ext = np.bincount(codes % (19 ** k), minlength=19 ** k)[prev]
    hist = np.bincount(ext, minlength=20)
    print(f"k={k}->{k+1}: |I_k|={prev.sum()} |I_k+1|={nxt.sum()} |pi(I_k+1)|={len(proj)} "
          f"subset={inside} surviving fraction={len(proj)/prev.sum():.4f} mean extensions={ext.mean():.3f}")
    print("   histogram of #extensions (0..19):", hist.tolist())
    prev = nxt
