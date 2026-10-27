// Exact regular-language PREIMAGE search for exterior B cuts.
// The arithmetic is the position model documented in structure/bauto.cpp;
// this implementation works on phase-labelled words for every repetition.
// A symbol is phase*(4*b) + L*(2*b) + H*b + Y, with Y=0 when g=0.
// JSON dumps use p196-exterior-dfa-v1; finals contains accepting state IDs,
// transitions contains rows of [symbol,target], and missing transitions reject.
#include "finite_automata.hpp"
#include <csignal>
#include <iostream>
#include <sstream>
#include <sys/resource.h>
#include <unistd.h>

namespace a113backward {
using a113fa::Budget;
using a113fa::DFA;
using a113fa::NFA;
using a113fa::LimitReached;
using a113fa::State;
using a113fa::Label;

struct Options {
  int base=10, period=0, depth=12, dump_depth=-1, count_k=3, memory_mib=2048;
  std::string e,g;
  a113fa::Limits limits;
};
static uint64_t number(const std::string& s) {
  if (s.empty() || s.find_first_not_of("0123456789")!=std::string::npos)
    throw std::invalid_argument("unsigned decimal integer required");
  return std::stoull(s);
}
static Options parse(int argc,char** argv) {
  if (argc<4) throw std::invalid_argument("usage: exterior_backward_regular BASE E G [options]");
  Options o; uint64_t b=number(argv[1]);
  if (b<2 || b>62) throw std::invalid_argument("base must be 2..62");
  o.base=b; o.e=argv[2]; o.g=argv[3];
  if (o.e.empty() || o.e.size()>256 || o.e.size()!=o.g.size() ||
      o.e.find_first_not_of("01")!=std::string::npos || o.g.find_first_not_of("01")!=std::string::npos)
    throw std::invalid_argument("equal nonempty binary streams of length at most 256 required");
  o.period=o.e.size();
  for (int i=4;i<argc;++i) {
    std::string flag=argv[i];
    if (++i==argc) throw std::invalid_argument("missing option value");
    uint64_t value=number(argv[i]);
    if (flag=="--depth" && value<=1000) o.depth=value;
    else if (flag=="--dump-depth" && value<=1000) o.dump_depth=value;
    else if (flag=="--count-k" && value>=1 && value<=16) o.count_k=value;
    else if (flag=="--states" && value>=1 && value<=5000000) o.limits.max_states=value;
    else if (flag=="--edges" && value>=1 && value<=100000000) o.limits.max_edges=value;
    else if (flag=="--ops" && value>=1 && value<=20000000000ULL) o.limits.max_operations=value;
    else if (flag=="--seconds" && value>=1 && value<=1800) o.limits.seconds=value;
    else if (flag=="--memory-mib" && value>=64 && value<=8192) o.memory_mib=value;
    else throw std::invalid_argument("unknown option or unsupported limit");
  }
  if (o.dump_depth>o.depth) throw std::invalid_argument("dump depth exceeds search depth");
  return o;
}
static std::string quoted(const std::string& s) {
  std::string out="\"";
  for (unsigned char c:s) {
    if (c=='"' || c=='\\') { out+='\\'; out+=c; }
    else if (c>=32 && c<127) out+=c;
    else out+='?';
  }
  return out+'"';
}
static void alarm_handler(int) {
  const char message[]="{\"status\":\"UNDECIDED\",\"reason\":\"wall_timeout\"}\n";
  (void)!write(1,message,sizeof(message)-1); _exit(3);
}
static void resources(const Options& o) {
  rlimit prior;
  if (getrlimit(RLIMIT_AS,&prior)) throw LimitReached("cannot inspect memory limit");
  rlim_t cap=static_cast<rlim_t>(o.memory_mib)<<20;
  if (prior.rlim_cur!=RLIM_INFINITY) cap=std::min(cap,prior.rlim_cur);
  if (prior.rlim_max!=RLIM_INFINITY) cap=std::min(cap,prior.rlim_max);
  rlimit next{cap,prior.rlim_max};
  if (setrlimit(RLIMIT_AS,&next)) throw LimitReached("cannot set memory limit");
  std::signal(SIGALRM,alarm_handler); alarm(static_cast<unsigned>(o.limits.seconds));
}
static long rss_mib() {
  rusage usage;
  return getrusage(RUSAGE_SELF,&usage)?-1:usage.ru_maxrss/1024;
}
struct Symbol { int phase,L,H,Y; };
struct Tile { Label output; uint8_t next; };
using Relation=std::vector<std::vector<Tile>>;

struct Engine {
  const Options& o;
  Budget& budget;
  int b,p,domain;
  std::unordered_map<Label,Relation> inverse_cache,forward_cache;
  size_t raw_states=0,raw_edges=0,intersection_states=0;
  explicit Engine(const Options& options,Budget& z):o(options),budget(z),b(o.base),p(o.period),domain(2*b-1) {
    // Every terminal symbol has the constant coefficient b-1 self-loop.
    // This establishes Q+ subset PRE(Q+) locally, for every word repetition.
    for (int t=0;t<p;++t) {
      int e=o.e[t]-'0',g=o.g[t]-'0'; Label q=label(t,e,1-e,g?(b-1)*e:0);
      bool found=false;
      for (const Tile& tile:inverse(q)[b-1]) if (tile.output==q && tile.next==b-1) found=true;
      if (!found) throw std::logic_error("terminal neutral-column self-loop failed");
    }
  }
  Label label(int phase,int L,int H,int Y) const {
    if (phase<0 || phase>=p || L<0 || L>1 || H<0 || H>1 || Y<0 || Y>=b ||
        (o.g[phase]=='0' && Y!=0)) throw std::logic_error("invalid generated symbol");
    return phase*(4*b)+L*(2*b)+H*b+Y;
  }
  Symbol decode(Label value) const {
    Symbol s; s.phase=value/(4*b); int rest=value%(4*b);
    s.L=rest/(2*b); s.H=(rest/b)%2; s.Y=rest%b;
    if (s.phase>=p || (o.g[s.phase]=='0' && s.Y)) throw std::logic_error("invalid internal alphabet label");
    return s;
  }
  DFA reduce(const NFA& n) {
    NFA useful=a113fa::trim(n,budget);
    DFA d=a113fa::determinize(useful,budget);
    return a113fa::minimize(d,budget);
  }
  DFA boundary(bool terminal) {
    NFA n;
    for (int i=0;i<=p;++i) n.add_state(i==p);
    n.add_initial(0);
    Label first=0;
    for (int t=0;t<p;++t) {
      int e=o.e[t]-'0',g=o.g[t]-'0';
      Label a=terminal?label(t,e,1-e,g?(b-1)*e:0):label(t,0,g,g?1:0);
      if (!t) first=a;
      n.add_edge(t,a,t+1);
    }
    n.add_edge(p,first,1); // positive powers; accepting boundaries keep outgoing edges
    return reduce(n);
  }

