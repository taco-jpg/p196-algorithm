// Exact fixed-(e,g) exterior reachability, with independently derived inverse gaps.
// The physical first column uses the existing forward B relation unchanged.
// Every subsequent column is generic.  Backward search has one neutral target.
// A completed negative covers every finite width for this prescribed driver;
// a resource/depth interruption is always UNDECIDED.
//
// Build: c++ -O2 -std=c++17 calculation/agent-117/fixed_driver_exterior.cpp -o /tmp/fixed_driver_exterior
// Run:   /tmp/fixed_driver_exterior --cap 1000000 --seconds 30
// Local relation audit: --mode predecessors --L BITSTRING --H BITSTRING --Y d,d,...
// Y digits are ordered by increasing phase t with g[t]=1.
#define main agent117_original_bauto_main
#include "../neutral_band/structure/bauto.cpp"
#undef main

#include <array>
#include <charconv>
#include <csignal>
#include <limits>
#include <set>
#include <sstream>
#include <stdexcept>
#include <sys/resource.h>
#include <unistd.h>

namespace fixed_driver {
constexpr int MAX_PERIOD = 32;
using Column = array<uint8_t, MAX_PERIOD>;
const string DEFAULT_E = "010100110100101011001011";
const string DEFAULT_G = "110001001000110001001000";

struct Options {
  string es = DEFAULT_E, gs = DEFAULT_G, mode = "search", ls, hs, ys;
  uint64_t cap = 1000000, operations = 100000000;
  int base = 10, seconds = 30, memory_mb = 4096, max_depth = -1;
  bool dump_states = false;
};
struct Statistics {
  uint64_t operations = 0, arcs = 0, expanded = 0;
  uint64_t forward_transitions = 0, forward_expanded = 0;
  size_t initial = 0, visited = 0, maximum_predecessors = 0;
  size_t forward_visited = 0;
  int complete_depth = -1;
  int forward_complete_depth = -1;
  bool forward_exhausted = false;
  uint64_t accepting_emissions = 0, accepting_expansions = 0;
  set<u64> accepted_e;
  vector<size_t> frontiers;
  vector<size_t> forward_frontiers;
  chrono::steady_clock::time_point start = chrono::steady_clock::now();
};
struct Stop : exception {
  string reason;
  explicit Stop(string why) : reason(std::move(why)) {}
  const char* what() const noexcept override { return reason.c_str(); }
};
struct Budget {
  const Options& o; Statistics& s;
  void tick() {
    if (++s.operations > o.operations) throw Stop("OPERATION_CAP");
    if ((s.operations & 1023) == 0 &&
        chrono::duration<double>(chrono::steady_clock::now() - s.start).count() >= o.seconds)
      throw Stop("TIMEOUT");
  }
};
struct Edge { K128 key; Column column; };
struct Node { K128 key; uint32_t next; uint32_t depth; Column column; };

// Async-signal-safe fallback also interrupts the unchanged forward generator.
void wall_alarm(int) {
  const char msg[] = "{\"format\":\"agent117-fixed-driver-exterior-v1\",\"status\":\"TIMEOUT\",\"decision\":\"UNDECIDED\",\"complete\":false,\"reason\":\"hard wall-clock guard\"}\n";
  (void)!write(STDOUT_FILENO, msg, sizeof(msg) - 1);
  _exit(124);
}

uint64_t number(const string& s, const char* name) {
  if (s.empty()) throw invalid_argument(string("empty ") + name);
  uint64_t out = 0;
  auto r = from_chars(s.data(), s.data() + s.size(), out);
  if (r.ec != errc() || r.ptr != s.data() + s.size())
    throw invalid_argument(string("invalid unsigned decimal ") + name);
  return out;
}
Options parse(int argc, char** argv) {
  Options o;
  for (int i = 1; i < argc; ++i) {
    string a = argv[i];
    if (a == "--dump-states") { o.dump_states = true; continue; }
    if (a == "--help") {
      puts("fixed_driver_exterior [--mode search|bidirectional] [--base 2..62] [--e BITS --g BITS] [--cap N] [--seconds 1..1500] [--ops N] [--memory-mb 64..4096] [--max-depth N] [--dump-states]\n  --mode predecessors --L BITS --H BITS --Y d,d,...  emits exact unique predecessors (cap <= 10000)");
      exit(0);
    }
    if (i + 1 >= argc) throw invalid_argument("missing option value");
    string value = argv[++i];
    if (a == "--e") o.es = value;
    else if (a == "--g") o.gs = value;
    else if (a == "--mode") o.mode = value;
    else if (a == "--L") o.ls = value;
    else if (a == "--H") o.hs = value;
    else if (a == "--Y") o.ys = value;
    else if (a == "--cap") o.cap = number(value, "cap");
    else if (a == "--ops") o.operations = number(value, "ops");
    else {
      uint64_t n = number(value, a.c_str());
      if (n > numeric_limits<int>::max()) throw invalid_argument("integer option exceeds INT_MAX");
      if (a == "--base") o.base = static_cast<int>(n);
      else if (a == "--seconds") o.seconds = static_cast<int>(n);
      else if (a == "--memory-mb") o.memory_mb = static_cast<int>(n);
      else if (a == "--max-depth") o.max_depth = static_cast<int>(n);
      else throw invalid_argument("unknown option " + a);
    }
  }
  if (o.base < 2 || o.base > 62) throw invalid_argument("supported bases are 2..62");
  if (o.gs.empty() || o.gs.size() > MAX_PERIOD || o.es.size() != o.gs.size())
    throw invalid_argument("equal nonempty e/g lengths 1..32 are required");
  for (char c : o.gs + o.es) if (c != '0' && c != '1') throw invalid_argument("e/g must be binary");
  if (o.gs.find('1') == string::npos) throw invalid_argument("this gap-factorized solver requires positive overflow");
  if (o.cap < 1 || o.cap > 20000000 || o.operations < 1 || o.operations > 5000000000ULL)
    throw invalid_argument("unsupported cap or operation budget");
  if (o.seconds < 1 || o.seconds > 1500 || o.memory_mb < 64 || o.memory_mb > 4096)
    throw invalid_argument("unsupported wall-clock or memory budget");
  if (o.mode != "search" && o.mode != "bidirectional" && o.mode != "predecessors") throw invalid_argument("unsupported mode");
  if ((o.dump_states || o.mode == "predecessors") && o.cap > 10000)
    throw invalid_argument("explicit state output requires cap <= 10000");
  return o;
}
u64 bits(const string& s) {
  if (static_cast<int>(s.size()) != p) throw invalid_argument("carry bitstring has wrong length");
  u64 out = 0;
  for (int t = 0; t < p; ++t) {
    if (s[t] != '0' && s[t] != '1') throw invalid_argument("carry bitstring must be binary");
    out |= u64(s[t] - '0') << t;
  }
  return out;
}
void initialize(const Options& o) {
  b = o.base; p = static_cast<int>(o.gs.size());
  g.assign(p, 0); Gidx.clear();
  for (int t = 0; t < p; ++t) if ((g[t] = o.gs[t] - '0')) Gidx.push_back(t);
  ydig = 1; while ((1 << ydig) < b) ++ydig;
  if (2 * p + ydig * static_cast<int>(Gidx.size()) > 127)
    throw invalid_argument("exact 127-bit packing bound exceeded");
}
void guards(const Options& o) {
  rlimit lim;
  if (getrlimit(RLIMIT_AS, &lim)) throw runtime_error("getrlimit failed");
  rlim_t requested = static_cast<rlim_t>(o.memory_mb) * 1024 * 1024;
  lim.rlim_cur = min(lim.rlim_max, requested);
  if (setrlimit(RLIMIT_AS, &lim)) throw runtime_error("setrlimit failed");
  signal(SIGALRM, wall_alarm);
  alarm(o.seconds);
}

// For a successor cut (A,Hn,D), an overflow fixes its column x uniquely.
// Put d=D-Hn. Interior d gives x=d+b*A; d=-1 or b-1 gives x=b-1.
// From each next overflow, walk the intervening g=0 gap backwards.  For
// candidate old carries l,h, 2*x = next_x-l-Hn+b*(A+h); all divisions and
// bounds are checked.  At the preceding overflow old Y=next_x-low_digit.
// The gaps have disjoint old-cut fields; their Cartesian product is exact.
struct Inverse {
  u64 A, Hn;
  array<int, MAX_PERIOD> D{}, forced{};
  Budget& budget;
  vector<vector<Edge>> pieces;
  Column work{};

