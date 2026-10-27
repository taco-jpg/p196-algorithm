// Independent checker of a p11 regular-language center invariant.
// No automata or local-relation code is imported from the search engine.
// The certificate is untrusted data; missing output symbols/transitions lead
// to a rejecting sink, and resource limits never imply a negative result.
#include <algorithm>
#include <array>
#include <chrono>
#include <csignal>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>
#include <sys/resource.h>
#include <unistd.h>

namespace independent {
constexpr uint32_t sink = std::numeric_limits<uint32_t>::max();
constexpr int none = -1, base = 10, phases = 11, types = 2, coeffs = 19;
enum Kind { generic, odd, even, extra, inactive };
using Profile = std::array<Kind,phases>;
struct Limit : std::runtime_error { using std::runtime_error::runtime_error; };
struct Options {
  std::string path = "-";
  uint64_t states = 5000000, operations = 600000000;
  unsigned seconds = 180, memory_mib = 4096;
};
struct Budget {
  Options options;
  uint64_t operations = 0, peak_states = 0, local_calls = 0;
  std::chrono::steady_clock::time_point start = std::chrono::steady_clock::now();
  explicit Budget(const Options& o):options(o) {}
  void check() const {
    if (std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count() >= options.seconds)
      throw Limit("wall_time");
  }
  void tick(uint64_t n = 1) {
    if (n > options.operations-operations) throw Limit("operation_cap");
    uint64_t before = operations; operations += n;
    if ((before >> 10) != (operations >> 10)) check();
  }
  void size(uint64_t n) {
    peak_states = std::max(peak_states,n);
    if (n > options.states) throw Limit("state_cap");
    check();
  }
};

static uint64_t unsigned_number(const std::string& value) {
  if (value.empty() || value.find_first_not_of("0123456789") != std::string::npos)
    throw std::invalid_argument("unsigned integer required");
  return std::stoull(value);
}
static Options options(int argc, char** argv) {
  Options o; int i = 1;
  if (i < argc && std::string(argv[i]).rfind("--",0) != 0) o.path = argv[i++];
  while (i < argc) {
    std::string key = argv[i++];
    if (i == argc) throw std::invalid_argument("missing option value");
    uint64_t n = unsigned_number(argv[i++]);
    if (key == "--states" && n >= 1 && n <= 50000000) o.states = n;
    else if (key == "--ops" && n >= 1 && n <= 20000000000ULL) o.operations = n;
    else if (key == "--seconds" && n >= 1 && n <= 1800) o.seconds = n;
    else if (key == "--memory-mib" && n >= 64 && n <= 8192) o.memory_mib = n;
    else throw std::invalid_argument("unknown option or unsupported limit");
  }
  return o;
}
static void alarm_handler(int) {
  const char text[] = "{\"status\":\"UNDECIDED\",\"reason\":\"wall_timeout\"}\n";
  (void)!write(1,text,sizeof(text)-1); _exit(3);
}
static void resources(const Options& o) {
  rlimit prior;
  if (getrlimit(RLIMIT_AS,&prior)) throw Limit("cannot_read_memory_limit");
  rlim_t cap = static_cast<rlim_t>(o.memory_mib) << 20;
  if (prior.rlim_cur != RLIM_INFINITY) cap = std::min(cap,prior.rlim_cur);
  if (prior.rlim_max != RLIM_INFINITY) cap = std::min(cap,prior.rlim_max);
  rlimit next{cap,prior.rlim_max};
  if (setrlimit(RLIMIT_AS,&next)) throw Limit("cannot_set_memory_limit");
  std::signal(SIGALRM,alarm_handler); alarm(o.seconds);
}
static std::string quoted(const std::string& s) {
  std::string out = "\"";
  for (unsigned char c : s) {
    if (c == '\\' || c == '"') { out += '\\'; out += c; }
    else if (c >= 32 && c < 127) out += c;
    else out += '?';
  }
  return out+'"';
}
struct Edge { uint32_t label, target; };
struct DFA {
  uint32_t initial = 0;
  std::vector<uint8_t> final;
  std::vector<std::vector<Edge>> edges;
  uint32_t move(uint32_t q, uint32_t label) const {
    if (q == sink || label == sink) return sink;
    const auto& row = edges[q];
    auto p = std::lower_bound(row.begin(),row.end(),label,
                            [](const Edge& x,uint32_t a){return x.label<a;});
    return p != row.end() && p->label == label ? p->target : sink;
  }
  bool accepting(uint32_t q) const { return q != sink && final[q]; }
};
struct Letter {
  int type = 0, z = none;
  // Three bytes per phase: l, r, Rd+1, in the segment's chronological order.
  std::string cfg;
};
static std::string key(const Letter& letter) {
  std::string result;
  result.reserve(letter.cfg.size()+2);
  result.push_back(static_cast<char>(letter.type));
  result.push_back(static_cast<char>(letter.z+1));
  result += letter.cfg; return result;
}
struct Choice { int first; std::string cfg; };
struct Jump { uint32_t output; uint8_t next; };
using GenericRelation = std::array<std::vector<Jump>,coeffs>;
using TailRelation = std::array<std::vector<uint8_t>,coeffs>;
struct PairState {
  uint32_t source, target;
  uint8_t current, first;
  bool operator==(const PairState& o) const {
    return source==o.source && target==o.target && current==o.current && first==o.first;
  }
};
struct PairHash {
  size_t operator()(const PairState& s) const {
    uint64_t h = (static_cast<uint64_t>(s.source)<<32)|s.target;
    h ^= static_cast<uint64_t>(s.current+coeffs*s.first)*0x9e3779b97f4a7c15ULL;
    h ^= h>>30; h *= 0xbf58476d1ce4e5b9ULL;
    h ^= h>>27; h *= 0x94d049bb133111ebULL;
    return static_cast<size_t>(h^(h>>31));
  }
};

struct Checker {
  Budget& budget;
  std::array<int,phases> e{}, g{}, v{}, delta{};
  std::array<std::vector<int>,types> order;
  std::vector<Letter> alphabet;
  std::unordered_map<std::string,uint32_t> labels;
  DFA invariant, initial;
  std::array<std::unordered_map<uint32_t,GenericRelation>,2> generic_cache;
  std::array<std::unordered_map<uint32_t,TailRelation>,4> tail_cache;
  uint64_t last_states = 0;
  explicit Checker(Budget& b):budget(b) {}

