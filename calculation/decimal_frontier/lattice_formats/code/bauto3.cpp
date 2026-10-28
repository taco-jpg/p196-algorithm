// Exact position-automaton for B-cycles of the autonomous B-system (all lengths n at once).
// Method: scan B positions k=0,1,2,..; cut state (L,H,Y):
//   L[t] carry into position k from below at time t (determined), H[t] carry position k must pass down to k-1 (required),
//   Y[t] partner digit (x_t[k-1]+h_{t,k-1}) mod b for the times with gam_t=1 (gam shifts the mirror partner by one position).
// A position = choice of x_0[k] and guesses Hn[t]; the p-step trajectory x_{t+1} = (x_t+L_t)%b + (g_t ? Y_t : (x_t+Hn_t)%b)
// must close (x_p = x_0) and satisfy floor((x_t+Hn_t)/b)=H_t.   Accept: L[t]+H[t]=1 and Y_t=(b-1)*L_t (neutral band above).
// usage: bauto b pmin pmax [-w] [-part i n] [-g string]      (g = gam pattern, all necklaces of each length if omitted)
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <vector>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <algorithm>
#include <chrono>
using namespace std;
typedef uint64_t u64; typedef unsigned __int128 K128;
struct KH{size_t operator()(const K128&k)const{u64 a=(u64)k,c=(u64)(k>>64);return (size_t)((a*0x9E3779B97F4A7C15ULL)^(c*0xC2B2AE3D27D4EB4FULL)^(a>>29));}};
int b,p; vector<int> g; vector<int> Gidx; // times with g=1
int ydig; // bits per Y digit
vector<int> Kb; // band coefficient schedule (period q); empty => neutral mode
vector<int> cst, dst; // per time: steady carry and steady digit
static inline K128 pack(u64 L,u64 H,const int*Y,int ng){K128 k=(K128)L|((K128)H<<p);int sh=2*p;for(int i=0;i<ng;i++){k|=((K128)Y[i])<<sh;sh+=ydig;}return k;}
static inline void unpack(K128 k,u64&L,u64&H,int*Y,int ng){L=(u64)k&((1ULL<<p)-1);H=(u64)(k>>p)&((1ULL<<p)-1);int sh=2*p;for(int i=0;i<ng;i++){Y[i]=(int)((k>>sh)&(((K128)1<<ydig)-1));sh+=ydig;}}
struct Res{bool any=false;vector<pair<u64,int>> acc;};
// enumerate transitions of one position
template<class F> void transitions(u64 L,u64 H,const int*Y,int ng,bool first,F emit){
  int yi[64];{int c=0;for(int t=0;t<p;t++)yi[t]=g[t]?c++:-1;}
  for(int x0=(first?1:0);x0<=2*b-2;x0++){
    // DFS over t choosing Hn_t
    int xs[64];int hn[64];
    // iterative recursion with explicit stack
    struct Fr{int t;int x;int ch;};
    vector<Fr> st;st.push_back({0,x0,0});xs[0]=x0;
    while(!st.empty()){
      Fr&f=st.back();
      if(f.t==p){
        if(f.x==x0){ // closed
          u64 L2=0,H2=0;int Y2[64];
          for(int t=0;t<p;t++){L2|=(u64)((xs[t]+((L>>t)&1))/b)<<t;H2|=(u64)hn[t]<<t;}
          for(int i=0;i<ng;i++){int t=Gidx[i];Y2[i]=(xs[t]+hn[t])%b;}
          emit(L2,H2,Y2,xs,hn);
        }
        st.pop_back();continue;
      }
      if(f.ch>=2){st.pop_back();continue;}
      int c=f.ch++;int t=f.t,x=f.x;
      if(first&&x==0){continue;}
      if((x+c)/b!=(int)((H>>t)&1))continue;
      int nx=(x+(int)((L>>t)&1))%b + (g[t]?Y[yi[t]]:(x+c)%b);
      xs[t]=x;hn[t]=c;
      if(t+1<p){xs[t+1]=nx;st.push_back({t+1,nx,0});}
      else{ if(nx==x0){ // close
          u64 L2=0,H2=0;int Y2[64];
          for(int tt=0;tt<p;tt++){L2|=(u64)((xs[tt]+((L>>tt)&1))/b)<<tt;H2|=(u64)hn[tt]<<tt;}
          for(int i=0;i<ng;i++){int tt=Gidx[i];Y2[i]=(xs[tt]+hn[tt])%b;}
          emit(L2,H2,Y2,xs,hn);} }
    }
  }
}
bool accepting(u64 L,u64 H,const int*Y,int ng){
  if(Kb.empty()){
    for(int t=0;t<p;t++){int l=(L>>t)&1,h=(H>>t)&1;if(l+h!=1)return false;}
    for(int i=0;i<ng;i++){int l=(L>>Gidx[i])&1;if(Y[i]!=(b-1)*l)return false;}
    return true;
  }
  for(int t=0;t<p;t++){int l=(L>>t)&1,h=(H>>t)&1;if(l!=cst[t]||h!=cst[t])return false;}
  for(int i=0;i<ng;i++){if(Y[i]!=dst[Gidx[i]])return false;}
  return true;
}

