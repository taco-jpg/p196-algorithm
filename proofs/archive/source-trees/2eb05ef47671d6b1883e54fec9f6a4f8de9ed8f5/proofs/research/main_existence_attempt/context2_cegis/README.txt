CONTEXT-TWO CEGIS SEARCH
This is a search for a nonempty safe forward-invariant finite-word language,
not a finite numerical orbit search. A cap or timeout is UNKNOWN.

The language permits adjacent carry-tile features (previous,current), with
-1 as a beginning sentinel. There are 21,409 possible features. Exact
nonemptiness uses the 874-node graph consisting of the two anchored start
states and one node per ordinary carry tile. A reachable accepting path
can be made simple, so 10-bit increasing ranks suffice without imposing
any bound on the orbit length or on words admitted by the language.

For each SAT model, BFS extracts an actual canonical accepted word. The
search calls context_closure.safety and context_closure.image_features to
compute the solver-free least feature closure. A safe fixed point would
be a candidate requiring a separate independent all-length audit.

An unsafe result is greedily reduced to a smaller initial feature set.
A proposed clause is never learned merely from a solver claim. Instead a
separate generator produces an unsafe derivation:
  * Each newly added feature is witnessed by an actual finite accepted
    input word and the feature set of its numerical G-image.
  * The final admitted word reaches a decimal palindrome in two ordinary
    reverse-and-add operations.
A fresh verifier checks every word by actual integer reversal/addition.
It computes carry-tile IDs directly from the complete integer carry vector,
without reusing guessed transducer paths or the exact graph-closure engine.
Only after verification does the solver receive the unsafe-core clause.

Soundness of a clause is monotonicity: any closed feature set containing
its initial core must contain every concretely derived feature. It would
then admit the checked two-step palindrome witness and violate safety.
No clause is learned from an interrupted proof, graph cap, or unknown.

The main search has a 180-second search budget, excluding encoding setup
and final file output, and a 100,000-node graph cap. A real-time signal plus
SMT timeout bounds the search; the SMT library can return slightly after
its requested interrupt. The result records actual elapsed search time.

Run:
  python main_existence_attempt/context2_cegis/search.py --seconds 180 --cap 100000
Replay all retained concrete unsafe proofs without SMT search:
  python main_existence_attempt/context2_cegis/search.py --verify main_existence_attempt/context2_cegis/unsafe_derivations_180.json

Implementation checks completed before the 180-second run:
  input words corresponding to 196, 18887, 10, the single pair-sum 2,
  and folded word ((14,5,18),None). Numeric carry paths matched the archived
  history paths. All five unsafe derivations replayed successfully.

A candidate finite decimal witness would be T^2(realize(input word));
safety in this encoding checks that G(input word) is outside the exact
palindrome-predecessor language. No existence conclusion is drawn unless
such a candidate passes the further independent all-length audit.

REQUESTED RUN RESULT
The 180-second run returned UNKNOWN at 180.003426 seconds. It extracted
one SAT witness and learned one independently verified unsafe-core clause.
No graph cap occurred, and no safe fixed-point candidate was found.
The one learned clause excludes the starting terminal feature (-1,873),
which represents the single central pair-sum 4. There are no image rounds
in that proof: its realized integer 2 goes to 4 and then 8, a palindrome.
A fresh --verify replay checked the retained proof successfully.

The observed bottleneck was SMT solving after the first learned clause.
Nothing in this timeout excludes context-two invariant languages. An
alternative bounded-Int-rank encoding or always-false phase selection
has been identified but was not part of the requested 180-second run.