  Inverse(K128 target, Budget& bg) : budget(bg) {
    int yy[64]; unpack(target, A, Hn, yy, static_cast<int>(Gidx.size()));
    forced.fill(-1); D.fill(-1);
    for (size_t i = 0; i < Gidx.size(); ++i) {
      int t = Gidx[i], d = yy[i] - int((Hn >> t) & 1);
      D[t] = yy[i];
      forced[t] = (d == -1 || d == b - 1) ? b - 1 : d + b * int((A >> t) & 1);
    }
  }
  void gap(int slot, int t, int next_x, u64 L, u64 H, vector<Edge>& out) {
    budget.tick();
    int a = Gidx[slot], at = int((A >> t) & 1), ht = int((Hn >> t) & 1);
    if (t == a) {
      int x = forced[t];
      for (int l = 0; l < 2; ++l) {
        if (x < 0 || x > 2 * b - 2 || (x + l) / b != at || (x + ht) % b != D[t]) continue;
        int h = (x + ht) / b, y = next_x - (x + l) % b;
        if (h > 1 || y < 0 || y >= b) continue;
        work[t] = static_cast<uint8_t>(x);
        K128 key = K128(L | (u64(l) << t)) | (K128(H | (u64(h) << t)) << p);
        key |= K128(y) << (2 * p + ydig * slot);
        if (out.size() >= budget.o.cap) throw Stop("LOCAL_GAP_CAP");
        out.push_back({key, work});
      }
      return;
    }
    for (int l = 0; l < 2; ++l) for (int h = 0; h < 2; ++h) {
      int numerator = next_x - l - ht + b * (at + h);
      if (numerator % 2) continue;
      int x = numerator / 2;
      if (x < 0 || x > 2 * b - 2 || (x + l) / b != at || (x + ht) / b != h) continue;
      if ((x + l) % b + (x + ht) % b != next_x) throw logic_error("inverse local identity");
      work[t] = static_cast<uint8_t>(x);
      gap(slot, (t + p - 1) % p, x, L | (u64(l) << t), H | (u64(h) << t), out);
    }
  }
  bool build() {
    pieces.resize(Gidx.size());
    for (size_t i = 0; i < Gidx.size(); ++i) {
      work.fill(255);
      int end = Gidx[(i + 1) % Gidx.size()];
      gap(static_cast<int>(i), (end + p - 1) % p, forced[end], 0, 0, pieces[i]);
      auto& v = pieces[i];
      sort(v.begin(), v.end(), [](const Edge& x, const Edge& y) { return x.key < y.key; });
      v.erase(unique(v.begin(), v.end(), [](const Edge& x, const Edge& y) { return x.key == y.key; }), v.end());
      if (v.empty()) return false;
    }
    return true;
  }
  template<class F> void product(size_t i, K128 key, Column& col, F& emit) {
    budget.tick();
    if (i == pieces.size()) { emit(key, col); return; }
    int a = Gidx[i], end = Gidx[(i + 1) % Gidx.size()];
    for (const Edge& piece : pieces[i]) {
      int t = a;
      do { col[t] = piece.column[t]; t = (t + 1) % p; } while (t != end);
      product(i + 1, key | piece.key, col, emit);
    }
  }
  template<class F> void run(F emit) {
    if (!build()) return;
    Column col{};
    product(0, 0, col, emit);
  }
};

string bit_string(u64 x) {
  string r; for (int t = 0; t < p; ++t) r += char('0' + ((x >> t) & 1)); return r;
}
void print_state(K128 key) {
  u64 L, H; int Y[64]; unpack(key, L, H, Y, static_cast<int>(Gidx.size()));
  printf("{\"L\":\"%s\",\"H\":\"%s\",\"Y\":[", bit_string(L).c_str(), bit_string(H).c_str());
  for (size_t i = 0; i < Gidx.size(); ++i) printf("%s%d", i ? "," : "", Y[i]);
  printf("]}");
}
void print_column(const Column& x) {
  printf("["); for (int t = 0; t < p; ++t) printf("%s%u", t ? "," : "", unsigned(x[t])); printf("]");
}
void audit_acceptance(Statistics& s, u64 L, u64 H, const int* Y, bool expansion) {
  if (!accepting(L, H, Y, static_cast<int>(Gidx.size()))) return;
  s.accepted_e.insert(L);
  if (expansion) ++s.accepting_expansions; else ++s.accepting_emissions;
}
void header(const Options& o, const Statistics& s, const string& status, const string& decision, bool complete) {
  printf("{\"format\":\"agent117-fixed-driver-exterior-v1\",\"base\":%d,\"e\":\"%s\",\"g\":\"%s\",\"mode\":\"%s\",\"status\":\"%s\",\"decision\":\"%s\",\"complete\":%s,\"initial_states\":%zu,\"reverse_visited\":%zu,\"reverse_expanded\":%llu,\"reverse_arcs\":%llu,\"maximum_predecessors\":%zu,\"complete_depth\":%d,\"operations\":%llu,\"cap\":%llu,\"operation_cap\":%llu,\"seconds\":%d,\"memory_mb\":%d,\"elapsed_seconds\":%.6f,\"reverse_frontiers\":[",
      b, o.es.c_str(), o.gs.c_str(), o.mode.c_str(), status.c_str(), decision.c_str(), complete ? "true" : "false",
      s.initial, s.visited, (unsigned long long)s.expanded, (unsigned long long)s.arcs, s.maximum_predecessors, s.complete_depth,
      (unsigned long long)s.operations, (unsigned long long)o.cap, (unsigned long long)o.operations, o.seconds, o.memory_mb,
      chrono::duration<double>(chrono::steady_clock::now() - s.start).count());
  for (size_t i = 0; i < s.frontiers.size(); ++i) printf("%s%zu", i ? "," : "", s.frontiers[i]);
  printf("],\"forward_visited\":%zu,\"forward_expanded\":%llu,\"forward_transitions\":%llu,\"forward_complete_depth\":%d,\"forward_frontiers\":[",
    s.forward_visited, (unsigned long long)s.forward_expanded, (unsigned long long)s.forward_transitions, s.forward_complete_depth);
  for (size_t i = 0; i < s.forward_frontiers.size(); ++i) printf("%s%zu", i ? "," : "", s.forward_frontiers[i]);
  printf("],\"all_e_audit_complete\":%s,\"all_e_accepts\":%zu,\"accepting_forward_emissions\":%llu,\"accepting_forward_expansions\":%llu,\"accepted_e_streams\":[",
    s.forward_exhausted ? "true" : "false", s.accepted_e.size(), (unsigned long long)s.accepting_emissions, (unsigned long long)s.accepting_expansions);
  bool first = true;
  for (u64 es : s.accepted_e) { printf("%s\"%s\"", first ? "" : ",", bit_string(es).c_str()); first = false; }
  printf("]");
}
vector<int> normalize(const vector<int>& word, int& carry) {
  vector<int> d;
  for (int x : word) { int z = x + carry; d.push_back(z % b); carry = z / b; }
  return d;
}
void replay(const Options& o, const vector<Column>& cols) {
  if (cols.empty()) throw logic_error("empty reconstructed exterior");
  vector<vector<int>> words(p);
  for (const Column& c : cols) for (int t = 0; t < p; ++t) words[t].push_back(c[t]);
  for (int t = 0; t < p; ++t) {
    if (!words[t][0]) throw logic_error("zero physical head in reconstructed exterior");
    int e = 0; auto low = normalize(words[t], e);
    if (e != o.es[t] - '0') throw logic_error("wrong reconstructed e");
    auto rev = words[t]; reverse(rev.begin(), rev.end());
    int overflow = 1 - e; auto high = normalize(rev, overflow); reverse(high.begin(), high.end());
    if (overflow != g[t]) throw logic_error("wrong reconstructed g");
    if (overflow) { low.push_back((b - 1) * (1 - e)); high.insert(high.begin(), 1); }
    vector<int> raw;
    for (size_t i = 0; i < low.size(); ++i) raw.push_back(low[i] + high[i]);
    auto expected = words[(t + 1) % p]; if (overflow) expected.push_back(b - 1);
    if (raw != expected) throw logic_error("reconstructed fixed-width exterior edge failed arithmetic replay");
  }
}
void witness(const Options& o, Statistics& s, const vector<Column>& cols, const vector<K128>& cuts) {
  replay(o, cols);
  s.accepted_e.insert(bits(o.es));
  header(o, s, "ACCEPT", "B_CYCLE", true);
  printf(",\"width\":%zu,\"arithmetic_replay\":true,\"u\":[", cols.size());
  for (int t = 0; t < p; ++t) printf("%s%d", t ? "," : "", g[t]);
  printf("],\"B\":[");
  for (int t = 0; t < p; ++t) {
    printf("%s[", t ? "," : "");
    for (size_t k = 0; k < cols.size(); ++k) printf("%s%u", k ? "," : "", unsigned(cols[k][t]));
    printf("]");
  }
  printf("],\"columns\":[");
  for (size_t k = 0; k < cols.size(); ++k) { if (k) printf(","); print_column(cols[k]); }
  printf("],\"cuts\":[");
  for (size_t k = 0; k < cuts.size(); ++k) { if (k) printf(","); print_state(cuts[k]); }
  puts("]}");
}

int search(const Options& o, Statistics& stats) {
  Budget budget{o, stats}; int ng = static_cast<int>(Gidx.size()), Y[64];
  for (int i = 0; i < ng; ++i) Y[i] = 1;
  u64 gm = bits(o.gs), em = bits(o.es), mask = (u64(1) << p) - 1;
  K128 physical = pack(0, gm, Y, ng);
  for (int i = 0; i < ng; ++i) Y[i] = (b - 1) * int((em >> Gidx[i]) & 1);
  K128 terminal = pack(em, mask ^ em, Y, ng);
  unordered_map<K128, uint32_t, KH> first_id, seen;
  vector<Edge> first;
  vector<Node> nodes;
  string status = "EXHAUSTED";
  uint32_t found_first = 0, found_successor = 0;
  Column found_column{};
  try {
    int initialY[64]; for (int i = 0; i < ng; ++i) initialY[i] = 1;
    transitions(0, gm, initialY, ng, true, [&](u64 L, u64 H, int* yy, int* xs, int*) {
      budget.tick(); K128 key = pack(L, H, yy, ng);
      if (first_id.count(key)) return;
      if (first.size() >= o.cap) throw Stop("INITIAL_STATE_CAP");
      Column col{}; for (int t = 0; t < p; ++t) col[t] = static_cast<uint8_t>(xs[t]);
      first_id.emplace(key, static_cast<uint32_t>(first.size())); first.push_back({key, col});
      stats.initial = first.size();
    });
    auto one = first_id.find(terminal);
    if (one != first_id.end()) { witness(o, stats, {first[one->second].column}, {physical, terminal}); return 0; }
    if (!first.empty()) {
      if (first.size() + 1 > o.cap) throw Stop("STATE_CAP");
      nodes.push_back({terminal, 0, 0, {}}); seen.emplace(terminal, 0);
      stats.visited = 1; stats.frontiers.push_back(1);
      size_t begin = 0, end = 1; int depth = 0;
      while (begin < end) {
        if (o.max_depth >= 0 && depth >= o.max_depth) throw Stop("DEPTH_CAP");
        for (size_t i = begin; i < end; ++i) {
          budget.tick(); K128 current = nodes[i].key;
          size_t local_count = 0;
          Inverse inv(current, budget);
          inv.run([&](K128 pred, const Column& col) {
            ++stats.arcs; ++local_count;
            auto match = first_id.find(pred);
            if (match != first_id.end()) {
              found_first = match->second; found_successor = static_cast<uint32_t>(i); found_column = col;
              throw Stop("FOUND");
            }
            if (seen.count(pred)) return;
            if (nodes.size() + first.size() >= o.cap) throw Stop("STATE_CAP");
            uint32_t id = static_cast<uint32_t>(nodes.size());
            seen.emplace(pred, id); nodes.push_back({pred, static_cast<uint32_t>(i), static_cast<uint32_t>(depth + 1), col});
            stats.visited = nodes.size();
          });
          stats.maximum_predecessors = max(stats.maximum_predecessors, local_count);
          ++stats.expanded;
        }
        stats.complete_depth = depth;
        begin = end; end = nodes.size(); ++depth;
        stats.frontiers.push_back(end - begin);
      }
    }
  } catch (const Stop& stop) {
    if (stop.reason == "FOUND") {
      vector<Column> cols{first[found_first].column, found_column};
      vector<K128> cuts{physical, first[found_first].key, nodes[found_successor].key};
      uint32_t at = found_successor;
      while (at != 0) { cols.push_back(nodes[at].column); at = nodes[at].next; cuts.push_back(nodes[at].key); }
      witness(o, stats, cols, cuts); return 0;
    }
    status = stop.reason;
  }
  bool complete = status == "EXHAUSTED";
  header(o, stats, status, complete ? "NO_B_CYCLE" : "UNDECIDED", complete);
  if (o.dump_states) {
    printf(",\"reverse_states\":[");
    for (size_t i = 0; i < nodes.size(); ++i) {
      if (i) printf(",");
      printf("{\"depth\":%u,\"state\":", nodes[i].depth); print_state(nodes[i].key); printf("}");
    }
    printf("]");
  }
  puts("}");
  return complete ? 0 : 2;
}

int predecessor_mode(const Options& o, Statistics& stats) {
  Budget budget{o, stats}; int Y[64], ng = static_cast<int>(Gidx.size());
  stringstream ss(o.ys); string item; int n = 0;
  while (getline(ss, item, ',')) {
    uint64_t digit = number(item, "Y digit");
    if (n >= ng || digit >= static_cast<uint64_t>(b)) throw invalid_argument("wrong Y vector");
    Y[n++] = static_cast<int>(digit);
  }
  if (n != ng || (!o.ys.empty() && o.ys.back() == ',')) throw invalid_argument("wrong Y vector length");
  K128 target = pack(bits(o.ls), bits(o.hs), Y, ng);
  vector<Edge> edges; string status = "COMPLETE";
  try {
    Inverse inv(target, budget);
    inv.run([&](K128 key, const Column& col) {
      if (edges.size() >= o.cap) throw Stop("STATE_CAP");
      edges.push_back({key, col}); ++stats.arcs; stats.visited = edges.size();
    });
  } catch (const Stop& s) { status = s.reason; }
  sort(edges.begin(), edges.end(), [](const Edge& a, const Edge& b) { return a.key < b.key; });
  bool complete = status == "COMPLETE";
  header(o, stats, status, complete ? "RELATION_COMPLETE" : "UNDECIDED", complete);
  printf(",\"successor\":"); print_state(target); printf(",\"predecessors\":[");
  for (size_t i = 0; i < edges.size(); ++i) {
    if (i) printf(",");
    printf("{\"state\":"); print_state(edges[i].key); printf(",\"column\":"); print_column(edges[i].column); printf("}");
  }
  puts("]}"); return complete ? 0 : 2;
}

int bidirectional(const Options& o, Statistics& stats) {
  Budget budget{o, stats}; int ng = static_cast<int>(Gidx.size()), Y[64];
  u64 gm = bits(o.gs), em = bits(o.es), mask = (u64(1) << p) - 1;
  for (int i = 0; i < ng; ++i) Y[i] = 1;
  K128 physical = pack(0, gm, Y, ng);
  for (int i = 0; i < ng; ++i) Y[i] = (b - 1) * int((em >> Gidx[i]) & 1);
  K128 terminal = pack(em, mask ^ em, Y, ng);
  vector<Node> fnodes, rnodes;
  unordered_map<K128, uint32_t, KH> fseen, rseen;
  // Node0 is only first-column provenance.  It is deliberately absent from
  // fseen: a later generic return to the physical cut remains expandable.
  fnodes.push_back({physical, 0, 0, {}});
  rnodes.push_back({terminal, 0, 0, {}}); rseen.emplace(terminal, 0);
  stats.forward_visited = stats.visited = 1;
  stats.frontiers.push_back(1); stats.forward_frontiers.push_back(1);
  uint32_t found_f = 0, found_r = 0; Column bridge{};
  string status = "EXHAUSTED";
  auto allocation = [&]() {
    if (fnodes.size() + rnodes.size() >= o.cap) throw Stop("STATE_CAP");
  };
  try {
    if (fnodes.size() + rnodes.size() > o.cap) throw Stop("STATE_CAP");
    int initialY[64]; for (int i = 0; i < ng; ++i) initialY[i] = 1;
    audit_acceptance(stats, 0, gm, initialY, true);
    transitions(0, gm, initialY, ng, true, [&](u64 L, u64 H, int* yy, int* xs, int*) {
      budget.tick(); ++stats.forward_transitions;
      audit_acceptance(stats, L, H, yy, false);
      K128 key = pack(L, H, yy, ng); Column col{};
      for (int t = 0; t < p; ++t) col[t] = static_cast<uint8_t>(xs[t]);
      if (key == terminal) { found_f = found_r = 0; bridge = col; throw Stop("FOUND"); }
      if (fseen.count(key)) return;
      allocation();
      uint32_t id = static_cast<uint32_t>(fnodes.size());
      fseen.emplace(key, id); fnodes.push_back({key, 0, 1, col});
      stats.forward_visited = fnodes.size(); stats.initial = fnodes.size() - 1;
    });
    stats.forward_expanded = 1; stats.forward_complete_depth = 0;
    stats.forward_frontiers.push_back(fnodes.size() - 1);
    size_t fb = 1, fe = fnodes.size(), rb = 0, re = 1;
    int fd = 1, rd = 0;
    while (fb < fe && rb < re) {
      bool forward = fe - fb <= re - rb;
      if (forward) {
        if (o.max_depth >= 0 && fd >= o.max_depth) throw Stop("DEPTH_CAP");
        for (size_t i = fb; i < fe; ++i) {
          u64 L, H; int yy[64]; unpack(fnodes[i].key, L, H, yy, ng);
          audit_acceptance(stats, L, H, yy, true);
          transitions(L, H, yy, ng, false, [&](u64 L2, u64 H2, int* y2, int* xs, int*) {
            budget.tick(); ++stats.forward_transitions;
            audit_acceptance(stats, L2, H2, y2, false);
            K128 key = pack(L2, H2, y2, ng);
            auto match = rseen.find(key);
            if (match != rseen.end()) {
              found_f = static_cast<uint32_t>(i); found_r = match->second;
              for (int t = 0; t < p; ++t) bridge[t] = static_cast<uint8_t>(xs[t]);
              throw Stop("FOUND");
            }
            if (fseen.count(key)) return;
            allocation(); Column col{};
            for (int t = 0; t < p; ++t) col[t] = static_cast<uint8_t>(xs[t]);
            uint32_t id = static_cast<uint32_t>(fnodes.size());
            fseen.emplace(key, id); fnodes.push_back({key, static_cast<uint32_t>(i), static_cast<uint32_t>(fd + 1), col});
            stats.forward_visited = fnodes.size();
          });
          ++stats.forward_expanded;
        }
        stats.forward_complete_depth = fd;
        fb = fe; fe = fnodes.size(); ++fd;
        stats.forward_frontiers.push_back(fe - fb);
      } else {
        if (o.max_depth >= 0 && rd >= o.max_depth) throw Stop("DEPTH_CAP");
        for (size_t i = rb; i < re; ++i) {
          size_t count = 0; Inverse inv(rnodes[i].key, budget);
          inv.run([&](K128 key, const Column& col) {
            ++stats.arcs; ++count;
            auto match = fseen.find(key);
            if (match != fseen.end()) {
              found_f = match->second; found_r = static_cast<uint32_t>(i); bridge = col;
              throw Stop("FOUND");
            }
            if (rseen.count(key)) return;
            allocation(); uint32_t id = static_cast<uint32_t>(rnodes.size());
            rseen.emplace(key, id); rnodes.push_back({key, static_cast<uint32_t>(i), static_cast<uint32_t>(rd + 1), col});
            stats.visited = rnodes.size();
          });
          stats.maximum_predecessors = max(stats.maximum_predecessors, count);
          ++stats.expanded;
        }
        stats.complete_depth = rd;
        rb = re; re = rnodes.size(); ++rd;
        stats.frontiers.push_back(re - rb);
      }
    }
    stats.forward_exhausted = fb == fe;
  } catch (const Stop& stop) {
    if (stop.reason == "FOUND") {
      vector<Column> cols; vector<K128> cuts;
      uint32_t at = found_f;
      while (at != 0) { cols.push_back(fnodes[at].column); cuts.push_back(fnodes[at].key); at = fnodes[at].next; }
      reverse(cols.begin(), cols.end()); reverse(cuts.begin(), cuts.end()); cuts.insert(cuts.begin(), physical);
      cols.push_back(bridge); cuts.push_back(rnodes[found_r].key);
      at = found_r;
      while (at != 0) { cols.push_back(rnodes[at].column); at = rnodes[at].next; cuts.push_back(rnodes[at].key); }
      witness(o, stats, cols, cuts); return 0;
    }
    status = stop.reason;
  }
  bool complete = status == "EXHAUSTED";
  header(o, stats, status, complete ? "NO_B_CYCLE" : "UNDECIDED", complete);
  if (o.dump_states) {
    for (int side = 0; side < 2; ++side) {
      const auto& nodes = side ? fnodes : rnodes;
      printf(",\"%s_states\":[", side ? "forward" : "reverse");
      for (size_t i = 0; i < nodes.size(); ++i) {
        if (i) printf(",");
        printf("{\"depth\":%u,\"state\":", nodes[i].depth); print_state(nodes[i].key); printf("}");
      }
      printf("]");
    }
  }
  puts("}"); return complete ? 0 : 2;
}
} // namespace fixed_driver

int main(int argc, char** argv) {
  using namespace fixed_driver;
  Options o; Statistics stats;
  try {
    o = parse(argc, argv); initialize(o); guards(o);
    int code = o.mode == "predecessors" ? predecessor_mode(o, stats) :
      o.mode == "bidirectional" ? bidirectional(o, stats) : search(o, stats);
    alarm(0); return code;
  } catch (const invalid_argument& err) {
    alarm(0); fprintf(stderr, "INVALID_INPUT: %s\n", err.what()); return 64;
  } catch (const bad_alloc&) {
    // Search containers have unwound before this handler, releasing memory.
    // Preserve the last fully completed layers for a reproducible handoff.
    alarm(0); header(o, stats, "MEMORY_LIMIT", "UNDECIDED", false); puts("}"); return 2;
  } catch (const Stop& stop) {
    alarm(0); header(o, stats, stop.reason, "UNDECIDED", false); puts("}"); return 2;
  } catch (const exception& err) {
    alarm(0); fprintf(stderr, "ERROR: %s\n", err.what());
    puts("{\"format\":\"agent117-fixed-driver-exterior-v1\",\"status\":\"ERROR\",\"decision\":\"UNDECIDED\",\"complete\":false}"); return 70;
  }
}
