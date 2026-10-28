// Mandatory independent full-SCC controls for all-k SIXTH-column transfer proof.
// Compare the exact published base9 and base13 control state/SCC counts.
#include <bits/stdc++.h>
using namespace std;
struct Graph {
 int b,p,k;string g; vector<int> gi, yidx; unsigned long long gs=0;
 using u64=unsigned long long;
 vector<u64> nodes;
 vector<int> depths;
 vector<vector<int>> adj;
 unordered_map<u64,int> id;
 Graph(int b_,string g_):b(b_),p((int)g_.size()),g(g_){k=0;while((1<<k)<b)k++;yidx.resize(p,-1);for(int t=0;t<p;t++)if(g[t]=='1'){gs|=1ULL<<t;yidx[t]=gi.size();gi.push_back(t);}id.reserve(1200000);}
 u64 pack(u64 L,u64 H,const vector<int>&Y){u64 z=L|(H<<p);int s=2*p;for(int y:Y){z|=(u64)y<<s;s+=k;}return z;}
 void unpack(u64 z,u64&L,u64&H,vector<int>&Y){u64 mask=(1ULL<<p)-1;L=z&mask;H=(z>>p)&mask;Y.clear();int s=2*p;for(int i=0;i<(int)gi.size();i++){Y.push_back((z>>s)&((1ULL<<k)-1));s+=k;}}
 void trans(u64 key,bool first,vector<u64>&outputs){
   u64 L,H;vector<int>Y;unpack(key,L,H,Y);
   int x[64]={0},h[64]={0};
   auto dfs=[&](auto&& self,int t,int firstX)->void{
      if(t==p){if(x[p]!=firstX)return;u64 L2=0,H2=0;vector<int>Y2;
        for(int j=0;j<p;j++){L2|=(u64)((x[j]+((L>>j)&1))/b)<<j;H2|=(u64)h[j]<<j;}
        for(int j:gi)Y2.push_back((x[j]+h[j])%b);
        u64 v=pack(L2,H2,Y2);if(find(outputs.begin(),outputs.end(),v)==outputs.end())outputs.push_back(v);
        return;}
      for(int c=0;c<=1;c++){
        if((x[t]+c)/b!=(int)((H>>t)&1))continue;
        h[t]=c;
        x[t+1]=(x[t]+((L>>t)&1))%b + ((g[t]=='1')?Y[yidx[t]]:(x[t]+c)%b);
        self(self,t+1,firstX);
      }
   };
   for(int x0=first?1:0;x0<=2*b-2;x0++){x[0]=x0;dfs(dfs,0,x0);}
 }
 void build(int cap=1400000){vector<int> ys(gi.size(),1);u64 start=pack(0,gs,ys);nodes={start};depths={0};adj={{}};id[start]=0;
   for(size_t i=0;i<nodes.size();i++){
     vector<u64> outs;trans(nodes[i],i==0,outs);
     for(u64 z:outs){auto it=id.find(z);int j;
       if(it==id.end()){j=nodes.size();if(j>=cap)throw runtime_error("CAP");id[z]=j;nodes.push_back(z);depths.push_back(depths[i]+1);adj.emplace_back();}
       else j=it->second;
       adj[i].push_back(j);
     }
   }
 }
 void scc(){int n=nodes.size(),ecount=0;vector<vector<int>> back(n);for(int i=0;i<n;i++)for(int j:adj[i]){back[j].push_back(i);ecount++;}
   vector<char> vis(n,0); vector<int> order;order.reserve(n);
   for(int i=0;i<n;i++){if(vis[i])continue;vector<pair<int,int>> stack={{i,0}};vis[i]=1;
    while(!stack.empty()){int v=stack.back().first;int &q=stack.back().second;
      if(q<(int)adj[v].size()){int j=adj[v][q++];if(!vis[j]){vis[j]=1;stack.push_back({j,0});}}
      else{order.push_back(v);stack.pop_back();}}
   }
   fill(vis.begin(),vis.end(),0);vector<tuple<int,int,int,int>> cdata;
   for(int rr=n-1;rr>=0;rr--){int i=order[rr];if(vis[i])continue;vector<int> stack={i};vis[i]=1;int sz=0, min_depth=1e9, repr=-1;
     while(!stack.empty()){int v=stack.back();stack.pop_back();sz++;if(depths[v]<min_depth){min_depth=depths[v];repr=v;}
       for(int j:back[v])if(!vis[j]){vis[j]=1;stack.push_back(j);} }
     bool self=false;if(sz==1)for(int j:adj[i])if(j==i)self=true;
     if(sz>1||self)cdata.push_back({min_depth,sz,repr,self?1:0});
   }
   sort(cdata.begin(),cdata.end());cout<<"base="<<b<<" g="<<g<<" nodes="<<n<<" edges="<<ecount<<" nontriv_scc="<<cdata.size()<<"\n";
   for(auto [d,s,v,self]:cdata)cout<<"  SCC depth="<<d<<" size="<<s<<" self="<<self<<"\n";
 }
};
int main(){for(auto [b,g]:vector<pair<int,string>>{{9,"1100011000"},{13,"1010010000"},{17,"1100011000"}}){auto x=Graph(b,g);x.build();if(b==9)assert(x.nodes.size()==956310);if(b==13)assert(x.nodes.size()==250302);if(b==17)assert(x.nodes.size()==1);x.scc();}}