  static std::string token(std::istream& in) {
    std::string s;
    if (!(in>>s)) throw std::invalid_argument("truncated certificate");
    return s;
  }
  static uint64_t nat(std::istream& in) { return unsigned_number(token(in)); }
  static int integer(std::istream& in) {
    std::string s = token(in); size_t consumed = 0;
    long long value = std::stoll(s,&consumed);
    if (consumed != s.size() || value < std::numeric_limits<int>::min() ||
        value > std::numeric_limits<int>::max()) throw std::invalid_argument("invalid integer");
    return static_cast<int>(value);
  }
  void read(std::istream& in) {
    if (token(in)!="A113REG1" || nat(in)!=base || nat(in)!=phases)
      throw std::invalid_argument("certificate format/base/period");
    const std::string es = token(in), gs = token(in), vs = token(in);
    if (es!="10100110011" || gs!="11100010000" || vs!="01000010000")
      throw std::invalid_argument("only the specified p11 driver and balanced schedule are supported");
    for (int t=0;t<phases;++t) { e[t]=es[t]-'0'; g[t]=gs[t]-'0'; v[t]=vs[t]-'0'; }
    for (int t=1;t<phases;++t) delta[t]=delta[t-1]+g[t-1]-2*v[t-1];
    // Derive the chronological segments from the trim positions, including
    // the wrap of phases 0,1 into the NEXT unit of an alternating word.
    std::vector<int> ends;
    for (int t=0;t<phases;++t) if (v[t]) ends.push_back(t);
    for (int s=0;s<types;++s) {
      int t=(ends[s]+1)%phases;
      do { order[s].push_back(t); t=(t+1)%phases; }
      while (!v[order[s].back()]);
    }
    if (nat(in)!=types) throw std::invalid_argument("segment count");
    uint64_t alphabet_size=nat(in);
    if (!alphabet_size || alphabet_size>=sink) throw std::invalid_argument("alphabet size");
    if (alphabet_size>1000000) throw Limit("alphabet_cap");
    for (int s=0;s<types;++s) {
      if (nat(in)!=order[s].size()) throw std::invalid_argument("segment length");
      for (int t:order[s]) if (integer(in)!=t) throw std::invalid_argument("segment chronological order");
    }
    alphabet.reserve(alphabet_size);
    for (uint32_t a=0;a<alphabet_size;++a) {
      budget.tick(); Letter letter; letter.type=integer(in); letter.z=integer(in);
      if (letter.type<0 || letter.type>=types || letter.z<none || letter.z>=coeffs)
        throw std::invalid_argument("symbol type or pending coefficient");
      for (int t:order[letter.type]) {
        int l=integer(in), r=integer(in), rd=integer(in);
        if (l<0 || l>1 || r<0 || r>1 || (g[t] ? rd<0 || rd>=base : rd!=none))
          throw std::invalid_argument("symbol carry or high digit");
        letter.cfg.push_back(static_cast<char>(l)); letter.cfg.push_back(static_cast<char>(r));
        letter.cfg.push_back(static_cast<char>(rd+1));
      }
      if (!labels.emplace(key(letter),a).second) throw std::invalid_argument("duplicate semantic symbol");
      alphabet.push_back(std::move(letter));
    }
    uint64_t n=nat(in), start=nat(in);
    if (!n || n>=sink || start>=n) throw std::invalid_argument("DFA size or initial state");
    budget.size(n); invariant.initial=start; invariant.final.resize(n); invariant.edges.resize(n);
    for (uint32_t q=0;q<n;++q) {
      int f=integer(in); uint64_t degree=nat(in);
      if (f<0 || f>1 || degree>alphabet_size) throw std::invalid_argument("DFA final bit or degree");
      invariant.final[q]=f; auto& row=invariant.edges[q]; row.reserve(degree);
      for (uint64_t j=0;j<degree;++j) {
        budget.tick(); uint64_t a=nat(in), to=nat(in);
        if (a>=alphabet_size || to>=n) throw std::invalid_argument("DFA edge bounds");
        row.push_back({static_cast<uint32_t>(a),static_cast<uint32_t>(to)});
      }
      std::sort(row.begin(),row.end(),[](const Edge& x,const Edge& y){return x.label<y.label;});
      for (size_t j=1;j<row.size();++j)
        if (row[j-1].label==row[j].label) throw std::invalid_argument("nondeterministic DFA label");
    }
    if (token(in)!="END") throw std::invalid_argument("certificate end marker");
    std::string trailing;
    if (in>>trailing) throw std::invalid_argument("trailing certificate data");
    initial.final={0,0,1}; initial.edges.resize(3);
    for (int s=0;s<types;++s) {
      Letter start_letter; start_letter.type=s;
      for (int t:order[s]) {
        start_letter.cfg.push_back(static_cast<char>(e[t]));
        start_letter.cfg.push_back(static_cast<char>(1-e[t]));
        start_letter.cfg.push_back(static_cast<char>(g[t]?(base-1)*e[t]+1:0));
      }
      auto found=labels.find(key(start_letter));
      if (found==labels.end()) throw std::invalid_argument("missing independently constructed initial symbol");
      initial.edges[s].push_back({found->second,static_cast<uint32_t>(s+1)});
      if (s==0) initial.edges[2].push_back({found->second,1});
    }
    budget.check();
  }

