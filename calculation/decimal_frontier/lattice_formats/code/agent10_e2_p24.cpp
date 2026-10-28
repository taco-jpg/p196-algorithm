// Agent 10 E2: exact finite-state position automaton and backward uniform-lattice cone.
// Controls: engine 9 1100011000 1200000 ; engine 13 1010010000 400000.
// Exclusion: engine 10 000100010001000100010001 2400000 backraw
//            engine 10 000100010001000100010001 300000 back
// All caps are state counts; only EXHAUSTED proves absence of the target.
#include <bits/stdc++.h>
using namespace std;
using u64=uint64_t;using u128=unsigned __int128;
struct Hash {size_t operator()(u128 x)const {u64 a=(u64)x,b=(u64)(x>>64); a^=b+0x9e3779b97f4a7c15ULL+(a<<6)+(a>>2);a^=a>>30;a*=0xbf58476d1ce4e5b9ULL;a^=a>>27;a*=0x94d049bb133111ebULL;return a^(a>>31);}};
int b,p,ng,ydig;vector<int> g,gi,yt;
inline int bit(u64 a,int t){return (a>>t)&1;}
inline u128 key(u64 L,u64 H,const int *Y){u128 k=(u128)L|((u128)H<<p);int sh=2*p;for(int i=0;i<ng;i++){k|=(u128)Y[i]<<sh;sh+=ydig;}return k;}
inline void unkey(u128 k,u64 &L,u64&H,int *Y){u64 m=((1ULL<<p)-1);L=(u64)k&m;H=(u64)(k>>p)&m;int sh=2*p;for(int i=0;i<ng;i++){Y[i]=(int)((k>>sh)&((1<<ydig)-1));sh+=ydig;}}
// Enumerate all exact time-periodic columns of the position automaton.
template<class F>void succ(u128 src,bool first,F emit){u64 L,H;int Y[64],xs[64],C[64];unkey(src,L,H,Y);
 auto go=[&](auto&&self,int t,int x,int x0)->void{
  if(t==p){if(x==x0){u64 l=0,h=0;int y[64];for(int s=0;s<p;s++){l|=(u64)((xs[s]+bit(L,s))/b)<<s;h|=(u64)C[s]<<s;}for(int j=0;j<ng;j++){int s=gi[j];y[j]=(xs[s]+C[s])%b;}emit(key(l,h,y));}return;}
  if(x<0||x>2*b-2 || (first&&x==0))return;
  xs[t]=x;for(int c=0;c<=1;c++){if((x+c)/b!=bit(H,t))continue;C[t]=c;int nx=(x+bit(L,t))%b+(g[t]?Y[yt[t]]:(x+c)%b);self(self,t+1,nx,x0);}
 };
 for(int x0=first?1:0;x0<=2*b-2;x0++)go(go,0,x0,x0);
}
// Exact backward predecessor enumeration; target is a post-column cut state.
template<class F>void preds(u128 target,F emit){u64 L2,H2;int Y2[64],xs[64],Ls[64],Ys[64];unkey(target,L2,H2,Y2);
 auto fin=[&](){u64 L=0,H=0;int Y[64];for(int t=0;t<p;t++){L|=(u64)Ls[t]<<t;H|=(u64)((xs[t]+bit(H2,t))/b)<<t;}for(int j=0;j<ng;j++)Y[j]=Ys[gi[j]];emit(key(L,H,Y));};
 auto go=[&](auto&&self,int t,int x,int x0)->void{
   if(x<0||x>2*b-2)return; xs[t]=x;int c=bit(H2,t),l2=bit(L2,t);
   for(int l=0;l<2;l++){
    if((x+l)/b!=l2)continue;
    if(g[t]&&(x+c)%b!=Y2[yt[t]])continue;
    Ls[t]=l;int dig=(x+l)%b;
    if(!g[t]){Ys[t]=-1;int nx=dig+(x+c)%b;
      if(t+1==p){if(nx==x0)fin();}else self(self,t+1,nx,x0);
    }else for(int y=0;y<b;y++){Ys[t]=y;int nx=dig+y;
      if(t+1==p){if(nx==x0)fin();}else self(self,t+1,nx,x0);
    }
   }
 };
 for(int x0=0;x0<=2*b-2;x0++)go(go,0,x0,x0);
}
// Quotient by 4-position cyclic time shifts for g=(0001)^6.
static bool quotient=false;
inline u128 canon(u128 k){if(!quotient)return k;u64 L,H;int Y[64];unkey(k,L,H,Y);u128 best=k;
 for(int z=1;z<6;z++){int shift=4*z;u64 mask=(1ULL<<p)-1;u64 lr=((L>>shift)|(L<<(p-shift)))&mask;u64 hr=((H>>shift)|(H<<(p-shift)))&mask;int y[64];for(int j=0;j<ng;j++)y[j]=Y[(j+z)%ng];u128 q=key(lr,hr,y);if(q<best)best=q;}
 return best;
}
void backward_run(size_t cap){
 vector<int> nxt(2*b-1,-1);for(int v=0;v<=2*b-2;v++)if(v!=b-1){int c=v>=b;nxt[v]=2*((v+c)%b);}
 vector<vector<int>> loops;vector<int>mark(2*b-1);
 for(int a=0;a<=2*b-2;a++)if(a!=b-1&&!mark[a]){vector<int>seq;int v=a;while(v>=0&&v<=2*b-2&&v!=b-1&&!mark[v]){mark[v]=1;seq.push_back(v);v=nxt[v];}if(v>=0&&v<=2*b-2&&mark[v]==1){vector<int>lp{v};for(int q=nxt[v];q!=v;q=nxt[q])lp.push_back(q);loops.push_back(lp);}for(int t:seq)mark[t]=2;}
 u64 Hg=0;int Y0[64];for(int t=0;t<p;t++)if(g[t])Hg|=(1ULL<<t);for(int i=0;i<ng;i++)Y0[i]=1;u128 start=key(0,Hg,Y0);unordered_set<u128,Hash> startNext;succ(start,true,[&](u128 k){startNext.insert(canon(k));});
 cerr<<"start immediate successors "<<startNext.size()<<" loops "<<loops.size()<<"\n";
 unordered_set<u128,Hash> seen;seen.reserve(cap*2);
 vector<u128> frontier, next;
 for(auto &lp:loops)if(p%lp.size()==0)for(size_t ph=0;ph<lp.size();ph++){
 u64 L=0,H=0;int Y[64];for(int t=0;t<p;t++){int u=lp[(t+ph)%lp.size()];if(u>=b){L|=1ULL<<t;H|=1ULL<<t;}}
 for(int j=0;j<ng;j++){int t=gi[j];int u=lp[(t+ph)%lp.size()];Y[j]=(u+(u>=b))%b;}
 u128 raw=key(L,H,Y);bool self=false;succ(raw,false,[&](u128 w){if(w==raw)self=true;});if(!self){cerr<<"BUG: uniform target is not a self-loop\n";exit(5);}u128 k=canon(raw);if(seen.insert(k).second)frontier.push_back(k);
 }
 cerr<<"target seeds="<<frontier.size()<<"\n";
 int depth=0;bool hit=false,capped=false;
 for(;!frontier.empty()&&!capped&&!hit;depth++){
 next.clear();for(u128 v:frontier){preds(v,[&](u128 k){if(capped||hit)return;static uint64_t samples=0; ++samples;if(!quotient && samples%10000==0){bool edge=false;succ(k,false,[&](u128 q){if(q==v)edge=true;});if(!edge){cerr<<"BUG reverse nonedge\n";exit(6);}}k=canon(k);if(startNext.count(k)){hit=true;return;}if(seen.count(k))return;if(seen.size()>=cap){capped=true;return;}seen.insert(k);next.push_back(k);});if(hit||capped)break;}
 cerr<<"back_depth="<<depth+1<<" total="<<seen.size()<<" next_frontier="<<next.size()<<" hit="<<hit<<" capped="<<capped<<"\n";
 frontier.swap(next);
 }
 cout<<"BACKWARD result="<<(hit?"CANDIDATE_REACHABLE_UNREPLAYED":(capped?"UNDECIDED_CAP":"EXHAUSTED"))<<" depth="<<depth<<" visited="<<seen.size()<<"\n";
}
struct Graph {vector<u128> ks;vector<uint32_t> edgeSource,edgeTarget;vector<int> depth;unordered_map<u128,uint32_t,Hash> ids;bool capped=false;uint32_t cap;Graph(uint32_t c):cap(c){ks.reserve(c);depth.reserve(c);ids.reserve(c*2);}
 uint32_t add(u128 k,int dep){auto it=ids.find(k);if(it!=ids.end())return it->second;if(ks.size()>=cap){capped=true;return UINT32_MAX;}uint32_t id=ks.size();ids[k]=id;ks.push_back(k);depth.push_back(dep);return id;}
 void bfs(u128 start){add(start,0);for(uint32_t i=0;i<ks.size()&&!capped;i++){succ(ks[i],i==0,[&](u128 v){uint32_t j=add(v,depth[i]+1);if(j!=UINT32_MAX){edgeSource.push_back(i);edgeTarget.push_back(j);}});if((i+1)%500000==0){cerr<<"N="<<ks.size()<<" expanded="<<i+1<<" edges="<<edgeTarget.size()<<"\n";}}}
};
void cycles(Graph& gph){size_t N=gph.ks.size();vector<vector<uint32_t>> adj(N),rev(N);for(size_t j=0;j<gph.edgeTarget.size();j++){auto u=gph.edgeSource[j],v=gph.edgeTarget[j];adj[u].push_back(v);rev[v].push_back(u);}vector<uint8_t> visited(N);vector<uint32_t> order;order.reserve(N);for(uint32_t i=0;i<N;i++)if(!visited[i]){vector<pair<uint32_t,size_t>> st;st.emplace_back(i,0);visited[i]=1;while(!st.empty()){auto &pr=st.back();auto v=pr.first;if(pr.second==adj[v].size()){order.push_back(v);st.pop_back();continue;}auto to=adj[v][pr.second++];if(!visited[to]){visited[to]=1;st.emplace_back(to,0);}}}
 fill(visited.begin(),visited.end(),0);int scc=0,loops=0,nontriv=0;for(auto it=order.rbegin();it!=order.rend();++it){uint32_t i=*it;if(visited[i])continue;vector<uint32_t> stk{i};visited[i]=1;vector<uint32_t> members;while(!stk.empty()){auto v=stk.back();stk.pop_back();members.push_back(v);for(auto to:rev[v])if(!visited[to]){visited[to]=1;stk.push_back(to);}}
 bool self=false;if(members.size()==1)for(auto to:adj[members[0]])if(to==members[0])self=true;
 if(members.size()>1||self){nontriv++;int mindep=INT_MAX,maxdep=0;for(auto k:members){mindep=min(mindep,gph.depth[k]);maxdep=max(maxdep,gph.depth[k]);}if(self)loops++;if(nontriv<=20)cout<<"SCC size="<<members.size()<<" self="<<self<<" min_depth="<<mindep<<" max_depth="<<maxdep<<"\n";}
 scc++;}
 cout<<"GRAPH states="<<N<<" edges="<<gph.edgeTarget.size()<<" scc="<<scc<<" cyclic_scc="<<nontriv<<" loops="<<loops<<" capped="<<gph.capped<<"\n";
}
int main(int ac,char**av){if(ac<4){cerr<<"usage: engine BASE STREAM CAP [back|backraw]\n";return 2;}b=atoi(av[1]);string s=av[2];p=s.size();uint32_t cap=atol(av[3]);if(p>=63){cerr<<"key capacity exceeded\n";return 2;}ydig=1;while((1<<ydig)<b)ydig++;ng=0;yt.assign(p,-1);for(int i=0;i<p;i++){int c=s[i]-'0';g.push_back(c);if(c){yt[i]=ng++;gi.push_back(i);}}if(2*p+ydig*ng>128){cerr<<"key capacity exceeded\n";return 2;}
 u64 H=0;int Y[64];for(int i=0;i<p;i++)if(g[i])H|=1ULL<<i;for(int i=0;i<ng;i++)Y[i]=1;
 if(ac>4&&(string(av[4])=="back"||string(av[4])=="backraw")){quotient=(string(av[4])=="back" && p==24 && s=="000100010001000100010001");backward_run(cap);return 0;}auto start=key(0,H,Y);Graph graph(cap);graph.bfs(start);cycles(graph);
}
