// Independent delayed-output regular-language adapter. Each word contains
// any positive number of repetitions of the unit's ordered segment types.
// Build with regular_center.py; the pinned local transfer is a temporary header.
#define main a111_existing_frontend_main
#include "a111_existing.hpp"
#undef main
#include "regular.hpp"

namespace agent111_regular {
using a111r::DFA;
using a111r::State;
using a111r::Symbol;
using a111r::Word;

static Symbol typed(uint32_t type, uint32_t id) { return (uint64_t(type) << 32) | id; }
static uint32_t type_of(Symbol symbol) { return static_cast<uint32_t>(symbol >> 32); }
static uint32_t id_of(Symbol symbol) { return static_cast<uint32_t>(symbol); }
static bool nonempty(const DFA& dfa) {
  return std::any_of(dfa.nodes.begin(), dfa.nodes.end(), [](const auto& n) { return n.accept; });
}

// One fresh table adapter for each signature. Fast itself persists: equal
// local configurations of a type retain the same symbol IDs across layers.
struct LocalTable {
  Fast& fast;
  std::vector<SigTab*> signatures;
  std::unordered_map<uint64_t, std::vector<a111r::Choice>> cache;

  LocalTable(Fast& source, int layer, bool generic) : fast(source) {
    for (int s = 0; s < fast.NS; ++s) signatures.push_back(fast.sigFor(s, layer, generic));
  }
  Ent entry(uint32_t type, uint32_t input) {
    if (type >= static_cast<uint32_t>(fast.NS) || input >= fast.sg[type].lidInfo.size())
      throw std::logic_error("unknown typed local state");
    SigTab* sig = signatures[type];
    if (input >= sig->ent.size() || sig->ent[input].start == UNSET)
      fast.fill(static_cast<int>(type), sig, input);
    return sig->ent[input];
  }
  const std::vector<a111r::Choice>& rows(uint32_t type, uint32_t input) {
    uint64_t key = typed(type, input);
    auto old = cache.find(key);
    if (old != cache.end()) return old->second;
    Ent range = entry(type, input);
    std::vector<a111r::Choice> rows;
    rows.reserve(range.cnt);
    for (uint32_t i = 0; i < range.cnt; ++i) {
      OutE row = fast.sg[type].pool.at(static_cast<size_t>(range.start) + i);
      rows.push_back({row.yid, static_cast<int>(row.c)});
    }
    return cache.emplace(key, std::move(rows)).first->second;
  }
  bool find(uint32_t type, uint32_t input, uint32_t y, int c, uint32_t& offset) {
    Ent range = entry(type, input);
    for (uint32_t i = 0; i < range.cnt; ++i) {
      OutE row = fast.sg[type].pool.at(static_cast<size_t>(range.start) + i);
      if (row.yid == y && static_cast<int>(row.c) == c) { offset = range.start + i; return true; }
    }
    return false;
  }
};

struct Period {
  bool found = false;
  int start = 0, length = 0;
  std::vector<DFA> frontiers;
};

struct Runner {
  Fast fast;
  DFA initial;
  a111r::Limits limits;
  size_t images = 0;
  int export_layer = -1, export_k = 1;
  size_t export_limit = 1000000;

  explicit Runner(a111r::Limits bounds) : fast(g_cap), limits(bounds) {
    if (!setup_instance(2 * (120 + 2 * P + 8))) throw std::logic_error("invalid unit geometry");
    fast.init(order);
    Word unit;
    const auto start = fast.startState();
    for (uint32_t s = 0; s < start.size(); ++s) unit.push_back(typed(s, start[s]));
    initial = a111r::positive_powers(unit);
  }

  std::string count(const DFA& dfa, int repetitions) const {
    auto n = a111r::count_length(dfa, static_cast<size_t>(fast.NS) * repetitions);
    return n.saturated ? "at_least_18446744073709551615" : std::to_string(n.value);
  }

