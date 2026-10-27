// Exact full-correlation block MDD for decimal g=(1000)^G exterior cuts.
// Positional equations: existing neutral_band/structure/bauto.cpp.
// MDD motivation: Agent118's center transducer; Agent103 retains the G6 B task.
// This implementation independently uses four-time blocks and coefficient ports.
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
using namespace std;
using Id=uint32_t;
using Count=unsigned __int128;
using Arc=pair<int,Id>;
struct Limit { string reason; };
struct Tile { int out,right; array<int,4> coefficients; bool positive; };
using Local=array<vector<Tile>,19>;
static array<Local,2560> tiles;

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
static string decimal(Count n){if(!n)return "0";string s;while(n){s+=char('0'+n%10);n/=10;}reverse(s.begin(),s.end());return s;}
static bool terminal_symbol(int s){int L=s&15,H=(s>>4)&15,Y=s>>8;return H==(15^L)&&Y==9*(L&1);}

static void build_tiles(){
  for(int s=0;s<2560;++s){
    int L=s&15,H=(s>>4)&15,Y=s>>8;
    for(int hn=0;hn<16;++hn)for(int yn=0;yn<10;++yn){
      int x=10*(H&1)+yn-(hn&1),left=x;
      if(x<0||x>18)continue;
      int ln=0;bool good=true,positive=true;array<int,4> xs{};
      for(int t=0;t<4;++t){
        int l=(L>>t)&1,h=(H>>t)&1,hnext=(hn>>t)&1;
        if((x+hnext)/10!=h){good=false;break;}
        xs[t]=x;positive=positive&&x>0;
        ln|=((x+l)/10)<<t;
        x=(x+l)%10+(t==0?Y:(x+hnext)%10);
      }
      if(good)tiles[s][left].push_back({ln+(hn<<4)+(yn<<8),x,xs,positive});
    }
  }
}

