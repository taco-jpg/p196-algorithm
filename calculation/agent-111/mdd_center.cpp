// Exact correlated-frontier MDD adapter for the pinned existing local center
// transfer. Build with mdd_center.py; no generated upstream copy is committed.
#define main a111_existing_frontend_main
#include "a111_existing.hpp"
#undef main
#include "mdd.hpp"
#include <unordered_set>

namespace agent111_mdd {
using Id = a111::MDD::Id;
using Label = a111::MDD::Label;

struct Adapter {
  Fast& fast;
  std::vector<SigTab*> signatures;
  std::unordered_map<uint64_t, std::vector<a111::Choice>> cached;

  Adapter(Fast& source, int layer, bool generic) : fast(source) {
    for (int s = 0; s < fast.NS; ++s) signatures.push_back(fast.sigFor(s, layer, generic));
  }

  const Ent& entry(size_t segment, Label input) {
    SigTab* sig = signatures.at(segment);
    if (input >= fast.sg.at(segment).lidInfo.size()) throw std::logic_error("unknown local state label");
    if (input >= sig->ent.size() || sig->ent[input].start == UNSET)
      fast.fill(static_cast<int>(segment), sig, input);
    return sig->ent[input];
  }

  const std::vector<a111::Choice>& rows(size_t segment, Label input) {
    uint64_t key = (uint64_t(segment) << 32) | input;
    auto found = cached.find(key);
    if (found != cached.end()) return found->second;
    const Ent en = entry(segment, input);
    std::vector<a111::Choice> choices;
    choices.reserve(en.cnt);
    for (uint32_t k = 0; k < en.cnt; ++k) {
      const OutE row = fast.sg[segment].pool[static_cast<size_t>(en.start) + k];
      choices.push_back({row.yid, static_cast<int>(row.c)});
    }
    return cached.emplace(key, std::move(choices)).first->second;
  }

  bool find_row(size_t segment, Label input, uint32_t y, int c, uint32_t& offset) {
    const Ent en = entry(segment, input);
    for (uint32_t k = 0; k < en.cnt; ++k) {
      const OutE row = fast.sg[segment].pool[static_cast<size_t>(en.start) + k];
      if (row.yid == y && static_cast<int>(row.c) == c) {
        offset = en.start + k; return true;
      }
    }
    return false;
  }
};

struct Period {
  bool found = false;
  int start = 0, length = 0;
  std::vector<Id> roots;
  std::vector<std::string> frontier_counts;
};

class Runner {
public:
  Fast fast;
  a111::MDD graph;
  Id initial;
  uint64_t work_cap;
  bool diff;
  size_t diff_limit;
  size_t images = 0, diff_images = 0;

  Runner(size_t nodes, uint64_t work, bool compare, size_t compare_limit)
      : fast(g_cap), graph(static_cast<size_t>(count(v.begin(), v.end(), 1)), nodes),
        initial(0), work_cap(work), diff(compare), diff_limit(compare_limit) {
    if (!setup_instance(2 * (120 + 2 * P + 8))) throw std::logic_error("invalid padded geometry");
    fast.init(order);
    initial = graph.singleton(fast.startState());
  }

  std::string cardinality(Id root) const {
    auto c = graph.count(root);
    return c.saturated ? "at_least_18446744073709551615" : std::to_string(c.value);
  }