  void export_words(const DFA& dfa, int layer) {
    if (layer != export_layer) return;
    const size_t length = static_cast<size_t>(fast.NS) * export_k;
    auto words = a111r::enumerate_length(dfa, length, export_limit);
    for (const auto& word : words) {
      printf("REGULAR_WORD layer=%d k=%d word=[", layer, export_k);
      for (size_t i = 0; i < word.size(); ++i) {
        uint32_t s = type_of(word[i]);
        auto [y, z] = fast.sg.at(s).lidInfo.at(id_of(word[i]));
        const std::string& cfg = fast.sg[s].cfg.at(y);
        printf("%s{\"type\":%u,\"z\":%d,\"cfg\":[", i ? "," : "", s, static_cast<int>(z));
        for (size_t j = 0; j < cfg.size(); ++j)
          printf("%s%u", j ? "," : "", static_cast<unsigned>(static_cast<uint8_t>(cfg[j])));
        printf("]}");
      }
      printf("]\n");
    }
    printf("REGULAR_EXPORT layer=%d k=%d words=%zu\n", layer, export_k, words.size());
    fflush(stdout);
  }

  DFA image(const DFA& source, int layer, bool generic) {
    LocalTable table(fast, layer, generic);
    a111r::Stats stats;
    DFA output = a111r::cyclic_image(
        source,
        [&](uint32_t s, uint32_t x) -> const std::vector<a111r::Choice>& { return table.rows(s, x); },
        [&](uint32_t s, uint32_t y, int c) { return typed(s, fast.getLid(s, y, c)); },
        limits, &stats);
    ++images;
    if (g_sz) {
      printf("REGULAR_LAYER layer=%d mode=%s nfa_states=%zu nfa_edges=%zu subset_states=%zu "
             "subset_edges=%zu states=%zu edges=%zu work=%llu count1=%s count2=%s count3=%s\n",
             layer + 1, generic ? "generic" : "tail", stats.nfa_states, stats.nfa_edges,
             stats.subset_states, stats.subset_edges, output.nodes.size(), a111r::edge_count(output),
             static_cast<unsigned long long>(stats.work), count(output, 1).c_str(),
             count(output, 2).c_str(), count(output, 3).c_str());
      fflush(stdout);
    }
    if (generic) export_words(output, layer + 1);
    return output;
  }

  Period detect(int horizon) {
    Period period; period.frontiers.push_back(initial);
    export_words(initial, 0);
    for (int j = 0; j < horizon; ++j) {
      DFA next = image(period.frontiers.back(), j, true);
      if (!nonempty(next)) {
        period.found = true; period.start = j + 1; period.length = 1;
        period.frontiers.push_back(std::move(next)); return period;
      }
      // F0 has a special signature and cannot be used as a recurrence witness.
      for (size_t old = 1; old < period.frontiers.size(); ++old) if (next == period.frontiers[old]) {
        period.found = true; period.start = static_cast<int>(old);
        period.length = static_cast<int>(period.frontiers.size() - old); return period;
      }
      period.frontiers.push_back(std::move(next));
    }
    return period;
  }

  DFA finite(int width, std::vector<DFA>* saved = nullptr) {
    if (!setup_instance(width)) return a111r::empty_language();
    DFA frontier = initial;
    if (saved) { saved->clear(); saved->push_back(frontier); }
    for (int j = 0; j < Jall; ++j) {
      frontier = image(frontier, j, false);
      if (saved) saved->push_back(frontier);
      if (!nonempty(frontier)) break;
    }
    return frontier;
  }

  DFA tail(int width, const Period& period) {
    if (!setup_instance(width)) return a111r::empty_language();
    int first_tail = *std::min_element(J.begin(), J.end()) - 1;
    int index = first_tail < period.start ? first_tail :
                period.start + (first_tail - period.start) % period.length;
    DFA frontier = period.frontiers.at(index);
    for (int j = first_tail; j < Jall && nonempty(frontier); ++j) frontier = image(frontier, j, false);
    return frontier;
  }

