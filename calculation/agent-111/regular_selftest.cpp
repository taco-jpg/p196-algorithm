// Independent exact-language controls for regular.hpp. No bounded enumeration
// is used to assert equality of infinite languages: that uses product BFS.
// Build: c++ -O2 -std=c++17 calculation/agent-111/regular_selftest.cpp -o /tmp/a111_regular_test
// Run: /tmp/a111_regular_test [finite_random_cases=1000]
#include "regular.hpp"
#include <algorithm>
#include <cstdint>
#include <functional>
#include <iostream>
#include <limits>
#include <map>
#include <optional>
#include <random>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using Symbol = uint64_t;
using Word = std::vector<Symbol>;
using Words = std::set<Word>;
using Relations = std::map<Symbol, std::vector<a111r::Choice>>;

struct Counts {
  uint64_t equivalences = 0, product_states = 0, canonical_cases = 0;
  uint64_t nfa_cases = 0, finite_images = 0, infinite_images = 0;
  uint64_t raw_choices = 0, output_words = 0, changed_relations = 0;
  uint64_t rejection_cases = 0, cap_cases = 0, pair_distinctions = 0;
};

static void require(bool good, const std::string& why) {
  if (!good) throw std::runtime_error(why);
}
static Symbol symbol(uint32_t type, uint32_t value) {
  return (uint64_t(type) << 32) | value;
}
static uint32_t type_of(Symbol s) { return uint32_t(s >> 32); }
static uint32_t value_of(Symbol s) { return uint32_t(s); }

// Independent partial-DFA representation. Missing transitions enter a rejecting
// sink. This representation and the product checker do not call core helpers.
struct Ref {
  size_t start = 0;
  std::vector<std::map<Symbol, size_t>> next{{}};
  std::vector<bool> accept{false};
  size_t add(bool final = false) {
    next.emplace_back(); accept.push_back(final); return next.size() - 1;
  }
};

static Ref reference(const a111r::DFA& d) {
  Ref r;
  if (d.nodes.empty()) return r;
  r.start = d.start; r.next.assign(d.nodes.size(), {});
  r.accept.assign(d.nodes.size(), false);
  require(r.start < r.next.size(), "core returned invalid start state");
  for (size_t i = 0; i < d.nodes.size(); ++i) {
    r.accept[i] = d.nodes[i].accept;
    for (auto [x, q] : d.nodes[i].edges) {
      require(q < r.next.size(), "core returned invalid transition target");
      auto inserted = r.next[i].emplace(x, q);
      require(inserted.second || inserted.first->second == q,
              "core returned conflicting deterministic edges");
    }
  }
  return r;
}
static a111r::DFA core(const Ref& r) {
  a111r::DFA d; d.start = a111r::State(r.start); d.nodes.resize(r.next.size());
  for (size_t i = 0; i < r.next.size(); ++i) {
    d.nodes[i].accept = r.accept[i];
    for (auto [x, q] : r.next[i]) d.nodes[i].edges.push_back({x, a111r::State(q)});
  }
  return d;
}
static bool same_structure(const a111r::DFA& a, const a111r::DFA& b) {
  if (a.start != b.start || a.nodes.size() != b.nodes.size()) return false;
  for (size_t i = 0; i < a.nodes.size(); ++i)
    if (a.nodes[i].accept != b.nodes[i].accept || a.nodes[i].edges != b.nodes[i].edges)
      return false;
  return true;
}
static bool accepts_ref(const Ref& r, const Word& w) {
  size_t q = r.start;
  for (Symbol x : w) {
    auto it = r.next[q].find(x);
    if (it == r.next[q].end()) return false;
    q = it->second;
  }
  return r.accept[q];
}
static std::string show(const Word& w) {
  std::ostringstream out; out << '[';
  for (size_t i = 0; i < w.size(); ++i) out << (i ? "," : "") << w[i];
  return out.str() + ']';
}

