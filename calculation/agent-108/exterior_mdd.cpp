// Exact correlated exterior MDD for supplied decimal overflow words.
// Overflow gaps 1..5; optional prescribed carry word at the neutral terminal.
// Positional equations: existing neutral_band/structure/bauto.cpp.
// MDD motivation: Agent118's center transducer; Agent103 retains the G6 B task.
// Generalizes Agent108 saturation MDD; primary SQ5 lift remains Agent117.
// Nonuniform time blocks connect through exact coefficient ports.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <deque>
#include <functional>
#include <iostream>
#include <limits>
#include <map>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>
#include "wide_count.hpp"
using namespace std;
using Id=uint32_t;
using Count=agent108::WideCount;
using Arc=pair<int,Id>;
struct Limit { string reason; };
struct Tile { int out,right; array<int,5> coefficients; bool positive; };
using Local=array<vector<Tile>,19>;
static array<vector<Local>,6> tables;

static unsigned long long number(const char *s,unsigned long long maximum) {
  if(!s||!*s)throw invalid_argument("missing nonnegative integer");
  unsigned long long n=0;
  for(const char *p=s;*p;++p){
    if(*p<'0'||*p>'9')throw invalid_argument("invalid nonnegative integer");
    unsigned d=*p-'0';
    if(n>maximum/10||(n==maximum/10&&d>maximum%10))throw invalid_argument("integer outside supported range");
    n=10*n+d;
  }
  return n;
}
static string decimal(const Count& n){return n.decimal();}
static bool terminal_symbol(int s,int length,int required){
  int mask=(1<<length)-1,L=s&mask,H=(s>>length)&mask,Y=s>>(2*length);
  return H==(mask^L)&&Y==9*(L&1)&&(required<0||L==required);
}
struct Pattern {
  string original,word;int shift=0,P=0;vector<int> lengths,starts,initial;
};
static Pattern pattern(const string &original){
  if(original.empty()||original.find_first_not_of("01")!=string::npos)
    throw invalid_argument("g must be a nonempty binary word");
  if(original.size()>96)throw Limit{"unsupported_period"};
  Pattern p;p.original=original;p.P=original.size();
  auto first=original.find('1');if(first==string::npos)throw Limit{"unsupported_zero_overflow"};
  p.shift=first;p.word=original.substr(first)+original.substr(0,first);
  for(int t=0;t<p.P;++t)if(p.word[t]=='1')p.starts.push_back(t);
  if(2*p.P+4*p.starts.size()>240)throw Limit{"unsupported_count_budget"};
  for(size_t j=0;j<p.starts.size();++j){
    int next=j+1<p.starts.size()?p.starts[j+1]:p.P;
    int length=next-p.starts[j];if(length>5)throw Limit{"unsupported_overflow_gap"};
    p.lengths.push_back(length);p.initial.push_back((1<<length)+(1<<(2*length)));
  }
  return p;
}
static vector<int> target_low(const Pattern &p,const string &e){
  vector<int> result(p.lengths.size(),-1);if(e.empty())return result;
  if(int(e.size())!=p.P||e.find_first_not_of("01")!=string::npos)
    throw invalid_argument("e must be a binary word of the same length as g");
  string rotated=e.substr(p.shift)+e.substr(0,p.shift);
  for(size_t j=0;j<p.lengths.size();++j){result[j]=0;for(int t=0;t<p.lengths[j];++t)result[j]|=(rotated[p.starts[j]+t]-'0')<<t;}
  return result;
}
static void build_tiles(int length){
  if(!tables[length].empty())return;
  int mask=(1<<length)-1,alphabet=10*(1<<(2*length));tables[length].resize(alphabet);
  for(int s=0;s<alphabet;++s){
    int L=s&mask,H=(s>>length)&mask,Y=s>>(2*length);
    for(int hn=0;hn<=mask;++hn)for(int yn=0;yn<10;++yn){
      int x=10*(H&1)+yn-(hn&1),left=x;
      if(x<0||x>18)continue;
      int ln=0;bool good=true,positive=true;array<int,5> xs{};
      for(int t=0;t<length;++t){
        int l=(L>>t)&1,h=(H>>t)&1,hnext=(hn>>t)&1;
        if((x+hnext)/10!=h){good=false;break;}
        xs[t]=x;positive=positive&&x>0;ln|=((x+l)/10)<<t;
        x=(x+l)%10+(t==0?Y:(x+hnext)%10);
      }
      if(good)tables[length][s][left].push_back({ln+(hn<<length)+(yn<<(2*length)),x,xs,positive});
    }
  }
}

