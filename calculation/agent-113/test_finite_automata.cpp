#include "finite_automata.hpp"
#include <iostream>
#include <numeric>
#include <random>

using namespace a113fa;

static void require(bool condition, const char* message) {
  if (!condition) throw std::runtime_error(message);
}

// Independent bit-vector simulation; no toolkit transition/membership calls.
static bool word_oracle(const NFA& a, const std::vector<Label>& word) {
  std::vector<uint8_t> active(a.size(),0);
  for (State q : a.initial) active[q] = 1;
  for (Label symbol : word) {
    std::vector<uint8_t> next(a.size(),0);
    for (State q = 0; q < a.size(); ++q) if (active[q])
      for (const auto& e : a.edges[q]) if (e.label == symbol) next[e.to] = 1;
    active.swap(next);
  }
  for (State q = 0; q < a.size(); ++q) if (active[q] && a.final[q]) return true;
  return false;
}

static DFA renamed(const DFA& a, std::mt19937& rng) {
  std::vector<State> perm(a.size()); std::iota(perm.begin(),perm.end(),0);
  std::shuffle(perm.begin(),perm.end(),rng);
  DFA out; for (size_t q = 0; q < a.size(); ++q) out.add_state(false);
  out.initial = perm[a.initial];
  for (State q = 0; q < a.size(); ++q) {
    out.final[perm[q]] = a.final[q];
    for (const auto& e : a.edges[q]) out.edges[perm[q]].push_back({e.label,perm[e.to]});
    std::shuffle(out.edges[perm[q]].begin(),out.edges[perm[q]].end(),rng);
  }
  return out;
}

static void basic_cases() {
  Budget budget;
  NFA plus;
  plus.add_state(); plus.add_state(); plus.add_state(true);
  plus.add_initial(0); plus.add_edge(0,17,1); plus.add_edge(1,29,2); plus.add_edge(2,17,1);
  DFA d = minimize(determinize(trim(plus,budget),budget),budget);
  require(d.size() == 3,"(AB)+ should have three partial-DFA states");
  for (size_t length = 0; length <= 20; ++length)
    require(count_words(d,length,budget) == (length > 0 && length % 2 == 0 ? 1 : 0),"(AB)+ count");
  require(accepts(d,{17,29,17,29}),"(AB)+ membership");
  require(!accepts(d,{29,17}),"(AB)+ wrong order");

  NFA overlap;
  for (int q = 0; q < 5; ++q) overlap.add_state(q==2 || q==3);
  overlap.add_initial(0); overlap.add_initial(1); overlap.add_initial(1);
  overlap.add_edge(0,0,2); overlap.add_edge(0,0,2); overlap.add_edge(1,0,2);
  overlap.add_edge(0,std::numeric_limits<Label>::max(),2);
  overlap.add_edge(0,9,4); overlap.add_edge(4,9,4);
  NFA reduced = trim(overlap,budget);
  require(reduced.size() == 3,"unreachable and non-coreachable trimming");
  DFA unique = minimize(determinize(overlap,budget),budget);
  require(unique.size()==2 && count_words(unique,1,budget)==2,"unique words, not NFA paths");
  require(accepts(unique,{0}) && accepts(unique,{std::numeric_limits<Label>::max()}),"full uint32 label range");

  NFA empty;
  require(determinize(empty,budget)==empty_dfa(),"empty NFA representation");
  NFA eps; eps.add_state(true); eps.add_initial(0);
  DFA epsd = determinize(eps,budget);
  require(count_words(epsd,0,budget)==1 && count_words(epsd,1,budget)==0,"empty word acceptance");

  DFA sink;
  sink.add_state(false); sink.add_state(true); sink.add_state(false);
  sink.add_edge(0,1,1); sink.add_edge(0,2,2); sink.add_edge(2,1,2); sink.add_edge(2,2,2);
  DFA partial; partial.add_state(false); partial.add_state(true); partial.add_edge(0,1,1);
  require(equivalent(sink,partial,budget),"implicit rejecting sink equivalence");
  require(minimize(sink,budget)==minimize(partial,budget),"sink removal canonicalization");
  DFA extra_label = partial;
  extra_label.add_edge(0,std::numeric_limits<Label>::max(),1);
  require(!equivalent(partial,extra_label,budget),"new accepted label must reach implicit rejecting sink");
  require(!equivalent(extra_label,partial,budget),"new-label inequivalence is symmetric");

  DFA binary; binary.add_state(true); binary.add_edge(0,0,0); binary.add_edge(0,1,0);
  require(count_words(binary,100,budget)==(Integer(1)<<100),"big-integer unique-word count");
  require(count_words(binary,100,budget).str()=="1267650600228229401496703205376",
          "independently known decimal 2^100");
  Integer carried(999999999999999999ULL); carried += Integer(1);
  require(carried.str()=="1000000000000000000","base-10^9 carry across limbs");
  auto negative = binary; negative.final[0]=0;
  require(!equivalent(binary,negative,budget),"empty-word inequivalence");
  require(minimize(negative,budget)==empty_dfa(),"nonaccepting cycle is empty language");

  DFA chain;
  for (int i = 0; i < 32; ++i) chain.add_state(i==31);
  for (int i = 0; i < 31; ++i) chain.add_edge(i,7,i+1);
  require(minimize(chain,budget).size()==32,"deep distinguishing suffixes");
}

