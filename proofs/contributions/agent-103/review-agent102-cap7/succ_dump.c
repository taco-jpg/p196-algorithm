/* dump successors of states read from stdin: "c m b0 b1 ..." -> "c' n b'0 ..." */
#include <stdio.h>
#include <stdint.h>
#define CAP 7
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
int main(void){ int c,m; while(scanf("%d %d",&c,&m)==2){ uint8_t B[16],Bp[16]; for(int i=0;i<m;i++){int x; scanf("%d",&x); B[i]=x;} int cp,g; int n=succ(c,B,m,Bp,&cp,&g); printf("%d %d %d",cp,n,g); for(int i=0;i<n;i++) printf(" %d",Bp[i]); printf("\n"); } return 0; }