// Exact equivalence over all finite words, including unbounded lengths. A BFS
// visits the finite product of the two partial automata plus rejecting sinks.
// The union of outgoing alphabets is sufficient: any other symbol kills both.
static std::optional<Word> distinguish(const Ref& a, const Ref& b, Counts& count) {
  struct Visit { size_t a, b, parent; Symbol letter; };
  const size_t absent = std::numeric_limits<size_t>::max();
  std::vector<Visit> queue{{a.start, b.start, absent, 0}};
  std::map<std::pair<size_t, size_t>, size_t> seen;
  seen[{a.start, b.start}] = 0;
  auto accepting = [](const Ref& r, size_t q) {
    return q < r.next.size() && r.accept[q];
  };
  auto step = [](const Ref& r, size_t q, Symbol x) {
    if (q == r.next.size()) return q;
    auto it = r.next[q].find(x);
    return it == r.next[q].end() ? r.next.size() : it->second;
  };
  for (size_t head = 0; head < queue.size(); ++head) {
    require(queue.size() < 2000000, "independent product-oracle budget exceeded");
    const Visit v = queue[head]; ++count.product_states;
    if (accepting(a, v.a) != accepting(b, v.b)) {
      Word witness;
      for (size_t i = head; queue[i].parent != absent; i = queue[i].parent)
        witness.push_back(queue[i].letter);
      std::reverse(witness.begin(), witness.end());
      require(accepts_ref(a, witness) != accepts_ref(b, witness),
              "independent product checker returned an invalid witness");
      return witness;
    }
    std::set<Symbol> letters;
    if (v.a < a.next.size()) for (auto [x, q] : a.next[v.a]) letters.insert(x);
    if (v.b < b.next.size()) for (auto [x, q] : b.next[v.b]) letters.insert(x);
    for (Symbol x : letters) {
      size_t qa = step(a, v.a, x), qb = step(b, v.b, x);
      if (seen.emplace(std::make_pair(qa, qb), queue.size()).second)
        queue.push_back({qa, qb, head, x});
    }
  }
  return std::nullopt;
}
static void equivalent(const a111r::DFA& actual, const Ref& wanted,
                       Counts& count, const std::string& label) {
  auto difference = distinguish(reference(actual), wanted, count);
  require(!difference, label + " language mismatch at " +
          (difference ? show(*difference) : std::string()));
  ++count.equivalences;
}

static Ref trie(const Words& words) {
  Ref r;
  for (const Word& w : words) {
    size_t q = 0;
    for (Symbol x : w) {
      auto it = r.next[q].find(x);
      if (it == r.next[q].end()) {
        size_t new_q = r.add(); r.next[q][x] = new_q; q = new_q;
      } else q = it->second;
    }
    r.accept[q] = true;
  }
  return r;
}
static Ref without_epsilon(Ref r) {
  // A fresh start is essential when the old accepting start is revisited.
  const auto first = r.next[r.start];
  size_t start = r.add(false); r.next[start] = first; r.start = start;
  return r;
}
static Ref powers(const Word& word) {
  require(!word.empty(), "reference positive power needs a nonempty word");
  Ref r;
  for (size_t i = 0; i < word.size(); ++i) r.add(i + 1 == word.size());
  for (size_t i = 0; i < word.size(); ++i) r.next[i][word[i]] = i + 1;
  r.next[word.size()][word[0]] = 1;
  return r;
}

static void canonical_shape(const a111r::DFA& d, Counts& count, bool pairs = true) {
  Ref r = reference(d);
  if (d.nodes.empty()) return;
  require(d.start == 0, "canonical start is not zero");
  std::vector<size_t> queue{0}; std::vector<bool> seen(d.nodes.size(), false); seen[0] = true;
  for (size_t h = 0; h < queue.size(); ++h) {
    const auto& edges = d.nodes[queue[h]].edges;
    for (size_t j = 1; j < edges.size(); ++j)
      require(edges[j-1].first < edges[j].first, "canonical edges are not unique/sorted");
    for (auto [x, q] : edges) if (!seen[q]) {
      require(q == queue.size(), "canonical numbering is not sorted-edge BFS");
      seen[q] = true; queue.push_back(q);
    }
  }
  require(queue.size() == d.nodes.size(), "canonical DFA retained unreachable states");
  bool any_final = std::any_of(r.accept.begin(), r.accept.end(), [](bool x) { return x; });
  if (!any_final) {
    require(d.nodes.size() == 1 && d.nodes[0].edges.empty(),
            "empty language retains unproductive structure");
    return;
  }
  std::vector<bool> productive = r.accept;
  bool changed = true;
  while (changed) {
    changed = false;
    for (size_t q = 0; q < r.next.size(); ++q) if (!productive[q])
      for (auto [x, target] : r.next[q]) if (productive[target]) {
        productive[q] = true; changed = true; break;
      }
  }
  require(std::all_of(productive.begin(), productive.end(), [](bool x) { return x; }),
          "canonical DFA retained nonproductive states");
  if (pairs && r.next.size() <= 80) for (size_t i = 0; i < r.next.size(); ++i)
    for (size_t j = i + 1; j < r.next.size(); ++j) {
      Ref a = r, b = r; a.start = i; b.start = j;
      require(bool(distinguish(a, b, count)), "two minimized states have equal right languages");
      ++count.pair_distinctions;
    }
}