  Id image(Id root, int layer, bool generic) {
    Adapter adapter(fast, layer, generic);
    Id result = a111::cyclic_image(
        graph, root,
        [&](size_t s, Label x) -> const std::vector<a111::Choice>& { return adapter.rows(s, x); },
        [&](size_t s, uint32_t y, int c) -> Label { return fast.getLid(static_cast<int>(s), y, c); },
        work_cap);
    ++images;
    if (diff) {
      auto input = graph.enumerate(root, diff_limit);
      std::vector<uint32_t> flat;
      for (const auto& row : input) flat.insert(flat.end(), row.begin(), row.end());
      StateSet explicit_output;
      if (!fast.step(flat, layer, generic, explicit_output))
        throw a111::Limit("DIFF explicit frontier cap");
      std::vector<std::vector<Label>> expected;
      for (size_t i = 0; i < explicit_output.n; ++i)
        expected.emplace_back(explicit_output.data.begin() + i * fast.NS,
                              explicit_output.data.begin() + (i + 1) * fast.NS);
      std::sort(expected.begin(), expected.end());
      auto actual = graph.enumerate(result, diff_limit);
      if (actual != expected) throw std::logic_error("MDD / explicit complete frontier mismatch");
      ++diff_images;
    }
    if (g_sz)
      printf("MDD_LAYER layer=%d mode=%s tuples=%s arena_nodes=%zu images=%zu\n",
             layer + 1, generic ? "generic" : "tail", cardinality(result).c_str(),
             graph.node_count(), images);
    return result;
  }

  Period detect(int horizon) {
    Period answer;
    answer.roots.push_back(initial);
    std::unordered_map<Id, int> seen; // F0 is deliberately omitted: its signature is special.
    for (int layer = 0; layer < horizon; ++layer) {
      Id next = image(answer.roots.back(), layer, true);
      answer.frontier_counts.push_back(cardinality(next));
      if (!next) {
        answer.start = layer + 1; answer.length = 1; answer.found = true;
        answer.roots.push_back(0); return answer;
      }
      auto found = seen.find(next);
      if (found != seen.end()) {
        answer.start = found->second;
        answer.length = static_cast<int>(answer.roots.size()) - found->second;
        answer.found = true; return answer;
      }
      seen[next] = static_cast<int>(answer.roots.size());
      answer.roots.push_back(next);
    }
    return answer;
  }

  bool finite(int width, std::vector<Id>* saved = nullptr) {
    if (!setup_instance(width)) return false;
    Id root = initial;
    if (saved) { saved->clear(); saved->push_back(root); }
    for (int layer = 0; layer < Jall; ++layer) {
      root = image(root, layer, false);
      if (saved) saved->push_back(root);
      if (!root) return false;
    }
    return true;
  }

  bool tail(int width, const Period& periodic) {
    if (!setup_instance(width)) return false;
    int first_tail = *min_element(J.begin(), J.end()) - 1;
    int index = first_tail < periodic.start ? first_tail :
                periodic.start + (first_tail - periodic.start) % periodic.length;
    Id root = periodic.roots.at(index);
    for (int layer = first_tail; layer < Jall && root; ++layer)
      root = image(root, layer, false);
    return root != 0;
  }

