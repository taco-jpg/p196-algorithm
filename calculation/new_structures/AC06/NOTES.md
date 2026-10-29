# AC06 notes and discarded route

Prior AB06 had 400/68,590 sampled length-seven odd centres in its #476 CELL line. T12 provides the centre/J separation and cuts; R30 independently specifies the pairword-to-decimal correspondence. A requested window of radius 122+|C|+30 is NOT automatically J-independent since it can touch the J-side cone. Radius 5 is protected by the 26-column T12 gap for k>=100. We therefore tested both windows, without strict-W9 intermediate pruning.

Exhaustive six cells at lengths 7,8: 596,733 cases; zero radius-five matches, all gamma=(1000)^30. Ordinary-bigint Python controls: 90 cases at five widths; separate 60 varied-J controls. For lengths 9..14, plain enumeration up to 19^7 per U is prohibitive: seek 120-layer two-ended carry MDD/SAT with actual gamma shifts and non-strict endpoint logic. Those widths remain open.
