// Independently reconstructed exact lattice position automaton, controls only.
#include <bits/stdc++.h>
using namespace std; using u64=uint64_t;
int b,p,G,ydig,N;vector<int> g,idx;
u64 dp[65][63];int valid[2][63],bv[2][63],car[2][63],part[63][2];
static inline u64 pack(int L,int H,const int*Y){u64 k=(u64)L|((u64)H<<p);int sh=2*p;for(int i=0;i<G;i++){k|=(u64)Y[i]<<sh;sh+=ydig;}return k;}
static inline void unpack(u64 k,int &L,int&H,int*Y){L=k&((1u<<p)-1);H=(k>>p)&((1u<<p)-1);int sh=2*p;for(int i=0;i<G;i++){Y[i]=(k>>sh)&((1<<ydig)-1);sh+=ydig;}}
void setup(string s,int base){b=base;p=s.size();g.assign(p,0);idx.clear();for(int t=0;t<p;t++)if(s[t]=='1'){g[t]=1;idx.push_back(t);}G=idx.size();ydig=1;while((1<<ydig)<b)ydig++;N=2*b-1;
 for(int h=0;h<2;h++)for(int x=0;x<N;x++){valid[h][x]=0;for(int c=0;c<2;c++)if((x+c>=b)==(h!=0))valid[h][x]|=1<<c;bv[h][x]=(x+h)%b;car[h][x]=x+h>=b;}
 for(int x=0;x<N;x++)for(int c=0;c<2;c++)part[x][c]=(x+c)%b;
}
template<class F>void edges(u64 key,bool first,F emit){
 int L,H,Y[64],Lt[64],Ht[64],Yt[64],gi[64];unpack(key,L,H,Y);
 int ii=0;for(int t=0;t<p;t++){Lt[t]=(L>>t)&1;Ht[t]=(H>>t)&1;gi[t]=g[t]?ii++:-1;Yt[t]=g[t]?Y[gi[t]]:0;}
 for(int x=0;x<N;x++)dp[p][x]=1ULL<<x;
 for(int t=p-1;t>=0;t--)for(int x=0;x<N;x++){
  if(first&&x==0){dp[t][x]=0;continue;}
  int vc=valid[Ht[t]][x];if(!vc){dp[t][x]=0;continue;}
  int base=bv[Lt[t]][x];u64 z=0;
  if(g[t])z=dp[t+1][base+Yt[t]];
  else{if(vc&1)z|=dp[t+1][base+part[x][0]];if(vc&2)z|=dp[t+1][base+part[x][1]];}
  dp[t][x]=z;
 }
 int xs[65],cs[64],choice[65];
 for(int x0=first?1:0;x0<N;x0++){
  if(!(dp[0][x0]&(1ULL<<x0)))continue;
  int t=0;xs[0]=x0;choice[0]=0;
  while(t>=0){
   if(t==p){int L2=0,H2=0,Y2[64];for(int j=0;j<p;j++){L2|=car[Lt[j]][xs[j]]<<j;H2|=cs[j]<<j;if(g[j])Y2[gi[j]]=part[xs[j]][cs[j]];}
    emit(pack(L2,H2,Y2));t--;continue;}
   int vc=valid[Ht[t]][xs[t]],ok=0;
   while(choice[t]<2){int c=choice[t]++;
    if(!((vc>>c)&1))continue;
    int base=bv[Lt[t]][xs[t]],nx=base+(g[t]?Yt[t]:part[xs[t]][c]);
    if(!(dp[t+1][nx]&(1ULL<<x0)))continue;
    cs[t]=c;xs[t+1]=nx;t++;choice[t]=0;ok=1;break;
   }
   if(!ok)t--;
  }
 }
}
struct Node{u64 key;int par;};
int main(int argc,char**argv){if(argc!=3){fprintf(stderr,"usage: controls BASE OVERFLOW\n");return 2;}string s=argv[2];setup(s,atoi(argv[1]));
 int Y0[64];for(int i=0;i<G;i++)Y0[i]=1;int H=0;for(int t=0;t<p;t++)H|=g[t]<<t;u64 start=pack(0,H,Y0);
 vector<Node>nodes{{start,-1}};vector<vector<int>>adj(1);unordered_map<u64,int>id;id[start]=0;
 for(int i=0;i<(int)nodes.size();i++){
  vector<int> out;edges(nodes[i].key,i==0,[&](u64 k){
   auto it=id.find(k);int j;
   if(it==id.end()){j=nodes.size();id[k]=j;nodes.push_back({k,i});adj.emplace_back();}
   else j=it->second;
   if(find(out.begin(),out.end(),j)==out.end())out.push_back(j);
  });adj[i].swap(out);
 }
 int n=nodes.size(),e=0;for(auto&v:adj)e+=v.size();
 vector<int>ord(n,-1),low(n,-1),comp(n,-1),stk;vector<char>on(n,0);int timer=0,nc=0;vector<vector<int>>groups;
 for(int r=0;r<n;r++)if(ord[r]<0){vector<pair<int,int>>dfs{{r,0}};ord[r]=low[r]=timer++;stk.push_back(r);on[r]=1;
  while(!dfs.empty()){
   int v=dfs.back().first,&i=dfs.back().second;
   if(i<(int)adj[v].size()){
    int w=adj[v][i++];if(ord[w]<0){ord[w]=low[w]=timer++;stk.push_back(w);on[w]=1;dfs.push_back({w,0});}
    else if(on[w])low[v]=min(low[v],ord[w]);
   }else{
    if(low[v]==ord[v]){vector<int>grp;for(;;){int w=stk.back();stk.pop_back();on[w]=0;comp[w]=nc;grp.push_back(w);if(w==v)break;}groups.push_back(move(grp));nc++;}
    dfs.pop_back();if(!dfs.empty())low[dfs.back().first]=min(low[dfs.back().first],low[v]);
   }
  }
 }
 int non=0;vector<pair<int,int>>depthsizes;vector<int>depth(n);for(int i=1;i<n;i++)depth[i]=depth[nodes[i].par]+1;
 for(auto&c:groups){bool self=false;if(c.size()==1)for(int x:adj[c[0]])if(x==c[0])self=true;
  if(c.size()==1&&!self)continue;non++;
  int minimum=n;for(int x:c)minimum=min(minimum,depth[x]);
  depthsizes.push_back({minimum,(int)c.size()});
 }
 sort(depthsizes.begin(),depthsizes.end());printf("b=%d g=%s states=%d edges=%d nontrivial_sccs=%d\n",b,s.c_str(),n,e,non);
 for(auto [d,sz]:depthsizes)printf("SCC min_depth=%d size=%d\n",d,sz);
}
