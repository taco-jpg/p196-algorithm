# Historical execution-order guard failure

The first attempted audit launch occurred while the seven-module compile process
was still finishing. Its guard required all seven module receipts and stopped
with exit 1 before invoking Lean. The observed stderr was:

```
Traceback (most recent call last):
  File "<stdin>", line 7, in <module>
AssertionError
```

A following consistency check correctly detected that the old 75-theorem log did
not yet match the new 98-theorem audit source; it exited 1. Neither failed guard
was recorded as a mathematical compilation failure or as an audit success.
After the compile process actually exited 0, the audit was launched again.
