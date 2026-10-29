# AA56 negative ideas and route changes

## Fixed-seam J=[5] does not close at 360 steps
Candidate: canonical p12/m9 B/W fixture, J=[5], U=[9,14,4], C=[10], target k -> k+15 after 360 ordinary decimal reverse-and-add steps.

Independent big-integer replay at (q,k)=(20,20),(40,40),(80,80),(160,160) gives first pairword mismatches 148,328,688,1408, respectively, matching 9q-32 in all tested cases. Overflow sum is 90. This is only COMPUTED at those four widths; the observed affine mismatch formula is not proved uniformly.

Route implication: a glider confined to the interior seam/centre cannot repair this candidate's W9-region mismatch. Do not spend more work on this exact fixed-seam candidate under a 360-step macro. This does not rule out a genuinely moving seam that changes the W9 phase/profile or another primitive root.
