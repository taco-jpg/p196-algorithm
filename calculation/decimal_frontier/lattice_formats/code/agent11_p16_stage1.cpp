// Independent exact p16 neutral-exterior position-automaton experiment.
// Local experiment only: not a repository result or a verified certificate.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <string>
#include <unistd.h>
using namespace std;
using u64=uint64_t;
static constexpr int P=16,B=10,G=8,N=19;
static constexpr u64 MASK16=65535ULL, EMPTY=~0ULL;
static u64 dp[17][19];
static int valid[2][19], bv[2][19], car[2][19], part[19][2];
static long long expanded=0;
static inline u64 mix(u64 x) {x^=x>>33;x*=0xff51afd7ed558ccdULL;x^=x>>33;x*=0xc4ceb9fe1a85ec53ULL;x^=x>>33;return x;}
static inline int rot16(int x,int shift){return ((x>>shift)|(x<<(16-shift)))&0xffff;}
static inline u64 pack(int L,int H,const unsigned char *Y) {
  u64 v=0;for(int i=7;i>=0;i--)v=v*10+Y[i];
  return (u64)L|((u64)H<<16)|(v<<32);
}
static inline void unpack(u64 key,int&L,int&H,unsigned char*Y){
 L=(int)(key&65535); H=(int)((key>>16)&65535);u64 v=key>>32;
 for(int i=0;i<8;i++){Y[i]=v%10;v/=10;}
}
static inline u64 canonical(int L,int H,const unsigned char*Y){
 // Rotate by 2j time slots, with one simultaneous Y index shift.
 u64 best=pack(L,H,Y);
 unsigned char rot[8];
 for(int j=1;j<8;j++) {
   for(int i=0;i<8;i++)rot[i]=Y[(i+j)&7];
   u64 k=pack(rot16(L,2*j),rot16(H,2*j),rot);
   if(k<best)best=k;
 }
 return best;
}
struct HashSet{
 vector<u64> slots;size_t occupied=0;
 void init(size_t n=8192){slots.assign(n,EMPTY);occupied=0;}
 void grow(){vector<u64> old;old.swap(slots);slots.assign(old.size()*2,EMPTY);
  size_t mask=slots.size()-1;
  for(u64 k:old)if(k!=EMPTY){size_t pos=mix(k)&mask;while(slots[pos]!=EMPTY)pos=(pos+1)&mask;slots[pos]=k;}
 }
 bool insert(u64 k){if((occupied+1)*10>slots.size()*8)grow();size_t m=slots.size()-1,pos=mix(k)&m;
  for(;;){if(slots[pos]==EMPTY){slots[pos]=k;occupied++;return true;}
  if(slots[pos]==k)return false;pos=(pos+1)&m;}
 }
};
static inline bool accepting(int L,int H,const unsigned char*Y){
 if((L^H)!=65535)return false;
 for(int i=0;i<8;i++)if(Y[i]!=(unsigned char)(9*((L>>(2*i+1))&1)))return false;
 return true;
}
template<class Func>static inline void successors(u64 key,bool first,Func emit){
 int L,H;unsigned char Y[8];unpack(key,L,H,Y);int Lt[16],Ht[16],Yt[16];
 for(int t=0;t<16;t++){Lt[t]=(L>>t)&1;Ht[t]=(H>>t)&1;Yt[t]=(t&1)?Y[t>>1]:0;}
 for(int x=0;x<N;x++)dp[16][x]=1ULL<<x;
 for(int t=15;t>=0;t--){
  int ll=Lt[t],hh=Ht[t];
  for(int x=0;x<19;x++){
   if(first&&x==0){dp[t][x]=0;continue;}
   int vc=valid[hh][x];if(!vc){dp[t][x]=0;continue;}
   int base=bv[ll][x];u64 z=0;
   if(t&1)z=dp[t+1][base+Yt[t]];
   else{if(vc&1)z|=dp[t+1][base+part[x][0]];if(vc&2)z|=dp[t+1][base+part[x][1]];}
   dp[t][x]=z;
  }
 }
 int xs[17],cs[16],choice[17];
 for(int x0=first?1:0;x0<N;x0++){
  if(!(dp[0][x0]&(1ULL<<x0)))continue;
  int t=0;xs[0]=x0;choice[0]=0;
  while(t>=0){
   if(t==16){int L2=0,H2=0;unsigned char Y2[8];
    for(int j=0;j<16;j++){L2|=car[Lt[j]][xs[j]]<<j;H2|=cs[j]<<j;if(j&1)Y2[j>>1]=part[xs[j]][cs[j]];}
    emit(canonical(L2,H2,Y2));t--;continue;}
   int vc=valid[Ht[t]][xs[t]],ok=0;
   while(choice[t]<2){int c=choice[t]++;
    if(!((vc>>c)&1))continue;
    int base=bv[Lt[t]][xs[t]];int nx=base+((t&1)?Yt[t]:part[xs[t]][c]);
    if(!(dp[t+1][nx]&(1ULL<<x0)))continue;
    cs[t]=c;xs[t+1]=nx;t++;choice[t]=0;ok=1;break;
   }
   if(!ok)t--;
  }
 }
}
static void init(){for(int h=0;h<2;h++)for(int x=0;x<19;x++){
 valid[h][x]=0;for(int c=0;c<2;c++)if((x+c>=10)==(h!=0))valid[h][x]|=1<<c;
 bv[h][x]=(x+h)%10;car[h][x]=(x+h>=10);
}for(int x=0;x<19;x++)for(int c=0;c<2;c++)part[x][c]=(x+c)%10;}
int main(int argc,char**argv){init();size_t CAP=argc>1?strtoull(argv[1],nullptr,10):1000000;
 double SEC=argc>2?atof(argv[2]):120;auto t0=chrono::steady_clock::now();
 unsigned char sy[8]={1,1,1,1,1,1,1,1};u64 seed=pack(0,0xaaaa,sy);
 HashSet tab;tab.init();tab.insert(seed);vector<u64>fr(1,seed),nf;
 int depth=0;size_t acc=0;bool capped=false;
 const char* cp=getenv("P16_CKPT");
 auto save=[&](){if(!cp)return;string tmp=string(cp)+".tmp";
 FILE*f=fopen(tmp.c_str(),"wb");if(!f)return;uint64_t v[5]={0x50313643504B5431ULL,(uint64_t)depth,(uint64_t)acc,(uint64_t)tab.occupied,(uint64_t)tab.slots.size()};
 bool ok=fwrite(v,sizeof(v),1,f)==1&&fwrite(tab.slots.data(),sizeof(u64),tab.slots.size(),f)==tab.slots.size();
 uint64_t n=fr.size();ok=ok&&fwrite(&n,sizeof(n),1,f)==1&&fwrite(fr.data(),sizeof(u64),fr.size(),f)==fr.size();
 ok=ok&&fclose(f)==0;if(ok)rename(tmp.c_str(),cp);else remove(tmp.c_str());};
 if(cp){FILE*f=fopen(cp,"rb");if(f){u64 v[5];bool ok=fread(v,sizeof(v),1,f)==1 && v[0]==0x50313643504B5431ULL;
  if(ok){depth=v[1];acc=v[2];tab.occupied=v[3];tab.slots.resize(v[4]);ok=fread(tab.slots.data(),sizeof(u64),tab.slots.size(),f)==tab.slots.size();
   u64 n=0;ok=ok&&fread(&n,sizeof(n),1,f)==1; if(ok){fr.resize(n);ok=fread(fr.data(),sizeof(u64),n,f)==n;}}
  fclose(f);if(!ok){fprintf(stderr,"invalid checkpoint\n");return 3;}fprintf(stderr,"resumed depth=%d states=%zu\n",depth,tab.occupied);}}

 while(!fr.empty()){
  nf.clear();for(size_t i=0;i<fr.size();i++){
   int L,H;unsigned char Y[8];unpack(fr[i],L,H,Y);
   if(accepting(L,H,Y))acc++;
   successors(fr[i],depth==0,[&](u64 k){if(tab.insert(k))nf.push_back(k);});
   // Commit the full frontier before enforcing cap, so the checkpoint is valid.
  }
  if(capped)break;
  fr.swap(nf);depth++;
  auto elapsed=chrono::duration<double>(chrono::steady_clock::now()-t0).count();
  printf("depth %d frontier %zu total %zu acc %zu seconds %.1f\n",depth,fr.size(),tab.occupied,acc,elapsed);fflush(stdout);
  if(depth%50==0)save();
  if(tab.occupied>CAP||elapsed>SEC){capped=true;save();break;}
 }
 auto elapsed=chrono::duration<double>(chrono::steady_clock::now()-t0).count();
 if(!capped && cp)remove(cp);
 printf("STATUS %s total=%zu depth=%d wdone=%d acc=%zu elapsed=%.1f\n",capped?"CAPPED":(acc?"ACCEPT":"EXHAUSTED"),tab.occupied,depth,depth-1,acc,elapsed);
}
