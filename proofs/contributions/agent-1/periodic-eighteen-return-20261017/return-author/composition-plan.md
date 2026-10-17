# Root composition obligations, not proof evidence

Fix k(t)=quotientPathExponent B H w (2*N+3) t and C(t)=quotientClockSum B H w t. Initial k0 is definitionally 2*N+3; finite guard holds for every t<=N by the existing lower bound. The natural recurrence is definitional. Clock's actual-carry step supplies the exact C recurrence without inventing another sum.

Assume a full return solely inside the contradiction proof. Existing ReturnClock yields G>0, C(N)=8*G and signed delta=G. Guarded accounting yields k(N)=2*N+3+G; use omega on the Int/Nat casts only after obtaining that accounting identity.

Band must provide a0,b0 with maximal run over initial E word, a0<=|B0| and |B0|+4*(2*N+3)<=b0. Substitute hw only at the supplied initial word, not through every intermediate state. Choose I=|B0|+N; arithmetic gives a0+N<=I and I+N<b0. Track then yields the maximal run at N, its anchor inequalities and a0+C(N)<=aN.

Rewrite only the final word using the three literal endpoint equalities. Since k(N)>=k0, I lies in both left E bands. Band's static-left-boundary theorem compares this final run to the initial run. Equality aN=a0 and C(N)=8*G>0 contradict the tracking advance. This proof requires no safety, no phase catalogue, no all-time trajectory and no statement about other ancestries.

All displayed implications remain WIP until the final source compiles with its actual dependencies and passes the recorded audits.