  // PRE consumes a new symbol (Ln,Hn,Yn) and emits an old symbol (L,H,Y),
  // while its control still follows the forward coefficient xin -> xout.
  // At g=1, Yn fixes xin=Yn+b*H-Hn, so only two candidate xin values exist.
  const Relation& inverse(Label input) {
    auto found=inverse_cache.find(input);
    if (found!=inverse_cache.end()) return found->second;
    Symbol next=decode(input); Relation relation(domain); bool overflow=o.g[next.phase]=='1';
    auto add_for_x=[&](int x) {
      if (x<0 || x>=domain) return;
      int H=(x+next.H)/b,high=(x+next.H)%b;
      if (overflow && high!=next.Y) return;
      for (int L=0;L<=1;++L) {
        budget.tick(); if ((x+L)/b!=next.L) continue;
        int low=(x+L)%b,choices=overflow?b:1;
        for (int Y=0;Y<choices;++Y) {
          budget.tick(); int xout=low+(overflow?Y:high);
          if (xout<0 || xout>=domain) throw std::logic_error("inverse coefficient range");
          relation[x].push_back({label(next.phase,L,H,Y),static_cast<uint8_t>(xout)});
        }
      }
    };
    if (overflow) for (int H=0;H<=1;++H) add_for_x(next.Y+b*H-next.H);
    else for (int x=0;x<domain;++x) add_for_x(x);
    return inverse_cache.emplace(input,std::move(relation)).first->second;
  }
  const Relation& forward(Label input) {
    auto found=forward_cache.find(input);
    if (found!=forward_cache.end()) return found->second;
    Symbol old=decode(input); Relation relation(domain); bool overflow=o.g[old.phase]=='1';
    for (int x=0;x<domain;++x) for (int Hn=0;Hn<=1;++Hn) {
      budget.tick(); if ((x+Hn)/b!=old.H) continue;
      int Ln=(x+old.L)/b, high=(x+Hn)%b;
      int xout=(x+old.L)%b+(overflow?old.Y:high);
      if (xout<0 || xout>=domain) throw std::logic_error("forward coefficient range");
      relation[x].push_back({label(old.phase,Ln,Hn,overflow?high:0),static_cast<uint8_t>(xout)});
    }
    return forward_cache.emplace(input,std::move(relation)).first->second;
  }