  // At fixed output length, find one FULL accepting predecessor path in the
  // old DFA, constrained by each local output row. Merging reachable states
  // at an equal position preserves one complete prefix, never projections.
  Word predecessor(const DFA& old, const Word& target, LocalTable& table,
                   std::vector<uint32_t>& row_offsets) {
    struct Back { State previous; Symbol input; uint32_t row; };
    std::vector<std::map<State, Back>> levels(target.size() + 1);
    levels[0].emplace(old.start, Back{old.start, 0, 0});
    uint64_t work = 0;
    for (size_t i = 0; i < target.size(); ++i) {
      uint32_t type = type_of(target[i]);
      if (type != i % fast.NS) throw std::logic_error("unexpected accepted type sequence");
      auto [y, unused_z] = fast.sg[type].lidInfo.at(id_of(target[i]));
      (void)unused_z;
      Symbol previous = target[(i + target.size() - 1) % target.size()];
      int c = fast.sg[type_of(previous)].lidInfo.at(id_of(previous)).second;
      for (const auto& [state, back] : levels[i]) {
        (void)back;
        for (auto [symbol, next] : old.nodes.at(state).edges) {
          if (++work > limits.work) throw a111r::Limit("regular witness work cap");
          if (type_of(symbol) != type || levels[i + 1].count(next)) continue;
          uint32_t offset;
          if (table.find(type, id_of(symbol), y, c, offset))
            levels[i + 1].emplace(next, Back{state, symbol, offset});
        }
      }
      if (levels[i + 1].empty()) throw std::logic_error("regular predecessor path missing");
    }
    State end = UINT32_MAX;
    for (const auto& [state, back] : levels.back()) {
      (void)back; if (old.nodes.at(state).accept) { end = state; break; }
    }
    if (end == UINT32_MAX) throw std::logic_error("regular predecessor has no accepting endpoint");
    Word result(target.size()); row_offsets.resize(target.size());
    for (size_t i = target.size(); i > 0; --i) {
      const Back back = levels[i].at(end);
      result[i - 1] = back.input; row_offsets[i - 1] = back.row; end = back.previous;
    }
    if (end != old.start || !a111r::accepts(old, result)) throw std::logic_error("invalid predecessor path");
    return result;
  }