struct Node { int level; vector<Arc> arcs; Count count,accepts; };
struct Arena {
  int G,P;vector<int> lengths,starts,required_low;size_t cap;uint64_t operation_cap,operations=0;
  unsigned seconds;chrono::steady_clock::time_point began;
  deque<Node> nodes;
  unordered_map<uint64_t,vector<Id>> unique;
  unordered_map<uint64_t,Id> union_memo;
  Arena(const Pattern &p,const string &e,size_t n,uint64_t ops,unsigned sec):G(p.lengths.size()),P(p.P),lengths(p.lengths),starts(p.starts),required_low(target_low(p,e)),cap(n),operation_cap(ops),seconds(sec),began(chrono::steady_clock::now()){
    for(int length:lengths)build_tiles(length);
    nodes.push_back({-1,{},0,0});nodes.push_back({G,{},1,1});
  }
  double elapsed()const{return chrono::duration<double>(chrono::steady_clock::now()-began).count();}
  void tick(){if(operations>=operation_cap)throw Limit{"operation_cap"};++operations;if((operations&16383)==0&&elapsed()>=seconds)throw Limit{"time_cap"};}
  Id intern(int level,vector<Arc> arcs){
    tick();arcs.erase(remove_if(arcs.begin(),arcs.end(),[](Arc a){return a.second==0;}),arcs.end());
    if(arcs.empty())return 0;
    uint64_t hash=1469598103934665603ULL;hash=(hash^uint64_t(level))*1099511628211ULL;
    int prior=-1;
    for(Arc a:arcs){
      if(a.first<=prior||a.first>=10*(1<<(2*lengths[level]))||a.first<0||a.second>=nodes.size()||nodes[a.second].level!=level+1)
        throw logic_error("malformed ordered MDD node");
      prior=a.first;hash=(hash^uint64_t(a.first))*1099511628211ULL;hash=(hash^uint64_t(a.second))*1099511628211ULL;
    }
    auto &bucket=unique[hash];for(Id id:bucket)if(nodes[id].level==level&&nodes[id].arcs==arcs)return id;
    if(nodes.size()>=cap)throw Limit{"node_cap"};
    Count count=0,accepts=0;for(Arc a:arcs){count+=nodes[a.second].count;if(terminal_symbol(a.first,lengths[level],required_low[level]))accepts+=nodes[a.second].accepts;}
    Id id=nodes.size();nodes.push_back({level,move(arcs),count,accepts});bucket.push_back(id);return id;
  }
  Id unite(Id a,Id b){
    tick();if(a==b||b==0)return a;if(a==0)return b;if(a>b)swap(a,b);
    if(nodes[a].level!=nodes[b].level)throw logic_error("MDD level mismatch");
    uint64_t key=(uint64_t(a)<<32)|b;auto found=union_memo.find(key);if(found!=union_memo.end())return found->second;
    const auto &x=nodes[a].arcs,&y=nodes[b].arcs;vector<Arc> z;size_t i=0,j=0;
    while(i<x.size()||j<y.size()){
      if(j==y.size()||(i<x.size()&&x[i].first<y[j].first))z.push_back(x[i++]);
      else if(i==x.size()||y[j].first<x[i].first)z.push_back(y[j++]);
      else{z.emplace_back(x[i].first,unite(x[i].second,y[j].second));++i;++j;}
    }
    Id result=intern(nodes[a].level,move(z));union_memo.emplace(key,result);return result;
  }
  Id singleton(const vector<int> &word){
    if(int(word.size())!=G)throw logic_error("wrong MDD word length");
    Id id=1;for(int i=G-1;i>=0;--i)id=intern(i,{{word[i],id}});return id;
  }
  Id image(Id root,bool first){
    unordered_map<uint64_t,Id> memo;
    function<Id(Id,int,int)> visit=[&](Id old,int required,int initial)->Id{
      tick();if(!old)return 0;if(old==1)return required==initial?1:0;
      uint64_t key=uint64_t(old)*361+19*required+initial;
      auto found=memo.find(key);if(found!=memo.end())return found->second;
      map<int,Id> target;
      for(Arc arc:nodes[old].arcs)for(const Tile &tile:tables[lengths[nodes[old].level]][arc.first][required]){
        tick();if(first&&!tile.positive)continue;
        Id child=visit(arc.second,tile.right,initial);if(!child)continue;
        auto it=target.find(tile.out);if(it==target.end())target.emplace(tile.out,child);else it->second=unite(it->second,child);
      }
      Id answer=intern(nodes[old].level,vector<Arc>(target.begin(),target.end()));memo.emplace(key,answer);return answer;
    };
    Id out=0;for(int initial=0;initial<19;++initial)out=unite(out,visit(root,initial,initial));return out;
  }
  vector<int> accepted_word(Id root)const{
    if(!nodes[root].accepts)throw logic_error("no accepting word");
    vector<int> word;
    while(root!=1){bool found=false;for(Arc a:nodes[root].arcs)if(terminal_symbol(a.first,lengths[nodes[root].level],required_low[nodes[root].level])&&nodes[a.second].accepts){word.push_back(a.first);root=a.second;found=true;break;}if(!found)throw logic_error("acceptance count mismatch");}
    return word;
  }
  pair<vector<int>,vector<int>> predecessor(Id root,const vector<int> &target,bool first){
    unordered_set<uint64_t> failed;
    vector<int> word(G),column(P);
    function<bool(Id,int,int)> visit=[&](Id old,int required,int initial)->bool{
      tick();if(!old)return false;if(old==1)return required==initial;
      uint64_t key=uint64_t(old)*361+19*required+initial;if(failed.count(key))return false;
      int level=nodes[old].level;
      for(Arc arc:nodes[old].arcs)for(const Tile &tile:tables[lengths[nodes[old].level]][arc.first][required]){
        tick();if(tile.out!=target[level]||(first&&!tile.positive))continue;
        if(visit(arc.second,tile.right,initial)){
          word[level]=arc.first;for(int t=0;t<lengths[level];++t)column[starts[level]+t]=tile.coefficients[t];return true;
        }
      }
      failed.insert(key);return false;
    };
    for(int initial=0;initial<19;++initial)if(visit(root,initial,initial))return {word,column};
    throw logic_error("reached MDD word has no predecessor");
  }
};

