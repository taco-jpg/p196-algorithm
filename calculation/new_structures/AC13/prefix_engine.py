"""Independent Python implementation of the executable carry-prefix proof."""
from carry_prefix import B,W,certified_prefix,common_prefix
def cone_trace(J,U,q=14,known_u_copies=50,steps=120):
    initial=tuple(B+W*q+list(J)+list(U)*known_u_copies)
    result,ambiguous=certified_prefix(initial,steps)
    target=tuple(B+W*q)
    ix=common_prefix(result,target)
    return len(initial),len(result),ix,ambiguous,result