  // Rebuild all actual finite layers, choose a shortest accepted word, and
  // recover its local coefficient columns backwards. The resulting temporal
  // period can exceed the unit's fixed-array bound; replay uses dynamic arrays.
  std::vector<std::vector<int>> witness(int width) {
    std::vector<DFA> fronts;
    DFA last = finite(width, &fronts);
    auto selected = a111r::shortest_word(last);
    if (!selected || selected->empty() || selected->size() % fast.NS)
      throw std::logic_error("regular hit has no nonempty typed witness");
    Word target = *selected;
    size_t repetitions = target.size() / fast.NS;
    if (repetitions > 1000000 / static_cast<size_t>(P))
      throw a111r::Limit("regular witness temporal-length cap");
    size_t total = repetitions * P;
    if (total > limits.work / static_cast<size_t>(std::max(Jall, 1)))
      throw a111r::Limit("regular witness column cap");
    std::vector<std::vector<uint8_t>> columns(Jall, std::vector<uint8_t>(total, 255));
    int anchor = fast.sg.front().times.front();
    for (int j = Jall - 1; j >= 0; --j) {
      LocalTable table(fast, j, false);
      std::vector<uint32_t> offsets;
      Word previous = predecessor(fronts.at(j), target, table, offsets);
      for (size_t i = 0; i < target.size(); ++i) {
        uint32_t s = type_of(target[i]); const auto& seg = fast.sg[s];
        for (size_t q = 0; q < seg.times.size(); ++q) {
          int t = seg.times[q];
          size_t actual = ((i / fast.NS) * P + t + (t < anchor ? P : 0)) % total;
          columns[j][actual] = seg.colpool.at(static_cast<size_t>(offsets[i]) * seg.times.size() + q);
        }
      }
      target = std::move(previous);
    }
    if (!a111r::accepts(initial, target)) throw std::logic_error("witness misses initial positive powers");
    std::vector<std::vector<int>> centers(total);
    for (size_t t = 0; t < total; ++t) {
      int phase = t % P; centers[t].resize(m[phase]);
      for (int j = 0; j < J[phase]; ++j)
        centers[t][j] = centers[t][m[phase] - 1 - j] = columns[j][t];
      for (int x : centers[t]) if (x < 0 || x > 2 * b - 2)
        throw std::logic_error("witness coefficient outside center domain");
    }
    for (size_t t = 0; t < total; ++t) {
      std::vector<int> next; int phase = t % P;
      if (!cstep_forced(centers[t], e[phase], g[phase], v[phase], next) ||
          next != centers[(t + 1) % total]) throw std::logic_error("regular witness arithmetic replay failed");
    }
    return centers;
  }
};

int main(int argc, char** argv) {
  int horizon = 120, export_layer = -1, export_k = 1;
  size_t export_limit = 1000000;
  a111r::Limits limits;
  bool generic_only = false;
  std::vector<char*> filtered{argv[0]};
  try {
    for (int i = 1; i < argc; ++i) {
      std::string option = argv[i];
      if (option == "-generic-only") generic_only = true;
      else if (option == "-layers" || option == "-work-cap" || option == "-edge-cap" ||
               option == "-export-layer" || option == "-export-k" || option == "-export-limit") {
        if (++i == argc) throw std::invalid_argument("missing regular option argument");
        long long value = a111_number(argv[i], option.c_str());
        if (value < (option == "-export-layer" ? 0 : 1))
          throw std::invalid_argument("regular limits must be positive (export layer may be zero)");
        if (option == "-work-cap") limits.work = value;
        else if (option == "-edge-cap") limits.edges = value;
        else if (option == "-export-limit") export_limit = value;
        else if (option == "-export-k") {
          if (value > 10000) throw std::invalid_argument("export repetition cap is 10000");
          export_k = value;
        } else {
          if (value > 10000) throw std::invalid_argument("generic layer cap is 10000");
          if (option == "-layers") horizon = value; else export_layer = value;
        }
      } else filtered.push_back(argv[i]);
    }
    a111_validate(static_cast<int>(filtered.size()), filtered.data());
  } catch (const std::exception& error) {
    fprintf(stderr, "INVALID_OR_UNSUPPORTED: %s\n", error.what()); return 2;
  }
  b = std::stoi(filtered[1]); es_ = filtered[2]; gs_ = filtered[3]; P = es_.size();
  e.resize(P); g.resize(P); v.resize(P);
  for (int t = 0; t < P; ++t) { e[t] = es_[t] - '0'; g[t] = gs_[t] - '0'; }
  int low = std::stoi(filtered[4]), high = std::stoi(filtered[5]);
  bool all_widths = false, forbidden_legacy = false;
  std::string pattern;
  for (size_t i = 6; i < filtered.size(); ++i) {
    std::string option = filtered[i];
    if (option == "-v") pattern = filtered[++i];
    else if (option == "-cap") { g_cap = std::stol(filtered[++i]); limits.states = g_cap; }
    else if (option == "-allm") all_widths = true;
    else if (option == "-sz") g_sz = true;
    else if (option == "-w") g_wit = true;
    else if (option == "-legacy" || option == "-wlegacy") forbidden_legacy = true;
  }
  for (int t = 0; t < P; ++t) v[t] = pattern[t] - '0';
  int K = std::count(v.begin(), v.end(), 1);
  if (!K || forbidden_legacy || (export_layer >= 0 && !generic_only && !all_widths)) {
    fprintf(stderr, "INVALID_OR_UNSUPPORTED: regular engine requires trims, no legacy fallback, and generic mode for export\n");
    return 2;
  }
  double started = nowsec();
  std::unique_ptr<Runner> runner;
  try {
    runner = std::make_unique<Runner>(limits);
    runner->export_layer = export_layer; runner->export_k = export_k; runner->export_limit = export_limit;
    int jstar = 0, per = 0, mlo = low, classes = 0, feasible_classes = 0, tails = 0, hits = 0;
    auto emit = [&](int width, const DFA& result, const char* tag) {
      ++tails;
      if (!nonempty(result)) return;
      // A regular-language hit is checked by reconstructing and replaying a
      // concrete finite period even when the caller omits witness printing.
      auto centers = runner->witness(width);
      ++hits;
      printf("%s b=%d e=%s g=%s v=%s m0=%d repeats=%zu actual_period=%zu replay=ok",
             tag, b, es_.c_str(), gs_.c_str(), pattern.c_str(), width, centers.size() / P, centers.size());
      if (g_wit) for (size_t t = 0; t < centers.size(); ++t) {
        printf(" C%zu=[", t);
        for (size_t i = 0; i < centers[t].size(); ++i) printf("%s%d", i ? "," : "", centers[t][i]);
        printf("]");
      }
      printf("\n"); fflush(stdout);
    };
    if (generic_only || all_widths) {
      Period period = runner->detect(horizon);
      if (!period.found) throw a111r::Limit("generic layer horizon=" + std::to_string(horizon));
      jstar = period.start; per = period.length;
      printf("REGULAR_PERIOD jstar=%d period=%d equality=full_canonical_DFA\n", jstar, per); fflush(stdout);
      if (generic_only) {
        printf("DONE v=%s status=generic_period jstar=%d period=%d images=%zu sec=%.3f rssMB=%ld\n",
               pattern.c_str(), jstar, per, runner->images, nowsec() - started, rss_mb());
        return 0;
      }
      bool lower_found = false;
      for (mlo = 1; mlo < 100000; ++mlo) {
        if (!setup_instance(mlo)) continue;
        if (*std::min_element(J.begin(), J.end()) - 1 >= jstar && mlo > 2 * P) {
          lower_found = true; break;
        }
      }
      if (!lower_found) throw a111r::Limit("all-width representative bound");
      for (int width = 1; width < mlo; ++width) emit(width, runner->tail(width, period), "FEASIBLE");
      for (int width = mlo; width < mlo + 2 * per; ++width) {
        ++classes;
        DFA result = runner->tail(width, period);
        if (nonempty(result)) ++feasible_classes;
        emit(width, result, "FEASIBLE_CLASS");
      }
    } else {
      for (int width = low; width <= high; ++width) emit(width, runner->finite(width), "FEASIBLE");
    }
    printf("DONE v=%s status=%s quantifier=all_positive_repetitions jstar=%d period=%d mlo=%d "
           "classes=%d feasible_classes=%d images=%zu tails=%d sec=%.3f rssMB=%ld\n",
           pattern.c_str(), hits ? "hit" : "none", jstar, per, mlo, classes, feasible_classes,
           runner->images, tails, nowsec() - started, rss_mb());
    return 0;
  } catch (const a111r::Limit& error) {
    fprintf(stderr, "UNDECIDED: %s\n", error.what());
  } catch (const std::bad_alloc&) {
    fprintf(stderr, "UNDECIDED: allocation limit\n");
  } catch (const std::exception& error) {
    fprintf(stderr, "REGULAR_ERROR: %s\n", error.what()); return 4;
  }
  printf("%s b=%d e=%s g=%s v=%s reason=resource_limit\n",
         all_widths || generic_only ? "NOPERIOD" : "CAPPED", b, es_.c_str(), gs_.c_str(), pattern.c_str());
  printf("DONE v=%s status=%s images=%zu sec=%.3f\n", pattern.c_str(),
         all_widths || generic_only ? "noperiod" : "capped", runner ? runner->images : 0, nowsec() - started);
  return 0;
}
} // namespace agent111_regular

int main(int argc, char** argv) { return agent111_regular::main(argc, argv); }
