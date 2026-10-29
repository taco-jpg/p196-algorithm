// K2 pilot: exact two-step pairword erasure search, no negative result published.
// Reproduces from repository lattice snapshot without external deps.
#include <bits/stdc++.h>
using namespace std;
static constexpr int MAXN=900;
using PW=array<uint8_t,MAXN>;
struct Lat{int g[12],w[12][9],b[12][34];};
Lat load(const char*fn){ifstream in(fn);int p,bb,m,base;in>>p>>bb>>m>>base;assert(p==12&&bb==34&&m==9&&base==10);Lat L{};for(auto &g:L.g)in>>g;for(auto&row:L.w)for(auto&v:row)in>>v;for(int t=0;t<12;t++)for(int i=0;i<9;i++){int x;in>>x;}for(auto&row:L.b)for(auto&v:row)in>>v;assert(in.good() || in.eof());return L;}
int step(const PW& p,int n,PW& next){uint8_t d[MAXN];int carry=0;for(int i=0;i<n;i++){int v=p[i]+carry;d[i]=v%10;carry=v/10;}int len=n;if(carry)d[len++]=carry;for(int i=0;i<len;i++)next[i]=d[i]+d[len-i-1];return len;}
PW word(const Lat&l,int t,int n){PW p{};for(int i=0;i<(n+1)/2;i++){int q=i<34?l.b[t][i]:l.w[t][(i-34)%9];if(n%2&&i==n/2&&q%2)q+=(q<18?1:-1);p[i]=p[n-i-1]=q;}return p;}
int main(int argc,char**argv){auto L=load(argc>1?argv[1]:"/mnt/data/agent5-work/lat_p12m9.txt");uint64_t total=0,nonerase=0,hits=0;for(int n:{400,401}){for(int t=0;t<12;t++){if(L.g[t])continue;PW base=word(L,t,n),b1{},b2{};int nb1=step(base,n,b1);int nb2=step(b1,nb1,b2);assert(nb1==n);uint64_t phase=0;
 for(int r=0;r<9;r++)for(int width=1;width<=3;width++){
   int pos=52+r; PW changed=base;
   auto enumerate=[&](auto&& self,int j)->void{
     if(j==width){total++;phase++;PW a1{},a2{};int nc1=step(changed,n,a1);if(nc1!=nb1)return;bool different=false;for(int k=0;k<nb1;k++)if(a1[k]!=b1[k]){different=true;break;}if(!different)return;nonerase++;int nc2=step(a1,nc1,a2);if(nc2!=nb2)return;for(int k=0;k<nb2;k++)if(a2[k]!=b2[k])return;hits++;
       cout<<"TWO_STEP_HIT t="<<t<<" n="<<n<<" r="<<r<<" width="<<width<<" pos="<<pos<<" vals=";for(int x=0;x<width;x++)cout<<(int)changed[pos+x]<<",";cout<<"\n";return;}
     int i=pos+j;
     for(int v=0;v<=18;v++){if(v==base[i])continue;changed[i]=changed[n-i-1]=v;self(self,j+1);}
     changed[i]=changed[n-i-1]=base[i];
   };
   enumerate(enumerate,0);
 }
 cout<<"COMPLETE_SOURCE_PHASE n="<<n<<" t="<<t<<" states="<<phase<<"\n";
 }}cerr<<"TWO_STEP_EXHAUSTIVE_PILOT candidates="<<total<<" distinct_first_step="<<nonerase<<" hit="<<hits<<" n=400,401 gamma0 all9 phases all9 residues widths<=3\n";return 0;}