  // Select a full correlated predecessor path, never independent coordinate
  // projections. A target lid records (y_i,z_i), hence its required row is
  // (y_i,c_i=z_(i-1)); this closes the temporal segment ring including K=1.
  std::vector<std::vector<int>> witness(int width) {
    std::vector<Id> roots;
    if (!finite(width, &roots)) throw std::logic_error("feasible MDD has no witness frontier");
    std::vector<Label> target = graph.pick(roots.back());
    std::vector<std::vector<uint8_t>> columns(Jall, std::vector<uint8_t>(P, 255));
    for (int layer = Jall - 1; layer >= 0; --layer) {
      Adapter adapter(fast, layer, false);
      std::vector<uint32_t> required_y(fast.NS), row_offset(fast.NS);
      std::vector<int> required_c(fast.NS);
      for (int s = 0; s < fast.NS; ++s) {
        required_y[s] = fast.sg[s].lidInfo.at(target[s]).first;
        int previous = s ? s - 1 : fast.NS - 1;
        required_c[s] = static_cast<int>(fast.sg[previous].lidInfo.at(target[previous]).second);
      }
      std::vector<Label> predecessor(fast.NS);
      std::unordered_set<Id> failed;
      std::function<bool(Id)> choose = [&](Id node) {
        if (!node || failed.count(node)) return false;
        if (node == 1) return true;
        size_t s = graph.level(node);
        for (auto [input, child] : graph.edges(node)) {
          uint32_t offset;
          if (adapter.find_row(s, input, required_y[s], required_c[s], offset) && choose(child)) {
            predecessor[s] = input; row_offset[s] = offset; return true;
          }
        }
        failed.insert(node); return false;
      };
      if (!choose(roots[layer])) throw std::logic_error("MDD witness predecessor missing");
      for (int s = 0; s < fast.NS; ++s) {
        const auto& segment = fast.sg[s];
        for (size_t k = 0; k < segment.times.size(); ++k)
          columns[layer][segment.times[k]] = segment.colpool.at(
              static_cast<size_t>(row_offset[s]) * segment.times.size() + k);
      }
      target = std::move(predecessor);
    }
    if (target != fast.startState()) throw std::logic_error("witness does not reach initial frontier");
    std::vector<std::vector<int>> centers(P);
    for (int t = 0; t < P; ++t) {
      centers[t].resize(m[t]);
      for (int j = 0; j < J[t]; ++j)
        centers[t][j] = centers[t][m[t] - 1 - j] = columns[j][t];
    }
    if (!verify_cycle(centers)) throw std::logic_error("MDD witness failed independent C++ edge replay");
    return centers;
  }
};

int main(int argc, char** argv) {
  bool diff = false;
  uint64_t work_cap = 50000000;
  size_t diff_limit = 1000000;
  int horizon = 120;
  std::vector<char*> filtered{argv[0]};
  try {
    for (int i = 1; i < argc; ++i) {
      std::string opt = argv[i];
      if (opt == "-diff") diff = true;
      else if (opt == "-work-cap" || opt == "-diff-limit" || opt == "-layers") {
        if (++i == argc) throw std::runtime_error("missing MDD option argument");
        long long value = a111_number(argv[i], opt.c_str());
        if (value < 1) throw std::runtime_error("MDD limits must be positive");
        if (opt == "-work-cap") work_cap = static_cast<uint64_t>(value);
        else if (opt == "-diff-limit") diff_limit = static_cast<size_t>(value);
        else {
          if (value > 10000) throw std::runtime_error("supported generic horizon: 1..10000");
          horizon = static_cast<int>(value);
        }
      } else filtered.push_back(argv[i]);
    }
    a111_validate(static_cast<int>(filtered.size()), filtered.data());
  } catch (const std::exception& error) {
    fprintf(stderr, "INVALID_OR_UNSUPPORTED: %s\n", error.what()); return 2;
  }

  b = std::stoi(filtered[1]); es_ = filtered[2]; gs_ = filtered[3]; P = es_.size();
  e.resize(P); g.resize(P); v.assign(P, 0);
  for (int t = 0; t < P; ++t) { e[t] = es_[t] - '0'; g[t] = gs_[t] - '0'; }
  int low = std::stoi(filtered[4]), high = std::stoi(filtered[5]);
  std::string pattern;
  bool all_lengths = false, legacy = false;
  for (size_t i = 6; i < filtered.size(); ++i) {
    std::string opt = filtered[i];
    if (opt == "-v") pattern = filtered[++i];
    else if (opt == "-cap") g_cap = std::stol(filtered[++i]);
    else if (opt == "-allm") all_lengths = true;
    else if (opt == "-w") g_wit = true;
    else if (opt == "-sz") g_sz = true;
    else if (opt == "-legacy") legacy = true;
    else if (opt == "-wlegacy") g_wlegacy = true;
  }
  for (int t = 0; t < P; ++t) v[t] = pattern[t] - '0';
  int K = count(v.begin(), v.end(), 1);
  if (!K || legacy) {
    fprintf(stderr, "MDD_FALLBACK: original engine for zero trims or explicit -legacy\n");
    return a111_existing_frontend_main(static_cast<int>(filtered.size()), filtered.data());
  }

  std::unique_ptr<Runner> runner;
  double start_time = nowsec();
  try {
    runner = std::make_unique<Runner>(static_cast<size_t>(g_cap), work_cap, diff, diff_limit);
    int jstar = 0, per = 0, mlo = low, classes = 0, feasible_classes = 0, tails = 0;
    auto emit_result = [&](int width, bool feasible, const char* tag) {
      std::vector<std::vector<int>> centers;
      if (feasible && g_wit) {
        if (g_wlegacy) {
          std::vector<size_t> sizes;
          if (solve_instance(width, true, g_cap, &centers, &sizes) != 1 || !verify_cycle(centers))
            throw a111::Limit("legacy witness unavailable after exact MDD hit");
        } else centers = runner->witness(width);
      }
      if (g_sz) printf("sizes m0=%d r=%d: MDD\n", width, feasible ? 1 : 0);
      ++g_ninst;
      report(pattern, width, feasible ? 1 : 0, centers, tag);
    };

    if (all_lengths) {
      Period periodic = runner->detect(horizon);
      if (g_sz) {
        fprintf(stderr, "detect sizes:");
        for (const auto& count : periodic.frontier_counts) fprintf(stderr, " %s", count.c_str());
        fprintf(stderr, "\n");
      }
      if (!periodic.found) {
        printf("NOPERIOD b=%d e=%s g=%s v=%s reason=generic_layer_limit horizon=%d\n",
               b, es_.c_str(), gs_.c_str(), pattern.c_str(), horizon);
        printf("DONE idx=%ld v=%s status=noperiod arena_nodes=%zu images=%zu diff_images=%zu sec=%.3f\n",
               rank_of(pattern, K), pattern.c_str(), runner->graph.node_count(), runner->images,
               runner->diff_images, nowsec() - start_time);
        return 0;
      }
      jstar = periodic.start; per = periodic.length;
      bool found_low = false;
      for (mlo = 1; mlo < 100000; ++mlo) {
        if (!setup_instance(mlo)) continue;
        int j0 = *min_element(J.begin(), J.end()) - 1;
        if (j0 >= jstar && mlo > 2 * P) { found_low = true; break; }
      }
      if (!found_low) throw a111::Limit("all-length representative lower-bound limit");
      for (int width = 1; width < mlo; ++width) {
        bool feasible = runner->tail(width, periodic); ++tails;
        emit_result(width, feasible, "FEASIBLE");
      }
      for (int width = mlo; width < mlo + 2 * per; ++width) {
        if (!setup_instance(width)) continue;
        ++classes;
        bool feasible = runner->tail(width, periodic); ++tails;
        if (feasible) ++feasible_classes;
        emit_result(width, feasible, "FEASIBLE_CLASS");
      }
    } else {
      for (int width = low; width <= high; ++width) {
        bool feasible = runner->finite(width); ++tails;
        emit_result(width, feasible, "FEASIBLE");
      }
    }
    printf("DONE idx=%ld v=%s status=%s jstar=%d period=%d mlo=%d classes=%d feasible_classes=%d "
           "arena_nodes=%zu union_cache=%zu images=%zu tails=%d diff_images=%zu sec=%.3f rssMB=%ld\n",
           rank_of(pattern, K), pattern.c_str(), g_count ? "hit" : "none", jstar, per, mlo,
           classes, feasible_classes, runner->graph.node_count(), runner->graph.union_cache_size(),
           runner->images, tails, runner->diff_images, nowsec() - start_time, rss_mb());
    return 0;
  } catch (const a111::Limit& error) {
    fprintf(stderr, "UNDECIDED: %s\n", error.what());
  } catch (const std::bad_alloc&) {
    fprintf(stderr, "UNDECIDED: allocation limit\n");
  } catch (const std::exception& error) {
    fprintf(stderr, "MDD_ERROR: %s\n", error.what()); return 4;
  }
  printf("%s b=%d e=%s g=%s v=%s reason=resource_limit\n", all_lengths ? "NOPERIOD" : "CAPPED",
         b, es_.c_str(), gs_.c_str(), pattern.c_str());
  printf("DONE idx=%ld v=%s status=%s arena_nodes=%zu images=%zu sec=%.3f\n", rank_of(pattern, K),
         pattern.c_str(), all_lengths ? "noperiod" : "capped", runner ? runner->graph.node_count() : 0,
         runner ? runner->images : 0, nowsec() - start_time);
  return 0;
}
} // namespace agent111_mdd

int main(int argc, char** argv) { return agent111_mdd::main(argc, argv); }
