#ifndef AGENT111_REGULAR_HPP
#define AGENT111_REGULAR_HPP

#include <algorithm>
#include <cstdint>
#include <functional>
#include <limits>
#include <map>
#include <optional>
#include <queue>
#include <stdexcept>
#include <string>
#include <tuple>
#include <unordered_map>
#include <utility>
#include <vector>

namespace a111r {
using Symbol = uint64_t;
using State = uint32_t;
using Word = std::vector<Symbol>;
struct Node { bool accept = false; std::vector<std::pair<Symbol, State>> edges; };
struct DFA { std::vector<Node> nodes; State start = 0; };
struct NFA { std::vector<Node> nodes; std::vector<State> starts; };
struct Limits { size_t states = 200000, edges = 2000000; uint64_t work = 50000000; };
struct Limit : std::runtime_error { using std::runtime_error::runtime_error; };
struct Count { uint64_t value = 0; bool saturated = false; };
struct Stats {
  size_t nfa_states = 0, nfa_edges = 0, subset_states = 0, subset_edges = 0;
  size_t canonical_states = 0, canonical_edges = 0;
  uint64_t work = 0;
};

inline bool operator==(const DFA& a, const DFA& b) {
  if (a.start != b.start || a.nodes.size() != b.nodes.size()) return false;
  for (size_t i = 0; i < a.nodes.size(); ++i)
    if (a.nodes[i].accept != b.nodes[i].accept || a.nodes[i].edges != b.nodes[i].edges) return false;
  return true;
}
inline bool operator!=(const DFA& a, const DFA& b) { return !(a == b); }
inline DFA empty_language() { return DFA{{Node{}}, 0}; }
inline size_t edge_count(const DFA& dfa) {
  size_t total = 0; for (const auto& node : dfa.nodes) total += node.edges.size(); return total;
}

namespace detail {
struct Budget {
  Limits limits; uint64_t used = 0;
  explicit Budget(Limits value) : limits(value) {}
  void tick(uint64_t amount = 1) {
    if (amount > limits.work - used) throw Limit("regular work cap=" + std::to_string(limits.work));
    used += amount;
  }
  void states(size_t n) const {
    if (n > limits.states || n >= UINT32_MAX)
      throw Limit("regular state cap states=" + std::to_string(n) + " cap=" + std::to_string(limits.states));
  }
  void edges(size_t n) const {
    if (n > limits.edges)
      throw Limit("regular edge cap edges=" + std::to_string(n) + " cap=" + std::to_string(limits.edges));
  }
};

inline DFA canonicalize(DFA input, Budget& budget) {
  if (input.nodes.empty()) return empty_language();
  size_t n = input.nodes.size(); budget.states(n);
  if (input.start >= n) throw std::invalid_argument("DFA start outside state set");
  size_t edges = 0;
  for (auto& node : input.nodes) {
    budget.tick();
    std::sort(node.edges.begin(), node.edges.end());
    std::vector<std::pair<Symbol, State>> normalized;
    for (auto arc : node.edges) {
      budget.tick();
      if (arc.second >= n) throw std::invalid_argument("DFA target outside state set");
      if (!normalized.empty() && normalized.back().first == arc.first) {
        if (normalized.back().second != arc.second)
          throw std::invalid_argument("conflicting deterministic equal-label arcs");
      } else normalized.push_back(arc);
    }
    node.edges = std::move(normalized); edges += node.edges.size(); budget.edges(edges);
  }
  std::vector<uint8_t> reachable(n, 0), productive(n, 0);
  std::vector<State> queue{input.start}; reachable[input.start] = 1;
  for (size_t head = 0; head < queue.size(); ++head)
    for (auto [label, target] : input.nodes[queue[head]].edges) {
      (void)label; budget.tick();
      if (!reachable[target]) { reachable[target] = 1; queue.push_back(target); }
    }
  std::vector<std::vector<State>> reverse(n);
  for (State state : queue)
    for (auto [label, target] : input.nodes[state].edges) {
      (void)label; reverse[target].push_back(state);
    }
  std::vector<State> live;
  for (State state : queue) if (input.nodes[state].accept) { productive[state] = 1; live.push_back(state); }
  for (size_t head = 0; head < live.size(); ++head)
    for (State predecessor : reverse[live[head]]) {
      budget.tick();
      if (!productive[predecessor]) { productive[predecessor] = 1; live.push_back(predecessor); }
    }
  if (!productive[input.start]) return empty_language();

  // Removing nonproductive targets makes every absent label the same implicit
  // rejecting sink; explicit dead cycles cannot distort Moore refinement.
  const State absent = UINT32_MAX;
  std::vector<State> mapping(n, absent);
  DFA trimmed;
  for (State state : queue) if (productive[state]) {
    mapping[state] = static_cast<State>(trimmed.nodes.size()); trimmed.nodes.push_back(Node{});
  }
  trimmed.start = mapping[input.start];
  for (State state : queue) if (productive[state]) {
    Node& output = trimmed.nodes[mapping[state]];
    output.accept = input.nodes[state].accept;
    for (auto [label, target] : input.nodes[state].edges)
      if (productive[target]) output.edges.push_back({label, mapping[target]});
  }
  n = trimmed.nodes.size();
  std::vector<State> group(n);
  std::map<bool, State> first_groups;
  for (size_t i = 0; i < n; ++i) {
    bool accept = trimmed.nodes[i].accept;
    auto [it, inserted] = first_groups.emplace(accept, static_cast<State>(first_groups.size()));
    (void)inserted; group[i] = it->second;
  }
  size_t groups = first_groups.size();
  while (true) {
    using Signature = std::pair<State, std::vector<std::pair<Symbol, State>>>;
    std::map<Signature, State> signatures;
    std::vector<State> refined(n);
    for (size_t i = 0; i < n; ++i) {
      budget.tick();
      Signature signature{group[i], {}}; // refine within old groups, never merge them
      for (auto [label, target] : trimmed.nodes[i].edges) {
        budget.tick(); signature.second.push_back({label, group[target]});
      }
      auto [it, inserted] = signatures.emplace(std::move(signature), static_cast<State>(signatures.size()));
      (void)inserted; refined[i] = it->second;
    }
    size_t next_groups = signatures.size();
    group = std::move(refined);
    if (next_groups == groups) break;
    groups = next_groups;
  }
  std::vector<State> representative(groups, absent);
  for (State state = 0; state < n; ++state)
    if (representative[group[state]] == absent) representative[group[state]] = state;
  DFA result;
  std::vector<State> numbered(groups, absent), bfs{group[trimmed.start]};
  numbered[bfs.front()] = 0; result.nodes.push_back(Node{});
  for (size_t head = 0; head < bfs.size(); ++head) {
    const Node& source = trimmed.nodes[representative[bfs[head]]];
    Node output; output.accept = source.accept;
    for (auto [label, target] : source.edges) {
      State target_group = group[target];
      if (numbered[target_group] == absent) {
        numbered[target_group] = static_cast<State>(bfs.size());
        bfs.push_back(target_group); result.nodes.push_back(Node{});
      }
      output.edges.push_back({label, numbered[target_group]});
    }
    result.nodes[head] = std::move(output);
  }
  return result;
}

inline DFA determinize(const NFA& nfa, Budget& budget, Stats* statistics = nullptr) {
  if (nfa.nodes.empty() || nfa.starts.empty()) return empty_language();
  budget.states(nfa.nodes.size());
  size_t arcs = 0;
  for (const auto& node : nfa.nodes) for (auto [label, target] : node.edges) {
    (void)label; budget.tick();
    if (target >= nfa.nodes.size()) throw std::invalid_argument("NFA target outside state set");
    budget.edges(++arcs);
  }
  std::vector<State> initial = nfa.starts;
  for (State state : initial)
    if (state >= nfa.nodes.size()) throw std::invalid_argument("NFA start outside state set");
  std::sort(initial.begin(), initial.end());
  initial.erase(std::unique(initial.begin(), initial.end()), initial.end());
  std::map<std::vector<State>, State> intern;
  std::vector<std::vector<State>> subsets{initial};
  intern.emplace(initial, 0);
  DFA output; output.nodes.push_back(Node{});
  size_t output_arcs = 0;
  for (size_t head = 0; head < subsets.size(); ++head) {
    const auto subset = subsets[head]; // appending subsets must not invalidate this traversal
    Node node;
    std::map<Symbol, std::vector<State>> destinations;
    for (State state : subset) {
      budget.tick(); node.accept = node.accept || nfa.nodes[state].accept;
      for (auto [label, target] : nfa.nodes[state].edges) {
        budget.tick(); destinations[label].push_back(target);
      }
    }
    for (auto& [label, targets] : destinations) {
      std::sort(targets.begin(), targets.end());
      targets.erase(std::unique(targets.begin(), targets.end()), targets.end());
      auto found = intern.find(targets);
      State target;
      if (found == intern.end()) {
        budget.states(subsets.size() + 1);
        target = static_cast<State>(subsets.size());
        intern.emplace(targets, target); subsets.push_back(targets); output.nodes.push_back(Node{});
      } else target = found->second;
      node.edges.push_back({label, target}); budget.edges(++output_arcs);
    }
    output.nodes[head] = std::move(node);
  }
  if (statistics) { statistics->subset_states = output.nodes.size(); statistics->subset_edges = output_arcs; }
  return canonicalize(std::move(output), budget);
}
} // namespace detail

inline DFA canonicalize(DFA input, Limits limits = {}) {
  detail::Budget budget(limits); return detail::canonicalize(std::move(input), budget);
}
inline DFA determinize(const NFA& input, Limits limits = {}) {
  detail::Budget budget(limits); return detail::determinize(input, budget);
}
inline DFA positive_powers(const Word& unit) {
  if (unit.empty()) throw std::invalid_argument("positive powers require a nonempty unit");
  DFA result; result.nodes.resize(unit.size() + 1);
  for (size_t i = 0; i < unit.size(); ++i)
    result.nodes[i].edges.push_back({unit[i], static_cast<State>(i + 1)});
  result.nodes.back().accept = true;
  result.nodes.back().edges.push_back({unit.front(), 1});
  return canonicalize(std::move(result));
}
inline bool accepts(const DFA& dfa, const Word& word) {
  if (dfa.nodes.empty()) return false;
  State state = dfa.start;
  for (Symbol symbol : word) {
    const auto& edges = dfa.nodes.at(state).edges;
    auto found = std::find_if(edges.begin(), edges.end(), [&](auto arc) { return arc.first == symbol; });
    if (found == edges.end()) return false;
    state = found->second;
  }
  return dfa.nodes.at(state).accept;
}
inline std::vector<Word> enumerate_length(const DFA& dfa, size_t length, size_t max_words = 1000000) {
  std::vector<Word> words; Word current;
  if (dfa.nodes.empty()) return words;
  std::function<void(State, size_t)> visit = [&](State state, size_t remaining) {
    if (!remaining) {
      if (dfa.nodes.at(state).accept) {
        if (words.size() >= max_words) throw Limit("regular enumeration word cap");
        words.push_back(current);
      }
      return;
    }
    for (auto [label, target] : dfa.nodes.at(state).edges) {
      current.push_back(label); visit(target, remaining - 1); current.pop_back();
    }
  };
  visit(dfa.start, length);
  std::sort(words.begin(), words.end());
  words.erase(std::unique(words.begin(), words.end()), words.end());
  return words;
}
inline std::optional<Word> shortest_word(const DFA& dfa) {
  if (dfa.nodes.empty()) return std::nullopt;
  const State absent = UINT32_MAX;
  std::vector<State> parent(dfa.nodes.size(), absent), queue{dfa.start};
  std::vector<Symbol> incoming(dfa.nodes.size());
  parent[dfa.start] = dfa.start;
  for (size_t head = 0; head < queue.size(); ++head) {
    State state = queue[head];
    if (dfa.nodes[state].accept) {
      Word word;
      while (state != dfa.start) { word.push_back(incoming[state]); state = parent[state]; }
      std::reverse(word.begin(), word.end()); return word;
    }
    for (auto [label, target] : dfa.nodes[state].edges) if (parent[target] == absent) {
      parent[target] = state; incoming[target] = label; queue.push_back(target);
    }
  }
  return std::nullopt;
}
inline Count add_count(Count a, Count b) {
  if (a.saturated || b.saturated || UINT64_MAX - a.value < b.value) return {UINT64_MAX, true};
  return {a.value + b.value, false};
}
inline Count count_length(const DFA& dfa, size_t length) {
  if (dfa.nodes.empty()) return {};
  std::vector<Count> current(dfa.nodes.size()), next(dfa.nodes.size());
  current.at(dfa.start) = {1, false};
  for (size_t i = 0; i < length; ++i) {
    std::fill(next.begin(), next.end(), Count{});
    for (size_t state = 0; state < dfa.nodes.size(); ++state)
      for (auto [label, target] : dfa.nodes[state].edges) {
        (void)label; next.at(target) = add_count(next[target], current[state]);
      }
    current.swap(next);
  }
  Count count;
  for (size_t state = 0; state < dfa.nodes.size(); ++state)
    if (dfa.nodes[state].accept) count = add_count(count, current[state]);
  return count;
}

struct Choice { uint32_t y; int c; };
using Local = std::function<const std::vector<Choice>&(uint32_t, uint32_t)>;
using Encode = std::function<Symbol(uint32_t, uint32_t, int)>;

// Delayed-output transducer for image(L minus {epsilon}). Only its terminal
// node accepts: a pending state may both continue the input and close a
// nonempty accepted input prefix. An accepting old start is kept unchanged,
// so nonempty input words that revisit it are retained.
inline DFA cyclic_image(const DFA& input, const Local& local, const Encode& encode,
                        Limits limits = {}, Stats* statistics = nullptr) {
  detail::Budget budget(limits);
  if (input.nodes.empty()) return empty_language();
  if (input.start >= input.nodes.size()) throw std::invalid_argument("image start outside state set");
  struct Key {
    State q; uint32_t type, y; int first_c;
    bool operator<(const Key& other) const {
      return std::tie(q, type, y, first_c) < std::tie(other.q, other.type, other.y, other.first_c);
    }
  };
  NFA nfa; nfa.nodes.push_back(Node{true, {}}); // terminal only; never an initial pending node
  std::vector<Key> pending{{0, 0, 0, 0}};
  std::map<Key, State> intern;
  auto state_for = [&](const Key& key) {
    auto found = intern.find(key);
    if (found != intern.end()) return found->second;
    budget.states(nfa.nodes.size() + 1);
    State id = static_cast<State>(nfa.nodes.size());
    intern.emplace(key, id); pending.push_back(key); nfa.nodes.push_back(Node{});
    return id;
  };
  for (auto [symbol, target] : input.nodes[input.start].edges) {
    if (target >= input.nodes.size()) throw std::invalid_argument("image target outside state set");
    uint32_t type = static_cast<uint32_t>(symbol >> 32), id = static_cast<uint32_t>(symbol);
    for (const auto& row : local(type, id)) {
      budget.tick(); nfa.starts.push_back(state_for({target, type, row.y, row.c}));
    }
  }
  std::sort(nfa.starts.begin(), nfa.starts.end());
  nfa.starts.erase(std::unique(nfa.starts.begin(), nfa.starts.end()), nfa.starts.end());
  size_t arc_count = 0;
  for (size_t cursor = 1; cursor < pending.size(); ++cursor) {
    Key key = pending[cursor]; // interning successors can reallocate the arena
    Node node;
    if (input.nodes[key.q].accept) {
      budget.tick(); node.edges.push_back({encode(key.type, key.y, key.first_c), 0});
    }
    for (auto [symbol, target] : input.nodes[key.q].edges) {
      if (target >= input.nodes.size()) throw std::invalid_argument("image target outside state set");
      uint32_t type = static_cast<uint32_t>(symbol >> 32), id = static_cast<uint32_t>(symbol);
      for (const auto& row : local(type, id)) {
        budget.tick();
        State next = state_for({target, type, row.y, key.first_c});
        node.edges.push_back({encode(key.type, key.y, row.c), next});
      }
    }
    std::sort(node.edges.begin(), node.edges.end());
    node.edges.erase(std::unique(node.edges.begin(), node.edges.end()), node.edges.end());
    arc_count += node.edges.size(); budget.edges(arc_count);
    nfa.nodes[cursor] = std::move(node);
  }
  if (statistics) { statistics->nfa_states = nfa.nodes.size(); statistics->nfa_edges = arc_count; }
  DFA result = detail::determinize(nfa, budget, statistics);
  if (statistics) {
    statistics->canonical_states = result.nodes.size(); statistics->canonical_edges = edge_count(result);
    statistics->work = budget.used;
  }
  return result;
}
} // namespace a111r
#endif
