// Appended by bauto_guarded.py to the existing bauto.cpp transition core.
// A completion status is about the selected finite automaton, not a Lean proof.
#include <cerrno>
#include <climits>
#include <iostream>
#include <stdexcept>

struct Options107 {
  int base, pmin, pmax;
  u64 part = 0, parts = 1, cap = 150000000;
  int depth = 400;
  bool witness = false, verbose = false;
  string fixed;
};

static u64 number107(const char *s, u64 maximum, const char *label) {
  if (!s || !*s) throw invalid_argument(string("missing ") + label);
  u64 n = 0;
  for (const char *q = s; *q; ++q) {
    if (*q < '0' || *q > '9')
      throw invalid_argument(string("invalid integer for ") + label);
    unsigned digit = unsigned(*q - '0');
    if (n > maximum / 10 || (n == maximum / 10 && digit > maximum % 10))
      throw invalid_argument(string("integer out of range for ") + label);
    n = 10*n + digit;
  }
  return n;
}

static Options107 options107(int argc, char **argv) {
  if (argc < 4)
    throw invalid_argument("usage: BASE PMIN PMAX [-g BITS] [-w] [-v] [-part I N] [-cap N] [-depth D]");
  Options107 o;
  // The transition core uses signed int expressions such as 2*b-2.
  o.base = int(number107(argv[1], INT_MAX/2, "base"));
  o.pmin = int(number107(argv[2], 63, "minimum period"));
  o.pmax = int(number107(argv[3], 63, "maximum period"));
  if (o.base < 2 || o.pmin < 1 || o.pmax < o.pmin)
    throw invalid_argument("require base>=2 and 1<=PMIN<=PMAX<=63");
  for (int i = 4; i < argc; ++i) {
    string a = argv[i];
    auto value = [&]() -> const char * {
      if (++i >= argc) throw invalid_argument("missing option value");
      return argv[i];
    };
    if (a == "-w") o.witness = true;
    else if (a == "-v") o.verbose = true;
    else if (a == "-g") {
      o.fixed = value();
      if (o.fixed.empty() || o.fixed.find_first_not_of("01") != string::npos)
        throw invalid_argument("-g requires a nonempty binary word");
    } else if (a == "-part") {
      o.part = number107(value(), ULLONG_MAX, "partition index");
      o.parts = number107(value(), ULLONG_MAX, "partition count");
    } else if (a == "-cap") {
      o.cap = number107(value(), ULLONG_MAX, "state cap");
    } else if (a == "-depth") {
      o.depth = int(number107(value(), INT_MAX-1, "depth cap"));
    } else throw invalid_argument("unknown option");
  }
  if (!o.cap || !o.parts || o.part >= o.parts)
    throw invalid_argument("require cap>0 and 0<=partition index<partition count");
  if (!o.fixed.empty() && (o.pmin != o.pmax || int(o.fixed.size()) != o.pmin))
    throw invalid_argument("fixed -g requires PMIN=PMAX=word length");
  return o;
}

struct StateCap107 {};
struct Accepted107 { u64 e; int depth; vector<vector<int>> rows; };
struct Outcome107 {
  string reason;
  size_t states = 0;
  int depth = 0;
  vector<Accepted107> accepted;
  bool exhausted() const { return reason == "frontier_empty"; }
};

static Outcome107 search107(const Options107 &o) {
  Outcome107 out;
  int ng = int(Gidx.size());
  // Same supported capacity as upstream; never call pack beyond that limit.
  if (2*p + ydig*ng > 127) {
    out.reason = "unsupported_key";
    return out;
  }
  int initialY[64];
  for (int i = 0; i < ng; ++i) initialY[i] = 1;
  u64 initialH = 0;
  for (int t = 0; t < p; ++t) initialH |= u64(g[t]) << t;
  K128 start = pack(0, initialH, initialY, ng);
  unordered_set<K128,KH> seen;
  seen.insert(start);
  unordered_map<K128,pair<K128,vector<int>>,KH> parent;
  if (o.witness) parent[start] = {0, {}};
  unordered_set<u64> acceptedE;
  vector<K128> frontier = {start}, next;
  for (int depth = 0; ; ++depth) {
    out.depth = depth;
    if (frontier.empty()) { out.reason = "frontier_empty"; break; }
    // Harvest the entire reached layer even when its expansion is capped.
    for (K128 s : frontier) {
      u64 L, H; int Y[64];
      unpack(s, L, H, Y, ng);
      if (accepting(L,H,Y,ng) && acceptedE.insert(L).second) {
        Accepted107 a{L, depth, {}};
        if (o.witness) {
          vector<vector<int>> columns;
          K128 cursor = s;
          while (cursor != start) {
            const auto &edge = parent.at(cursor);
            columns.push_back(edge.second);
            cursor = edge.first;
          }
          reverse(columns.begin(), columns.end());
          a.rows.resize(p);
          for (int t = 0; t < p; ++t) {
            for (const auto &col : columns) a.rows[t].push_back(col[t]);
            while (!a.rows[t].empty() && a.rows[t].back() == b-1)
              a.rows[t].pop_back();
          }
        }
        out.accepted.push_back(move(a));
      }
    }
    if (depth >= o.depth) { out.reason = "depth_cap"; break; }
    next.clear();
    try {
      for (K128 s : frontier) {
        u64 L,H; int Y[64];
        unpack(s,L,H,Y,ng);
        transitions(L,H,Y,ng,depth==0,
          [&](u64 L2,u64 H2,int *Y2,int *xs,int *) {
            K128 k = pack(L2,H2,Y2,ng);
            if (seen.find(k) != seen.end()) return;
            // Check before insertion, rather than allowing a full-layer overshoot.
            if (seen.size() >= o.cap) throw StateCap107{};
            seen.insert(k);
            next.push_back(k);
            if (o.witness) parent[k] = {s, vector<int>(xs,xs+p)};
          });
      }
    } catch (const StateCap107 &) { out.reason = "state_cap"; break; }
    frontier.swap(next);
  }
  out.states = seen.size();
  sort(out.accepted.begin(),out.accepted.end(),
       [](const Accepted107 &a,const Accepted107 &c){return a.e<c.e;});
  return out;
}

