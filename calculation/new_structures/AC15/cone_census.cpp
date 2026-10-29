// AC15: exact centre-independent endpoint carry cone for rooted phase 6.
// Build: c++ -O3 -std=c++17 cone_census.cpp -o cone_census
// Usage: ./cone_census LENGTH(3|4) U_RANK(0..29) FIRST_CODE LAST_CODE
// LAST_CODE is exclusive; full range is 19^LENGTH.
#include <vector>
#include <algorithm>
#include <chrono>
#include <iostream>
#include <cstdint>
#include <cstdlib>
using V=std::vector<unsigned char>;
constexpr int Q=14, K=100, PH=6, CUT=34+9*Q;
const int B[34]={2,11,3,6,0,1,17,7,2,14,9,14,1,2,9,5,9,17,14,4,17,4,12,15,9,18,9,7,10,16,10,6,12,8};
const int W[9]={5,9,16,0,9,11,1,10,8};
const int GAM[12]={1,0,0,0,1,0,0,0,1,0,0,0};
struct Stat {
 uint64_t n=0,returned=0,clockbad=0,cone_error=0;
 unsigned min_prefix=1000000,max_prefix=0,min_cone=1000000;
 uint64_t histogram[CUT+4]{};
};
static void init(V& p,int len,uint64_t code,int uidx){
 int U[3]={9,2*(uidx/3),18-2*(uidx/3)};
 std::rotate(U,U+uidx%3,U+3);
 p.clear();p.reserve(34+9*Q+len+3*K+20);
 for(auto x:B)p.push_back(x);
 for(int r=0;r<Q;r++)for(auto x:W)p.push_back(x);
 int J[4];for(int i=len-1;i>=0;i--){J[i]=code%19;code/=19;}
 for(int i=0;i<len;i++)p.push_back(J[i]);
 for(int r=0;r<K;r++)for(int z=0;z<3;z++)p.push_back(U[z]);
}
// Folded-prefix lemma: x is the known least-significant half prefix of
// a symmetric coefficient word (all coefficients 0..18). The unknown
// interior can send either carry bit 0 or 1 into the mirrored high segment.
// In its reverse-order normalization, the last (highest-index) non-nine
// x[j] resets that carry. Thus positions i<j have identical high digits,
// and the final overflow gamma is independent of the unknown interior.
// With gamma=0, preserve j prefix sites; gamma=1 shifts the high index by
// one and preserves min(n,j+1) prefix sites. No strict-phase W9 hypothesis.
static int advance(V& p,V& lo,V& hi,V& next){
 const int n=p.size();int j=-1;
 for(int i=n-1;i>=0;i--)if(p[i]!=9){j=i;break;}
 if(j<0)return -2;
 int c=0;lo.resize(n);
 for(int i=0;i<n;i++){
  const int z=(int)p[i]+c;lo[i]=z%10;c=z/10;
 }
 c=0;hi.resize(n);
 for(int i=n-1;i>=0;i--){
  const int z=(int)p[i]+c;hi[i]=z%10;c=z/10;
 }
 const int gamma=c;
 const int keep=std::min(n,j+gamma);
 if(keep<CUT)return -1;
 next.resize(keep);
 if(gamma==0){
  for(int i=0;i<keep;i++)next[i]=lo[i]+hi[i];
 }else{
  next[0]=lo[0]+1;
  for(int i=1;i<keep;i++)next[i]=lo[i]+hi[i-1];
 }
 p.swap(next);
 return gamma;
}
static Stat scan(int len,int uidx,uint64_t start,uint64_t end){
 Stat s;V p,lo,hi,next;
 for(uint64_t code=start;code<end;code++){
  init(p,len,code,uidx);bool ok=true;
  for(int t=0;t<120;t++){
   const int gamma=advance(p,lo,hi,next);
   if(gamma<0){s.cone_error++;ok=false;break;}
   if(gamma!=GAM[(PH+t)%12]){s.clockbad++;ok=false;break;}
  }
  s.n++;
  if(!ok)continue;
  s.min_cone=std::min(s.min_cone,(unsigned)p.size());
  unsigned i=0;
  while(i<CUT && p[i]==(i<34?B[i]:W[(i-34)%9]))++i;
  s.histogram[i]++;
  s.min_prefix=std::min(s.min_prefix,i);
  s.max_prefix=std::max(s.max_prefix,i);
  if(i==CUT)s.returned++;
 }
 return s;
}
int main(int argc,char**argv){
 if(argc!=5){
  std::cerr<<"usage: cone_census J_LENGTH U_RANK START_CODE STOP_CODE\n";
  return 2;
 }
 const int len=atoi(argv[1]),uidx=atoi(argv[2]);
 const uint64_t start=atoll(argv[3]),end=atoll(argv[4]);
 if((len!=3&&len!=4)||uidx<0||uidx>=30||start>end||
    end>(len==3?6859u:130321u))return 2;
 auto tic=std::chrono::steady_clock::now();
 const Stat s=scan(len,uidx,start,end);
 std::cout<<"{\"length\":"<<len<<",\"u_rank\":"<<uidx
          <<",\"start\":"<<start<<",\"stop\":"<<end
          <<",\"cases\":"<<s.n<<",\"Wok\":"<<s.returned
          <<",\"clockbad\":"<<s.clockbad
          <<",\"cone_error\":"<<s.cone_error
          <<",\"min_cone\":"<<s.min_cone
          <<",\"min_prefix\":"<<s.min_prefix
          <<",\"max_prefix\":"<<s.max_prefix<<",\"hist\":{";
 bool first=true;
 for(int i=0;i<CUT+4;i++)if(s.histogram[i]){
  if(!first)std::cout<<",";
  first=false;
  std::cout<<"\""<<i<<"\":"<<s.histogram[i];
 }
 std::cout<<"},\"seconds\":"
          <<std::chrono::duration<double>(
              std::chrono::steady_clock::now()-tic).count()
          <<"}\n";
}
