// AC13 two-ended carry-prefix endpoint-only census, phase 4 p12/m9.
// The hidden high-side carry is allowed BOTH values at EVERY step.
// Keeping only the common prefix is sound for arbitrary centres and k>=50.
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
static constexpr int B[]={10,4,7,5,13,6,11,1,9,16,16,18,10,9,4,8,1,7,0,2,15,15,9,7,7,10,17,14,18,8,6,6,18,4};
static constexpr int W[]={8,1,15,4,0,5,5,18,4};
static constexpr int MAXN=650;
static constexpr int CUT=34+9*14;
struct Verdict {int mismatch,retained,ambiguous;};
struct Engine {
 uint8_t p[MAXN],nxt[MAXN],low[MAXN],hi0[MAXN],hi1[MAXN];
 Verdict check(const int *J,int n,const int *U,int copies) {
  int L=0;for(int x:B)p[L++]=x;
  for(int q=0;q<14;q++)for(int x:W)p[L++]=x;
  for(int j=0;j<n;j++)p[L++]=J[j];
  for(int q=0;q<copies;q++)for(int j=0;j<3;j++)p[L++]=U[j];
  int ambiguous=0;
  for(int t=0;t<120;t++){
   int c=0;for(int i=0;i<L;i++){int z=p[i]+c;low[i]=z%10;c=z/10;}
   int c0=0,c1=1;
   for(int i=L-1;i>=0;i--){
    int z0=p[i]+c0,z1=p[i]+c1;
    hi0[i]=z0%10;hi1[i]=z1%10;c0=z0/10;c1=z1/10;
   }
   if(c0!=c1)ambiguous++;
   int R=0;
   for(;R<L;R++){
    int y0=(R==0&&c0)?c0:(c0?hi0[R-1]:hi0[R]);
    int y1=(R==0&&c1)?c1:(c1?hi1[R-1]:hi1[R]);
    if(y0!=y1)break;
    nxt[R]=uint8_t(low[R]+y0);
   }
   L=R;std::memcpy(p,nxt,size_t(L));
   if(L==0)break;
  }
  for(int i=0;i<std::min(L,CUT);i++){
   int expected=i<34?B[i]:W[(i-34)%9];
   if(p[i]!=expected)return {i,L,ambiguous};
  }
  return {-1,L,ambiguous};
 }
};
int main(int argc,char **argv){
 int copies=argc>1?std::atoi(argv[1]):50;
 long long limit=argc>2?std::atoll(argv[2]):-1;
 int index=argc>3?std::atoi(argv[3]):-1;
 if(copies<1||copies>100||index>=30)return 3;
 long long total=0,proved=0,unresolved=0,gamma_ambiguous=0;
 int minret=9999,maxret=0,mindiff=9999,maxdiff=-1;
 long long hist[CUT+1]={};
 int firstN=0,firstJ[4]={},firstU[3]={},firstR=0;
 Engine engine;auto start=std::chrono::steady_clock::now();
 for(int a=0;a<=18;a+=2)for(int rot=0;rot<3;rot++){
  int raw[3]={9,a,18-a},U[3]={raw[rot],raw[(rot+1)%3],raw[(rot+2)%3]};
  int ui=(a/2)*3+rot;
  if(index>=0&&ui!=index)continue;
  for(int n=3;n<=4;n++){
   int count=n==3?6859:130321;
   for(int code=0;code<count;code++){
    if(limit>=0&&total>=limit)goto finished;
    int J[4]={};int tmp=code;
    for(int j=0;j<n;j++){J[j]=tmp%19;tmp/=19;}
    auto v=engine.check(J,n,U,copies);
    total++;if(v.ambiguous)gamma_ambiguous++;
    minret=std::min(minret,v.retained);maxret=std::max(maxret,v.retained);
    if(v.mismatch>=0){
     proved++;mindiff=std::min(mindiff,v.mismatch);
     maxdiff=std::max(maxdiff,v.mismatch);hist[v.mismatch]++;
    }else{
     unresolved++;if(unresolved==1){
      firstN=n;firstR=v.retained;for(int j=0;j<4;j++)firstJ[j]=J[j];
      for(int j=0;j<3;j++)firstU[j]=U[j];
     }
    }
   }
  }
 }
finished:
 auto now=std::chrono::steady_clock::now();
 printf("RESULT known_u_copies=%d Uindex=%d total=%lld proved=%lld unresolved=%lld gamma_ambiguous=%lld minretained=%d maxretained=%d mindiff=%d maxdiff=%d seconds=%.6f\n",copies,index,total,proved,unresolved,gamma_ambiguous,minret,maxret,mindiff,maxdiff,std::chrono::duration<double>(now-start).count());
 printf("DIFF_HIST");for(int i=0;i<=CUT;i++)if(hist[i])printf(" %d:%lld",i,hist[i]);printf("\n");
 if(unresolved)printf("FIRST_UNRESOLVED n=%d retained=%d J=[%d,%d,%d,%d] U=[%d,%d,%d]\n",firstN,firstR,firstJ[0],firstJ[1],firstJ[2],firstJ[3],firstU[0],firstU[1],firstU[2]);
 return unresolved?2:0;
}
