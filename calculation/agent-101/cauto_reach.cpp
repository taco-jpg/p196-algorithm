// Agent 101: exact existential all-length center decision by cumulative reachability.
// Reuse the established layer relation; do not modify or duplicate its source.
// This returns one existence decision, not a classification of length residues.
#define main agent101_upstream_cauto_main
#ifndef AGENT101_CAUTO_SOURCE
#define AGENT101_CAUTO_SOURCE "../neutral_band/structure/cauto_fast.cpp"
#endif
#include AGENT101_CAUTO_SOURCE
#undef main

#include <csignal>
#include <iostream>
#include <stdexcept>
#include <unistd.h>

namespace Agent101Reach {
struct Limit : std::runtime_error { using std::runtime_error::runtime_error; };
struct Input : std::runtime_error { using std::runtime_error::runtime_error; };
struct Options { long cap=1000000; unsigned seconds=300, memory=2048; };
struct Stats { size_t visited=0, max_frontier=0; unsigned depth=0; size_t tails=0; } stats;
static double started;

static void time_limit(int) {
  const char msg[]="{\"status\":\"UNDECIDED\",\"reason\":\"wall_timeout\"}\n";
  (void)!write(STDOUT_FILENO,msg,sizeof(msg)-1);
  _exit(3);
}

static unsigned long long positive(const char* text) {
  std::string s(text); std::size_t pos=0;
  if(s.empty() || s.find_first_not_of("0123456789")!=std::string::npos)
    throw Input("numeric options require positive decimal integers");
  auto n=std::stoull(s,&pos);
  if(pos!=s.size() || !n)throw Input("numeric options must be positive");
  return n;
}

static Options parse(int argc,char** argv) {
  if(argc<5)throw Input("usage: cauto_reach BASE E G V [--cap N] [--seconds N] [--memory-mb N]");
  const auto base=positive(argv[1]);
  if(base<2 || base>62)throw Input("supported bases are 2..62");
  b=static_cast<int>(base); es_=argv[2]; gs_=argv[3]; string vs=argv[4];
  P=es_.size();
  if(P<1 || P>MAXP || gs_.size()!=es_.size() || vs.size()!=es_.size())
    throw Input("nonempty equal stream lengths must fit upstream MAXP");
  if(es_.find_first_not_of("01")!=string::npos || gs_.find_first_not_of("01")!=string::npos ||
     vs.find_first_not_of("01")!=string::npos)throw Input("all three streams must be binary");
  e.resize(P);g.resize(P);v.resize(P);int G=0,K=0;
  for(int t=0;t<P;++t){e[t]=es_[t]-'0';g[t]=gs_[t]-'0';v[t]=vs[t]-'0';G+=g[t];K+=v[t];}
  if(G!=2*K)throw Input("unbalanced length schedule: sum(g) must equal 2*sum(v)");
  if(K<1 || K>MAXNS)throw Input("fast segment engine requires 1..MAXNS trims");
  Options options;
  for(int i=5;i<argc;i+=2) {
    if(i+1>=argc)throw Input("option requires a value");
    string key=argv[i];auto value=positive(argv[i+1]);
    if(key=="--cap") {
      if(value>100000000)throw Input("state cap exceeds guarded index range");
      options.cap=static_cast<long>(value);
    } else if(key=="--seconds") {
      if(value>1800)throw Input("maximum wall budget is 1800 seconds");
      options.seconds=value;
    } else if(key=="--memory-mb") {
      if(value>8192)throw Input("maximum memory budget is 8192 MiB");
      options.memory=value;
    } else throw Input("unknown option");
  }
  return options;
}

static void resource_limits(const Options& o) {
  struct rlimit prior;
  if(getrlimit(RLIMIT_AS,&prior)!=0)throw Limit("cannot inspect address-space limit");
  rlim_t requested=static_cast<rlim_t>(o.memory)*1024*1024;
  if(prior.rlim_max!=RLIM_INFINITY)requested=std::min(requested,prior.rlim_max);
  struct rlimit lim={requested,prior.rlim_max};
  if(setrlimit(RLIMIT_AS,&lim)!=0)throw Limit("cannot enforce address-space limit");
  std::signal(SIGALRM,time_limit);alarm(o.seconds);
}

static StateSet advance(Fast& F,const vector<uint32_t>& input,int j,bool generic) {
  StateSet out;
  if(!F.step(input,j,generic,out))throw Limit("transition_frontier_cap");
  stats.max_frontier=std::max(stats.max_frontier,out.n);
  return out;
}

static bool fixed_width(Fast& F,int m0) {
  if(!setup_instance(m0))throw std::runtime_error("invalid predicted feasible length");
  vector<uint32_t> cur=F.startState();
  for(int j=0;j<Jall;++j) {
    auto out=advance(F,cur,j,false);
    if(out.n==0)return false;
    cur=std::move(out.data);
  }
  return !cur.empty();
}

static bool tail(Fast& F,const vector<uint32_t>& frontier,int representative) {
  ++stats.tails;
  if(!setup_instance(representative) || *min_element(J.begin(),J.end())!=2)
    throw std::runtime_error("tail representative must start at generic depth one");
  vector<uint32_t> cur=frontier;
  for(int j=1;j<Jall;++j) {
    auto out=advance(F,cur,j,false);
    if(out.n==0)return false;
    cur=std::move(out.data);
  }
  return !cur.empty();
}

static void fields(const Options& o) {
  string vs;for(int x:v)vs+=char('0'+x);
  std::cout<<",\"base\":"<<b<<",\"period\":"<<P<<",\"e\":\""<<es_
    <<"\",\"g\":\""<<gs_<<"\",\"v\":\""<<vs<<"\",\"visited\":"<<stats.visited
    <<",\"generic_depth\":"<<stats.depth<<",\"max_frontier\":"<<stats.max_frontier
    <<",\"tail_calls\":"<<stats.tails<<",\"state_cap\":"<<o.cap
    <<",\"rss_mb\":"<<rss_mb()<<",\"seconds\":"<<nowsec()-started;
}

static void positive_result(Fast& F,int m0,const Options& o) {
  vector<vector<int>> witness;
  // Deliberately avoid get_witness: its legacy fallback has a separate packed-key limit.
  int result=witness_fast(F,m0,witness);
  if(result!=1 || !verify_cycle(witness))throw Limit("positive_witness_replay_incomplete");
  alarm(0);
  std::cout<<"{\"status\":\"FEASIBLE\",\"m0\":"<<m0<<",\"C\":[";
  for(std::size_t t=0;t<witness.size();++t) {
    if(t)std::cout<<',';
    std::cout<<'[';
    for(std::size_t j=0;j<witness[t].size();++j){if(j)std::cout<<',';std::cout<<witness[t][j];}
    std::cout<<']';
  }
  std::cout<<']';fields(o);std::cout<<"}\n";
}

static void solve(const Options& o) {
  int delta=0,minimum=0;
  for(int t=0;t<P;++t){minimum=std::min(minimum,delta);delta+=g[t]-2*v[t];}
  if(delta!=0)throw Input("length schedule does not close");
  const int a=1-minimum;
  if(!setup_instance(a+3))throw std::runtime_error("length construction failed");
  if(nseg<1 || nseg>MAXNS)throw Input("unsupported segment count");
  for(const auto& segment:order)
    if(segment.empty() || segment.size()>MAXL)throw Input("segment exceeds upstream MAXL");
  Fast F(o.cap);F.init(order);
  // Exactly two positive initial lengths have no stationary generic prefix.
  for(int m0=a;m0<a+2;++m0)if(fixed_width(F,m0)) {positive_result(F,m0,o);return;}
  setup_instance(a+3);
  auto first=advance(F,F.startState(),0,true);
  vector<uint32_t> frontier=std::move(first.data);
  StateSet seen;seen.init(F.NS,first.n+16);
  for(std::size_t i=0;i<first.n;++i)seen.insert(&frontier[i*F.NS]);
  stats.visited=seen.n;
  unsigned depth=1;
  // Each delta frontier contains complete tuples first discovered at this depth.
  // A tuple's two tail answers do not depend on its earlier/later occurrences.
  while(!frontier.empty()) {
    stats.depth=depth;
    for(int parity=0;parity<2;++parity)if(tail(F,frontier,a+2+parity)) {
      const int m0=a+2*static_cast<int>(depth)+parity;
      positive_result(F,m0,o);return;
    }
    auto out=advance(F,frontier,1,true);vector<uint32_t> fresh;
    for(std::size_t i=0;i<out.n;++i) {
      const uint32_t* word=&out.data[i*F.NS];
      if(seen.insert(word)) {
        if(seen.n>static_cast<std::size_t>(o.cap))throw Limit("cumulative_state_cap");
        fresh.insert(fresh.end(),word,word+F.NS);
      }
    }
    stats.visited=seen.n;frontier=std::move(fresh);++depth;
  }
  alarm(0);std::cout<<"{\"status\":\"NONE\",\"all_lengths\":true";
  fields(o);std::cout<<"}\n";
}
} // namespace Agent101Reach

int main(int argc,char** argv) {
  using namespace Agent101Reach;
  started=nowsec();
  try {Options o=parse(argc,argv);resource_limits(o);solve(o);return 0;}
  catch(const Input& ex){alarm(0);std::cout<<"{\"status\":\"UNDECIDED\",\"reason\":\"invalid_or_unsupported_input\",\"detail\":\""<<ex.what()<<"\"}\n";return 2;}
  catch(const Limit& ex){alarm(0);std::cout<<"{\"status\":\"UNDECIDED\",\"reason\":\""<<ex.what()<<"\",\"visited\":"<<stats.visited<<"}\n";return 3;}
  catch(const std::bad_alloc&){alarm(0);std::cout<<"{\"status\":\"UNDECIDED\",\"reason\":\"memory_limit\"}\n";return 3;}
  catch(const std::exception& ex){alarm(0);std::cerr<<"ERROR: "<<ex.what()<<'\n';std::cout<<"{\"status\":\"UNDECIDED\",\"reason\":\"internal_error\"}\n";return 4;}
}