static a111r::DFA adversarial(const Ref& input, std::mt19937_64& rng) {
  const size_t n = input.next.size();
  a111r::DFA d; d.nodes.resize(2*n + 3); d.start = a111r::State(2*input.start);
  std::set<Symbol> alphabet;
  for (const auto& edges : input.next) for (auto [x, q] : edges) alphabet.insert(x);
  Symbol fresh = 0; while (alphabet.count(fresh)) ++fresh;
  for (size_t q = 0; q < n; ++q) for (size_t copy = 0; copy < 2; ++copy) {
    auto& node = d.nodes[2*q + copy]; node.accept = input.accept[q];
    for (auto [x, target] : input.next[q]) {
      a111r::State to = a111r::State(2*target + ((copy + x) & 1));
      node.edges.push_back({x, to});
      if (rng() % 3 == 0) node.edges.push_back({x, to});
    }
    node.edges.push_back({fresh, a111r::State(2*n + copy)});
  }
  // Two equivalent dead states, and an unreachable accepting component.
  d.nodes[2*n].edges.push_back({fresh, a111r::State(2*n+1)});
  d.nodes[2*n+1].edges.push_back({fresh, a111r::State(2*n)});
  d.nodes[2*n+2].accept = true;
  d.nodes[2*n+2].edges.push_back({fresh, a111r::State(2*n+2)});
  std::vector<a111r::State> perm(d.nodes.size());
  for (size_t i = 0; i < perm.size(); ++i) perm[i] = a111r::State(i);
  std::shuffle(perm.begin(), perm.end(), rng);
  a111r::DFA renamed; renamed.nodes.resize(d.nodes.size()); renamed.start = perm[d.start];
  for (size_t i = 0; i < d.nodes.size(); ++i) {
    auto& dest = renamed.nodes[perm[i]]; dest.accept = d.nodes[i].accept;
    for (auto [x, q] : d.nodes[i].edges) dest.edges.push_back({x, perm[q]});
    std::shuffle(dest.edges.begin(), dest.edges.end(), rng);
  }
  return renamed;
}
static Ref random_dfa(std::mt19937_64& rng, size_t n) {
  Ref r; while (r.next.size() < n) r.add(); r.start = rng() % n;
  for (size_t q = 0; q < n; ++q) {
    r.accept[q] = rng() % 3 == 0;
    for (uint32_t t = 0; t < 2; ++t) for (uint32_t x = 0; x < 2; ++x)
      if (rng() % 3 != 0) r.next[q][symbol(t, x)] = rng() % n;
  }
  return r;
}
static void canonical_tests(std::mt19937_64& rng, Counts& count) {
  // Self-check the independent oracle on a zero-length and one-letter witness.
  Ref empty, epsilon = trie(Words{Word{}}), a = trie(Words{Word{7}}), b = trie(Words{Word{8}});
  auto w0 = distinguish(empty, epsilon, count);
  auto w1 = distinguish(a, b, count);
  require(w0 && w0->empty() && w1 && w1->size() == 1, "product oracle self-check");
  require(!(core(empty) == core(epsilon)) && !(core(a) == core(b)),
          "DFA structural equality accepted different structures");
  for (size_t k = 0; k < 240; ++k) {
    Ref r = random_dfa(rng, 1 + rng()%7);
    auto first = a111r::canonicalize(core(r));
    auto second = a111r::canonicalize(adversarial(r, rng));
    equivalent(first, r, count, "canonical original");
    equivalent(second, r, count, "renamed/split/dead/unreachable");
    require(same_structure(first, second) && first == second,
            "equivalent adversarial DFA has different canonical form");
    require(same_structure(first, a111r::canonicalize(first)), "canonicalization not idempotent");
    canonical_shape(first, count); ++count.canonical_cases;
  }
  Ref wide = trie(Words{{symbol(UINT32_MAX, UINT32_MAX)},
                       {symbol(UINT32_MAX, 0), symbol(0, UINT32_MAX)}, Word{}});
  auto normalized = a111r::canonicalize(adversarial(wide, rng));
  equivalent(normalized, wide, count, "full uint64 symbol range");
  canonical_shape(normalized, count); ++count.canonical_cases;
}

