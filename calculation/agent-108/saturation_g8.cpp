// Fixed saturated driver for the existing exact positional B automaton.
// Mathematical transition core: neutral_band/structure/bauto.cpp (unchanged).
// Completion guards credit Agent107; time-rotation quotient credits Agent103.
// Agent108 scope: g=(1000)^G, especially the distinct P32/G8 application.
#define main upstream_bauto_main_108
#include "../neutral_band/structure/bauto.cpp"
#undef main
#include <cerrno>
#include <cmath>
#include <iostream>
#include <limits>
#include <stdexcept>

struct Limit108 { string reason; };
struct Edge108 { K128 parent; vector<int> column; int rotation; };
struct Accept108 { K128 state; int depth; };

static unsigned long long number108(const char *s, unsigned long long maximum) {
  if (!s || !*s) throw invalid_argument("missing nonnegative integer");
  unsigned long long v=0;
  for (const char *q=s; *q; ++q) {
    if (*q<'0'||*q>'9') throw invalid_argument("invalid nonnegative integer");
    unsigned d=*q-'0';
    if(v>maximum/10 || (v==maximum/10 && d>maximum%10))
      throw invalid_argument("integer outside supported range");
    v=10*v+d;
  }
  return v;
}

static u64 mask108() { return (1ULL<<p)-1; }
static u64 rotate_bits108(u64 v,int r) {
  r%=int(Gidx.size()); if(r<0)r+=Gidx.size();
  int shift=4*r;
  return shift ? ((v>>shift)|(v<<(p-shift)))&mask108() : v;
}
static K128 rotate108(K128 s,int r) {
  int ng=Gidx.size(); r%=ng; if(r<0)r+=ng;
  if(!r)return s;
  u64 L,H;int Y[64],Z[64];unpack(s,L,H,Y,ng);
  for(int j=0;j<ng;++j)Z[j]=Y[(j+r)%ng];
  return pack(rotate_bits108(L,r),rotate_bits108(H,r),Z,ng);
}
static pair<K128,int> canonical108(K128 s,bool quotient) {
  pair<K128,int> answer{s,0};
  if(quotient)for(int r=1;r<int(Gidx.size());++r) {
    K128 z=rotate108(s,r); if(z<answer.first)answer={z,r};
  }
  return answer;
}
static string bits108(u64 x) {
  string s;for(int t=0;t<p;++t)s+=char('0'+((x>>t)&1));return s;
}
static void setup108(int ng) {
  b=10;p=4*ng;ydig=4;g.assign(p,0);Gidx.clear();
  for(int t=0;t<p;t+=4){g[t]=1;Gidx.push_back(t);}
  if(ng<1||ng>10||p>=64||2*p+ydig*ng>127)
    throw invalid_argument("supported saturation G is 1..10");
}
static void print_state108(K128 s) {
  u64 L,H;int Y[64];unpack(s,L,H,Y,Gidx.size());
  cout<<"["<<L<<","<<H<<",[";
  for(size_t j=0;j<Gidx.size();++j){if(j)cout<<',';cout<<Y[j];}
  cout<<"]]";
}

// Complete local successor set for the independent tuple differential tests.
static int step108(int argc,char **argv) {
  if(argc!=7)throw invalid_argument("usage: --step G L H YCSV FIRST");
  int ng=number108(argv[2],10);setup108(ng);
  u64 L=number108(argv[3],mask108()),H=number108(argv[4],mask108());
  vector<int> y;string word=argv[5],field;
  for(char c:word){if(c==','){if(field.empty())throw invalid_argument("empty Y field");y.push_back(number108(field.c_str(),9));field.clear();}else field+=c;}
  if(field.empty())throw invalid_argument("empty Y field");
  y.push_back(number108(field.c_str(),9));
  if(int(y.size())!=ng)throw invalid_argument("wrong Y length");
  bool first=number108(argv[6],1);
  vector<K128> out;
  transitions(L,H,y.data(),ng,first,[&](u64 l,u64 h,int *z,int *,int *) {
    if(out.size()>=1000000)throw Limit108{"step_output_cap"};
    out.push_back(pack(l,h,z,ng));
  });
  sort(out.begin(),out.end());out.erase(unique(out.begin(),out.end()),out.end());
  cout<<"[";for(size_t j=0;j<out.size();++j){if(j)cout<<',';print_state108(out[j]);}cout<<"]\n";
  return 0;
}

