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
int main(int argc,char**argv){
  b=atoi(argv[1]);int pmin=atoi(argv[2]),pmax=atoi(argv[3]);bool wit=false;int part=0,nparts=1;string gfix;bool verb=false;unsigned long long CAPS=150000000ULL;
  for(int i=4;i<argc;i++){string a=argv[i];if(a=="-w")wit=true;else if(a=="-part"){part=atoi(argv[++i]);nparts=atoi(argv[++i]);}else if(a=="-g"){gfix=argv[++i];}else if(a=="-v")verb=true;else if(a=="-band"){string v=argv[++i];size_t pos=0;while(pos<=v.size()){size_t c=v.find(',',pos);if(c==string::npos)c=v.size();Kb.push_back(atoi(v.substr(pos,c-pos).c_str()));pos=c+1;}}else if(a=="-nodepth0"){}else if(a=="-cap")CAPS=strtoull(argv[++i],0,10);}
  ydig=1;while((1<<ydig)<b)ydig++;
  long idx=0;
  for(p=pmin;p<=pmax;p++){
    for(u64 gm=0;gm<(1ULL<<p);gm++){
      if(!gfix.empty()){ if((int)gfix.size()!=p)continue; u64 v=0;for(int t=0;t<p;t++)if(gfix[t]=='1')v|=1ULL<<t; if(v!=gm)continue; }
      else{ // necklace representative: minimal rotation
        bool ok=true;int q=Kb.empty()?1:(int)Kb.size(); if(p%q!=0)continue; for(int r=q;r<p&&ok;r+=q){u64 rot=((gm>>r)|(gm<<(p-r)))&((1ULL<<p)-1);if(rot<gm)ok=false;} if(!ok)continue; }
      if((idx++)%nparts!=part)continue;
      if(!Kb.empty()&&p%(int)Kb.size()!=0)continue; cst.assign(p,0);dst.assign(p,0); if(!Kb.empty()){bool bad=false;for(int t=0;t<p;t++){int k=Kb[t%Kb.size()];if(k==b-1){bad=true;break;}cst[t]=(k>=b);dst[t]=(k+cst[t])%b;int kn=Kb[(t+1)%Kb.size()];if(kn!=2*dst[t])bad=true;} if(bad){fprintf(stderr,"band schedule is not a loop\n");return 1;}}
      g.assign(p,0);Gidx.clear();for(int t=0;t<p;t++){g[t]=(gm>>t)&1;if(g[t])Gidx.push_back(t);}
      int ng=Gidx.size(); if(2*p+ydig*ng>127){fprintf(stderr,"key too long\n");continue;}
      int Y0[64];for(int i=0;i<ng;i++)Y0[i]=1;
      u64 Hs=0;for(int t=0;t<p;t++)Hs|=(u64)g[t]<<t;
      auto T0=chrono::steady_clock::now();K128 start=pack(0,Hs,Y0,ng);
      unordered_set<K128,KH> seen;seen.insert(start);
      unordered_map<K128,pair<K128,vector<int>>,KH> par; if(wit)par[start]={0,vector<int>()};
      vector<K128> fr={start},nf;int depth=0;
      string gs;for(int t=0;t<p;t++)gs+=char('0'+g[t]);
      if(verb)fprintf(stderr,"start g=%s\n",gs.c_str());
      unordered_map<u64,int> accE; // e stream -> depth
      unordered_map<u64,K128> accState;
      while(!fr.empty()&&depth<400){
        nf.clear();
        for(K128 s:fr){
          u64 L,H;int Y[64];unpack(s,L,H,Y,ng);
          if((depth>0||Kb.empty())&&accepting(L,H,Y,ng)&&!accE.count(L)){accE[L]=depth;accState[L]=s;}
          transitions(L,H,Y,ng,depth==0,[&](u64 L2,u64 H2,int*Y2,int*xs,int*hn){
            K128 k=pack(L2,H2,Y2,ng);
            if(seen.insert(k).second){nf.push_back(k);if(wit){par[k]={s,vector<int>(xs,xs+p)};}}
          });
        }
        fr.swap(nf);depth++;
        if(seen.size()>CAPS){fprintf(stderr,"state cap reached g=%s\n",gs.c_str());break;}
      }
      if(verb){double el=chrono::duration<double>(chrono::steady_clock::now()-T0).count();if(el>=0.0)fprintf(stderr,"  g=%s states=%zu depth=%d time=%.1fs\n",gs.c_str(),seen.size(),depth,el);}
      if(!accE.empty()){
        for(auto&kv:accE){
          string es;for(int t=0;t<p;t++)es+=char('0'+((kv.first>>t)&1));
          printf("ACCEPT b=%d p=%d g=%s e=%s depth=%d states=%zu",b,p,gs.c_str(),es.c_str(),kv.second,seen.size());
          if(wit){ // reconstruct columns
            vector<vector<int>> cols;K128 s=accState[kv.first];while(par[s].second.size()){cols.push_back(par[s].second);s=par[s].first;if(s==start)break;}
            reverse(cols.begin(),cols.end());
            printf(" B_t=");for(int t=0;t<p;t++){printf("[");vector<int> r;for(auto&c:cols)r.push_back(c[t]);while(!r.empty()&&r.back()==b-1)r.pop_back();for(size_t i=0;i<r.size();i++)printf("%d%s",r[i],i+1<r.size()?",":"");printf("]");}
          }
          printf("\n");fflush(stdout);
        }
      }
    }
    fprintf(stderr,"b=%d p=%d done\n",b,p);
  }
}