static void nfa_tests(std::mt19937_64& rng, Counts& count) {
  {
    // Infinite union a* | b*, using multiple starts and duplicate transitions.
    a111r::NFA nfa; nfa.nodes.resize(2); nfa.starts = {0, 1, 0};
    nfa.nodes[0].accept = nfa.nodes[1].accept = true;
    nfa.nodes[0].edges = {{7, 0}, {7, 0}}; nfa.nodes[1].edges = {{8, 1}};
    Ref expected; expected.accept[0] = true; expected.add(true); expected.add(true);
    expected.next[0] = {{7,1},{8,2}}; expected.next[1] = {{7,1}}; expected.next[2] = {{8,2}};
    auto actual = a111r::determinize(nfa);
    equivalent(actual, expected, count, "infinite NFA union");
    canonical_shape(actual, count); ++count.nfa_cases;
  }
  {
    // Infinite words ending in 00. Equal-label arcs genuinely diverge.
    a111r::NFA nfa; nfa.nodes.resize(3); nfa.starts = {0};
    nfa.nodes[0].edges = {{0,0},{1,0},{0,1}};
    nfa.nodes[1].edges = {{0,2}}; nfa.nodes[2].accept = true;
    Ref expected; expected.add(); expected.add(true);
    expected.next[0] = {{0,1},{1,0}}; expected.next[1] = {{0,2},{1,0}};
    expected.next[2] = {{0,2},{1,0}};
    auto actual = a111r::determinize(nfa);
    equivalent(actual, expected, count, "infinite NFA suffix");
    canonical_shape(actual, count); ++count.nfa_cases;
  }
  for (size_t iteration = 0; iteration < 240; ++iteration) {
    const size_t depth = 1 + rng()%4, width = 3;
    a111r::NFA nfa; nfa.nodes.resize((depth+1)*width); nfa.starts = {0,1,0};
    for (size_t level = 0; level <= depth; ++level) for (size_t i = 0; i < width; ++i) {
      auto& node = nfa.nodes[level*width+i]; node.accept = rng()%3 == 0;
      if (level == depth) continue;
      for (unsigned k = 0, end = rng()%7; k < end; ++k)
        node.edges.push_back({symbol(rng()%2, rng()%3),
                              a111r::State((level+1)*width+rng()%width)});
    }
    Words expected; Word prefix;
    std::function<void(size_t,size_t)> walk = [&](size_t q, size_t length) {
      require(length <= depth, "finite NFA oracle exceeded construction depth");
      if (nfa.nodes[q].accept) expected.insert(prefix);
      for (auto [x, target] : nfa.nodes[q].edges) {
        prefix.push_back(x); walk(target, length+1); prefix.pop_back();
      }
    };
    for (auto start : nfa.starts) walk(start, 0);
    auto actual = a111r::determinize(nfa);
    equivalent(actual, trie(expected), count, "finite complete NFA paths");
    canonical_shape(actual, count); ++count.nfa_cases;
  }
}

