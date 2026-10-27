// Independent complete-frontier export through the original explicit Fast.
// Build against the temporary header from long_center.patched_source().
#define main a111_explicit_original_frontend
#include "a111_existing.hpp"
#undef main

int main(int argc, char** argv) {
  try {
    int layers = -1, unit_k = -1;
    std::vector<char*> filtered{argv[0]};
    for (int i = 1; i < argc; ++i) {
      std::string option = argv[i];
      if (option == "-layers" || option == "-unit-k") {
        if (++i == argc) throw std::runtime_error("missing explicit export option value");
        long long value = a111_number(argv[i], option.c_str());
        if (option == "-layers") {
          if (layers != -1 || value < 1 || value > 8)
            throw std::runtime_error("require exactly one -layers in 1..8");
          layers = static_cast<int>(value);
        } else {
          if (unit_k != -1 || value < 1 || value > MAXNS)
            throw std::runtime_error("require exactly one -unit-k in 1..MAXNS");
          unit_k = static_cast<int>(value);
        }
      } else filtered.push_back(argv[i]);
    }
    a111_validate(static_cast<int>(filtered.size()), filtered.data());
    if (layers < 1 || unit_k < 1)
      throw std::runtime_error("explicit export requires -layers and -unit-k");
    b = static_cast<int>(a111_number(filtered[1], "base"));
    es_ = filtered[2]; gs_ = filtered[3]; P = static_cast<int>(es_.size());
    std::string pattern;
    for (size_t i = 6; i < filtered.size(); ++i) {
      std::string option = filtered[i];
      if (option == "-v") pattern = filtered[++i];
      else if (option == "-cap") g_cap = static_cast<long>(a111_number(filtered[++i], "cap"));
      else if (option != "-q" && option != "-sz")
        throw std::runtime_error("explicit export supports only -v, -cap, -q, -sz");
    }
    e.resize(P); g.resize(P); v.resize(P);
    for (int t = 0; t < P; ++t) {
      e[t] = es_[t] - '0'; g[t] = gs_[t] - '0'; v[t] = pattern[t] - '0';
    }
    int segments = std::count(v.begin(), v.end(), 1);
    if (!segments || segments % unit_k)
      throw std::runtime_error("unit-k must divide the positive segment count");
    int repetitions = segments / unit_k;
    if (P % repetitions) throw std::runtime_error("unit repetition does not divide period");
    int unit_period = P / repetitions;
    for (int t = 0; t < P; ++t)
      if (e[t] != e[t % unit_period] || g[t] != g[t % unit_period] ||
          v[t] != v[t % unit_period])
        throw std::runtime_error("driver and trim must repeat the declared unit");
    if (!setup_instance(2 * (layers + 2 * P + 8)) || noV)
      throw std::runtime_error("invalid explicit generic geometry");
    Fast fast(g_cap);
    fast.init(order);
    std::vector<uint32_t> frontier = fast.startState();
    for (int j = 0; j < layers; ++j) {
      StateSet output;
      if (!fast.step(frontier, j, true, output))
        throw std::runtime_error("explicit generic frontier cap");
      frontier = std::move(output.data);
      printf("EXPLICIT_LAYER layer=%d tuples=%zu\n", j + 1, frontier.size() / fast.NS);
      fflush(stdout);
    }
    for (size_t at = 0; at < frontier.size(); at += fast.NS) {
      printf("EXPLICIT_WORD layer=%d word=[", layers);
      for (int s = 0; s < fast.NS; ++s) {
        auto [y, z] = fast.sg.at(s).lidInfo.at(frontier[at + s]);
        const std::string& cfg = fast.sg[s].cfg.at(y);
        printf("%s{\"type\":%d,\"z\":%d,\"cfg\":[", s ? "," : "", s % unit_k,
               static_cast<int>(z));
        for (size_t q = 0; q < cfg.size(); ++q)
          printf("%s%u", q ? "," : "", static_cast<unsigned>(static_cast<uint8_t>(cfg[q])));
        printf("]}");
      }
      printf("]\n");
    }
    printf("EXPLICIT_DONE layer=%d tuples=%zu unit_k=%d repetitions=%d\n", layers,
           frontier.size() / fast.NS, unit_k, repetitions);
    return 0;
  } catch (const std::exception& error) {
    fprintf(stderr, "UNDECIDED explicit_export: %s\n", error.what()); return 2;
  } catch (...) {
    fprintf(stderr, "UNDECIDED explicit_export: unexpected exception\n"); return 2;
  }
}
