# AC01 attempted approaches

- Raw replay of all centre lengths 7..14: not feasible at 4,320,346,920 candidates without a stronger *sound* necessary-condition pruner; do not call it exhausted.
- Restricting to a strict-phase W9 recurrence: unsound for endpoint-only centre search because W9 may heal; deliberately avoided.
- A windowed carry-equality induction with full fallback is sound but does not itself prove a regenerative decimal cycle. Next work needs a centre-map constraint solver or a general obstruction, not random replay volume.
