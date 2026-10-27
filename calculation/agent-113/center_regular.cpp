// Exact regular languages of complete center cuts over every unit repetition.
// The unchanged upstream source supplies local segment equations only.
#define main a113_upstream_main
#include "../neutral_band/structure/cauto_fast.cpp"
#undef main
#include "finite_automata.hpp"
#include <csignal>
#include <iostream>
#include <queue>
#include <unistd.h>

namespace a113regular {
using a113fa::NFA;
using a113fa::DFA;
using a113fa::Budget;
using a113fa::Limits;
using a113fa::LimitReached;

struct Options {
  Limits limits;
  int depth=12, count_k=3, dump_depth=-1, text_depth=-1, memory=2048;
  bool generic_only=false;
};
struct Letter { int type; uint32_t lid; };

static void alarm_handler(int) {
  const char msg[]="{\"status\":\"UNDECIDED\",\"reason\":\"wall_timeout\"}\n";
  (void)!write(1,msg,sizeof(msg)-1); _exit(3);
}
static uint64_t number(const char* a) {
  string s(a);
  if(s.empty() || s.find_first_not_of("0123456789")!=string::npos)
    throw invalid_argument("numeric options require unsigned decimal integers");
  return stoull(s);
}
static Options parse(int argc,char** argv) {
  if(argc<5)throw invalid_argument("usage: center_regular BASE E G V [options]");
  uint64_t base=number(argv[1]);
  if(base<2 || base>62)throw invalid_argument("base must be 2..62");
  b=base; es_=argv[2];gs_=argv[3];string vs=argv[4];
  if(es_.empty() || es_.size()>MAXP || gs_.size()!=es_.size() || vs.size()!=es_.size())
    throw invalid_argument("equal nonempty unit stream lengths <=32 required");
  if(es_.find_first_not_of("01")!=string::npos || gs_.find_first_not_of("01")!=string::npos ||
     vs.find_first_not_of("01")!=string::npos)throw invalid_argument("binary streams required");
  P=es_.size();e.resize(P);g.resize(P);v.resize(P);int G=0,K=0;
  for(int t=0;t<P;++t){e[t]=es_[t]-'0';g[t]=gs_[t]-'0';v[t]=vs[t]-'0';G+=g[t];K+=v[t];}
  if(K<1 || K>MAXNS || G!=2*K)throw invalid_argument("positive balanced binary trim count required");
  Options o;
  for(int i=5;i<argc;++i){
    string key=argv[i];
    if(key=="--generic-only"){o.generic_only=true;continue;}
    if(i+1==argc)throw invalid_argument("missing option value");
    uint64_t n=number(argv[++i]);
    if(key=="--depth" && n>=1 && n<=1000)o.depth=n;
    else if(key=="--count-k" && n>=1 && n<=16)o.count_k=n;
    else if(key=="--dump-depth" && n>=1 && n<=1000)o.dump_depth=n;
    else if(key=="--text-depth" && n>=1 && n<=1000){o.text_depth=n;o.generic_only=true;}
    else if(key=="--states" && n>=1 && n<=5000000)o.limits.max_states=n;
    else if(key=="--edges" && n>=1 && n<=100000000)o.limits.max_edges=n;
    else if(key=="--ops" && n>=1 && n<=10000000000ULL)o.limits.max_operations=n;
    else if(key=="--seconds" && n>=1 && n<=1800)o.limits.seconds=n;
    else if(key=="--memory-mib" && n>=64 && n<=8192)o.memory=n;
    else throw invalid_argument("unknown option or out-of-range value");
  }
  return o;
}
static void enforce_limits(const Options& o){
  struct rlimit old;
  if(getrlimit(RLIMIT_AS,&old))throw LimitReached("cannot inspect address-space limit");
  rlim_t n=static_cast<rlim_t>(o.memory)<<20;
  if(old.rlim_cur!=RLIM_INFINITY)n=min(n,old.rlim_cur);
  if(old.rlim_max!=RLIM_INFINITY)n=min(n,old.rlim_max);
  struct rlimit next={n,old.rlim_max};
  if(setrlimit(RLIMIT_AS,&next))throw LimitReached("cannot set address-space limit");
  signal(SIGALRM,alarm_handler);alarm(static_cast<unsigned>(o.limits.seconds));
}

struct Engine {
  Fast local;
  Budget& budget;
  vector<Letter> letters;
  map<pair<int,uint32_t>,uint32_t> letter_id;
  size_t last_raw_states=0,last_raw_edges=0;
  explicit Engine(Budget& z):local(static_cast<long>(z.limits.max_states)),budget(z){local.init(order);}
  uint32_t label(int s,uint32_t lid){
    auto key=make_pair(s,lid);auto it=letter_id.find(key);
    if(it!=letter_id.end())return it->second;
    if(letters.size()>=UINT32_MAX)throw LimitReached("alphabet index capacity");
    uint32_t id=letters.size();letters.push_back({s,lid});letter_id[key]=id;return id;
  }
  DFA reduce(const NFA& raw){
    auto core=a113fa::trim(raw,budget);
    auto d=a113fa::determinize(core,budget);
    return a113fa::minimize(d,budget);
  }
  DFA initial(){
    NFA n;int K=local.NS;
    for(int i=0;i<=K;++i)n.add_state(i==K);
    n.add_initial(0);auto w=local.startState();
    for(int s=0;s<K;++s)n.add_edge(s,label(s,w[s]),s+1);
    n.add_edge(K,label(0,w[0]),1); // positive powers, excluding epsilon
    return reduce(n);
  }
  vector<int> domain(const SigTab* sig){
    if(sig->types[0]>T_LEVEN)return {NONE};
    vector<int> out(2*b-1);for(int c=0;c<2*b-1;++c)out[c]=c;return out;
  }
  DFA image(const DFA& source,int j,bool generic){
    NFA old=a113fa::as_nfa(source),out;
    vector<SigTab*> sig(local.NS);
    vector<vector<int>> coeff(local.NS);
    for(int s=0;s<local.NS;++s){sig[s]=local.sigFor(s,j,generic);coeff[s]=domain(sig[s]);}
    struct Cut{uint32_t old;int current,first;};
    vector<Cut> cuts;unordered_map<uint64_t,uint32_t> ids;
    size_t edge_count=0;
    auto intern=[&](uint32_t q,int c,int first){
      uint64_t key=(static_cast<uint64_t>(q)<<16)|(static_cast<uint64_t>(c+1)<<8)|static_cast<uint64_t>(first+1);
      auto it=ids.find(key);if(it!=ids.end())return it->second;
      uint32_t id=out.add_state(old.final[q] && c==first);
      cuts.push_back({q,c,first});ids.emplace(key,id);budget.observe(out.size(),edge_count);return id;
    };
    for(uint32_t q:old.initial)for(int c:coeff[0])out.add_initial(intern(q,c,c));
    for(size_t qi=0;qi<cuts.size();++qi){
      Cut cut=cuts[qi];
      for(const auto& edge:old.edges[cut.old]){
        budget.tick();if(edge.label>=letters.size())throw runtime_error("unknown input alphabet label");
        Letter a=letters[edge.label];int s=a.type,sn=(s+1)%local.NS;
        if(a.lid>=sig[s]->ent.size() || sig[s]->ent[a.lid].start==UNSET)local.fill(s,sig[s],a.lid);
        Ent entry=sig[s]->ent[a.lid];
        for(uint32_t i=0;i<entry.cnt;++i){
          OutE choice=local.sg[s].pool[static_cast<size_t>(entry.start)+i];
          if(choice.c!=cut.current)continue;
          for(int next:coeff[sn]){
            budget.tick();uint32_t to=intern(edge.to,next,cut.first);
            uint32_t lid=local.getLid(s,choice.yid,next);
            out.add_edge(qi,label(s,lid),to);++edge_count;budget.observe(out.size(),edge_count);
          }
        }
      }
    }
    last_raw_states=out.size();last_raw_edges=edge_count;
    return reduce(out);
  }
  bool nonempty(const DFA& d){
    // Reduced DFAs have only useful states, except one rejecting empty root.
    return any_of(d.final.begin(),d.final.end(),[](uint8_t x){return x!=0;});
  }
  vector<uint32_t> shortest(const DFA& d){
    vector<int64_t> parent(d.size(),-2);vector<uint32_t> lab(d.size());queue<uint32_t> todo;
    parent[d.initial]=-1;todo.push(d.initial);uint32_t end=0;bool found=false;
    while(!todo.empty()){
      uint32_t q=todo.front();todo.pop();budget.tick();
      if(d.final[q]){end=q;found=true;break;}
      for(const auto& x:d.edges[q])if(parent[x.to]==-2){parent[x.to]=q;lab[x.to]=x.label;todo.push(x.to);}
    }
    if(!found)throw runtime_error("requested witness of empty language");
    vector<uint32_t> word;while(parent[end]>=0){word.push_back(lab[end]);end=parent[end];}
    reverse(word.begin(),word.end());return word;
  }
  void dump(const DFA& d,int depth){
    cout<<"{\"event\":\"dump\",\"depth\":"<<depth<<",\"base\":"<<b<<",\"e\":\""<<es_
      <<"\",\"g\":\""<<gs_<<"\",\"v\":\"";for(int x:v)cout<<x;cout<<"\",\"order\":[";
    for(int s=0;s<local.NS;++s){if(s)cout<<',';cout<<'[';for(size_t j=0;j<order[s].size();++j){if(j)cout<<',';cout<<order[s][j];}cout<<']';}
    cout<<"],\"alphabet\":[";
    for(size_t z=0;z<letters.size();++z){
      if(z)cout<<',';Letter a=letters[z];auto info=local.sg[a.type].lidInfo[a.lid];const string& cfg=local.sg[a.type].cfg[info.first];
      cout<<"{\"label\":"<<z<<",\"type\":"<<a.type<<",\"z\":"<<int(info.second)<<",\"cfg\":[";
      for(size_t i=0;i<cfg.size()/3;++i){if(i)cout<<',';cout<<'['<<int(static_cast<uint8_t>(cfg[3*i]))<<','<<int(static_cast<uint8_t>(cfg[3*i+1]))<<','<<int(static_cast<uint8_t>(cfg[3*i+2]))-1<<']';}cout<<"]}";
    }
    cout<<"],\"dfa\":{\"initial\":"<<d.initial<<",\"final\":[";
    for(size_t i=0;i<d.final.size();++i){if(i)cout<<',';cout<<int(d.final[i]);}cout<<"],\"edges\":[";
    for(size_t i=0;i<d.edges.size();++i){if(i)cout<<',';cout<<'[';for(size_t j=0;j<d.edges[i].size();++j){if(j)cout<<',';cout<<'['<<d.edges[i][j].label<<','<<d.edges[i][j].to<<']';}cout<<']';}cout<<"]}}\n"<<flush;
  }
  void dump_text(const DFA& d){
    cout<<"A113REG1\n"<<b<<' '<<P<<'\n'<<es_<<'\n'<<gs_<<'\n';for(int x:v)cout<<x;
    cout<<'\n'<<local.NS<<' '<<letters.size()<<'\n';
    for(const auto& ts:order){cout<<ts.size();for(int t:ts)cout<<' '<<t;cout<<'\n';}
    for(Letter a:letters){
      auto info=local.sg[a.type].lidInfo[a.lid];const string& cfg=local.sg[a.type].cfg[info.first];
      cout<<a.type<<' '<<int(info.second);
      for(size_t j=0;j<cfg.size()/3;++j)cout<<' '<<int(static_cast<uint8_t>(cfg[3*j]))<<' '
        <<int(static_cast<uint8_t>(cfg[3*j+1]))<<' '<<int(static_cast<uint8_t>(cfg[3*j+2]))-1;
      cout<<'\n';
    }
    cout<<d.size()<<' '<<d.initial<<'\n';
    for(size_t q=0;q<d.size();++q){cout<<int(d.final[q])<<' '<<d.edges[q].size();for(const auto& x:d.edges[q])cout<<' '<<x.label<<' '<<x.to;cout<<'\n';}
    cout<<"END\n"<<flush;
  }
  void progress(const DFA& d,int depth,int count_k){
    cout<<"{\"event\":\"generic\",\"depth\":"<<depth<<",\"raw_states\":"<<last_raw_states
      <<",\"raw_edges\":"<<last_raw_edges<<",\"dfa_states\":"<<d.size()<<",\"dfa_edges\":"<<d.edge_count()<<",\"count_by_k\":[";
    for(int k=1;k<=count_k;++k){if(k>1)cout<<',';cout<<'\"'<<a113fa::count_words(d,k*local.NS,budget)<<'\"';}
    cout<<"],\"operations\":"<<budget.operations<<",\"rss_mib\":"<<rss_mb()<<"}\n"<<flush;
  }
  bool report_positive(const DFA& d,int width){
    if(!nonempty(d))return false;
    auto word=shortest(d);
    if(word.empty() || word.size()%local.NS)throw runtime_error("accepted word outside positive unit repetitions");
    cout<<"{\"status\":\"CENTER_LANGUAGE_ACCEPTS\",\"initial_width\":"<<width
      <<",\"repetitions\":"<<word.size()/local.NS<<",\"integer_replay_required\":true,\"word\":[";
    for(size_t j=0;j<word.size();++j){if(j)cout<<',';cout<<word[j];}cout<<"]}\n"<<flush;return true;
  }
};

static int solve(const Options& o){
  Budget budget(o.limits);int delta=0,minimum=0;
  for(int t=0;t<P;++t){minimum=min(minimum,delta);delta+=g[t]-2*v[t];}
  if(delta)throw invalid_argument("unit widths do not close");
  int a=1-minimum;
  if(!setup_instance(a+3))throw runtime_error("initial width construction failed");
  for(const auto& segment:order)if(segment.empty() || segment.size()>MAXL)throw invalid_argument("unsupported segment length");
  Engine engine(budget);DFA start=engine.initial();
  if(!o.generic_only){
    for(int width=a;width<a+2;++width){
      setup_instance(width);DFA cut=start;
      for(int j=0;j<Jall && engine.nonempty(cut);++j)cut=engine.image(cut,j,false);
      cout<<"{\"event\":\"short_width\",\"width\":"<<width<<",\"empty\":"<<(engine.nonempty(cut)?"false":"true")<<"}\n"<<flush;
      if(engine.report_positive(cut,width))return 0;
    }
  }
  setup_instance(a+3);DFA cut=engine.image(start,0,true);vector<DFA> past;
  for(int depth=1;depth<=o.depth;++depth){
    if(o.text_depth==depth){budget.check_time();engine.dump_text(cut);return 0;}
    if(o.text_depth<0)engine.progress(cut,depth,o.count_k);
    if(o.dump_depth==depth){engine.dump(cut,depth);cout<<"{\"status\":\"DUMPED\",\"no_exclusion_claim\":true}\n";return 0;}
    if(!o.generic_only){
      for(size_t old=0;old<past.size();++old)if(cut==past[old]){
        cout<<"{\"status\":\"NO_CENTERS_ALL_REPETITIONS\",\"classification\":\"COMPUTED\",\"jstar\":"<<old+1
          <<",\"period\":"<<depth-(old+1)<<",\"unit_period\":"<<P<<",\"operations\":"<<budget.operations<<"}\n";return 0;
      }
      if(!engine.nonempty(cut)){
        cout<<"{\"status\":\"NO_CENTERS_ALL_REPETITIONS\",\"classification\":\"COMPUTED\",\"reason\":\"empty_generic_language\"}\n";return 0;
      }
      past.push_back(cut);
      for(int parity=0;parity<2;++parity){
        setup_instance(a+2+parity);DFA tail=cut;
        for(int j=1;j<Jall && engine.nonempty(tail);++j)tail=engine.image(tail,j,false);
        cout<<"{\"event\":\"tail\",\"depth\":"<<depth<<",\"parity\":"<<parity
          <<",\"empty\":"<<(engine.nonempty(tail)?"false":"true")<<"}\n"<<flush;
        if(engine.report_positive(tail,a+2*depth+parity))return 0;
      }
    }
    if(depth<o.depth)cut=engine.image(cut,1,true);
  }
  cout<<"{\"status\":\"UNDECIDED\",\"reason\":\"generic_language_depth_limit\",\"depth\":"<<o.depth<<"}\n";return 3;
}
} // namespace a113regular

int main(int argc,char** argv){
  using namespace a113regular;
  try{auto o=parse(argc,argv);enforce_limits(o);int result=solve(o);alarm(0);return result;}
  catch(const invalid_argument&){alarm(0);cout<<"{\"status\":\"INVALID\",\"reason\":\"unsupported_or_malformed_input\"}\n";return 2;}
  catch(const LimitReached& x){alarm(0);cout<<"{\"status\":\"UNDECIDED\",\"reason\":\""<<x.what()<<"\"}\n";return 3;}
  catch(const bad_alloc&){alarm(0);const char s[]="{\"status\":\"UNDECIDED\",\"reason\":\"memory_limit\"}\n";(void)!write(1,s,sizeof(s)-1);return 3;}
  catch(const exception& x){alarm(0);cerr<<x.what()<<'\n';cout<<"{\"status\":\"UNDECIDED\",\"reason\":\"internal_error\"}\n";return 4;}
}
