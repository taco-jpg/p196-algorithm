// Exact necessary-condition refinement for centered spatial-period-four bulks.
// This program supplies no finite exterior and asserts no Lychrel witness.
// Build: g++ -O3 -std=c++17 next_period4_refine.cpp -o next_period4_refine
// Run: ./next_period4_refine 5 next_period4_results.json
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <queue>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;
struct Bulk { array<int,4> q; int phase; array<int,2> next{{-1,-1}}; };
struct Node { int bulk; uint64_t q; int component; };
struct Graph { vector<array<int,2>> edge; vector<array<int,2>> flag; };
struct SCC { vector<int> id, size; vector<bool> growth; };
static array<int,4> forwardCarry(array<int,4> q) {
  array<int,4> a{}; int c=0;
  for(int pass=0;pass<2;pass++) for(int j=0;j<4;j++) {a[j]=c;c=(q[j]+c)/10;}
  return a;
}
static array<int,4> backwardCarry(array<int,4> q) {
  array<int,4> b{}; int c=0;
  for(int pass=0;pass<2;pass++) for(int j=3;j>=0;j--) {c=(q[j]+c)/10;b[j]=c;}
  return b;
}
static int code(array<int,4> q) {int n=0;for(int x:q)n=n*19+x;return n;}
static SCC components(const Graph& g) {
  const int n=g.edge.size(); vector<int> index(n,-1),low(n),stack,call;
  vector<uint8_t> active(n,0),position(n,0); SCC s; s.id.assign(n,-1);
  int tick=0;
  for(int root=0;root<n;root++) if(index[root]<0) {
    call.push_back(root); index[root]=low[root]=tick++; stack.push_back(root);active[root]=1;
    while(!call.empty()) {
      int u=call.back();
      if(position[u]<2) {
        int v=g.edge[u][position[u]++];if(v<0)continue;
        if(index[v]<0) {
          index[v]=low[v]=tick++;stack.push_back(v);active[v]=1;call.push_back(v);
        } else if(active[v]) low[u]=min(low[u],index[v]);
      } else {
        call.pop_back();
        if(!call.empty())low[call.back()]=min(low[call.back()],low[u]);
        if(low[u]==index[u]) {
          int id=s.size.size(),count=0;
          while(true) {int v=stack.back();stack.pop_back();active[v]=0;s.id[v]=id;count++;if(v==u)break;}
          s.size.push_back(count);
        }
      }
    }
  }
  s.growth.assign(s.size.size(),false);
  for(int u=0;u<n;u++)for(int e=0;e<2;e++) {
    int v=g.edge[u][e];if(v>=0&&s.id[u]==s.id[v]&&g.flag[u][e])s.growth[s.id[u]]=true;
  }
  return s;
}
static vector<Bulk> makeBulks() {
  const int base=19*19*19*19;vector<int> ids(8*base,-1);vector<Bulk> out;
  for(int s=0;s<8;s++)for(int n=0;n<base;n++) {
    int m=n;array<int,4> q{};for(int j=3;j>=0;j--){q[j]=m%19;m/=19;}
    if(q[0]==q[1]&&q[1]==q[2]&&q[2]==q[3])continue;
    bool valid=true;for(int j=0;j<4;j++)if(q[j]!=q[(s-1-j+8)%4])valid=false;
    if(!valid)continue;
    auto a=forwardCarry(q),b=backwardCarry(q);
    if(s%2==0)valid=a[(s/2)%4]==b[(s/2)%4];
    else {int j=((s-1)/2)%4;valid=q[j]%2==0&&a[j]==b[(j+1)%4];}
    if(valid){ids[s*base+n]=out.size();out.push_back({q,s});}
  }
  for(auto& v:out) {
    auto a=forwardCarry(v.q),b=backwardCarry(v.q);
    for(int h=0;h<2;h++) {
      array<int,4> q{};
      for(int j=0;j<4;j++) {
        int i=(j-h+4)%4;
        q[j]=(v.q[j]+a[j])%10+(v.q[i]+b[(i+1)%4])%10;
      }
      v.next[h]=ids[((v.phase+h)%8)*base+code(q)];
    }
  }
  return out;
}
static pair<uint64_t,int> outer(uint64_t code,int k,int inner) {
  vector<int> q(k),lo(k),hi(k);
  for(int j=k-1;j>=0;j--){q[j]=code%19;code/=19;}
  int c=0;
  for(int j=0;j<k;j++){int total=q[j]+c;lo[j]=total%10;c=total/10;}
  c=inner;
  for(int j=k-1;j>=0;j--){int total=q[j]+c;hi[j]=total%10;c=total/10;}
  int h=c;uint64_t target=0;
  for(int j=0;j<k;j++) {
    int digit=lo[j]+(h?(j==0?1:hi[j-1]):hi[j]);
    if(digit<0||digit>18||(j==0&&digit==0))throw runtime_error("invalid outer transition");
    target=19*target+digit;
  }
  return {target,h};
}
struct Connection {bool safe=false,shape=false;uint64_t outer=0;int overflow=0;};
static Connection connect(const Node& node,int k,const vector<Bulk>& bulks,int offset) {
  // At least sixteen bulk positions, plus phase, hence each direction has
  // reset its carry before it reaches the untouched periodic interior.
  int m=offset+bulks[node.bulk].phase,n=2*k+m;
  if(n+1>128)throw runtime_error("connector storage limit");
  array<int,128> q{},d{};uint64_t code=node.q;
  for(int j=k-1;j>=0;j--){q[j]=code%19;code/=19;}
  for(int j=0;j<m;j++)q[k+j]=bulks[node.bulk].q[j%4];
  for(int j=0;j<k;j++)q[n-1-j]=q[j];
  int carry=0;
  for(int j=0;j<n;j++){int total=q[j]+carry;d[j]=total%10;carry=total/10;}
  Connection out;out.overflow=carry;int length=n+carry;if(carry)d[n]=1;
  for(int j=0;j<length;j++)if(d[j]!=d[length-1-j])out.safe=true;
  int nb=bulks[node.bulk].next[carry];if(nb<0)return out;
  for(int j=0;j<k;j++)out.outer=19*out.outer+d[j]+d[length-1-j];
  out.shape=true;
  for(int j=0;j<m+carry;j++)if(d[k+j]+d[length-1-k-j]!=bulks[nb].q[j%4])out.shape=false;
  return out;
}
static uint64_t key(const Node& n,uint64_t power){return n.bulk*power+n.q;}
static vector<int> digits(uint64_t q,int k) {vector<int> d(k);for(int j=k-1;j>=0;j--){d[j]=q%19;q/=19;}return d;}
template<class T>static void arrayJSON(ostream& os,const T& x) {os<<'[';bool first=true;for(auto v:x){if(!first)os<<',';first=false;os<<v;}os<<']';}
static void cyclesJSON(ostream& os,const vector<Node>& nodes,const vector<Bulk>& bulks,
                       const Graph& g,const SCC& s,int k) {
  // One shortest return through an internal growth edge per positive SCC.
  vector<int> first(s.size.size(),-1),fe(s.size.size(),-1);
  for(int u=0;u<(int)nodes.size();u++)for(int e=0;e<2;e++) {
    int v=g.edge[u][e],c=s.id[u];
    if(v>=0&&s.id[v]==c&&g.flag[u][e]&&first[c]<0){first[c]=u;fe[c]=e;}
  }
  os<<'[';bool comma=false;int supplied=0;
  vector<int> parent(nodes.size(),-1),pe(nodes.size(),-1),seen(nodes.size(),-1);
  for(int c=0;c<(int)s.size.size();c++)if(s.growth[c]) {
    if(supplied>=1000)break;
    if(comma)os<<',';comma=true;supplied++;
    int u=first[c],e=fe[c],v=g.edge[u][e];queue<int> todo;todo.push(v);seen[v]=c;
    while(seen[u]!=c) {
      if(todo.empty())throw runtime_error("SCC return missing");
      int x=todo.front();todo.pop();
      for(int j=0;j<2;j++){int y=g.edge[x][j];if(y>=0&&s.id[y]==c&&seen[y]!=c){seen[y]=c;parent[y]=x;pe[y]=j;todo.push(y);}}
    }
    vector<pair<int,int>> path;int x=u;
    while(x!=v){int p=parent[x];path.push_back({p,pe[x]});x=p;}
    reverse(path.begin(),path.end());path.insert(path.begin(),{u,e});
    int growth=0;for(auto [x,j]:path)growth+=g.flag[x][j];
    os<<"{\"vertices\":"<<s.size[c]<<",\"period\":"<<path.size()<<",\"growth\":"<<growth<<",\"clock\":[";
    for(size_t t=0;t<path.size();t++){if(t)os<<',';os<<g.flag[path[t].first][path[t].second];}
    os<<"],\"bulk\":[";
    for(size_t t=0;t<path.size();t++){if(t)os<<',';arrayJSON(os,bulks[nodes[path[t].first].bulk].q);}
    os<<"],\"phases\":[";
    for(size_t t=0;t<path.size();t++){if(t)os<<',';os<<bulks[nodes[path[t].first].bulk].phase;}
    os<<"],\"outer_pairs\":[";
    for(size_t t=0;t<path.size();t++){if(t)os<<',';arrayJSON(os,digits(nodes[path[t].first].q,k));}
    os<<"]}";
  }
  os<<']';
}
int main(int argc,char**argv) {
  try {
    if(argc==3&&string(argv[1])=="--outer-check") {
      int k=stoi(argv[2]);uint64_t power=1;for(int i=0;i<k;i++)power*=19;
      for(uint64_t q=power/19;q<power;q++)for(int b=0;b<2;b++) {
        auto [next,h]=outer(q,k,b);cout<<q<<' '<<b<<' '<<next<<' '<<h<<'\n';
      }
      return 0;
    }
    int maxk=argc>1?stoi(argv[1]):4;string path=argc>2?argv[2]:"next_period4_results.json";
    auto bulks=makeBulks();Graph bg;
    for(const auto&b:bulks){bg.edge.push_back(b.next);bg.flag.push_back({0,1});}
    auto bs=components(bg);vector<Node> prev;
    for(int u=0;u<(int)bulks.size();u++)if(bs.growth[bs.id[u]])prev.push_back({u,0,bs.id[u]});
    ofstream out(path);out<<"{\"spatial_period\":4,\"bulk_states\":"<<bulks.size()<<",\"recurrent_bulk_states\":"<<prev.size()<<",\"levels\":[";out.flush();
    uint64_t power=1;
    for(int k=1;k<=maxk;k++) {
      auto start=chrono::steady_clock::now();int choices=k==1?18:19;
      size_t n=prev.size()*choices;
      if(n>50000000) {out<<"],\"stopped_before_width\":"<<k<<",\"candidate_states\":"<<n<<",\"complete_through_width\":"<<k-1<<"}\n";out.close();cerr<<"State budget before width "<<k<<": "<<n<<endl;return 0;}
      unordered_map<uint64_t,int> lookup;lookup.reserve(prev.size()*1.4);
      for(int i=0;i<(int)prev.size();i++)lookup.emplace(key(prev[i],power),i);
      vector<Node> nodes;nodes.reserve(n);
      for(const Node& p:prev)for(int d=(k==1?1:0);d<19;d++)nodes.push_back({p.bulk,p.q*19+d,p.component});
      Graph g;g.edge.assign(n,{-1,-1});g.flag.assign(n,{0,0});uint64_t edges=0;
      for(int u=0;u<(int)n;u++) {
        const auto node=nodes[u];int count=0;
        for(int b=0;b<2;b++) {
          auto [target,h]=outer(node.q,k,b);int nb=bulks[node.bulk].next[h];if(nb<0)continue;
          uint64_t oldtarget=target/19;auto it=lookup.find(nb*power+oldtarget);
          if(it==lookup.end()||prev[it->second].component!=node.component)continue;
          int v=it->second*choices+int(target%19)-(k==1?1:0);
          if(count&&g.edge[u][0]==v)continue;
          g.edge[u][count]=v;g.flag[u][count]=h;count++;edges++;
        }
      }
      auto s=components(g);uint64_t retained=0,internal=0;int pos=0;
      for(size_t c=0;c<s.size.size();c++)if(s.growth[c]){pos++;retained+=s.size[c];}
      for(int u=0;u<(int)n;u++)for(int e=0;e<2;e++){int v=g.edge[u][e];if(v>=0&&s.id[u]==s.id[v]&&s.growth[s.id[u]])internal++;}
      double sec=chrono::duration<double>(chrono::steady_clock::now()-start).count();
      if(k>1)out<<',';
      out<<"{\"outer_width\":"<<k<<",\"candidate_states\":"<<n<<",\"edges\":"<<edges<<",\"positive_components\":"<<pos<<",\"retained_states\":"<<retained<<",\"internal_edges\":"<<internal<<",\"seconds\":"<<sec<<",\"cycle_examples\":";
      cyclesJSON(out,nodes,bulks,g,s,k);out<<'}';out.flush();
      cout<<"width="<<k<<" candidates="<<n<<" edges="<<edges<<" positive_components="<<pos<<" recurrent_states="<<retained<<" internal_edges="<<internal<<" seconds="<<sec<<endl;
      // Exact full-exterior graph, restricted only by necessary recurrent
      // conditions. Every expanding closed family must survive this filter.
      Graph fg;fg.edge.assign(n,{-1,-1});fg.flag.assign(n,{0,0});
      uint64_t checked=0,valid=0,shaped=0,unsafe=0;
      for(int u=0;u<(int)n;u++)if(s.growth[s.id[u]]) {
        checked++;auto a=connect(nodes[u],k,bulks,16),b=connect(nodes[u],k,bulks,24);
        if(a.safe!=b.safe||a.shape!=b.shape||a.outer!=b.outer||a.overflow!=b.overflow)
          throw runtime_error("core-length independence check failed");
        if(!a.safe)unsafe++;
        if(a.shape)shaped++;
        if(!a.safe||!a.shape)continue;
        int nb=bulks[nodes[u].bulk].next[a.overflow];
        auto it=lookup.find(nb*power+a.outer/19);
        if(it==lookup.end())continue;
        int v=it->second*choices+int(a.outer%19)-(k==1?1:0);
        if(s.id[u]!=s.id[v])continue;
        bool matched=false;for(int e=0;e<2;e++)if(g.edge[u][e]==v&&g.flag[u][e]==a.overflow)matched=true;
        if(!matched)throw runtime_error("full connector not in necessary graph");
        fg.edge[u][0]=v;fg.flag[u][0]=a.overflow;valid++;
      }
      auto fs=components(fg);int fc=0;uint64_t fv=0;
      for(size_t i=0;i<fs.size.size();i++)if(fs.growth[i]){fc++;fv+=fs.size[i];}
      string cp="next_period4_full_width"+to_string(k)+".json";ofstream co(cp);
      co<<"{\"outer_width\":"<<k<<",\"necessary_recurrent_states\":"<<checked<<",\"shape_preserving_states\":"<<shaped<<",\"unsafe_states\":"<<unsafe<<",\"safe_edges_within_necessary_components\":"<<valid<<",\"positive_components\":"<<fc<<",\"cycle_states\":"<<fv<<",\"cycle_examples\":";
      cyclesJSON(co,nodes,bulks,fg,fs,k);co<<"}\n";
      cout<<"full_width="<<k<<" checked="<<checked<<" shape="<<shaped<<" unsafe="<<unsafe<<" edges="<<valid<<" positive_components="<<fc<<endl;
      prev.clear();prev.reserve(retained);
      for(int u=0;u<(int)n;u++)if(s.growth[s.id[u]])prev.push_back({nodes[u].bulk,nodes[u].q,s.id[u]});
      power*=19;
      if(prev.empty())break;
    }
    out<<"],\"scope\":\"Necessary bulk/exterior conditions, not a finite decimal existence witness.\"}\n";
  } catch(const exception& e){cerr<<e.what()<<endl;return 1;}
}
