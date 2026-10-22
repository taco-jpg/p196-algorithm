#!/usr/bin/env python3
"""Run a command, then print its wall time and peak RSS (children's ru_maxrss)."""
import resource
import subprocess
import sys
import time

t0 = time.time()
rc = subprocess.call(sys.argv[1:])
dt = time.time() - t0
ru = resource.getrusage(resource.RUSAGE_CHILDREN)
peak = ru.ru_maxrss * (1 if sys.platform == "darwin" else 1024)  # bytes
print(f"[measure] rc={rc} wall={dt:.1f}s user={ru.ru_utime:.1f}s peak_rss={peak / 2**20:.0f}MiB "
      f"cmd={' '.join(sys.argv[1:])}", file=sys.stderr)
sys.exit(rc)