  bool valid_word_shapes() {
    // Product with a four-state automaton for type language (0 1)^+.
    std::vector<std::pair<uint32_t,uint8_t>> queue{{invariant.initial,0}};
    std::vector<std::array<bool,4>> seen(invariant.edges.size());
    seen[invariant.initial][0]=true;
    for (size_t i=0;i<queue.size();++i) {
      auto [q,phase]=queue[i]; budget.tick();
      if (invariant.final[q] && phase!=2) return false;
      for (const Edge& edge:invariant.edges[q]) {
        budget.tick(); int type=alphabet[edge.label].type, next=3;
        if ((phase==0 || phase==2) && type==0) next=1;
        else if (phase==1 && type==1) next=2;
        if (!seen[edge.target][next]) {
          seen[edge.target][next]=true; queue.push_back({edge.target,static_cast<uint8_t>(next)});
          budget.size(queue.size());
        }
      }
    }
    last_states=queue.size(); budget.check(); return true;
  }

  Profile profile(int width,int j) const {
    Profile result;
    for (int t=0;t<phases;++t) {
      int n=width+delta[t], half=(n+1)/2, raw_half=(n+g[t]+1)/2;
      result[t] = j<half-1 ? generic : j==half-1 ? (n%2?odd:even) : j<raw_half ? extra : inactive;
    }
    return result;
  }
  int layers(int width) const {
    int count=0;
    for (int t=0;t<phases;++t) count=std::max(count,(width+delta[t]+g[t]+1)/2);
    return count;
  }

