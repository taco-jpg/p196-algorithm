// Agent 117: exact graph/witness tool for the fixed-schedule common-padding gauge.
// Reuses the existing exact generic layer relation.  This is not an
// all-length center solver or a replacement for Agent101's production engine.
// A spatial cycle witnesses an infinite strip, never a finite center.
#define main agent117_included_cauto_main
#include "../neutral_band/structure/cauto_fast.cpp"
#undef main

#include <array>
#include <csignal>
#include <iomanip>
#include <iostream>
#include <unistd.h>

namespace Agent117 {
volatile sig_atomic_t timeout_length = 0;
char timeout_message[256];

uint64_t natural_argument(const char* text, uint64_t maximum) {
  string token(text);
  if (token.empty() || token.find_first_not_of("0123456789") != string::npos)
    throw invalid_argument("numeric arguments must contain decimal digits only");
  uint64_t value = 0;
  for (char ch : token) {
    uint64_t digit = ch-'0';
    if (value > maximum/10 || (value == maximum/10 && digit > maximum%10))
      throw invalid_argument("numeric argument exceeds its hard limit");
    value = 10*value+digit;
  }
  return value;
}

void timeout_handler(int) {
  // write/_exit are async-signal-safe; no partially printed ordinary output.
  ssize_t ignored = write(STDOUT_FILENO, timeout_message, timeout_length);
  (void)ignored;
  _exit(124);
}

struct Node {
  St state;
  uint32_t parent = 0;
  array<uint8_t, MAXP> column{};
  uint8_t color = 0;
  uint32_t height = 0;
};
struct Frame {
  uint32_t id;
  Layer children;
  size_t next = 0;
  bool expanded = false;
  uint32_t best_child_height = 0;
  explicit Frame(uint32_t value) : id(value) {}
};
struct Witness {
  vector<uint32_t> prefix, cycle;
  array<uint8_t, MAXP> closing_column{};
};

bool initial_ghost(const St& s) {
  for (int t = 0; t < P; ++t)
    if (s.l[t] != e[t] || s.r[t] != 1-e[t]) return false;
  return true;
}

array<uint8_t, MAXP> copy_column(const vector<uint8_t>& column) {
  array<uint8_t, MAXP> result{};
  for (int t = 0; t < P; ++t) result[t] = column[t];
  return result;
}

Witness reconstruct(const vector<Node>& nodes, uint32_t from, uint32_t to,
                    const vector<uint8_t>& closing_column) {
  vector<uint32_t> chain;
  for (uint32_t id = from; ; id = nodes[id].parent) {
    chain.push_back(id);
    if (id == 0) break;
  }
  reverse(chain.begin(), chain.end());
  auto entry = find(chain.begin(), chain.end(), to);
  if (entry == chain.end()) throw runtime_error("gray target is not an ancestor");
  Witness result;
  result.prefix.assign(chain.begin(), entry+1);
  result.cycle.assign(entry, chain.end());
  result.cycle.push_back(to);
  result.closing_column = copy_column(closing_column);
  return result;
}

void print_vector(ostream& out, const vector<int>& values) {
  out << '[';
  for (size_t i = 0; i < values.size(); ++i) out << (i ? "," : "") << values[i];
  out << ']';
}
void print_state(ostream& out, const St& s) {
  const char* names[] = {"l", "r", "Rd", "Z"};
  const int8_t* values[] = {s.l, s.r, s.Rd, s.Z};
  out << '{';
  for (int field = 0; field < 4; ++field) {
    out << (field ? "," : "") << '"' << names[field] << "\":[";
    for (int t = 0; t < P; ++t) out << (t ? "," : "") << int(values[field][t]);
    out << ']';
  }
  out << '}';
}
void print_column(ostream& out, const array<uint8_t, MAXP>& column) {
  out << '[';
  for (int t = 0; t < P; ++t) out << (t ? "," : "") << int(column[t]);
  out << ']';
}
void print_walk(ostream& out, const vector<Node>& nodes, const vector<uint32_t>& ids,
                const array<uint8_t, MAXP>* closing = nullptr) {
  out << "{\"states\":[";
  for (size_t i = 0; i < ids.size(); ++i) {
    if (i) out << ',';
    print_state(out, nodes[ids[i]].state);
  }
  out << "],\"columns\":[";
  for (size_t i = 1; i < ids.size(); ++i) {
    if (i > 1) out << ',';
    print_column(out, closing && i+1 == ids.size() ? *closing : nodes[ids[i]].column);
  }
  out << "]}";
}

int execute(int radix, const string& ee, const string& gg, const string& vv, bool filtered, bool complete_graph,
            long cap, uint64_t edge_cap, int seconds) {
  b = radix; P = ee.size();
  if (b < 2 || b > 62) throw invalid_argument("base2..62 required");
  if (P < 1 || P > MAXP || gg.size() != ee.size() || vv.size() != ee.size() ||
      ee.find_first_not_of("01") != string::npos ||
      gg.find_first_not_of("01") != string::npos ||
      vv.find_first_not_of("01") != string::npos)
    throw invalid_argument("equal nonempty binary streams with P<=32 required");
  e.clear(); g.clear(); v.clear();
  for (int t = 0; t < P; ++t) {
    e.push_back(ee[t]-'0'); g.push_back(gg[t]-'0'); v.push_back(vv[t]-'0');
  }
  int G = count(gg.begin(), gg.end(), '1'), K = count(vv.begin(), vv.end(), '1');
  if (G == 0 || G != 2*K) throw invalid_argument("positive sum(g)=2sum(v) required");
  if (2*P+6*G+7*K > 256) throw invalid_argument("legacy key would exceed256 bits");
  if (cap < 1 || cap > 1000000 || edge_cap < 1 || edge_cap > 4000000 ||
      seconds < 1 || seconds > 30) throw invalid_argument("budget out of range");
  if (!setup_instance(8*P+100)) throw runtime_error("balanced setup failed");
  if (*min_element(J.begin(), J.end()) <= 2) throw runtime_error("generic layer guard failed");

  timeout_length = snprintf(timeout_message, sizeof(timeout_message),
    "{\"format\":\"agent117-common-padding-strip-v1\",\"status\":\"TIMEOUT\","
    "\"decision\":\"UNDECIDED\",\"hard_wall_seconds\":%d,"
    "\"note\":\"hard wall cap interrupted exploration; no exclusion\"}\n", seconds);
  struct sigaction action{}; action.sa_handler = timeout_handler;
  sigemptyset(&action.sa_mask); sigaction(SIGALRM, &action, nullptr);
  alarm(seconds);
  double started = nowsec();
  string status;
  vector<Node> nodes(1); nodes[0].state = start_state(); nodes[0].color = 2;
  unordered_map<LKey, uint32_t, LKH> index;
  Layer start, first;
  start.st.push_back(start_state()); start.par.push_back(0);
  bool initial_complete = run_layer(0, start, first, true,
                                    (long)min<uint64_t>(cap, edge_cap));
  size_t before = first.st.size(), removed = 0, ghosts = 0;
  uint64_t transitions = before, expanded = 0;
  size_t max_stack = 0, max_successors = before;
  Witness witness;
  bool has_cycle = false;
  uint32_t longest = 0;
  vector<uint32_t> seeds;
  if (!initial_complete) status = "CAPPED";
  else {
    for (uint32_t i = 0; i < first.st.size(); ++i) {
      bool ghost = initial_ghost(first.st[i]);
      bool allnine = all_of(first.cols[i].begin(), first.cols[i].end(),
                           [](uint8_t c) { return c == b-1; });
      if (ghost != allnine) throw runtime_error("initial noncollision audit failed");
      ghosts += ghost;
      if (filtered && ghost) ++removed;
      else seeds.push_back(i);
    }
    if (ghosts != 1) throw runtime_error("expected exactly one common-padding ghost");
  }

  for (uint32_t seed : seeds) {
    if (!status.empty()) break;
    LKey seed_key = pack(first.st[seed]);
    if (index.count(seed_key)) continue;  // Fully explored by an earlier DFS.
    if (nodes.size()-1 >= (size_t)cap) { status = "CAPPED"; break; }
    uint32_t root = nodes.size();
    Node node; node.state = first.st[seed]; node.column = copy_column(first.cols[seed]); node.color = 1;
    nodes.push_back(node); index.emplace(seed_key, root);
    vector<Frame> stack; stack.push_back(Frame{root});
    while (!stack.empty() && status.empty()) {
      max_stack = max(max_stack, stack.size());
      Frame& frame = stack.back();
      if (!frame.expanded) {
        if (transitions >= edge_cap) { status = "CAPPED"; break; }
        Layer singleton, next;
        singleton.st.push_back(nodes[frame.id].state); singleton.par.push_back(0);
        // j=1 always stays generic by the fixed J>2 guard; later ghost states
        // remain allowed.  All j>=1 generic relations are the same relation.
        long remaining = (long)min<uint64_t>(cap, edge_cap-transitions);
        bool complete = run_layer(1, singleton, next, true, remaining);
        transitions += next.st.size(); ++expanded;
        max_successors = max(max_successors, next.st.size());
        if (!complete || transitions > edge_cap) { status = "CAPPED"; break; }
        frame.children = std::move(next); frame.expanded = true;
      }
      if (frame.next == frame.children.st.size()) {
        uint32_t height = 1+frame.best_child_height;
        nodes[frame.id].height = height;
        longest = max(longest, height);
        nodes[frame.id].color = 2; stack.pop_back();
        if (!stack.empty()) stack.back().best_child_height = max(stack.back().best_child_height, height);
        continue;
      }
      size_t choice = frame.next++;
      const St& successor = frame.children.st[choice];
      LKey key = pack(successor); auto found = index.find(key);
      if (found != index.end()) {
        if (nodes[found->second].color == 1) {
          if (!has_cycle)
            witness = reconstruct(nodes, frame.id, found->second, frame.children.cols[choice]);
          has_cycle = true;
          if (!complete_graph) status = "SPATIAL_CYCLE";
        } else frame.best_child_height = max(frame.best_child_height, nodes[found->second].height);
        continue;
      }
      if (nodes.size()-1 >= (size_t)cap) { status = "CAPPED"; break; }
      Node child; child.state = successor; child.parent = frame.id;
      child.column = copy_column(frame.children.cols[choice]); child.color = 1;
      uint32_t id = nodes.size(); nodes.push_back(child); index.emplace(key, id);
      stack.push_back(Frame{id});
    }
  }
  bool exploration_completed = status.empty();
  if (status.empty()) status = has_cycle ? "SPATIAL_CYCLE" : "EXHAUSTED";
  double elapsed = nowsec()-started;
  alarm(0); // Final serialization is bounded by the already collected witness.
  cout << "{\"format\":\"agent117-common-padding-strip-v1\",\"base\":" << b << ",\"e\":";
  print_vector(cout, e); cout << ",\"g\":"; print_vector(cout, g); cout << ",\"v\":";
  print_vector(cout, v);
  cout << ",\"gauge_filtered\":" << (filtered ? "true" : "false")
       << ",\"status\":\"" << status << "\",\"decision\":\""
       << (status == "CAPPED" ? "UNDECIDED" : status == "SPATIAL_CYCLE" ?
           "INFINITE_GENERIC_STRIP_WITNESS" : "GENERIC_GRAPH_ACYCLIC")
       << "\",\"initial_complete\":" << (initial_complete ? "true" : "false")
       << ",\"initial_before\":" << before << ",\"initial_ghosts\":" << ghosts
       << ",\"initial_removed\":" << removed << ",\"initial_after\":" << seeds.size()
       << ",\"exploration_completed\":" << (exploration_completed ? "true" : "false")
       << ",\"visited\":" << nodes.size()-1 << ",\"expanded\":" << expanded
       << ",\"transitions\":" << transitions << ",\"max_stack\":" << max_stack
       << ",\"max_successors\":" << max_successors << ",\"cap\":" << cap
       << ",\"edge_cap\":" << edge_cap << ",\"hard_wall_seconds\":" << seconds
       << ",\"elapsed_seconds\":" << fixed << setprecision(6) << elapsed;
  cout << ",\"longest_generic_columns\":";
  if (status == "EXHAUSTED") cout << longest; else cout << "null";
  if (status == "SPATIAL_CYCLE") {
    cout << ",\"witness\":{\"prefix\":"; print_walk(cout, nodes, witness.prefix);
    cout << ",\"cycle\":"; print_walk(cout, nodes, witness.cycle, &witness.closing_column);
    cout << '}';
  }
  cout << ",\"scope\":\"generic outer layers only; midpoint closure omitted; no finite center or certificate\"}\n";
  return status == "CAPPED" ? 2 : 0;
}
} // namespace Agent117