static const std::vector<a111r::Choice>& row(const Relations& r, uint32_t type, uint32_t x) {
  static const std::vector<a111r::Choice> empty;
  auto it = r.find(symbol(type,x)); return it == r.end() ? empty : it->second;
}
static Symbol encoded(uint32_t type, uint32_t y, int next_c) {
  require(y < 4 && next_c >= -1 && next_c <= 2, "synthetic symbol outside encoding domain");
  return symbol(type, 4*y + uint32_t(next_c+1));
}
static Words explicit_image(const Words& input, const Relations& rows, Counts& count) {
  Words out;
  for (const Word& word : input) {
    if (word.empty()) continue;
    std::vector<a111r::Choice> choices(word.size());
    std::function<void(size_t)> walk = [&](size_t pos) {
      if (pos == word.size()) {
        Word image(word.size());
        for (size_t i = 0; i < word.size(); ++i)
          image[i] = encoded(type_of(word[i]), choices[i].y, choices[(i+1)%word.size()].c);
        out.insert(std::move(image)); ++count.raw_choices; return;
      }
      for (auto choice : row(rows, type_of(word[pos]), value_of(word[pos]))) {
        choices[pos] = choice; walk(pos+1);
      }
    };
    walk(0);
  }
  count.output_words += out.size(); return out;
}
static a111r::DFA finite_image(const Words& input, const Relations& rows, Counts& count) {
  auto local = [&](uint32_t t, uint32_t x) -> const std::vector<a111r::Choice>& {
    return row(rows,t,x);
  };
  Words expected = explicit_image(input, rows, count);
  auto actual = a111r::cyclic_image(core(trie(input)), local, encoded);
  equivalent(actual, trie(expected), count, "finite correlated cyclic image");
  require(same_structure(actual, a111r::canonicalize(core(trie(expected)))),
          "finite image not canonical");
  require(!accepts_ref(reference(actual), {}), "cyclic image accepted epsilon");
  for (size_t n = 0; n <= 5; ++n) {
    Words at_length;
    for (const auto& w : expected) if (w.size() == n) at_length.insert(w);
    auto enumerated = a111r::enumerate_length(actual,n,100000);
    require(Words(enumerated.begin(),enumerated.end()) == at_length,
            "enumerate_length differs from complete finite oracle");
    require(enumerated.size() == at_length.size(), "enumerate_length emitted duplicate words");
    auto amount = a111r::count_length(actual,n);
    require(!amount.saturated && amount.value == at_length.size(), "finite count mismatch");
  }
  auto shortest = a111r::shortest_word(actual);
  if (expected.empty()) require(!shortest, "shortest_word accepted empty language");
  else {
    size_t minimum = std::min_element(expected.begin(),expected.end(),
        [](const Word& a,const Word& b){ return a.size()<b.size(); })->size();
    require(shortest && expected.count(*shortest) && shortest->size()==minimum,
            "shortest_word is absent, unaccepted, or nonminimal");
  }
  ++count.finite_images; return actual;
}
static Relations random_rows(std::mt19937_64& rng, const Words& words) {
  Relations r;
  for (const auto& w : words) for (Symbol x : w) r[x];
  for (auto& [x, rows] : r) {
    for (unsigned i=0,end=rng()%4; i<end; ++i) rows.push_back({uint32_t(rng()%4),int(rng()%4)-1});
    if (!rows.empty() && rng()%3 == 0) rows.push_back(rows.front());
  }
  return r;
}
static void finite_tests(std::mt19937_64& rng, size_t rounds, Counts& count) {
  Relations one{{symbol(4,0),{{0,-1},{1,2},{0,-1}}}};
  finite_image(Words{Word{},Word{symbol(4,0)}},one,count);
  finite_image(Words{Word{}},one,count);
  Words diagonal{{symbol(0,0),symbol(1,0)}, {symbol(0,1),symbol(1,1)}};
  Relations correlated{{symbol(0,0),{{0,-1}}},{symbol(1,0),{{1,0}}},
                       {symbol(0,1),{{2,1}}},{symbol(1,1),{{3,2}}}};
  finite_image(diagonal,correlated,count);
  for (size_t i = 0; i < rounds; ++i) {
    Words input;
    for (unsigned k=0,end=rng()%13; k<end; ++k) {
      Word w(rng()%5);
      for (auto& x : w) x = symbol(rng()%3,rng()%3);
      input.insert(std::move(w));
    }
    if (i%4==0) { input.insert({symbol(0,0),symbol(1,0)}); input.insert({symbol(0,1),symbol(1,1)}); }
    auto first = random_rows(rng,input); finite_image(input,first,count);
    auto changed = random_rows(rng,input); finite_image(input,changed,count);
    ++count.changed_relations;
  }
}