  // Independently derived column arithmetic. At a segment's internal phases
  // v=0 forces the next coefficient to the raw reverse-and-add coefficient.
  // Its final v=1 phase checks the old pending coefficient (or b-1 at j=0).
  std::vector<Choice> local(const Letter& input,const Profile& kinds,bool first_layer) {
    ++budget.local_calls; budget.check();
    const auto& times=order[input.type];
    std::vector<Choice> result; std::string updated(times.size()*3,'\0');
    auto walk = [&](auto&& self,size_t i,int coefficient,int first_coefficient)->void {
      budget.tick(); int t=times[i]; Kind kind=kinds[t];
      bool active=kind<=even;
      if (active ? coefficient<0 || coefficient>=coeffs : coefficient!=none) return;
      int l=static_cast<unsigned char>(input.cfg[3*i]);
      int r=static_cast<unsigned char>(input.cfg[3*i+1]);
      int rd=static_cast<unsigned char>(input.cfg[3*i+2])-1;
      auto finish = [&](int lnext,int rnext,int next_rd,int raw) {
        updated[3*i]=static_cast<char>(lnext); updated[3*i+1]=static_cast<char>(rnext);
        updated[3*i+2]=static_cast<char>(next_rd+1);
        if (i+1==times.size()) {
          if (raw==(first_layer?base-1:input.z)) result.push_back({first_coefficient,updated});
        } else self(self,i+1,raw,first_coefficient);
      };
      if (!active) { finish(l,r,rd,kind==extra?2*rd:none); return; }
      int low=(coefficient+l)%base, lnext=(coefficient+l)/base;
      if (kind==odd) {
        if (lnext==r) finish(lnext,r,g[t]?low:none,low+(g[t]?rd:low));
        return;
      }
      for (int rin=0;rin<=1;++rin) {
        if (kind==even && rin!=lnext) continue;
        if ((coefficient+rin)/base!=r) continue;
        int high=(coefficient+rin)%base;
        finish(lnext,rin,g[t]?high:none,low+(g[t]?rd:high));
      }
    };
    if (kinds[times.front()]<=even)
      for (int c=0;c<coeffs;++c) walk(walk,0,c,c);
    else walk(walk,0,none,none);
    std::sort(result.begin(),result.end(),[](const Choice& a,const Choice& b){
      return a.first!=b.first ? a.first<b.first : a.cfg<b.cfg;
    });
    result.erase(std::unique(result.begin(),result.end(),[](const Choice& a,const Choice& b){
      return a.first==b.first && a.cfg==b.cfg;
    }),result.end());
    return result;
  }