static uint64_t randomized_cases() {
  std::mt19937 rng(113);
  const std::vector<Label> alphabet{0,1,5};
  uint64_t checks = 0;
  for (int trial = 0; trial < 120; ++trial) {
    NFA a; size_t n = 1+rng()%8;
    for (size_t i = 0; i < n; ++i) a.add_state(rng()%3==0);
    for (State q = 0; q < n; ++q) {
      if (rng()%3==0) a.add_initial(q);
      for (Label label : alphabet)
        for (State to = 0; to < n; ++to)
          if (rng()%7==0) a.add_edge(q,label,to);
    }
    Budget budget;
    NFA trimmed = trim(a,budget);
    DFA original = determinize(a,budget), minimal = minimize(original,budget);
    require(equivalent(original,minimal,budget),"random DFA minimization equivalence");
    require(minimize(minimal,budget)==minimal,"minimization idempotence");
    require(minimize(renamed(minimal,rng),budget)==minimal,"canonical state renaming");
    require(minimize(determinize(trimmed,budget),budget)==minimal,"trim language preservation");
    std::vector<std::vector<Label>> words(1);
    for (size_t length = 0; length <= 6; ++length) {
      size_t accepted = 0;
      for (const auto& word : words) {
        bool expected = word_oracle(a,word);
        require(accepts(a,word)==expected,"NFA independent membership");
        require(accepts(original,word)==expected,"subset construction independent membership");
        require(accepts(minimal,word)==expected,"minimized independent membership");
        accepted += expected; ++checks;
      }
      require(count_words(minimal,length,budget)==accepted,"DP counts distinct enumerated words");
      std::vector<std::vector<Label>> next;
      for (const auto& word : words) for (Label label : alphabet) {
        auto extended = word; extended.push_back(label); next.push_back(std::move(extended));
      }
      words.swap(next);
    }
  }
  return checks;
}

static void resource_and_validation_cases() {
  // Third symbol from the right is 1: four NFA states but eight DFA subsets.
  NFA a;
  for (int i = 0; i < 4; ++i) a.add_state(i==3);
  a.add_initial(0); a.add_edge(0,0,0); a.add_edge(0,1,0); a.add_edge(0,1,1);
  for (int i = 1; i < 3; ++i) { a.add_edge(i,0,i+1); a.add_edge(i,1,i+1); }
  Limits small; small.max_states=4;
  bool capped=false;
  try { Budget budget(small); (void)determinize(a,budget); }
  catch (const LimitReached&) { capped=true; }
  require(capped,"determinization state cap must not return a verdict");
  Limits operations; operations.max_operations=1;
  capped=false;
  try { Budget budget(operations); (void)trim(a,budget); }
  catch (const LimitReached&) { capped=true; }
  require(capped,"operation cap must throw");

  DFA malformed; malformed.add_state(true);
  malformed.edges[0]={{0,0},{0,0}};
  bool rejected=false;
  try { Budget budget; (void)count_words(malformed,1,budget); }
  catch (const std::invalid_argument&) { rejected=true; }
  require(rejected,"DFA duplicate labels must reject instead of double-counting");
}

int main() {
  try {
    basic_cases();
    uint64_t checks = randomized_cases();
    resource_and_validation_cases();
    std::cout << "PASS random_nfas=120 enumerated_words=" << checks
              << " canonicalization=120 bigint_bits=101 caps=2\n";
    return 0;
  } catch (const std::exception& ex) {
    std::cerr << "FAIL " << ex.what() << '\n'; return 1;
  }
}