  DFA transform(const DFA& source,bool backwards,bool positive) {
    if (backwards && positive) throw std::logic_error("positive restriction belongs to forward FIRST only");
    struct Cut { State source; uint8_t current,first; };
    std::vector<Cut> queue;
    std::unordered_map<uint64_t,State> ids;
    NFA output; size_t edge_count=0;
    auto intern=[&](State old,int x,int first) {
      uint64_t key=(static_cast<uint64_t>(old)<<16)|(static_cast<uint64_t>(x)<<8)|first;
      auto found=ids.find(key); if (found!=ids.end()) return found->second;
      budget.observe(output.size()+1,edge_count);
      State id=output.add_state(source.final[old] && x==first);
      ids.emplace(key,id); queue.push_back({old,static_cast<uint8_t>(x),static_cast<uint8_t>(first)}); return id;
    };
    for (int c=positive?1:0;c<domain;++c) output.add_initial(intern(source.initial,c,c));
    for (size_t i=0;i<queue.size();++i) {
      Cut state=queue[i];
      if (positive && state.current==0) continue; // strictly positive at EVERY temporal phase
      for (const auto& edge:source.edges[state.source]) {
        budget.tick();
        const Relation& relation=backwards?inverse(edge.label):forward(edge.label);
        for (const Tile& tile:relation[state.current]) {
          budget.tick(); State to=intern(edge.to,tile.next,state.first);
          output.add_edge(i,tile.output,to); budget.observe(output.size(),++edge_count);
        }
      }
    }
    raw_states=output.size(); raw_edges=edge_count;
    return reduce(output);
  }
  bool nonempty(const DFA& d) const {
    return std::any_of(d.final.begin(),d.final.end(),[](uint8_t x){return x!=0;});
  }