static int search108(int argc,char **argv) {
  if(argc<5)throw invalid_argument("usage: G STATE_CAP DEPTH_CAP SECONDS [--quotient] [--witness] [--layers]");
  int ng=number108(argv[1],10);setup108(ng);
  size_t cap=number108(argv[2],numeric_limits<size_t>::max());
  int maxdepth=number108(argv[3],1000000);
  unsigned long long seconds=number108(argv[4],1700);
  if(!cap||!seconds)throw invalid_argument("state/time limits must be positive");
  bool quotient=false,witness=false,layers=false;
  for(int j=5;j<argc;++j){string s=argv[j];if(s=="--quotient")quotient=true;else if(s=="--witness")witness=true;else if(s=="--layers")layers=true;else throw invalid_argument("unknown option");}
  int Y0[64];for(int j=0;j<ng;++j)Y0[j]=1;
  u64 H0=0;for(int t:Gidx)H0|=1ULL<<t;
  K128 start=pack(0,H0,Y0,ng);
  unordered_set<K128,KH> seen;seen.insert(start);
  unordered_map<K128,Edge108,KH> parents;
  vector<K128> front{start},next;
  vector<Accept108> accepted;
  unordered_set<u64> all_e;
  auto began=chrono::steady_clock::now();
  auto elapsed=[&](){return chrono::duration<double>(chrono::steady_clock::now()-began).count();};
  auto timecheck=[&](){if(elapsed()>=seconds)throw Limit108{"time_cap"};};
  int depth=0;size_t expanded=0;unsigned long long emitted=0;bool expanding=false;
  string reason;
  auto harvest=[&](const vector<K128>& layer,int width){
    for(K128 s:layer){
      u64 L,H;int Y[64];unpack(s,L,H,Y,ng);
      if(accepting(L,H,Y,ng)){
        bool fresh=false;
        for(int r=0;r<(quotient?ng:1);++r)fresh=all_e.insert(rotate_bits108(L,r)).second||fresh;
        if(fresh)accepted.push_back({s,width});
      }
    }
  };
  try {
    for(;;++depth){
      if(front.empty()){reason="frontier_empty";break;}
      // Harvest every fully reached layer, including a depth-limited layer.
      harvest(front,depth);
      if(layers)cout<<"{\"type\":\"LAYER\",\"depth\":"<<depth<<",\"frontier\":"<<front.size()<<",\"states\":"<<seen.size()<<",\"accepted_streams\":"<<all_e.size()<<"}\n"<<flush;
      if(depth>=maxdepth){reason="depth_cap";break;}
      next.clear();expanding=true;timecheck();
      for(K128 s:front){
        timecheck();u64 L,H;int Y[64];unpack(s,L,H,Y,ng);
        transitions(L,H,Y,ng,depth==0,[&](u64 l,u64 h,int *y,int *xs,int *){
          ++emitted;if((emitted&4095)==0)timecheck();
          auto z=canonical108(pack(l,h,y,ng),quotient);
          if(seen.find(z.first)!=seen.end())return;
          if(seen.size()>=cap)throw Limit108{"state_cap"};
          seen.insert(z.first);next.push_back(z.first);
          if(witness)parents.emplace(z.first,Edge108{s,vector<int>(xs,xs+p),z.second});
        });
        ++expanded;
      }
      front.swap(next);expanding=false;
    }
  } catch(const Limit108 &limit){reason=limit.reason;}
  // A capped expansion may already have inserted a terminal in the partial
  // next layer. Preserve it, including its parent path. Credit #335's review.
  if(expanding)harvest(next,depth+1);
  // External resource termination or a bad allocation never produces EXHAUSTED.
  cout<<"{\"type\":\"RESULT\",\"base\":10,\"G\":"<<ng<<",\"period\":"<<p
      <<",\"g\":\""<<bits108(H0)<<"\",\"quotient\":"<<(quotient?"true":"false")
      <<",\"status\":\""<<(reason=="frontier_empty"?"EXHAUSTED":"UNDECIDED")
      <<"\",\"reason\":\""<<reason<<"\",\"depth\":"<<depth<<",\"states\":"<<seen.size()
      <<",\"expanded\":"<<expanded<<",\"emitted\":"<<emitted<<",\"seconds\":"<<elapsed()<<",\"e\":[";
  vector<u64> es(all_e.begin(),all_e.end());sort(es.begin(),es.end());
  for(size_t j=0;j<es.size();++j){if(j)cout<<',';cout<<'"'<<bits108(es[j])<<'"';}
  cout<<"],\"witnesses\":[";
  if(witness)for(size_t j=0;j<accepted.size();++j){
    if(j)cout<<',';
    vector<Edge108> edges;K128 cursor=accepted[j].state;
    while(cursor!=start){const Edge108 &edge=parents.at(cursor);edges.push_back(edge);cursor=edge.parent;}
    reverse(edges.begin(),edges.end());vector<vector<int>> rows(p);int frame=0;
    for(const Edge108 &edge:edges){
      for(int t=0;t<p;++t)rows[t].push_back(edge.column[(t+4*frame)%p]);
      frame=(frame-edge.rotation+ng)%ng;
    }
    u64 L,H;int Y[64];unpack(accepted[j].state,L,H,Y,ng);
    cout<<"{\"e\":\""<<bits108(rotate_bits108(L,frame))<<"\",\"depth\":"<<accepted[j].depth<<",\"B_t\":[";
    for(int t=0;t<p;++t){if(t)cout<<',';while(!rows[t].empty()&&rows[t].back()==9)rows[t].pop_back();cout<<'[';for(size_t k=0;k<rows[t].size();++k){if(k)cout<<',';cout<<rows[t][k];}cout<<']';}
    cout<<"]}";
  }
  cout<<"]}\n"<<flush;
  return reason=="frontier_empty"?0:3;
}

int main(int argc,char **argv){
  try{if(argc>=2&&string(argv[1])=="--step")return step108(argc,argv);return search108(argc,argv);}
  catch(const Limit108 &e){cerr<<"{\"status\":\"UNDECIDED\",\"reason\":\""<<e.reason<<"\"}\n";return 3;}
  catch(const bad_alloc &){cerr<<"{\"status\":\"UNDECIDED\",\"reason\":\"memory_cap\"}\n";return 3;}
  catch(const exception &e){cerr<<"{\"status\":\"ERROR\",\"reason\":\""<<e.what()<<"\"}\n";return 2;}
}
