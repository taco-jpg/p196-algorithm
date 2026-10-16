/* Agent #102: complementary-band outer graph at cap 7 (|B| <= 7), same map as outer_graph.c.
   Memo (1 byte) for |B| <= 6; |B| = 7 states are recomputed along paths with a hard guard.
   Any path of more than GUARD consecutive length-7 states, or any revisit of an on-stack memo
   state, is reported as a potential cycle and aborts (never assumed away). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <omp.h>
#ifndef CAP
#define CAP 7
#endif
#define MCAP (CAP-1)
#define GUARD 2000
static uint64_t P19[10], OFF[10], PER;
static int kk(int x){return x>=10;} static int tt(int x){return x-9*kk(x);}
static int step(int c,const int*B,int L,int*c2,int*Bp,int*Lp){
  int DB[16],DRB[16],e=0;
  for(int i=0;i<L;i++){int s=B[i]+e;DB[i]=s%10;e=s/10;}
  int e0=e; e=kk(c);
  for(int i=0;i<L;i++){int s=B[L-1-i]+e;DRB[i]=s%10;e=s/10;}
  int g=e, tc=tt(c), u0=c+e0-10*kk(c);
  int X[17],Y[17]; for(int i=0;i<L;i++)X[i]=DB[i]; X[L]=u0;
  if(g==0){for(int i=0;i<L;i++)Y[i]=DRB[L-1-i]; Y[L]=tc;}
  else{Y[0]=1; for(int i=0;i<L;i++)Y[i+1]=DRB[L-1-i];}
  int n=L+1; for(int i=0;i<n;i++)Bp[i]=X[i]+Y[i];
  *c2=2*tc; while(n>0&&Bp[n-1]==*c2)n--;
  *Lp=n; return n<=CAP;
}
static uint64_t midx(int c,const int*B,int L){uint64_t v=0;for(int i=L-1;i>=0;i--)v=v*19+B[i];return (uint64_t)(c/2-1)*PER+OFF[L]+v;}
static void mdecode(uint64_t s,int*c,int*B,int*L){int ci=s/PER; uint64_t r=s%PER; int l=0; while(l<MCAP&&r>=OFF[l+1])l++;
  r-=OFF[l]; for(int i=0;i<l;i++){B[i]=r%19;r/=19;} *L=l; *c=2*(ci+1);}
static int valid(int c,const int*B,int L){ if(L==0)return 1; if(B[0]<1)return 0; if(B[L-1]==c)return 0; return 1;}
static uint8_t *T;
/* follow from (c,B,L) using only reads of T for memo states; returns exit time of the start;
   (used in phase 2, read-only) */