  bool intersection(const DFA& left,const DFA& right,std::vector<Label>& witness) {
    struct Pair { State left,right,parent; Label letter; };
    std::vector<Pair> queue;
    std::unordered_map<uint64_t,State> ids;
    auto intern=[&](State a,State b,State parent,Label letter) {
      uint64_t key=(static_cast<uint64_t>(a)<<32)|b;
      auto found=ids.find(key); if (found!=ids.end()) return found->second;
      budget.observe(queue.size()+1,0);
      State id=queue.size(); ids.emplace(key,id); queue.push_back({a,b,parent,letter}); return id;
    };
    intern(left.initial,right.initial,a113fa::absent,0);
    size_t edge_count=0;
    for (State i=0;i<queue.size();++i) {
      Pair state=queue[i]; budget.tick();
      if (left.final[state.left] && right.final[state.right]) {
        for (State q=i;queue[q].parent!=a113fa::absent;q=queue[q].parent) witness.push_back(queue[q].letter);
        std::reverse(witness.begin(),witness.end()); intersection_states=queue.size();
        budget.check_time(); return true;
      }
      const auto& a=left.edges[state.left]; const auto& b=right.edges[state.right];
      size_t ai=0,bi=0;
      while (ai<a.size() && bi<b.size()) {
        budget.tick();
        if (a[ai].label<b[bi].label) { ++ai; continue; }
        if (b[bi].label<a[ai].label) { ++bi; continue; }
        intern(a[ai].to,b[bi].to,i,a[ai].label); ++ai; ++bi;
        budget.observe(queue.size(),++edge_count);
      }
    }
    intersection_states=queue.size(); budget.check_time(); return false;
  }
  void progress(const DFA& d,int depth,const char* event) {
    std::vector<a113fa::Integer> counts;
    for (int k=1;k<=o.count_k;++k)
      counts.push_back(a113fa::count_words(d,static_cast<size_t>(p)*k,budget));
    const char* direction=std::string(event)=="positive_first"?"forward":"backward";
    std::cout<<"{\"event\":"<<quoted(event)<<",\"direction\":"<<quoted(direction)<<",\"depth\":"<<depth
             <<",\"raw_states\":"<<raw_states<<",\"raw_edges\":"<<raw_edges
             <<",\"dfa_states\":"<<d.size()<<",\"dfa_edges\":"<<d.edge_count()<<",\"count_by_k\":[";
    for (int k=1;k<=o.count_k;++k) {
      if (k>1) std::cout<<',';
      std::cout<<'"'<<counts[k-1]<<'"';
    }
    std::cout<<"],\"operations\":"<<budget.operations<<",\"rss_mib\":"<<rss_mib()<<"}\n"<<std::flush;
  }
  void dump(const DFA& d,int depth) {
    // Build a complete record before emitting it, so an operation/memory cap
    // during export still leaves a parseable UNDECIDED status record.
    std::ostringstream text;
    text<<"{\"event\":\"dump\",\"format\":\"p196-exterior-dfa-v1\",\"direction\":\"backward\""
             <<",\"role\":\"frontier\",\"base\":"<<b<<",\"unit_period\":"<<p
             <<",\"e\":"<<quoted(o.e)<<",\"g\":"<<quoted(o.g)<<",\"depth\":"<<depth
             <<",\"alphabet\":[";
    bool comma=false;
    for (int t=0;t<p;++t) for (int L=0;L<=1;++L) for (int H=0;H<=1;++H)
      for (int Y=0;Y<(o.g[t]=='1'?b:1);++Y) {
        budget.tick(); if (comma) text<<','; comma=true;
        text<<"{\"label\":"<<label(t,L,H,Y)<<",\"phase\":"<<t<<",\"L\":"<<L
                 <<",\"H\":"<<H<<",\"Y\":"<<Y<<'}';
      }
    text<<"],\"start\":"<<d.initial<<",\"finals\":["; comma=false;
    for (State q=0;q<d.size();++q) if (d.final[q]) {
      if (comma) text<<',';
      comma=true; text<<q;
    }
    text<<"],\"transitions\":[";
    for (State q=0;q<d.size();++q) {
      if (q) text<<',';
      text<<'[';
      for (size_t j=0;j<d.edges[q].size();++j) {
        budget.tick(); if (j) text<<',';
        text<<'['<<d.edges[q][j].label<<','<<d.edges[q][j].to<<']';
      }
      text<<']';
    }
    text<<"]}"; budget.check_time();
    std::cout<<text.str()<<'\n'<<std::flush; budget.check_time();
  }
  void candidate(const std::vector<Label>& word,int depth) {
    if (word.empty() || word.size()%p) throw std::logic_error("intersection outside positive repetitions");
    std::cout<<"{\"status\":\"CUT_INTERSECTION\",\"classification\":\"COMPUTED\",\"backward_depth\":"<<depth
             <<",\"padded_columns\":"<<depth+1<<",\"repetitions\":"<<word.size()/p
             <<",\"integer_replay_required\":true,\"word\":[";
    for (size_t i=0;i<word.size();++i) { if (i) std::cout<<','; std::cout<<word[i]; }
    std::cout<<"],\"intersection_states\":"<<intersection_states<<"}\n";
  }
};

static int solve(const Options& o) {
  Budget budget(o.limits); Engine engine(o,budget);
  DFA cut=engine.boundary(true),first;
  if (o.dump_depth<0) {
    first=engine.transform(engine.boundary(false),false,true);
    engine.progress(first,-1,"positive_first");
    if (!engine.nonempty(first)) {
      budget.check_time();
      std::cout<<"{\"status\":\"NO_EXTERIORS_ALL_REPETITIONS\",\"classification\":\"COMPUTED\",\"reason\":\"empty_positive_first\"}\n";
      return 0;
    }
  }
  engine.raw_states=cut.size(); engine.raw_edges=cut.edge_count();
  for (int depth=0;depth<=o.depth;++depth) {
    engine.progress(cut,depth,"preimage");
    if (o.dump_depth==depth) {
      engine.dump(cut,depth);
      std::cout<<"{\"status\":\"DUMPED\",\"no_exclusion_claim\":true}\n"; return 0;
    }
    if (o.dump_depth<0) {
      std::vector<Label> witness;
      if (engine.intersection(cut,first,witness)) { engine.candidate(witness,depth); return 0; }
      std::cout<<"{\"event\":\"first_intersection\",\"depth\":"<<depth
               <<",\"empty\":true,\"states\":"<<engine.intersection_states
               <<",\"operations\":"<<budget.operations<<"}\n"<<std::flush;
    }
    if (depth==o.depth) break;
    DFA next=engine.transform(cut,true,false);
    if (o.dump_depth<0 && next==cut) {
      budget.check_time();
      std::cout<<"{\"status\":\"NO_EXTERIORS_ALL_REPETITIONS\",\"classification\":\"COMPUTED\""
               <<",\"reason\":\"exact_backward_fixed_point\",\"depth\":"<<depth
               <<",\"unit_period\":"<<o.period<<",\"dfa_states\":"<<cut.size()
               <<",\"dfa_edges\":"<<cut.edge_count()<<",\"intersection_states\":"<<engine.intersection_states
               <<",\"operations\":"<<budget.operations<<"}\n"; return 0;
    }
    cut=std::move(next);
  }
  budget.check_time();
  std::cout<<"{\"status\":\"UNDECIDED\",\"reason\":\"backward_depth_limit\",\"depth\":"<<o.depth<<"}\n"; return 3;
}
} // namespace a113backward

int main(int argc,char** argv) {
  using namespace a113backward;
  try { Options o=parse(argc,argv); resources(o); int status=solve(o); alarm(0); return status; }
  catch (const std::invalid_argument& e) {
    alarm(0); std::cout<<"{\"status\":\"INVALID\",\"reason\":"<<quoted(e.what())<<"}\n"; return 2;
  }
  catch (const std::out_of_range&) {
    alarm(0); std::cout<<"{\"status\":\"INVALID\",\"reason\":\"integer_range\"}\n"; return 2;
  }
  catch (const LimitReached& e) {
    alarm(0); std::cout<<"{\"status\":\"UNDECIDED\",\"reason\":"<<quoted(e.what())<<"}\n"; return 3;
  }
  catch (const std::bad_alloc&) {
    alarm(0); const char text[]="{\"status\":\"UNDECIDED\",\"reason\":\"memory_limit\"}\n";
    (void)!write(1,text,sizeof(text)-1); return 3;
  }
  catch (const std::exception& e) {
    alarm(0); std::cout<<"{\"status\":\"UNDECIDED\",\"reason\":\"internal_error\",\"detail\":"<<quoted(e.what())<<"}\n";
    return 4;
  }
}