// Expected infinite language of closed binary paths. A symbol carries
// (own_bit,next_bit); the next symbol must start with next_bit. The state stores
// first_bit, required_bit, and type-pattern phase, then checks closure at accept.
static Ref closed_binary_paths(const std::vector<uint32_t>& types) {
  Ref r; const size_t period = types.size();
  for (size_t i=0;i<4*period;++i) r.add();
  auto state = [&](size_t phase,unsigned first,unsigned next) { return 1+4*phase+2*first+next; };
  for (unsigned first=0;first<2;++first) for (unsigned next=0;next<2;++next)
    r.next[0][symbol(types[0],2*first+next)] = state(1%period,first,next);
  for (size_t phase=0;phase<period;++phase) for (unsigned first=0;first<2;++first)
    for (unsigned need=0;need<2;++need) {
      size_t q=state(phase,first,need); r.accept[q]=(phase==0 && first==need);
      for (unsigned next=0;next<2;++next)
        r.next[q][symbol(types[phase],2*need+next)] = state((phase+1)%period,first,next);
    }
  return r;
}
static void infinite_tests(std::mt19937_64& rng, Counts& count) {
  const std::vector<a111r::Choice> binary_choices{{0,0},{1,1},{0,0}};
  for (const auto& types : std::vector<std::vector<uint32_t>>{{7},{3,9},{UINT32_MAX,0,17}}) {
    Word input_word; for (auto type : types) input_word.push_back(symbol(type,11));
    auto input = a111r::positive_powers(input_word);
    equivalent(input,powers(input_word),count,"positive powers");
    auto local = [&](uint32_t,uint32_t)->const std::vector<a111r::Choice>& { return binary_choices; };
    auto encoder = [](uint32_t t,uint32_t y,int c) { return symbol(t,2*y+uint32_t(c)); };
    auto actual = a111r::cyclic_image(input,local,encoder);
    equivalent(actual,closed_binary_paths(types),count,"infinite closed binary paths");
    canonical_shape(actual,count); ++count.infinite_images;
    for (size_t length=0;length<=8;++length) {
      auto n=a111r::count_length(actual,length);
      uint64_t want=length && length%types.size()==0 ? uint64_t(1)<<length : 0;
      require(!n.saturated && n.value==want,"infinite closed-path count/length mismatch");
    }
    if (types.size()==1) {
      auto exact=a111r::count_length(actual,63), saturated=a111r::count_length(actual,64);
      require(!exact.saturated && exact.value==(uint64_t(1)<<63) && saturated.saturated,
              "infinite language count overflow was not distinguished");
    }
    // Identical input automaton, changed signature: only the all-zero cycle.
    const std::vector<a111r::Choice> zeros{{0,0}};
    auto fixed = [&](uint32_t,uint32_t)->const std::vector<a111r::Choice>& { return zeros; };
    auto changed=a111r::cyclic_image(input,fixed,encoder);
    Word expected_word; for(auto type:types) expected_word.push_back(symbol(type,0));
    equivalent(changed,powers(expected_word),count,"changed infinite local relation");
    ++count.infinite_images; ++count.changed_relations;
  }
  // Exact unbounded identity/permutation tests on arbitrary cyclic DFAs.
  for (size_t iteration=0;iteration<120;++iteration) {
    Ref input=random_dfa(rng,1+rng()%6);
    if (iteration==0) {
      input=Ref{}; input.accept[0]=true;
      input.next[0]={{symbol(0,0),0},{symbol(1,1),0}};
    }
    for (uint32_t permutation : {uint32_t(0),uint32_t(0xa5a5a5a5)}) {
      Relations rows;
      for(const auto& edges:input.next) for(auto [x,q]:edges)
        rows[x]={{value_of(x)^permutation,0}};
      auto local=[&](uint32_t t,uint32_t x)->const std::vector<a111r::Choice>& { return row(rows,t,x); };
      auto encoder=[](uint32_t t,uint32_t y,int){return symbol(t,y);};
      Ref expected=input;
      for(auto& edges:expected.next) {
        std::map<Symbol,size_t> mapped;
        for(auto [x,q]:edges) mapped[symbol(type_of(x),value_of(x)^permutation)]=q;
        edges=std::move(mapped);
      }
      auto actual=a111r::cyclic_image(core(input),local,encoder);
      equivalent(actual,without_epsilon(expected),count,"infinite identity/permutation");
      require(!accepts_ref(reference(actual),{}),"infinite image retained epsilon");
      ++count.infinite_images;
    }
  }
  // An actual cyclic left-shift, with a different infinite resulting language.
  Word period{symbol(5,0),symbol(5,1)};
  Relations rows{{period[0],{{0,0}}},{period[1],{{0,1}}}};
  auto local=[&](uint32_t t,uint32_t x)->const std::vector<a111r::Choice>& { return row(rows,t,x); };
  auto next_only=[](uint32_t t,uint32_t,int c){return symbol(t,uint32_t(c));};
  auto shifted=a111r::cyclic_image(a111r::positive_powers(period),local,next_only);
  equivalent(shifted,powers(Word{period[1],period[0]}),count,"infinite cyclic shift");
  ++count.infinite_images;
}