int main(int argc, char** argv) {
  try {
    string ee="10100110011", gg="11100010000", vv="11000000000";
    int offset=1;
    if (argc >= 4 && argv[1][0] != '-') { ee=argv[1]; gg=argv[2]; vv=argv[3]; offset=4; }
    bool filtered=true, complete_graph=false; long cap=100000; uint64_t edge_cap=500000; int seconds=30, radix=10;
    for (int i=offset; i<argc; ++i) {
      string option=argv[i];
      if (option=="--unfiltered") filtered=false;
      else if (option=="--complete") complete_graph=true;
      else if (option=="--base" && i+1<argc) radix=Agent117::natural_argument(argv[++i],62);
      else if (option=="--cap" && i+1<argc) cap=Agent117::natural_argument(argv[++i],1000000);
      else if (option=="--edges" && i+1<argc) edge_cap=Agent117::natural_argument(argv[++i],4000000);
      else if (option=="--seconds" && i+1<argc) seconds=Agent117::natural_argument(argv[++i],30);
      else throw invalid_argument("usage: common_padding_graph [E G V] [--base2..62] [--unfiltered] [--complete] [--cap N] [--edges N] [--seconds1..30]");
    }
    return Agent117::execute(radix,ee,gg,vv,filtered,complete_graph,cap,edge_cap,seconds);
  } catch (const exception& error) {
    alarm(0); cerr << "Agent117 graph error: " << error.what() << '\n'; return 1;
  }
}