static int follow_ro(int c,int*B,int L){
  int steps=0, seven=0, c2,Bp[17],Lp, BB[17]; int cc=c,LL=L; memcpy(BB,B,sizeof(int)*L);
  for(;;){
    if(LL<=MCAP){int v=T[midx(cc,BB,LL)]; if(v==0||v==255){fprintf(stderr,"memo miss\n");exit(5);} return steps+v;}
    if(++seven>GUARD){fprintf(stderr,"GUARD exceeded: potential cycle\n");exit(3);}
    steps++;
    if(!step(cc,BB,LL,&c2,Bp,&Lp)) return steps;
    cc=c2; LL=Lp; memcpy(BB,Bp,sizeof(int)*Lp);
  }
}
int main(void){
  P19[0]=1; for(int i=1;i<10;i++)P19[i]=P19[i-1]*19;
  OFF[0]=0; for(int l=1;l<=MCAP+1;l++)OFF[l]=OFF[l-1]+P19[l-1]; PER=OFF[MCAP+1];
  uint64_t TOT=8*PER; T=calloc(TOT,1);
  uint64_t states=0,internal=0,exits=0; int maxt=0;
  uint64_t H[256]={0};
  /* phase 1: all |B|<=6 starts, sequential, memo with on-stack marks */
  uint64_t *stk=malloc(sizeof(uint64_t)*400000);
  int B[17],Bp[17],L,Lp,c,c2;
  for(uint64_t s=0;s<TOT;s++){
    mdecode(s,&c,B,&L); if(!valid(c,B,L))continue; states++;
    if(step(c,B,L,&c2,Bp,&Lp))internal++; else exits++;
    if(T[s])continue;
    int sp=0, extra=0, seven=0; uint64_t cur=s; int cc=c,LL=L,BB[17]; memcpy(BB,B,sizeof(int)*L);
    for(;;){
      if(LL<=MCAP){
        cur=midx(cc,BB,LL);
        if(T[cur]==255){fprintf(stderr,"CYCLE through memo state\n");exit(3);}
        if(T[cur]){extra=T[cur];break;}
        T[cur]=255; stk[sp++]=cur; seven=0;
        if(!step(cc,BB,LL,&c2,Bp,&Lp)){extra=0;break;}
      } else {
        if(++seven>GUARD){fprintf(stderr,"GUARD exceeded in phase 1\n");exit(3);}
        stk[sp++]=~(uint64_t)0; /* length-7 placeholder: counts one step, not memoized */
        if(!step(cc,BB,LL,&c2,Bp,&Lp)){extra=0;break;}
      }
      cc=c2; LL=Lp; memcpy(BB,Bp,sizeof(int)*Lp);
      if(sp>390000){fprintf(stderr,"stack\n");exit(6);}
    }
    int tval=extra;
    while(sp>0){uint64_t x=stk[--sp]; tval++; if(tval>254){fprintf(stderr,"time overflow\n");exit(4);} if(x!=~(uint64_t)0)T[x]=tval;}
  }
  for(uint64_t s=0;s<TOT;s++) if(T[s]){H[T[s]]++; if(T[s]>maxt)maxt=T[s];}
  printf("phase1 (|B|<=6 starts in the cap-7 graph): states=%llu internal=%llu exits=%llu max_exit=%d\n",
    (unsigned long long)states,(unsigned long long)internal,(unsigned long long)exits,maxt); fflush(stdout);
  /* phase 2: all |B|=7 starts, parallel, read-only memo */
  uint64_t N7=P19[7]; uint64_t s7=0,i7=0,e7=0; int max7=0; uint64_t H7[256]={0};
  int bestc=0,bestB[CAP]={0};
  #pragma omp parallel
  {
    uint64_t ls=0,li=0,le=0; int lmax=0,lc=0,lB[CAP]={0}; uint64_t lH[256]={0};
    #pragma omp for schedule(dynamic,1)
    for(int job=0;job<8*19;job++){
      int c=2*(job/19+1); int top=job%19;
      int B[17],Bp[17],c2,Lp;
      for(uint64_t r=0;r<P19[CAP-1];r++){
        uint64_t v=r; for(int i=0;i<CAP-1;i++){B[i]=v%19;v/=19;} B[CAP-1]=top;
        if(!valid(c,B,CAP))continue; ls++;
        if(step(c,B,CAP,&c2,Bp,&Lp))li++; else le++;
        int t=follow_ro(c,B,CAP); lH[t]++;
        if(t>lmax){lmax=t;lc=c;memcpy(lB,B,sizeof lB);}
      }
    }
    #pragma omp critical
    { s7+=ls;i7+=li;e7+=le; for(int i=0;i<256;i++)H7[i]+=lH[i];
      if(lmax>max7||(lmax==max7&&(lc<bestc))){max7=lmax;bestc=lc;memcpy(bestB,lB,sizeof bestB);} }
  }
  (void)N7;
  int M=maxt>max7?maxt:max7;
  printf("phase2 (|B|=CAP starts): states=%llu internal=%llu exits=%llu max_exit=%d example c=%d B=(",
    (unsigned long long)s7,(unsigned long long)i7,(unsigned long long)e7,max7,bestc);
  for(int i=0;i<CAP;i++)printf(i?",%d":"%d",bestB[i]); printf(")\n");
  printf("states=%llu internal_edges=%llu exit_edges=%llu cycles=0 max_exit_time=%d\n",
    (unsigned long long)(states+s7),(unsigned long long)(internal+i7),(unsigned long long)(exits+e7),M);
  printf("hist"); for(int i=1;i<=M;i++)printf(" %d:%llu",i,(unsigned long long)(H[i]+H7[i])); printf("\n");
  if(maxt>=max7){ for(uint64_t s=0;s<TOT;s++) if(T[s]==M){int c,B[8],L; mdecode(s,&c,B,&L); printf("argmax(memo) c=%d B=(",c); for(int i=0;i<L;i++)printf(i?",%d":"%d",B[i]); printf(")\n");} }
  return 0;
}
