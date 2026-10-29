// Independent exact finite-window prefix-pruned DFS for K1 rec0/m20 width14.
// Local experimental cross-check, no state cap and no claim until all slices finish.
// Usage: ./agent1_width14_dfs phase horizon first_digit [prefix_horizon]
// This solver does NOT use Z3, PySAT or the CNF encoding.
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include "agent1_width14_latdata.h"
using namespace std;
constexpr int K=20,W=14,FZ=6,X=-1;
int o,H,Hin,firstdigit, n0;
int cells[W],best[W];
unsigned long long nodes=0,leaves=0,prunes=0;
int maxlife=-1;
chrono::steady_clock::time_point started;
inline int cell(int t,int pos){return LAT_W[t&7][((pos-39)%20+20)%20];}
inline int cup(int t,int pos){return LAT_CUP[t&7][((pos-39)%20+20)%20];}
// Identical mathematical transition to published win.h, independently implemented.
inline bool step(const int* P,int* Q,int t,int n){
  int h=(n+1)/2, g=LAT_G[t&7], odd=n&1;
  int cu[K+1],up[K],dn[K],down[K];
  cu[0]=cup(t,h-K);
  for(int i=0;i<K;i++){
    int v=P[i],c=cu[i];
    if(v!=X && c!=X){int s=v+c;cu[i+1]=s>=10;up[i]=s-10*cu[i+1];}
    else {up[i]=X;cu[i+1]=(v==X)?X:((v>=10)?1:((v<=8)?0:X));}
  }
  int top;
  if(odd){dn[K-1]=cu[K-1];down[K-1]=up[K-1];dn[K-2]=cu[K];top=K-2;}
  else {dn[K-1]=cu[K];top=K-1;}
  if(!odd)down[K-1]=(P[K-1]!=X && dn[K-1]!=X)?(P[K-1]+dn[K-1])%10:X;
  for(int i=top;i>=0;i--){
    if(i<top){int v=P[i+1];dn[i]=(v==X)?X:((v>=10)?1:((v<=8)?0:dn[i+1]));}
    down[i]=(P[i]!=X && dn[i]!=X)?(P[i]+dn[i])%10:X;
  }
  int n2=n+g,dh=(n2+1)/2-h;
  for(int j=0;j<K;j++){
    if(j<2){Q[j]=cell(t+1,(n2+1)/2-K+j);continue;}
    int i=j+dh;
    int a,b;
    if(g==0){a=up[i];b=(odd && i==K-1)?up[i]:down[i];}
    else {a=(i<K)?up[i]:down[K-1];b=down[i-1];}
    int v=(a==X||b==X)?X:a+b;
    if(j<FZ){int target=cell(t+1,(n2+1)/2-K+j);if(v!=X&&v!=target)return false;Q[j]=target;}
    else Q[j]=v;
  }
  return true;
}
inline void initialize(int j,int* P){
  int h=(n0+1)/2;
  for(int i=0;i<FZ;i++)P[i]=cell(0,h-K+i);
  for(int i=0;i<W;i++)P[FZ+i]=(i<j)?cells[i]:X;
}
inline bool survives_prefix(int j){
  int P[K],Q[K],n=n0;initialize(j,P);
  for(int t=0;t<Hin;t++){
    if(!step(P,Q,t,n))return false;
    memcpy(P,Q,sizeof(P));n+=LAT_G[t&7];
    if(P[FZ]==X)break;
  }
  return true;
}
inline int full_life(){
  int P[K],Q[K],n=n0;initialize(W,P);
  for(int t=0;t<H;t++){
    if(!step(P,Q,t,n))return t;
    memcpy(P,Q,sizeof(P));n+=LAT_G[t&7];
  }
  return H;
}
void report(const char* tag,int life){
  auto sec=chrono::duration<double>(chrono::steady_clock::now()-started).count();
  printf("%s phase=%d H=%d first=%d nodes=%llu leaves=%llu prunes=%llu maxlife=%d life=%d wall=%.1f cells=",tag,o,H,firstdigit,nodes,leaves,prunes,maxlife,life,sec);
  for(int i=0;i<W;i++)printf("%s%d",i?",":"",(tag[0]=='S'||tag[0]=='C')?cells[i]:best[i]);
  puts("");fflush(stdout);
}
unsigned long long tree_levels[W+1]={0},tree_pruned[W+1]={0};
void prefix_tree(int j,int maxdepth){
  tree_levels[j]++;
  if(j==maxdepth)return;
  for(int d=0;d<=18;d++){
    if(j==W-1 && (n0&1) && (d&1))continue;
    cells[j]=d;
    if(!survives_prefix(j+1)){tree_pruned[j+1]++;continue;}
    prefix_tree(j+1,maxdepth);
  }
}
void dfs(int j){
  nodes++;
  if((nodes&((1ULL<<22)-1))==0)report("PROGRESS",-1);
  if(j==W){
    leaves++;int life=full_life();
    if(life>maxlife){maxlife=life;memcpy(best,cells,sizeof(cells));report("BEST",life);}
    if(life==H){report("SAT",life);exit(10);}
    return;
  }
  for(int d=0;d<=18;d++){
    if(j==W-1 && (n0&1) && (d&1))continue;
    cells[j]=d;
    if(!survives_prefix(j+1)){prunes++;continue;}
    dfs(j+1);
  }
}
int main(int argc,char**argv){
  if(argc<4){fprintf(stderr,"usage: %s phase horizon firstdigit [prefix_horizon]\n",argv[0]);return 2;}
  o=atoi(argv[1]);H=atoi(argv[2]);firstdigit=atoi(argv[3]);Hin=(argc>4 && strcmp(argv[4],"--check")!=0 && strcmp(argv[4],"--prefix")!=0 && strncmp(argv[4],"--tree=",7)!=0)?atoi(argv[4]):H;
  if(o<0||o>3||H<1||H>1000||firstdigit<0||firstdigit>18||Hin<1||Hin>H)return 2;
  n0=400+o;started=chrono::steady_clock::now();
  if(argc>=5 && strncmp(argv[4],"--tree=",7)==0){
    int depth=atoi(argv[4]+7);
    if(depth<1||depth>W)return 2;
    cells[0]=firstdigit;
    if(survives_prefix(1))prefix_tree(1,depth);
    else tree_pruned[1]++;
    printf("TREE phase=%d H=%d first=%d depth=%d",o,H,firstdigit,depth);
    for(int j=1;j<=depth;j++)printf(" level%d=%llu pruned%d=%llu",j,tree_levels[j],j,tree_pruned[j]);
    puts("");return 0;
  }
  if(argc>=5 && strcmp(argv[4],"--prefix")==0){
    cells[0]=firstdigit;
    bool ok=survives_prefix(1);
    printf("PREFIX phase=%d H=%d first=%d may_survive=%d\n",o,H,firstdigit,(int)ok);
    return ok?0:5;
  }
  if(argc>=6 && strcmp(argv[4],"--check")==0){
    char* v=argv[5];int j=0;
    while(*v && j<W){char* e=nullptr;long x=strtol(v,&e,10);if(e==v||x<0||x>18)return 3;cells[j++]=(int)x;v=e;if(*v==',')v++;else if(*v)return 3;}
    if(j!=W||*v)return 3;
    int life=full_life();report("CHECK",life);
    return life==H?0:4;
  }
  cells[0]=firstdigit;
  if(survives_prefix(1))dfs(1);else prunes++;
  report("DONE_SLICE",-1);
  return 0;
}