static void guard_tests(Counts& count) {
  auto reject=[&](const std::function<void()>& operation) {
    bool threw=false;
    try { operation(); } catch(const std::invalid_argument&) { threw=true; }
    require(threw,"malformed automaton not rejected by invalid_argument"); ++count.rejection_cases;
  };
  reject([]{a111r::DFA d;d.nodes.resize(1);d.start=1;a111r::canonicalize(d);});
  reject([]{a111r::DFA d;d.nodes.resize(1);d.nodes[0].edges={{7,1}};a111r::canonicalize(d);});
  reject([]{a111r::DFA d;d.nodes.resize(2);d.nodes[0].edges={{7,0},{7,1}};a111r::canonicalize(d);});
  reject([]{a111r::NFA n;n.nodes.resize(1);n.starts={1};a111r::determinize(n);});
  reject([]{a111r::NFA n;n.nodes.resize(1);n.starts={0};n.nodes[0].edges={{7,2}};a111r::determinize(n);});
  equivalent(a111r::canonicalize(a111r::DFA{}),Ref{},count,"empty DFA array");
  equivalent(a111r::determinize(a111r::NFA{}),Ref{},count,"empty NFA array");
  auto capped=[&](const std::function<void()>& operation) {
    bool threw=false;
    try { operation(); } catch(const a111r::Limit&) { threw=true; }
    require(threw,"resource cap did not throw its dedicated Limit"); ++count.cap_cases;
  };
  a111r::Limits limits; limits.states=1;
  capped([&]{a111r::canonicalize(core(powers(Word{1,2,3})),limits);});
  limits=a111r::Limits{}; limits.edges=1;
  capped([&]{a111r::canonicalize(core(powers(Word{1,2,3})),limits);});
  limits=a111r::Limits{}; limits.work=1;
  capped([&]{a111r::canonicalize(core(powers(Word{1,2,3})),limits);});
  limits=a111r::Limits{}; limits.states=1;
  const std::vector<a111r::Choice> choices{{0,0},{1,1}};
  auto local=[&](uint32_t,uint32_t)->const std::vector<a111r::Choice>&{return choices;};
  capped([&]{a111r::cyclic_image(core(powers(Word{symbol(3,0)})),local,encoded,limits);});
}

int main(int argc,char** argv) {
  try {
    size_t rounds=argc>1?std::stoul(argv[1]):1000;
    require(argc<=2 && rounds<=10000,"usage: regular_selftest [finite_random_cases<=10000]");
    std::mt19937_64 rng(111289); Counts count;
    canonical_tests(rng,count); nfa_tests(rng,count);
    finite_tests(rng,rounds,count); infinite_tests(rng,count); guard_tests(count);
    std::cout << "REGULAR_EXACT_LANGUAGE_CONTROLS PASS finite_random_cases=" << rounds
      << " canonical_cases=" << count.canonical_cases << " nfa_cases=" << count.nfa_cases
      << " finite_images=" << count.finite_images << " unbounded_images=" << count.infinite_images
      << " equivalences=" << count.equivalences << " product_states=" << count.product_states
      << " pair_distinctions=" << count.pair_distinctions << " raw_choices=" << count.raw_choices
      << " output_words=" << count.output_words << " changed_relations=" << count.changed_relations
      << " rejection_cases=" << count.rejection_cases << " cap_cases=" << count.cap_cases << '\n';
    return 0;
  } catch(const std::exception& error) {
    std::cerr << "REGULAR_EXACT_LANGUAGE_CONTROLS FAIL: " << error.what() << '\n';
    return 1;
  }
}