  const GenericRelation& generic_relation(uint32_t label,bool first) {
    auto& cache=generic_cache[first]; auto found=cache.find(label);
    if (found!=cache.end()) return found->second;
    GenericRelation relation; Profile kinds; kinds.fill(generic);
    const Letter& input=alphabet[label];
    for (const Choice& choice:local(input,kinds,first)) {
      if (choice.first<0 || choice.first>=coeffs) throw std::logic_error("generic coefficient domain");
      for (int next=0;next<coeffs;++next) {
        budget.tick(); Letter output{input.type,next,choice.cfg};
        auto p=labels.find(key(output));
        relation[choice.first].push_back({p==labels.end()?sink:p->second,static_cast<uint8_t>(next)});
      }
    }
    for (auto& row:relation) {
      std::sort(row.begin(),row.end(),[](const Jump& a,const Jump& b){
        return a.output!=b.output ? a.output<b.output : a.next<b.next;
      });
      row.erase(std::unique(row.begin(),row.end(),[](const Jump& a,const Jump& b){
        return a.output==b.output && a.next==b.next;
      }),row.end());
    }
    return cache.emplace(label,std::move(relation)).first->second;
  }

  bool inclusion(const DFA& source,bool first_layer) {
    std::vector<PairState> queue;
    std::unordered_set<PairState,PairHash> seen;
    for (int c=0;c<coeffs;++c) {
      PairState state{source.initial,invariant.initial,static_cast<uint8_t>(c),static_cast<uint8_t>(c)};
      seen.insert(state); queue.push_back(state);
    }
    budget.size(queue.size());
    for (size_t i=0;i<queue.size();++i) {
      PairState state=queue[i]; budget.tick();
      if (source.final[state.source] && state.current==state.first && !invariant.accepting(state.target)) {
        last_states=queue.size(); budget.check(); return false;
      }
      for (const Edge& edge:source.edges[state.source]) {
        const auto& row=generic_relation(edge.label,first_layer)[state.current];
        for (const Jump& jump:row) {
          budget.tick(); PairState next{edge.target,invariant.move(state.target,jump.output),jump.next,state.first};
          if (seen.insert(next).second) { queue.push_back(next); budget.size(queue.size()); }
        }
      }
    }
    last_states=queue.size(); budget.check(); return true;
  }

  const TailRelation& tail_relation(uint32_t label,int width) {
    auto& cache=tail_cache[width-1]; auto found=cache.find(label);
    if (found!=cache.end()) return found->second;
    int j0=width<=2?0:1;
    if (layers(width)!=j0+2) throw std::logic_error("unsupported number of terminal layers");
    Profile first_profile=profile(width,j0), second_profile=profile(width,j0+1);
    for (const auto& times:order)
      if (first_profile[times.front()]>even || second_profile[times.front()]<=even)
        throw std::logic_error("terminal coefficient domain does not match two-layer composition");
    TailRelation relation; const Letter& input=alphabet[label];
    for (const Choice& choice:local(input,first_profile,width<=2)) {
      if (choice.first<0 || choice.first>=coeffs) throw std::logic_error("first terminal coefficient domain");
      for (int next=0;next<coeffs;++next) {
        // The second-layer starting coefficient is NONE for BOTH segment
        // types. Hence its inter-segment closure is automatic. The pending
        // value seen by that layer is precisely the next segment's previous
        // layer coefficient, retained here as `next`.
        Letter middle{input.type,next,choice.cfg};
        auto terminal=local(middle,second_profile,false);
        bool succeeds=false;
        for (const Choice& end:terminal) {
          if (end.first!=none) throw std::logic_error("second terminal coefficient must be NONE");
          succeeds=true;
        }
        if (succeeds) relation[choice.first].push_back(static_cast<uint8_t>(next));
      }
    }
    for (auto& row:relation) {
      std::sort(row.begin(),row.end()); row.erase(std::unique(row.begin(),row.end()),row.end());
    }
    return cache.emplace(label,std::move(relation)).first->second;
  }