static void print107(const string &word, const Options107 &o, const Outcome107 &r) {
  cout << "{\"type\":\"STREAM\",\"base\":" << b
       << ",\"period\":" << p << ",\"g\":\"" << word
       << "\",\"status\":\"" << (r.exhausted()?"EXHAUSTED":"UNDECIDED")
       << "\",\"reason\":\"" << r.reason << "\",\"states\":" << r.states
       << ",\"depth\":" << r.depth << ",\"accepted\":[";
  bool comma = false;
  for (const auto &a : r.accepted) {
    if (comma) cout << ',';
    comma = true;
    cout << "{\"e\":\"";
    for (int t = 0; t < p; ++t) cout << ((a.e >> t)&1);
    cout << "\",\"depth\":" << a.depth;
    if (o.witness) {
      cout << ",\"B_t\":[";
      for (int t=0;t<p;++t) {
        if(t)cout<<',';
        cout<<'[';
        for(size_t i=0;i<a.rows[t].size();++i) {if(i)cout<<',';cout<<a.rows[t][i];}
        cout<<']';
      }
      cout << ']';
    }
    cout << '}';
  }
  cout << "]}\n" << flush;
}

int main(int argc,char **argv) {
  try {
    Options107 o = options107(argc,argv);
    b = o.base;
    ydig=1; while ((1U<<ydig) < unsigned(b)) ++ydig;
    cout << "{\"type\":\"SOURCE\",\"source_sha256\":\"" << AGENT107_SOURCE_SHA
         << "\",\"driver_sha256\":\"" << AGENT107_DRIVER_SHA << "\"}\n" << flush;
    u64 index=0, streams=0, exhausted=0, undecided=0, acceptingStreams=0;
    auto selected = [&](const string &word) {
      if ((index++ % o.parts) != o.part) return;
      g.assign(p,0); Gidx.clear();
      for(int t=0;t<p;++t) {g[t]=word[t]-'0'; if(g[t])Gidx.push_back(t);}
      if(o.verbose) cerr<<"start g="<<word<<'\n';
      Outcome107 result=search107(o);
      ++streams;
      if(result.exhausted())++exhausted;else ++undecided;
      if(!result.accepted.empty())++acceptingStreams;
      print107(word,o,result);
    };
    for(p=o.pmin;p<=o.pmax;++p) {
      if(!o.fixed.empty()) {selected(o.fixed);continue;}
      u64 limit=1ULL<<p, mask=limit-1;
      for(u64 gm=0;gm<limit;++gm) {
        bool canonical=true;
        for(int r=1;r<p&&canonical;++r)
          if((((gm>>r)|(gm<<(p-r)))&mask)<gm)canonical=false;
        if(!canonical)continue;
        string word;
        for(int t=0;t<p;++t)word+=char('0'+((gm>>t)&1));
        selected(word);
      }
    }
    cout<<"{\"type\":\"SUMMARY\",\"streams\":"<<streams
        <<",\"exhausted\":"<<exhausted<<",\"undecided\":"<<undecided
        <<",\"accepting_streams\":"<<acceptingStreams<<"}\n";
    return undecided?3:0;
  } catch(const exception &err) {
    // Error messages above are fixed strings, with no untrusted quoted values.
    cerr<<"{\"type\":\"ERROR\",\"error\":\""<<err.what()<<"\"}\n";
    return 2;
  }
}