struct Node { int level; vector<Arc> arcs; Count count,accepts; };
struct Arena {
  int G;size_t cap;uint64_t operation_cap,operations=0;
  unsigned seconds;chrono::steady_clock::time_point began;
  deque<Node> nodes;
  unordered_map<uint64_t,vector<Id>> unique;
  unordered_map<uint64_t,Id> union_memo;
  Arena(int g,size_t n,uint64_t ops,unsigned sec):G(g),cap(n),operation_cap(ops),seconds(sec),began(chrono::steady_clock::now()){
    nodes.push_back({-1,{},0,0});nodes.push_back({G,{},1,1});
  }
  double elapsed()const{return chrono::duration<double>(chrono::steady_clock::now()-began).count();}
  void tick(){if(++operations>operation_cap)throw Limit{"operation_cap"};if((operations&16383)==0&&elapsed()>=seconds)throw Limit{"time_cap"};}
  Id intern(int level,vector<Arc> arcs){
    tick();arcs.erase(remove_if(arcs.begin(),arcs.end(),[](Arc a){return a.second==0;}),arcs.end());
    if(arcs.empty())return 0;
    uint64_t hash=1469598103934665603ULL;hash=(hash^uint64_t(level))*1099511628211ULL;
    int prior=-1;
    for(Arc a:arcs){
      if(a.first<=prior||a.first>=2560||a.first<0||a.second>=nodes.size()||nodes[a.second].level!=level+1)
        throw logic_error("malformed ordered MDD node");
      prior=a.first;hash=(hash^uint64_t(a.first))*1099511628211ULL;hash=(hash^uint64_t(a.second))*1099511628211ULL;
    }
    auto &bucket=unique[hash];for(Id id:bucket)if(nodes[id].level==level&&nodes[id].arcs==arcs)return id;
    if(nodes.size()>=cap)throw Limit{"node_cap"};
    Count count=0,accepts=0;for(Arc a:arcs){count+=nodes[a.second].count;if(terminal_symbol(a.first))accepts+=nodes[a.second].accepts;}
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
      for(Arc arc:nodes[old].arcs)for(const Tile &tile:tiles[arc.first][required]){
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
    while(root!=1){bool found=false;for(Arc a:nodes[root].arcs)if(terminal_symbol(a.first)&&nodes[a.second].accepts){word.push_back(a.first);root=a.second;found=true;break;}if(!found)throw logic_error("acceptance count mismatch");}
    return word;
  }
  pair<vector<int>,vector<int>> predecessor(Id root,const vector<int> &target,bool first){
    unordered_set<uint64_t> failed;
    vector<int> word(G),column(4*G);
    function<bool(Id,int,int)> visit=[&](Id old,int required,int initial)->bool{
      tick();if(!old)return false;if(old==1)return required==initial;
      uint64_t key=uint64_t(old)*361+19*required+initial;if(failed.count(key))return false;
      int level=nodes[old].level;
      for(Arc arc:nodes[old].arcs)for(const Tile &tile:tiles[arc.first][required]){
        tick();if(tile.out!=target[level]||(first&&!tile.positive))continue;
        if(visit(arc.second,tile.right,initial)){
          word[level]=arc.first;for(int t=0;t<4;++t)column[4*level+t]=tile.coefficients[t];return true;
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
  if(argc==2&&string(argv[1])=="--tiles"){
    for(int s=0;s<2560;++s)for(int left=0;left<19;++left)for(const Tile&t:tiles[s][left])
      cout<<s<<' '<<t.out<<' '<<left<<' '<<t.right<<' '<<t.positive<<' '<<t.coefficients[0]<<' '<<t.coefficients[1]<<' '<<t.coefficients[2]<<' '<<t.coefficients[3]<<'\n';
    return 0;
  }
  // A finite complete-set image interface for independent correlation tests.
  // Input is N followed by N words of G symbols, whitespace separated.
  if(argc==4&&string(argv[1])=="--image"){
    int G=number(argv[2],10);bool first=number(argv[3],1);
    if(!G)throw invalid_argument("G must be 1..10");
    Arena arena(G,1000000,200000000,30);Id root=0;
    unsigned long long count;if(!(cin>>count)||count>100000)throw invalid_argument("bad finite-set size");
    for(unsigned long long n=0;n<count;++n){vector<int> word(G);for(int &s:word)if(!(cin>>s)||s<0||s>=2560)throw invalid_argument("bad finite-set symbol");root=arena.unite(root,arena.singleton(word));}
    string extra;if(cin>>extra)throw invalid_argument("trailing finite-set input");
    print_words(arena,arena.image(root,first),1000000);return 0;
  }
  if(argc<6)throw invalid_argument("usage: G NODE_CAP OPERATION_CAP DEPTH_CAP SECONDS [--witness] [--export-layer N]");
  int G=number(argv[1],10);if(!G)throw invalid_argument("G must be 1..10");
  size_t cap=number(argv[2],numeric_limits<uint32_t>::max());
  uint64_t ops=number(argv[3],numeric_limits<uint64_t>::max());
  int depthcap=number(argv[4],1000000);unsigned seconds=number(argv[5],1700);
  if(cap<2||!ops||!seconds)throw invalid_argument("invalid resource limit");
  bool witness=false;int export_layer=-1;
  for(int j=6;j<argc;++j){string s=argv[j];if(s=="--witness")witness=true;else if(s=="--export-layer"&&j+1<argc)export_layer=number(argv[++j],depthcap);else throw invalid_argument("unknown or incomplete option");}
  Arena arena(G,cap,ops,seconds);vector<Id> roots;unordered_map<Id,int> prior;
  Id root=0;int depth=0,cycle_start=-1;string reason;bool feasible=false;
  try{
    root=arena.singleton(vector<int>(G,272));roots.push_back(root);
    for(;;++depth){
      if(export_layer==depth){print_words(arena,root,1000000);return 0;}
      cout<<"{\"type\":\"LAYER\",\"G\":"<<G<<",\"depth\":"<<depth<<",\"root\":"<<root<<",\"states\":\""<<decimal(arena.nodes[root].count)<<"\",\"accepts\":\""<<decimal(arena.nodes[root].accepts)<<"\",\"nodes\":"<<arena.nodes.size()<<",\"operations\":"<<arena.operations<<"}\n"<<flush;
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
      if(current!=vector<int>(G,272))throw logic_error("witness does not start at physical boundary");
      reverse(columns.begin(),columns.end());string e;for(int s:terminal)for(int t=0;t<4;++t)e+=char('0'+((s>>t)&1));
      cout<<"{\"type\":\"WITNESS\",\"e\":\""<<e<<"\",\"B_t\":[";
      for(int t=0;t<4*G;++t){if(t)cout<<',';vector<int> row;for(const auto &col:columns)row.push_back(col[t]);while(!row.empty()&&row.back()==9)row.pop_back();cout<<'[';for(size_t j=0;j<row.size();++j){if(j)cout<<',';cout<<row[j];}cout<<']';}cout<<"]}\n"<<flush;
    }
  }catch(const Limit &limit){reason=limit.reason;}
  bool negative=reason=="empty_layer"||reason=="exact_layer_repeat";
  string status=feasible?"FEASIBLE":negative?"EXHAUSTED_NO_B":"UNDECIDED";
  cout<<"{\"type\":\"RESULT\",\"G\":"<<G<<",\"period\":"<<4*G<<",\"status\":\""<<status<<"\",\"reason\":\""<<reason<<"\",\"depth\":"<<depth<<",\"cycle_start\":"<<cycle_start<<",\"nodes\":"<<arena.nodes.size()<<",\"operations\":"<<arena.operations<<",\"seconds\":"<<arena.elapsed()<<"}\n"<<flush;
  return feasible||negative?0:3;
}
int main(int argc,char **argv){
  try{build_tiles();return run(argc,argv);}
  catch(const Limit &e){cerr<<"{\"status\":\"UNDECIDED\",\"reason\":\""<<e.reason<<"\"}\n";return 3;}
  catch(const bad_alloc &){cerr<<"{\"status\":\"UNDECIDED\",\"reason\":\"memory_cap\"}\n";return 3;}
  catch(const exception &e){cerr<<"{\"status\":\"ERROR\",\"reason\":\""<<e.what()<<"\"}\n";return 2;}
}
