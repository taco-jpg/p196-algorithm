#!/usr/bin/env python3
"""Run a command, then print its wall time and peak resident memory (stand-in for /usr/bin/time -v)."""
import resource
import subprocess
import sys
import time

t = time.time()
rc = subprocess.call(sys.argv[1:])
wall = time.time() - t
peak_kb = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss  # KiB on Linux, bytes on macOS
unit = "bytes" if sys.platform == "darwin" else "KiB"
print(f"[memtime] exit={rc} wall={wall:.1f}s peak_rss={peak_kb} {unit}", file=sys.stderr)
sys.exit(rc)
