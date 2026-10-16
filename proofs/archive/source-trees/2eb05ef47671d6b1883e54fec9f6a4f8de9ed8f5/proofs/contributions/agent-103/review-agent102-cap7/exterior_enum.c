/* Agent #103 independent enumeration of the complementary-band exterior map
   (c,B) -> (c',B') over even phases and trimmed B with |B| <= CAP.
   Map written from METHOD_AND_PROOF.md (3),(4),(6),(7) + suffix trimming;
   cross-checked against exterior_ref.py (Python) and literal integers.
   Exit time of a state = number of transitions until the first successor with |B'| > CAP. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#ifdef _OPENMP
#include <omp.h>
#endif
#ifndef CAP
#define CAP 7
#endif
#define MEMOMAX (CAP < 7 ? CAP : 6)
#define GUARD 100000
static const int PH[8] = {2,4,6,8,10,12,14,16};
static int phase_index(int c){ for(int i=0;i<8;i++) if(PH[i]==c) return i; return -1; }

/* successor; returns new length, writes Bp, *cp; returns -1 if invalid successor */
static int succ(int c, const uint8_t *B, int m, uint8_t *Bp, int *cp, int *gam){
  int k = c >= 10, t = c - 9*k, c2 = 2*t;
  uint8_t DB[16], DRB[16]; int e = 0;
  for(int i=0;i<m;i++){ int s=B[i]+e; DB[i]=s%10; e=s/10; }
  int u0 = c + e - 10*k;
  int g = k;
  for(int i=0;i<m;i++){ int s=B[m-1-i]+g; DRB[i]=s%10; g=s/10; }  /* N(rev B, k) */
  /* left = DB ++ [u0]; right = gamma==0 ? rev(DRB) ++ [t] : [1] ++ rev(DRB) */
  int n = m+1;
  for(int i=0;i<n;i++){
    int L = (i<m) ? DB[i] : u0;
    int R;
    if(g==0) R = (i<m) ? DRB[m-1-i] : t;
    else     R = (i==0) ? 1 : DRB[m-1-(i-1)];
    Bp[i] = (uint8_t)(L+R);
  }
  while(n>0 && Bp[n-1]==c2) n--;
  *cp = c2; *gam = g;
  if(n>0 && Bp[0]==0) return -1;          /* would leave the domain: must never happen */
  return n;
}

static int valid(int c, const uint8_t *B, int m){
  if(m==0) return 1;
  if(B[0]==0) return 0;
  if(B[m-1]==c) return 0;
  return 1;
}

static uint64_t pw19[9];
static uint64_t base_off[8];   /* offset of length m within one phase block */
static uint64_t per_phase;
static uint8_t *memo;          /* 0 unknown, 255 in progress, else exit time */
static uint64_t idx(int ci, const uint8_t *B, int m){
  uint64_t r=0; for(int i=m-1;i>=0;i--) r=r*19+B[i];
  return (uint64_t)ci*per_phase + base_off[m] + r;
}
static volatile int bad = 0;
static void report_bad(const char *why, int c, const uint8_t *B, int m){
  #pragma omp critical
  { fprintf(stderr,"BAD %s c=%d m=%d B=",why,c,m); for(int i=0;i<m;i++) fprintf(stderr,"%d,",B[i]); fprintf(stderr,"\n"); bad=1; }
}

/* exit time; memo used/filled only for m<=MEMOMAX and only when allow_write */
static int T(int c, const uint8_t *B, int m, int depth, int allow_write){
  if(depth > GUARD){ report_bad("guard",c,B,m); return 0; }
  uint64_t id=0; int memoable = (m<=MEMOMAX);
  if(memoable){
    id = idx(phase_index(c),B,m);
    uint8_t v = memo[id];
    if(v==255){ report_bad("cycle",c,B,m); return 0; }
    if(v) return v;
    if(allow_write) memo[id]=255;
  }
  uint8_t Bp[16]; int cp, gam;
  int n = succ(c,B,m,Bp,&cp,&gam);
  if(n<0){ report_bad("domain",c,B,m); return 0; }
  int r;
  if(n > CAP) r = 1;
  else r = 1 + T(cp,Bp,n,depth+1,allow_write);
  if(r>254){ report_bad("overflow-time",c,B,m); r=254; }
  if(memoable && allow_write) memo[id]=(uint8_t)r;
  return r;
}

int main(void){
  pw19[0]=1; for(int i=1;i<9;i++) pw19[i]=pw19[i-1]*19;
  base_off[0]=0; for(int m=1;m<=MEMOMAX+1 && m<8;m++) base_off[m]=base_off[m-1]+pw19[m-1];
  per_phase = base_off[MEMOMAX]+pw19[MEMOMAX];
  memo = calloc(8*per_phase,1); if(!memo){ fprintf(stderr,"oom\n"); return 2; }
  uint64_t states=0, internal=0, exits=0, hist[256]={0}; int best=0;
  /* phase A: all states with m<=MEMOMAX, single-threaded, filling memo */
  for(int ci=0;ci<8;ci++){
    int c=PH[ci];
    for(int m=0;m<=MEMOMAX;m++){
      uint8_t B[16];
      for(uint64_t r=0;r<pw19[m];r++){
        uint64_t x=r; for(int i=0;i<m;i++){ B[i]=x%19; x/=19; }
        if(!valid(c,B,m)) continue;
        int t = T(c,B,m,0,1);
        uint8_t Bp[16]; int cp,gam; int n=succ(c,B,m,Bp,&cp,&gam);
        states++; if(n>CAP) exits++; else internal++;
        hist[t]++; if(t>best) best=t;
      }
    }
  }
  /* phase B: m=7 (only when CAP>=7), read-only memo, parallel */
  if(CAP>=7){
    for(int ci=0;ci<8;ci++){
      int c=PH[ci];
      uint64_t lstates=0,lint=0,lexit=0,lhist[256]={0}; int lbest=0;
      #pragma omp parallel for schedule(dynamic,1<<16) reduction(+:lstates,lint,lexit) reduction(max:lbest)
      for(uint64_t r=0;r<pw19[7];r++){
        uint8_t B[16]; uint64_t x=r; for(int i=0;i<7;i++){ B[i]=x%19; x/=19; }
        if(!valid(c,B,7)) continue;
        int t = T(c,B,7,0,0);
        uint8_t Bp[16]; int cp,gam; int n=succ(c,B,7,Bp,&cp,&gam);
        lstates++; if(n>CAP) lexit++; else lint++;
        #pragma omp atomic
        lhist[t]++;
        if(t>lbest) lbest=t;
      }
      states+=lstates; internal+=lint; exits+=lexit; for(int i=0;i<256;i++) hist[i]+=lhist[i];
      if(lbest>best) best=lbest;
      fprintf(stderr,"phase c=%d done\n",c);
    }
  }
  printf("{\"cap\": %d, \"states\": %llu, \"internal_edges\": %llu, \"exit_edges\": %llu, \"max_exit_time\": %d, \"bad\": %d, \"histogram\": {",
         CAP,(unsigned long long)states,(unsigned long long)internal,(unsigned long long)exits,best,bad);
  int first=1; for(int i=0;i<256;i++) if(hist[i]){ printf("%s\"%d\": %llu",first?"":", ",i,(unsigned long long)hist[i]); first=0; }
  printf("}}\n");
  return bad?1:0;
}