struct Node{K128 key;int parent;};
int main(int argc,char**argv){
  b=atoi(argv[1]);int pmin=atoi(argv[2]),pmax=atoi(argv[3]);int part=0,nparts=1;string gfix;bool verb=false;unsigned long long CAPS=3000000ULL;int maxscc=6;string dumpfn;
  for(int i=4;i<argc;i++){string a=argv[i];if(a=="-part"){part=atoi(argv[++i]);nparts=atoi(argv[++i]);}else if(a=="-g"){gfix=argv[++i];}else if(a=="-v")verb=true;else if(a=="-cap")CAPS=strtoull(argv[++i],0,10);else if(a=="-maxscc")maxscc=atoi(argv[++i]);else if(a=="-dump")dumpfn=argv[++i];}
  ydig=1;while((1<<ydig)<b)ydig++;
  long idx=0;
  for(p=pmin;p<=pmax;p++){
    for(u64 gm=0;gm<(1ULL<<p);gm++){
      if(!gfix.empty()){ if((int)gfix.size()!=p)continue; u64 v=0;for(int t=0;t<p;t++)if(gfix[t]=='1')v|=1ULL<<t; if(v!=gm)continue; }
      else{ bool ok=true;for(int r=1;r<p&&ok;r++){u64 rot=((gm>>r)|(gm<<(p-r)))&((1ULL<<p)-1);if(rot<gm)ok=false;} if(!ok)continue; }
      if((idx++)%nparts!=part)continue;
      g.assign(p,0);Gidx.clear();for(int t=0;t<p;t++){g[t]=(gm>>t)&1;if(g[t])Gidx.push_back(t);}
      int ng=Gidx.size(); if(2*p+ydig*ng>127){fprintf(stderr,"key too long\n");continue;}
      string gs;for(int t=0;t<p;t++)gs+=char('0'+g[t]);
      int Y0[64];for(int i=0;i<ng;i++)Y0[i]=1;
      u64 Hs=0;for(int t=0;t<p;t++)Hs|=(u64)g[t]<<t;
      K128 start=pack(0,Hs,Y0,ng);
      unordered_map<K128,int,KH> id; vector<Node> nodes; vector<vector<int>> adj;
      id[start]=0;nodes.push_back({start,-1});adj.emplace_back();
      bool capped=false;
      for(size_t i=0;i<nodes.size();i++){
        u64 L,H;int Y[64];unpack(nodes[i].key,L,H,Y,ng);
        vector<int> out;
        transitions(L,H,Y,ng,i==0,[&](u64 L2,u64 H2,int*Y2,int*xs,int*hn){
          K128 k=pack(L2,H2,Y2,ng);
          auto it=id.find(k);int j;
          if(it==id.end()){ if(nodes.size()>=CAPS){capped=true;return;} j=nodes.size();id[k]=j;nodes.push_back({k,(int)i});adj.emplace_back(); }
          else j=it->second;
          for(int q:out)if(q==j)return;
          out.push_back(j);
        });
        adj[i]=out;
        if(capped)break;
      }
      size_t N=nodes.size();size_t E=0;for(auto&a:adj)E+=a.size();
      if(capped){fprintf(stderr,"CAPPED g=%s states=%zu\n",gs.c_str(),N);printf("CAPPED p=%d g=%s states=%zu\n",p,gs.c_str(),N);fflush(stdout);continue;}
      // Tarjan (iterative)
      vector<int> low(N,-1),num(N,-1),comp(N,-1);vector<char> on(N,0);vector<int> stk;int cnt=0,nc=0;
      vector<vector<int>> comps;
      for(size_t r=0;r<N;r++){ if(num[r]!=-1)continue;
        vector<pair<int,int>> cs;cs.push_back({(int)r,0});num[r]=low[r]=cnt++;stk.push_back(r);on[r]=1;
        while(!cs.empty()){
          int v=cs.back().first;int &ei=cs.back().second;
          if(ei<(int)adj[v].size()){int w=adj[v][ei++];
            if(num[w]==-1){num[w]=low[w]=cnt++;stk.push_back(w);on[w]=1;cs.push_back({w,0});}
            else if(on[w])low[v]=min(low[v],num[w]);
          } else {
            if(low[v]==num[v]){vector<int> c;while(true){int w=stk.back();stk.pop_back();on[w]=0;comp[w]=nc;c.push_back(w);if(w==v)break;}nc++;comps.push_back(c);}
            cs.pop_back();if(!cs.empty()){int u=cs.back().first;low[u]=min(low[u],low[v]);}
          }
        }
      }
      int nontriv=0;
      for(auto&c:comps){bool self=false;if(c.size()==1){for(int w:adj[c[0]])if(w==c[0])self=true;} if(c.size()>1||self)nontriv++;}
      {vector<int> lev(N,0);int ml=0;for(size_t i=1;i<N;i++){lev[i]=lev[nodes[i].parent]+1;if(lev[i]>ml)ml=lev[i];}
      printf("G p=%d g=%s states=%zu edges=%zu nontrivial_sccs=%d maxlev=%d\n",p,gs.c_str(),N,E,nontriv,ml);
      if(getenv("LEVPROF")){vector<long> cnt(ml+1,0);for(size_t i=0;i<N;i++)cnt[lev[i]]++;printf("levprof");for(int l=0;l<=ml;l++)printf(" %ld",cnt[l]);printf("\n");}}
      int shown=0;
      for(auto&c:comps){bool self=false;if(c.size()==1){for(int w:adj[c[0]])if(w==c[0])self=true;} if(!(c.size()>1||self))continue;
        if(shown>=maxscc)break; shown++;
        // shortest cycle through the min-depth member: BFS from member back to itself inside comp
        int r=c[0];for(int w:c)if(w<r)r=w; // smallest id = shallowest
        // BFS inside comp
        vector<int> pr(N,-2);vector<int> q;q.push_back(r);pr[r]=-1;int tgt=-1;
        for(size_t qi=0;qi<q.size()&&tgt<0;qi++){int v=q[qi];for(int w:adj[v]){if(comp[w]!=comp[r])continue;if(w==r){tgt=v;break;}if(pr[w]==-2){pr[w]=v;q.push_back(w);}}}
        vector<int> cyc;{int v=tgt;while(v!=-1){cyc.push_back(v);v=pr[v];}reverse(cyc.begin(),cyc.end());} // r ... tgt, then back to r
        // path from start to r
        vector<int> path;{int v=r;while(v!=-1){path.push_back(v);v=nodes[v].parent;}reverse(path.begin(),path.end());}
        auto cols=[&](const vector<int>&seq,bool closeBack,int firstFlagIdx){
          string out;
          for(size_t i=0;i+ (closeBack?0:1) <seq.size();i++){
            int a=seq[i];int bb=(i+1<seq.size())?seq[i+1]:seq[0];
            u64 L,H;int Y[64];unpack(nodes[a].key,L,H,Y,ng);
            vector<int> xs_found;bool got=false;
            transitions(L,H,Y,ng,a==0,[&](u64 L2,u64 H2,int*Y2,int*xs,int*hn){ if(got)return; K128 k=pack(L2,H2,Y2,ng); if(k==nodes[bb].key){got=true;xs_found.assign(xs,xs+p);} });
            out+="[";for(int t=0;t<p;t++){out+=to_string(xs_found[t]);if(t+1<p)out+=",";}out+="]";
          }
          return out;
        };
        string pcols=cols(path,false,0); // edges along path (start..r)
        string ccols=cols(cyc,true,0);
        printf("SCC p=%d g=%s size=%zu cyclen=%zu depth=%zu path=%s cyc=%s\n",p,gs.c_str(),c.size(),cyc.size(),path.size()-1,pcols.c_str(),ccols.c_str());
        if(!dumpfn.empty()){
          FILE*df=fopen(dumpfn.c_str(),"a");
          fprintf(df,"COMP p=%d g=%s size=%zu\n",p,gs.c_str(),c.size());
          for(int a:c){
            u64 L,H;int Y[64];unpack(nodes[a].key,L,H,Y,ng);
            transitions(L,H,Y,ng,a==0,[&](u64 L2,u64 H2,int*Y2,int*xs,int*hn){
              K128 k=pack(L2,H2,Y2,ng);auto it=id.find(k);if(it==id.end())return;int bb=it->second;if(comp[bb]!=comp[a])return;
              fprintf(df,"E %d %d",a,bb);for(int t=0;t<p;t++)fprintf(df," %d",xs[t]);fprintf(df,"\n");});
          }
          fclose(df);
        }
      }
      fflush(stdout);
    }
    fprintf(stderr,"b=%d p=%d done\n",b,p);
  }
}
