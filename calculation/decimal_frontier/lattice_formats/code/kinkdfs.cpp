// Exhaustive DFS (bottom-up digit assignment with ternary look-ahead pruning) for bounded time-periodic centre kinks.
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <vector>
#include <unordered_set>
using namespace std;
typedef uint64_t u64;
int p,nB,m; vector<int> gam; vector<vector<int>> Wt,cup; int b=10; const int X=-1;
int Wlim,K,Tper,maxper,o;
long long nodes=0, leaves=0, cycles=0, maxdepth_alive=0; long maxsteps=0;
vector<long long> levelcount;
int dig[64];
static inline int lat(int t,int hm,int i){return Wt[t%p][(((hm-K+i-nB)%m)+m)%m];}
// run simulation from state with `known` digits assigned (j of them); returns false if pruned; full=true => all digits known
bool simulate(int j,bool full,long &stepsOut,bool &cycleFound){
  int P[128],Pn[128]; long n=o; int t=0; int hm=(int)(((n+1)/2)%m);
  int base=K-Wlim;
  for(int i=0;i<base;i++)P[i]=lat(0,hm,i);
  for(int i=0;i<Wlim;i++)P[base+i]=(i<j)?dig[i]:X;
  unordered_set<u64> seen; long step=0; cycleFound=false;
  long lim=full?(long)Tper*maxper:(long)(Tper*maxper);
  for(step=0;step<lim;step++){
    // check lattice below core
    bool anyX=false;
    for(int i=0;i<base;i++){ if(P[i]==X){anyX=true;continue;} if(P[i]!=lat(t,hm,i)){stepsOut=step;return false;} }
    if(!full && anyX){stepsOut=step;return true;}  // cannot decide further
    if(full && step%Tper==0){ u64 h=1469598103934665603ULL; for(int i=base;i<K;i++){h^=(u64)(P[i]+1);h*=1099511628211ULL;}
      if(!seen.insert(h).second){cycleFound=true;stepsOut=step;return true;} }
    int g=gam[t%p]; bool odd=n%2!=0;
    int c0=cup[t%p][(((hm-K-nB)%m)+m)%m];
    int cu[130],Oup[130],cd[130],Odn[130];
    cu[0]=c0;
    for(int i=0;i<K;i++){
      int pv=P[i];
      if(pv!=X && cu[i]!=X){int sv=pv+cu[i];cu[i+1]=sv>=b;Oup[i]=sv-b*cu[i+1];}
      else{ Oup[i]=X; if(pv==X)cu[i+1]=X; else cu[i+1]=(pv>=b)?1:((pv<=b-2)?0:X); }
    }
    int top;
    if(odd){Odn[K-1]=Oup[K-1];cd[K-2]=cu[K];top=K-2;}else{cd[K-1]=cu[K];top=K-1;}
    for(int i=top;i>=0;i--){
      if(i<top){ int pv=P[i+1]; if(pv==X)cd[i]=X; else if(pv>=b)cd[i]=1; else if(pv<=b-2)cd[i]=0; else cd[i]=cd[i+1]; }
      Odn[i]=(P[i]!=X && cd[i]!=X)?(P[i]+cd[i])%b:X;
    }
    long n2=n+g; int delta=(int)((n2+1)/2-(n+1)/2); int nt=t+1; int hm2=(int)(((n2+1)/2)%m);
    for(int i2=0;i2<K;i2++){
      if(i2<2){Pn[i2]=lat(nt,hm2,i2);continue;}
      int i=i2+delta; int up,part;
      if(g==0){up=Oup[i];part=(odd&&i==K-1)?Oup[i]:Odn[i];}
      else{up=(i<=K-1)?Oup[i]:Odn[K-1];part=Odn[i-1];}
      Pn[i2]=(up==X||part==X)?X:up+part;
    }
    memcpy(P,Pn,sizeof(int)*K); n=n2; t=nt; hm=hm2;
  }
  stepsOut=step; return true;
}
void dfs(int j){
  nodes++; levelcount[j]++;
  long so; bool cf;
  if(j==Wlim){
    leaves++;
    bool ok=simulate(j,true,so,cf);
    if(so>maxsteps)maxsteps=so;
    if(ok&&cf){cycles++;printf("CYCLE o=%d digits(bottom->center):",o);for(int i=0;i<Wlim;i++)printf(" %d",dig[i]);printf(" steps=%ld\n",so);fflush(stdout);}
    return;
  }
  for(int d=0;d<=2*b-2;d++){
    dig[j]=d;
    bool ok=simulate(j+1,false,so,cf);
    if(!ok)continue;
    dfs(j+1);
  }
}
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"r"); Wlim=atoi(argv[2]); Tper=atoi(argv[3]); maxper=atoi(argv[4]); int olo=atoi(argv[5]),ohi=atoi(argv[6]);
  if(fscanf(f,"%d %d %d %d",&p,&nB,&m,&b)!=4)return 1; gam.resize(p); for(int t=0;t<p;t++)if(fscanf(f,"%d",&gam[t])!=1)return 1;
  Wt.assign(p,vector<int>(m)); cup.assign(p,vector<int>(m));
  for(int t=0;t<p;t++)for(int j=0;j<m;j++)if(fscanf(f,"%d",&Wt[t][j])!=1)return 1;
  for(int t=0;t<p;t++)for(int j=0;j<m;j++)if(fscanf(f,"%d",&cup[t][j])!=1)return 1;
  K=Wlim+10; if(K>120)return 2; if(ohi>2*m)ohi=2*m;
  levelcount.assign(Wlim+2,0);
  for(o=olo;o<ohi;o++){
    dfs(0);
    fprintf(stderr,"o=%d done nodes=%lld leaves=%lld cycles=%lld maxsteps=%ld\n",o,nodes,leaves,cycles,maxsteps);
  }
  printf("Wlim=%d nodes=%lld leaves=%lld cycles=%lld maxsteps=%ld levels:",Wlim,nodes,leaves,cycles,maxsteps);
  for(int j=0;j<=Wlim;j++)printf(" %lld",levelcount[j]); printf("\n");
}