  bool tail_empty(const DFA& source,int width) {
    // Encode (source state, first coefficient, current coefficient) exactly.
    auto encode=[](uint32_t q,int current,int first) {
      return (static_cast<uint64_t>(q)*coeffs+first)*coeffs+current;
    };
    std::vector<uint64_t> queue; std::unordered_set<uint64_t> seen;
    for (int c=0;c<coeffs;++c) {
      uint64_t state=encode(source.initial,c,c); seen.insert(state); queue.push_back(state);
    }
    budget.size(queue.size());
    for (size_t i=0;i<queue.size();++i) {
      uint64_t code=queue[i]; int current=code%coeffs; code/=coeffs;
      int first=code%coeffs; uint32_t q=code/coeffs; budget.tick();
      if (source.final[q] && current==first) {
        last_states=queue.size(); budget.check(); return false;
      }
      for (const Edge& edge:source.edges[q]) {
        const auto& row=tail_relation(edge.label,width)[current];
        for (int next:row) {
          budget.tick(); uint64_t dest=encode(edge.target,next,first);
          if (seen.insert(dest).second) { queue.push_back(dest); budget.size(queue.size()); }
        }
      }
    }
    last_states=queue.size(); budget.check(); return true;
  }
  bool report(const char* name,bool passed) {
    std::cout<<"{\"event\":\"obligation\",\"name\":"<<quoted(name)
             <<",\"passed\":"<<(passed?"true":"false")<<",\"states\":"<<last_states
             <<",\"operations\":"<<budget.operations<<"}\n"<<std::flush;
    return passed;
  }
  bool check() {
    if (!report("word_shapes",valid_word_shapes())) return false;
    if (!report("first_image_subset",inclusion(initial,true))) return false;
    if (!report("generic_image_subset",inclusion(invariant,false))) return false;
    for (int width=1;width<=4;++width) {
      const char* names[]={"q0_width_1_empty","q0_width_2_empty","odd_tail_empty","even_tail_empty"};
      if (!report(names[width-1],tail_empty(width<=2?initial:invariant,width))) return false;
    }
    budget.check(); return true;
  }
};
} // namespace independent

int main(int argc,char** argv) {
  using namespace independent;
  try {
    Options o=options(argc,argv); resources(o); Budget budget(o); Checker checker(budget);
    if (o.path=="-") checker.read(std::cin);
    else {
      std::ifstream in(o.path);
      if (!in) throw std::invalid_argument("cannot open certificate");
      checker.read(in);
    }
    bool verified=checker.check(); budget.check(); alarm(0);
    std::cout<<"{\"status\":\""<<(verified?"VERIFIED_INVARIANT":"REJECTED")
             <<"\",\"classification\":\"COMPUTED\",\"unit_period\":11,\"base\":10"
             <<",\"scope\":\"specified driver and binary schedule, all positive widths and repetitions\""
             <<",\"operations\":"<<budget.operations<<",\"peak_states\":"<<budget.peak_states
             <<",\"local_calls\":"<<budget.local_calls<<"}\n";
    return verified?0:1;
  } catch (const Limit& e) {
    alarm(0); std::cout<<"{\"status\":\"UNDECIDED\",\"reason\":"<<quoted(e.what())<<"}\n"; return 3;
  } catch (const std::bad_alloc&) {
    alarm(0); const char text[]="{\"status\":\"UNDECIDED\",\"reason\":\"memory_limit\"}\n";
    (void)!write(1,text,sizeof(text)-1); return 3;
  } catch (const std::invalid_argument& e) {
    alarm(0); std::cout<<"{\"status\":\"INVALID\",\"reason\":"<<quoted(e.what())<<"}\n"; return 2;
  } catch (const std::out_of_range&) {
    alarm(0); std::cout<<"{\"status\":\"INVALID\",\"reason\":\"integer_range\"}\n"; return 2;
  } catch (const std::exception& e) {
    alarm(0); std::cout<<"{\"status\":\"UNDECIDED\",\"reason\":\"internal_error\",\"detail\":"<<quoted(e.what())<<"}\n";
    return 4;
  }
}