static void print_words(Arena &arena,Id root,size_t cap){
  if(arena.nodes[root].count>cap)throw Limit{"export_cap"};
  bool comma=false;vector<int> word;
  function<void(Id)> visit=[&](Id node){
    if(!node)return;
    if(node==1){if(comma)cout<<',';comma=true;cout<<'[';for(size_t j=0;j<word.size();++j){if(j)cout<<',';cout<<word[j];}cout<<']';return;}
    for(Arc a:arena.nodes[node].arcs){word.push_back(a.first);visit(a.second);word.pop_back();}
  };
  cout<<'[';visit(root);cout<<"]\n";
}

static int run(int argc,char **argv){
  if(argc==3&&string(argv[1])=="--tiles"){
    int length=number(argv[2],5);if(length<1)throw invalid_argument("tile length must be 1..5");build_tiles(length);
    for(size_t s=0;s<tables[length].size();++s)for(int left=0;left<19;++left)for(const Tile&t:tables[length][s][left]){
      cout<<s<<' '<<t.out<<' '<<left<<' '<<t.right<<' '<<t.positive;
      for(int j=0;j<length;++j)cout<<' '<<t.coefficients[j];cout<<'\n';
    }
    return 0;
  }
  if(argc==4&&string(argv[1])=="--image"){
    Pattern p=pattern(argv[2]);bool first=number(argv[3],1);
    Arena arena(p,"",1000000,200000000,30);Id root=0;
    unsigned long long count;if(!(cin>>count)||count>100000)throw invalid_argument("bad finite-set size");
    for(unsigned long long n=0;n<count;++n){vector<int> word(p.lengths.size());for(size_t j=0;j<word.size();++j)if(!(cin>>word[j])||word[j]<0||word[j]>=10*(1<<(2*p.lengths[j])))throw invalid_argument("bad finite-set symbol");root=arena.unite(root,arena.singleton(word));}
    string extra;if(cin>>extra)throw invalid_argument("trailing finite-set input");
    print_words(arena,arena.image(root,first),1000000);return 0;
  }
  if(argc<6)throw invalid_argument("usage: GWORD NODE_CAP OPERATION_CAP DEPTH_CAP SECONDS [--e EWORD] [--witness] [--export-layer N]");
  Pattern p=pattern(argv[1]);
  size_t cap=number(argv[2],numeric_limits<uint32_t>::max());
  uint64_t ops=number(argv[3],numeric_limits<uint64_t>::max());
  int depthcap=number(argv[4],1000000);unsigned seconds=number(argv[5],1700);
  if(cap<2||!ops||!seconds)throw invalid_argument("invalid resource limit");
  bool witness=false;int export_layer=-1;string wanted_e;
  for(int j=6;j<argc;++j){string s=argv[j];if(s=="--witness")witness=true;else if(s=="--export-layer"&&j+1<argc)export_layer=number(argv[++j],depthcap);else if(s=="--e"&&j+1<argc){wanted_e=argv[++j];if(wanted_e.empty())throw invalid_argument("empty requested e");}else throw invalid_argument("unknown or incomplete option");}
  Arena arena(p,wanted_e,cap,ops,seconds);vector<Id> roots;unordered_map<Id,int> prior;
  Id root=0;int depth=0,cycle_start=-1;string reason;bool feasible=false;
  try{
    root=arena.singleton(p.initial);roots.push_back(root);
    for(;;++depth){
      if(export_layer==depth){print_words(arena,root,1000000);return 0;}
      cout<<"{\"type\":\"LAYER\",\"depth\":"<<depth<<",\"root\":"<<root<<",\"states\":\""<<decimal(arena.nodes[root].count)<<"\",\"accepts\":\""<<decimal(arena.nodes[root].accepts)<<"\",\"nodes\":"<<arena.nodes.size()<<",\"operations\":"<<arena.operations<<"}\n"<<flush;
      if(arena.nodes[root].accepts){feasible=true;reason="terminal_reached";break;}
      if(!root){reason="empty_layer";break;}
      if(depth>=1){auto it=prior.find(root);if(it!=prior.end()){cycle_start=it->second;reason="exact_layer_repeat";break;}prior[root]=depth;}
      if(depth>=depthcap){reason="depth_cap";break;}
      root=arena.image(root,depth==0);roots.push_back(root);
    }
    if(feasible&&witness){
      vector<int> terminal=arena.accepted_word(root),current=terminal;
      vector<vector<int>> columns;
      for(int n=depth;n>=1;--n){auto pred=arena.predecessor(roots[n-1],current,n==1);current=move(pred.first);columns.push_back(move(pred.second));}
      if(current!=p.initial)throw logic_error("witness does not start at physical boundary");
      reverse(columns.begin(),columns.end());string rotated_e;
      for(size_t j=0;j<terminal.size();++j)for(int t=0;t<p.lengths[j];++t)rotated_e+=char('0'+((terminal[j]>>t)&1));
      string e=rotated_e.substr(p.P-p.shift)+rotated_e.substr(0,p.P-p.shift);
      cout<<"{\"type\":\"WITNESS\",\"g\":\""<<p.original<<"\",\"e\":\""<<e<<"\",\"B_t\":[";
      for(int t=0;t<p.P;++t){if(t)cout<<',';int phase=(t-p.shift+p.P)%p.P;vector<int> row;for(const auto &col:columns)row.push_back(col[phase]);while(!row.empty()&&row.back()==9)row.pop_back();cout<<'[';for(size_t j=0;j<row.size();++j){if(j)cout<<',';cout<<row[j];}cout<<']';}cout<<"]}\n"<<flush;
    }
  }catch(const Limit &limit){reason=limit.reason;}
  bool negative=reason=="empty_layer"||reason=="exact_layer_repeat";
  string status=feasible?"FEASIBLE":negative?(wanted_e.empty()?"EXHAUSTED_NO_B":"EXHAUSTED_NO_B_FOR_E"):"UNDECIDED";
  cout<<"{\"type\":\"RESULT\",\"g\":\""<<p.original<<"\",\"requested_e\":\""<<wanted_e<<"\",\"period\":"<<p.P<<",\"G\":"<<p.lengths.size()<<",\"phase_rotation\":"<<p.shift<<",\"status\":\""<<status<<"\",\"reason\":\""<<reason<<"\",\"depth\":"<<depth<<",\"cycle_start\":"<<cycle_start<<",\"nodes\":"<<arena.nodes.size()<<",\"operations\":"<<arena.operations<<",\"seconds\":"<<arena.elapsed()<<"}\n"<<flush;
  return feasible||negative?0:3;
}
int main(int argc,char **argv){
  try{return run(argc,argv);}
  catch(const Limit &e){cerr<<"{\"status\":\"UNDECIDED\",\"reason\":\""<<e.reason<<"\"}\n";return 3;}
  catch(const bad_alloc &){cerr<<"{\"status\":\"UNDECIDED\",\"reason\":\"memory_cap\"}\n";return 3;}
  catch(const exception &e){cerr<<"{\"status\":\"ERROR\",\"reason\":\""<<e.what()<<"\"}\n";return 2;}
}
