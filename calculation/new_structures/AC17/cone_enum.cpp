#include <array>
#include <algorithm>
#include <cassert>
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include <chrono>
using namespace std;
constexpr int B[] = {10,4,15,4,1,7,9,11,11,18,0,18,6,9,17,4,0,12,0,2,10,1,12,4,2,15,0,13,4,8,4,8,10,15};
constexpr int W[] = {4,0,5,5,18,4,8,1,15};
constexpr int L0 = 280;
constexpr int CUT = 34+9*14;
static_assert(CUT==160);
struct Outcome {int first=-1,got=0,expected=0,finalL=0, gamma=0, clockError=0;};
inline Outcome test(int lenJ, int Jcode, const int U[3]) {
  uint8_t cur[600], nx[600], low[600], high[600];
  int j[5]={0,0,0,0,0}; int tmp=Jcode;
  for(int i=0;i<lenJ;i++){j[i]=tmp%19;tmp/=19;}
  int pos=0;
  for(int x:B)cur[pos++]=x;
  for(int i=0;i<126;i++)cur[pos++]=W[i%9];
  for(int i=0;i<lenJ;i++)cur[pos++]=j[i];
  while(pos<L0){cur[pos]=U[(pos-CUT-lenJ)%3];pos++;}
  int L=L0, nOver=0, err=0;
  for(int step=0;step<120;step++) {
    int c=0;
    for(int i=0;i<L;i++) {int v=int(cur[i])+c;low[i]=v%10;c=v/10;}
    c=0;
    for(int i=0;i<L;i++) {int v=int(cur[L-1-i])+c;high[i]=v%10;c=v/10;}
    int g=c; nOver+=g;
    err += (g!=(step%4==0));
    int trailing9=0;
    while(trailing9<L && cur[L-1-trailing9]==9)trailing9++;
    if(trailing9==L){return Outcome{-3,0,0,L,nOver,err};}
    int M=L-trailing9-1+g;
    if (M>L) M=L;
    if(M<0){return Outcome{-2,0,0,L,nOver,err};}
    for(int i=0;i<M;i++){
      int h=(g&&i==0)?1: high[L-1-i+g];
      nx[i]=low[i]+h;
    }
    memcpy(cur,nx,M);
    L=M;
  }
  Outcome a;a.finalL=L;a.gamma=nOver;a.clockError=err;
  for(int i=0;i<min(L,CUT);i++){
    int want = (i<34)?B[i]:W[(i-34)%9];
    if(cur[i]!=want){a.first=i;a.got=cur[i];a.expected=want;break;}
  }
  return a;
}
int main(int argc,char**argv){
 if(argc<2){fprintf(stderr,"usage: cone_enum U_rank [maxJcodes for diagnostic]\n");return 2;}
 int uidx=atoi(argv[1]); int cap=argc>=3?atoi(argv[2]):-1;
 if(uidx<0||uidx>=30)return 3;
 int a=2*(uidx/3), r=uidx%3;
 int src[3]={9,a,18-a},U[3]={src[r%3],src[(r+1)%3],src[(r+2)%3]};
 long long count=0, unresolved=0, badclock=0, got30=0;
 int minimumL=1000, minMismatch=9999,maxMismatch=-1;
 long long positions[200]={0}, lengths[601]={0};
 auto st=chrono::steady_clock::now();
 for(int jlen=3;jlen<=4;jlen++){
  int total=jlen==3?6859:130321;
  if(cap>=0)total=min(total,cap);
  for(int code=0;code<total;code++){
   Outcome o=test(jlen,code,U);count++;
   minimumL=min(minimumL,o.finalL);
   if(o.gamma==30)got30++;
   if(o.clockError)badclock++;
   if(o.first<0)unresolved++;
   else {positions[o.first]++;minMismatch=min(minMismatch,o.first);maxMismatch=max(maxMismatch,o.first);}
   if(o.finalL>=0&&o.finalL<601) lengths[o.finalL]++;
   if(o.first < 0 && unresolved<=5)fprintf(stderr,"UNRESOLVED U=%d jlen=%d code=%d L=%d g=%d err=%d\n",uidx,jlen,code,o.finalL,o.gamma,o.clockError);
  }
 }
 printf("RANK %d U=%d,%d,%d COUNT %lld UNRESOLVED %lld CLOCK_ERROR %lld GROWTH30 %lld MIN_L %d MISMATCH_MINMAX %d,%d TIME_SEC %.3f\n",uidx,U[0],U[1],U[2],count,unresolved,badclock,got30,minimumL,minMismatch,maxMismatch,chrono::duration<double>(chrono::steady_clock::now()-st).count());
 printf("POS_HIST:");for(int i=0;i<200;i++)if(positions[i])printf(" %d:%lld",i,positions[i]);printf("\n");
 printf("LEN_HIST:");for(int i=0;i<601;i++)if(lengths[i])printf(" %d:%lld",i,lengths[i]);printf("\n");
 return (unresolved||badclock||got30!=count)?1:0;
}
