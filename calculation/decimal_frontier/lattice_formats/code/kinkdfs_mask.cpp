// K1: exhaustive centre-window horizon DFS with conservative bitmask
// domain propagation. No possible concrete survivor is pruned.
// Based on the exact finite window map in lattice_formats/code/kinkdfs.cpp.
// Build: g++ -O3 -std=c++17 -DNDEBUG kinkdfs_mask.cpp -o kinkdfs_mask
// Usage: kinkdfs_mask lattice.txt WIDTH HORIZON OLO OHI [PREFIX]
// PREFIX is comma-separated free digits, low to high; independent partitions
// over (offset, prefix) permit resumable exhaustive runs.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
using namespace std;
using Mask=uint64_t;
static constexpr int KMAX=128;
struct Lat {
 int p=0,nB=0,m=0,b=0;
 vector<int> gam;
 vector<vector<int>> W,cu;
 bool load(const char *filename){
   FILE*f=fopen(filename,"r");if(!f)return false;
   if(fscanf(f,"%d %d %d %d",&p,&nB,&m,&b)!=4||p<=0||m<=0||b<2||b>32)return false;
   gam.resize(p); for(auto &a:gam)if(fscanf(f,"%d",&a)!=1)return false;
   W.assign(p,vector<int>(m));cu.assign(p,vector<int>(m));
   for(auto &row:W)for(auto &a:row)if(fscanf(f,"%d",&a)!=1)return false;
   for(auto &row:cu)for(auto &a:row)if(fscanf(f,"%d",&a)!=1)return false;
   fclose(f);
   // Fail closed on malformed inputs; invalid carry/coefficient domains
   // could otherwise turn a claimed finite-width exclusion into garbage.
   for(int g:gam)if(g!=0&&g!=1)return false;
   for(const auto& row:W)for(int v:row)if(v<0||v>2*b-2)return false;
   for(const auto& row:cu)for(int v:row)if(v!=0&&v!=1)return false;
   return true;
 }
 int idx(long k)const {int r=(int)((k-nB)%m);return r<0?r+m:r;}
 int cell(int t,long x)const {return W[t%p][idx(x)];}
 int carry(int t,long x)const{return cu[t%p][idx(x)];}
};
struct NC{Mask out;unsigned c;};
static inline NC norm(Mask p,unsigned cm,int b){
 Mask d=0;unsigned c=0;
 if(cm&1){Mask lo=p&((Mask(1)<<b)-1),hi=p>>b;
   d|=lo|hi; c|=(lo?1:0)|(hi?2:0);}
 if(cm&2){Mask lo=p&((Mask(1)<<(b-1))-1),hi=p>>(b-1);
   d|=(lo<<1)|hi; c|=(lo?1:0)|(hi?2:0);}
 return {d,c};
}
static inline Mask pairSum(Mask a,Mask z){
 Mask v=0;
 while(a){unsigned d=__builtin_ctzll(a);a&=a-1;v|=z<<d;}
 return v;
}
struct Search {
 Lat L;int w=0,K=0,H=0,n=0,t0=0,o=0;
 int digits[KMAX]{};
 uint64_t nodes[KMAX]{},leaves=0,prunes=0;
 Mask full=0,even=0;
 Search(const Lat& lat,int width,int horizon,int offset):L(lat),w(width),H(horizon),o(offset){
   K=w+10;
   full=(Mask(1)<<(2*L.b-1))-1;
   for(int v=0;v<=2*L.b-2;v+=2)even|=Mask(1)<<v;
   n=2*L.m*((max(400,2*L.nB+2*K)+2*L.m-1)/(2*L.m))+o;
 }
 bool feasible(int assigned) const {
   Mask s[KMAX],q[KMAX],up[KMAX],dn[KMAX];
   unsigned ca[KMAX+1],cd[KMAX];
   long h=(n+1)/2,cur_n=n;
   for(int i=0;i<K-w;i++)s[i]=Mask(1)<<L.cell(t0,h-K+i);
   for(int i=0;i<w;i++)s[K-w+i]=(i<assigned)?Mask(1)<<digits[i]:full;
   if(cur_n&1){s[K-1]&=even;if(!s[K-1])return false;}
   for(int step=0;step<H;step++){
     int t=t0+step,g=L.gam[t%L.p];bool odd=cur_n&1;
     ca[0]=1u<<L.carry(t,h-K);
     for(int i=0;i<K;i++){NC v=norm(s[i],ca[i],L.b);up[i]=v.out;ca[i+1]=v.c;}
     int top;
     if(odd){dn[K-1]=up[K-1];cd[K-2]=ca[K];top=K-2;}
     else{cd[K-1]=ca[K];top=K-1;}
     for(int i=top;i>=0;i--){NC v=norm(s[i],cd[i],L.b);dn[i]=v.out;if(i>0)cd[i-1]=v.c;}
     long n2=cur_n+g,h2=(n2+1)/2;int dh=int(h2-h);
     for(int j=0;j<K;j++){
       if(j<2){q[j]=Mask(1)<<L.cell(t+1,h2-K+j);continue;}
       int i=j+dh;Mask a,z;
       if(g==0){a=up[i];z=(odd&&i==K-1)?up[i]:dn[i];}
       else {a=(i<K)?up[i]:dn[K-1];z=dn[i-1];}
       Mask poss=pairSum(a,z);
       if(j<K-w){Mask req=Mask(1)<<L.cell(t+1,h2-K+j);
          if((poss&req)==0)return false;
          q[j]=req;
       }else q[j]=poss;
     }
     if(n2&1){q[K-1]&=even;if(!q[K-1])return false;}
     memcpy(s,q,sizeof(Mask)*K);h=h2;cur_n=n2;
   }
   return true;
 }
 void dfs(int assigned){
   nodes[assigned]++;
   if(assigned==w){leaves++;return;}
   for(int d=0;d<=2*L.b-2;d++){
     if(assigned==w-1 && (n&1) && (d&1))continue;
     digits[assigned]=d;
     if(feasible(assigned+1))dfs(assigned+1);
     else prunes++;
   }
 }
};
int main(int argc,char**argv){
 if(argc<6){fprintf(stderr,"usage: %s lat.txt W H OLO OHI [prefix]\n",argv[0]);return 1;}
 Lat L;if(!L.load(argv[1])){fprintf(stderr,"bad lattice file\n");return 2;}
 int w=atoi(argv[2]),H=atoi(argv[3]),lo=atoi(argv[4]),hi=atoi(argv[5]);
 if(w<1||w+10>=KMAX||H<1||lo<0||hi>2*L.m||hi<=lo)return 2;
 vector<int> prefix;
 if(argc>=7){string s=argv[6];size_t pos=0;
   while(pos<s.size()){
     size_t e=s.find(',',pos);if(e==string::npos)e=s.size();
     int d=atoi(s.substr(pos,e-pos).c_str());if(d<0||d>2*L.b-2)return 2;
     prefix.push_back(d);pos=e+1;
   }
   if((int)prefix.size()>w)return 2;
 }
 for(int o=lo;o<hi;o++){
   Search S(L,w,H,o);for(int i=0;i<(int)prefix.size();i++)S.digits[i]=prefix[i];
   auto start=chrono::steady_clock::now();
   if(S.feasible(prefix.size()))S.dfs(prefix.size());else S.prunes++;
   double dt=chrono::duration<double>(chrono::steady_clock::now()-start).count();
   printf("%s w=%d H=%d o=%d prefix=%s survivors=%llu prunes=%llu cpu_wall_s=%.3f levels:",argv[1],w,H,o,argc>=7?argv[6]:"*",(unsigned long long)S.leaves,(unsigned long long)S.prunes,dt);
   for(int i=0;i<=w;i++)printf(" %llu",(unsigned long long)S.nodes[i]);
   puts("");
   fflush(stdout);
 }
}
