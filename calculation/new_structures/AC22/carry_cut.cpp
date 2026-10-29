// AC22: exact endpoint-only two-ended carry-cut for symmetric decimal pairwords.
// Compile: g++ -O3 -std=c++17 -o ac22_cut carry_cut.cpp
// Exhaust full cell: ./ac22_cut --ai 0 --rot 0 --start 0 --limit 2476099 --initial 320
#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
using namespace std;
static constexpr int B[]={1,5,10,12,13,10,3,7,14,11,4,2,3,9,15,7,9,15,11,14,13,13,14,5,5,13,11,11,9,5,10,10,4,5};
static constexpr int W[]={10,14,13,12,9,7,10,4,5};
static uint8_t pref[2][600],lo[600],hi[600];
// This returns an EXACT prefix for every symmetric completion of the input.
// Non-nine P[r] fixes the high-side incoming carry regardless of the middle.
static int prefix_step(int src,int L,int &gam){
  int r=L-1;
  while(r>0 && pref[src][r]==9)--r;
  if(r==0)return 0;
  int c=0;
  for(int i=0;i<r;i++){int v=pref[src][i]+c;lo[i]=v%10;c=v/10;}
  c=(pref[src][r]>9);
  for(int i=r-1;i>=0;i--){int v=pref[src][i]+c;hi[i]=v%10;c=v/10;}
  gam=c;
  if(gam){pref[src^1][0]=lo[0]+1;for(int i=1;i<r;i++)pref[src^1][i]=lo[i]+hi[i-1];}
  else{for(int i=0;i<r;i++)pref[src^1][i]=lo[i]+hi[i];}
  return r;
}
static void setup(uint32_t jcode,int ai,int rot,int initial){
  int J[5];for(int h=0;h<5;h++){J[h]=jcode%19;jcode/=19;}
  int U[3]={9,2*ai,18-2*ai};rotate(U,U+rot,U+3);
  int j=0;for(int x:B)pref[0][j++]=x;for(int q=0;q<14;q++)for(int x:W)pref[0][j++]=x;
  for(int x:J)pref[0][j++]=x;
  for(int k=0;k<45;k++)for(int x:U)pref[0][j++]=x;
  for(int i=j;i<initial;i++)pref[0][i]=U[(i-j)%3];
}
static int run(uint32_t j,int ai,int rot,int initial,int &left,int &gamma,int &reason){
  setup(j,ai,rot,initial);int L=initial;gamma=0;reason=0;
  for(int t=0;t<120;t++){int g;L=prefix_step(t&1,L,g);if(L==0){left=0;reason=1;return -1;}gamma+=g;}
  left=L;
  if(gamma!=30){reason=2;return -1;}
  int h=0;
  for(int x:B){if(h>=L){reason=3;return -1;}if(pref[0][h]!=x)return h;h++;}
  for(int q=0;q<14;q++)for(int x:W){if(h>=L){reason=3;return -1;}if(pref[0][h]!=x)return h;h++;}
  int J[5];for(int x=0;x<5;x++){J[x]=j%19;j/=19;}
  for(int x:J){if(h>=L){reason=3;return -1;}if(pref[0][h]!=x)return h;h++;}
  int U[3]={9,2*ai,18-2*ai};rotate(U,U+rot,U+3);
  for(int x:U){if(h>=L){reason=3;return -1;}if(pref[0][h]!=x)return h;h++;}
  reason=4;return -1;
}
int main(int argc,char**argv){
  int init=320,ai=-1,rot=-1;uint32_t start=0,lim=1000;
  for(int i=1;i<argc;i++){string a=argv[i];if(a=="--initial")init=stoi(argv[++i]);else if(a=="--start")start=stoul(argv[++i]);else if(a=="--limit")lim=stoul(argv[++i]);else if(a=="--ai")ai=stoi(argv[++i]);else if(a=="--rot")rot=stoi(argv[++i]);}
  if(init<1||init>600||start>2476099){fprintf(stderr,"invalid arguments\n");return 2;}
  auto ts=chrono::steady_clock::now();uint64_t hist[600]={0},rs[6]={0},count=0,esc=0;int minL=999;
  for(int a=ai<0?0:ai;a<=(ai<0?9:ai);a++)for(int r=rot<0?0:rot;r<=(rot<0?2:rot);r++)for(uint32_t j=start;j<start+lim&&j<2476099;j++){
    int L,g,why,m=run(j,a,r,init,L,g,why);
    count++;if(L<minL)minL=L;
    if(m>=0&&m<600)hist[m]++;else {rs[why]++;esc++;if(esc<8)printf("ESC j=%u ai=%d rot=%d L=%d gamma=%d why=%d\n",j,a,r,L,g,why);}
  }
  auto te=chrono::steady_clock::now();printf("cases=%llu undecided=%llu minL=%d elapsed=%.4f\n",(unsigned long long)count,(unsigned long long)esc,minL,chrono::duration<double>(te-ts).count());
  for(int i=0;i<600;i++)if(hist[i])printf("%d:%llu ",i,(unsigned long long)hist[i]);puts("");
  for(int i=0;i<6;i++)if(rs[i])printf("reason%d=%llu ",i,(unsigned long long)rs[i]);puts("");
}
