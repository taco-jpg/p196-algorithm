#include <bits/stdc++.h>
using namespace std;
using u64=uint64_t;
struct State {int L,H; int Y; bool operator==(const State&o)const{return L==o.L&&H==o.H&&Y==o.Y;}};
struct Hash{size_t operator()(State const&s)const{return (size_t)s.L*16807u+(size_t)s.H*8191u+(size_t)s.Y*1315423911u;}};
constexpr int p=8; const int g[p]={1,0,1,0,1,0,1,0};
struct Edge{int to;array<uint8_t,p> x;};
struct Node{State q;int par,dep;vector<Edge> edges;};
int main(int argc,char**argv){int cap=argc>1?atoi(argv[1]):500000;
 vector<Node> v; unordered_map<State,int,Hash> id;
 State root{0,0b01010101,0x1111}; v.push_back({root,-1,0,{}});id[root]=0;
 size_t edges=0,maxdepth=0; bool capped=false;
 for(size_t i=0;i<v.size()&&!capped;i++){
  const State q=v[i].q; int y[p]; int shift=0;for(int t=0;t<p;t++)if(g[t])y[t]=(q.Y>>(4*shift++))&15;
  function<void(int,int,int,array<uint8_t,p>&,int,int)> dfs;
  dfs=[&](int t,int x,int x0,array<uint8_t,p>&xrow,int LL,int HH){
   if(t==p){if(x!=x0)return;int yy=0,cnt=0;
      for(int tt=0;tt<p;tt++)if(g[tt]){int digit=(int)xrow[tt]+((HH>>tt)&1);digit%=10;yy|=digit<<(cnt++*4);}
      State s{LL,HH,yy};auto found=id.find(s);int j;
      if(found==id.end()){if((int)v.size()>=cap){capped=true;return;}j=v.size();id[s]=j;v.push_back({s,(int)i,v[i].dep+1,{}});maxdepth=max(maxdepth,(size_t)v.back().dep);}else j=found->second;
      for(auto&e:v[i].edges)if(e.to==j)return;
      v[i].edges.push_back({j,xrow});edges++;return;
   }
   for(int h=0;h<2;h++){
      if((x+h)/10!=((q.H>>t)&1))continue;
      int nx=(x+((q.L>>t)&1))%10+(g[t]?y[t]:(x+h)%10);
      xrow[t]=x;int l2=LL|(((x+((q.L>>t)&1))/10)<<t);
      dfs(t+1,nx,x0,xrow,l2,HH|(h<<t));
   }
  };
  for(int x0=i==0?1:0;x0<=18;x0++){array<uint8_t,p>a{};dfs(0,x0,x0,a,0,0);if(capped)break;}
 }
 cerr<<"STATES "<<v.size()<<" EDGES "<<edges<<" CAPPED "<<capped<<" MAXDEP "<<maxdepth<<"\n";
 if(capped)return 2;
 int N=v.size();vector<int> ind(N,-1),low(N),stack,comp(N,-1),vis(N);int tick=0,ncomp=0;vector<vector<int>>comps;
 function<void(int)> visit=[&](int a){ind[a]=low[a]=tick++;stack.push_back(a);vis[a]=1;
  for(auto&e:v[a].edges){int b=e.to;if(ind[b]<0){visit(b);low[a]=min(low[a],low[b]);}else if(vis[b])low[a]=min(low[a],ind[b]);}
  if(low[a]==ind[a]){vector<int> mem;int b;do{b=stack.back();stack.pop_back();vis[b]=0;comp[b]=ncomp;mem.push_back(b);}while(b!=a);comps.push_back(mem);ncomp++;}
 };
 for(int a=0;a<N;a++)if(ind[a]<0)visit(a);
 int nontriv=0;for(auto&c:comps){bool self=false;if(c.size()==1)for(auto&e:v[c[0]].edges)if(e.to==c[0])self=true;if(c.size()==1&&!self)continue;
 nontriv++;int internal=0,branch=0;for(auto a:c){int d=0;for(auto&e:v[a].edges)if(comp[e.to]==comp[a])d++;internal+=d;if(d>1)branch++;}
 int rootid=*min_element(c.begin(),c.end());
 cout<<"SCC size="<<c.size()<<" edges="<<internal<<" branch_nodes="<<branch<<" min_depth="<<v[rootid].dep<<" root_id="<<rootid<<"\n";
 if(branch>0){
    int q=-1;for(int a:c){int d=0;for(auto&e:v[a].edges)if(comp[e.to]==comp[a])d++;if(d>=2&&(q<0||v[a].dep<v[q].dep))q=a;}
    if(c.size()>1000){for(auto a:c)if(v[a].q.L==89 && v[a].q.H==145 && v[a].q.Y==20576)q=a;}
   cout<<"BRANCH q="<<q<<" depth="<<v[q].dep<<" L="<<v[q].q.L<<" H="<<v[q].q.H<<" Y="<<v[q].q.Y<<"\n";
    auto emit=[&](string label,vector<Edge> path){cout<<label<<" n="<<path.size()<<" ";for(auto&e:path){for(auto x:e.x)cout<<"0123456789ABCDEFGHI"[(int)x];cout<<" ";}cout<<"\n";};
    vector<Edge> path;int cur=q;while(v[cur].par>=0){int from=v[cur].par;for(auto&e:v[from].edges)if(e.to==cur){path.push_back(e);break;}cur=from;}reverse(path.begin(),path.end());emit("ROOTPATH",path);
    // Two exact-length return walks sharing the last six exterior columns.
    const int suffix=6;
    int target=q;
    for(int z=0;z<suffix;z++)target=v[target].par;
    auto build=[&](int total)->vector<Edge>{
      const int steps=total-suffix;
      vector<unordered_map<int,pair<int,int>>> pred(steps+1);
      pred[0][q]={-1,-1};
      for(int t=0;t<steps;t++){
        for(auto &kv:pred[t]){int a=kv.first;
          for(int j=0;j<(int)v[a].edges.size();j++){
            int b=v[a].edges[j].to;
            if(comp[b]!=comp[q])continue;
            if(!pred[t+1].count(b))pred[t+1][b]={a,j};
          }
        }
      }
      if(!pred[steps].count(target))throw runtime_error("cannot reach suffix at exact length "+to_string(total));
      vector<Edge>result;int cur=target;
      for(int t=steps;t>0;t--){auto [a,j]=pred[t][cur];result.push_back(v[a].edges[j]);cur=a;}
      reverse(result.begin(),result.end());
      vector<Edge>suffixPath;cur=q;
      while(cur!=target){int a=v[cur].par;bool found=false;for(auto &e:v[a].edges)if(e.to==cur){suffixPath.push_back(e);found=true;break;}if(!found)throw runtime_error("suffix edge missing");cur=a;}
      reverse(suffixPath.begin(),suffixPath.end());
      result.insert(result.end(),suffixPath.begin(),suffixPath.end());
      return result;
    };
    emit("LOOPA",build(92));emit("LOOPB",build(97));

 }
 }
 cout<<"TOTAL NONTRIVIAL "<<nontriv<<"\n";
}
