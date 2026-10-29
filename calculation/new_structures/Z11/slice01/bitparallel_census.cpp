#include <immintrin.h>
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <iomanip>
#include <string>
#include <vector>
#include <limits>
#ifdef _OPENMP
#include <omp.h>
#endif
using V=std::vector<int>;
static const V B={10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5};
static const V W={5,18,4,8,1,15,4,0,5};
static const std::array<V,3> US={V{0,9,18},V{9,4,14},V{14,4,9}}; // lexicographic ranks 1, 13 and 25 of all 30 distinct charge-zero rotations
static constexpr int LANES=32, N=340, CUT=160, TOTAL=19*19*19*19*19;
using Vec=__m256i;
static inline Vec vset(int x){return _mm256_set1_epi8((char)x);}
static inline Vec vzero(){return _mm256_setzero_si256();}
static inline Vec vand(Vec a,Vec b){return _mm256_and_si256(a,b);}
static inline Vec vor(Vec a,Vec b){return _mm256_or_si256(a,b);}
static inline Vec vandnot(Vec a,Vec b){return _mm256_andnot_si256(a,b);}
static inline Vec vcmp_eq(Vec a,Vec b){return _mm256_cmpeq_epi8(a,b);}
static inline Vec vcmp_gt(Vec a,Vec b){return _mm256_cmpgt_epi8(a,b);}
static inline Vec vadd(Vec a,Vec b){return _mm256_add_epi8(a,b);}
static inline Vec vsub(Vec a,Vec b){return _mm256_sub_epi8(a,b);}
static inline Vec vblend(Vec a,Vec b,Vec mask){return _mm256_blendv_epi8(a,b,mask);}
static inline uint32_t bits(Vec x){return (uint32_t)_mm256_movemask_epi8(x);}
static inline int bitcount(uint32_t x){return __builtin_popcount(x);}
static inline int firstbit(uint32_t x){return __builtin_ctz(x);}
struct Batch {Vec p[2][N];Vec valid[2][N];Vec seen[N+1];Vec carryhi[N+1];};
static inline Vec mod10(Vec z,Vec nine,Vec ten){Vec over=vcmp_gt(z,nine);return vsub(z,vand(over,ten));}
static inline void step(Vec* p,Vec* valid,Vec* out,Vec* vout,Vec* seen,Vec* carryhi,Vec& gamma,int len){
  const Vec zero=vzero(),one=vset(1),nine=vset(9);
  seen[len]=zero;carryhi[len]=zero;
  for(int i=len-1;i>=0;--i){
    Vec is9=vcmp_eq(p[i],nine),ge10=vcmp_gt(p[i],nine);
    Vec non9=vand(valid[i],vandnot(is9,_mm256_set1_epi8((char)-1)));
    seen[i]=vand(valid[i],vor(non9,vand(is9,seen[i+1])));
    carryhi[i]=vand(valid[i],vor(ge10,vand(is9,carryhi[i+1])));
  }
  gamma=carryhi[0];
  Vec lowcarry=zero,ten=vset(10);
  for(int i=0;i<len;++i){
    Vec zlow=vadd(p[i],vand(lowcarry,one));
    Vec low=mod10(zlow,nine,ten);
    lowcarry=vcmp_gt(zlow,nine);
    Vec zhi0=vadd(p[i],vand(carryhi[i+1],one));
    Vec hi0=mod10(zhi0,nine,ten);
    Vec hi1;
    if(i==0) hi1=one;
    else {Vec zhi1=vadd(p[i-1],vand(carryhi[i],one));hi1=mod10(zhi1,nine,ten);}
    Vec high=vblend(hi0,hi1,gamma);
    out[i]=vadd(low,high);
    vout[i]=vand(valid[i],seen[i+1]);
  }
  for(int i=len;i<N;++i){out[i]=zero;vout[i]=zero;}
}
static V repeat(const V&w,int n){V r;r.reserve(w.size()*n);for(int i=0;i<n;i++)r.insert(r.end(),w.begin(),w.end());return r;}
static V full_step(const V&p){V y;y.reserve(p.size()+1);int c=0;for(int x:p){int z=x+c;y.push_back(z%10);c=z/10;}if(c)y.push_back(c);V r(y.size());for(size_t i=0;i<y.size();++i)r[i]=y[i]+y[y.size()-1-i];return r;}
static V full_source(const V&J,const V&C,const V&U,int q,int k){V h=B;V w=repeat(W,q);h.insert(h.end(),w.begin(),w.end());h.insert(h.end(),J.begin(),J.end());V u=repeat(U,k);h.insert(h.end(),u.begin(),u.end());V p=h;p.insert(p.end(),C.begin(),C.end());for(auto it=h.rbegin();it!=h.rend();++it)p.push_back(*it);return p;}
static V targetprefix(){V x=B;V w=repeat(W,14);x.insert(x.end(),w.begin(),w.end());return x;}
static V decode(int code){V j(5);for(int i=4;i>=0;--i){j[i]=code%19;code/=19;}return j;}
static uint32_t active_bits(int count){return count==32?0xffffffffu:((1u<<count)-1u);}
static void init_batch(Batch& b,const V& U,int start,int count){
  uint32_t ab=active_bits(count);Vec active=_mm256_setr_epi8(
    (char)((ab>>0)&1? -1:0),(char)((ab>>1)&1? -1:0),(char)((ab>>2)&1? -1:0),(char)((ab>>3)&1? -1:0),
    (char)((ab>>4)&1? -1:0),(char)((ab>>5)&1? -1:0),(char)((ab>>6)&1? -1:0),(char)((ab>>7)&1? -1:0),
    (char)((ab>>8)&1? -1:0),(char)((ab>>9)&1? -1:0),(char)((ab>>10)&1? -1:0),(char)((ab>>11)&1? -1:0),
    (char)((ab>>12)&1? -1:0),(char)((ab>>13)&1? -1:0),(char)((ab>>14)&1? -1:0),(char)((ab>>15)&1? -1:0),
    (char)((ab>>16)&1? -1:0),(char)((ab>>17)&1? -1:0),(char)((ab>>18)&1? -1:0),(char)((ab>>19)&1? -1:0),
    (char)((ab>>20)&1? -1:0),(char)((ab>>21)&1? -1:0),(char)((ab>>22)&1? -1:0),(char)((ab>>23)&1? -1:0),
    (char)((ab>>24)&1? -1:0),(char)((ab>>25)&1? -1:0),(char)((ab>>26)&1? -1:0),(char)((ab>>27)&1? -1:0),
    (char)((ab>>28)&1? -1:0),(char)((ab>>29)&1? -1:0),(char)((ab>>30)&1? -1:0),(char)((ab>>31)&1? -1:0));
  int js[LANES][5]{};for(int l=0;l<count;++l)js[l][0]=0;
  for(int l=0;l<count;++l){int code=start+l;for(int i=4;i>=0;--i){js[l][i]=code%19;code/=19;}}
  Vec* p=b.p[0];Vec* valid=b.valid[0];
  for(int i=0;i<N;++i){
    if(i<34)p[i]=vset(B[i]);
    else if(i<CUT)p[i]=vset(W[(i-34)%9]);
    else if(i<CUT+5){int j=i-CUT; p[i]=_mm256_setr_epi8(
      (char)js[0][j],(char)js[1][j],(char)js[2][j],(char)js[3][j],(char)js[4][j],(char)js[5][j],(char)js[6][j],(char)js[7][j],
      (char)js[8][j],(char)js[9][j],(char)js[10][j],(char)js[11][j],(char)js[12][j],(char)js[13][j],(char)js[14][j],(char)js[15][j],
      (char)js[16][j],(char)js[17][j],(char)js[18][j],(char)js[19][j],(char)js[20][j],(char)js[21][j],(char)js[22][j],(char)js[23][j],
      (char)js[24][j],(char)js[25][j],(char)js[26][j],(char)js[27][j],(char)js[28][j],(char)js[29][j],(char)js[30][j],(char)js[31][j]);}
    else p[i]=vset(U[(i-(CUT+5))%3]);
    valid[i]=active;
  }
}
struct Counts {uint64_t tested=0,clock_bad=0,unknown=0,valid_short=0,w9_mismatch=0,w9_same=0;uint64_t hist[160]={};uint64_t any_first_hist[160]={};int min_w=9999,max_w=-1,min_any=9999,max_any=-1;V minJ,maxJ;std::vector<int> survivors,short_codes,clock_codes;};
static void run_u(const V& U){
 Counts total;const V tgt=targetprefix();const int cut=CUT;const int nth=(TOTAL+LANES-1)/LANES;
 #ifdef _OPENMP
 omp_set_dynamic(0);
 #endif
 int nthreads=1;
 #ifdef _OPENMP
 nthreads=omp_get_max_threads();
 #endif
 std::vector<Counts> locals(nthreads);
 #pragma omp parallel
 {
  int tid=0;
  #ifdef _OPENMP
  tid=omp_get_thread_num();
  #endif
  Counts &c=locals[tid];Batch b;Vec wrong=vzero(),unknown=vzero();
  #pragma omp for schedule(dynamic,8)
  for(int batch=0;batch<nth;++batch){
    int start=batch*LANES,count=std::min(LANES,TOTAL-start);init_batch(b,U,start,count);Vec *p=b.p[0],*out=b.p[1],*valid=b.valid[0],*vout=b.valid[1];wrong=vzero();unknown=vzero();
    int len=N;for(int t=0;t<120;++t){Vec gamma;step(p,valid,out,vout,b.seen,b.carryhi,gamma,len);--len;Vec found=b.seen[0];unknown=vor(unknown,vandnot(found,_mm256_set1_epi8((char)-1)));Vec expect=vset((t%4==0)?-1:0);wrong=vor(wrong,_mm256_xor_si256(gamma,expect));std::swap(p,out);std::swap(valid,vout);}
    uint32_t ab=active_bits(count),badbits=bits(wrong)&ab,unkbits=bits(unknown)&ab;
    uint32_t validbits=bits(valid[CUT-1])&ab;uint32_t shortbits=ab&~validbits;
    c.clock_bad+=bitcount(badbits);c.unknown+=bitcount(unkbits);c.valid_short+=bitcount(shortbits);
    for(uint32_t z=badbits;z;z&=z-1){int l=firstbit(z);c.clock_codes.push_back(start+l);}
    for(uint32_t z=shortbits;z;z&=z-1){int l=firstbit(z);c.short_codes.push_back(start+l);}
    int firstW[LANES];int firstAny[LANES];for(int l=0;l<LANES;++l){firstW[l]=-1;firstAny[l]=-1;}
    uint32_t foundW=0,foundAny=0;
    for(int i=0;i<CUT;++i){
      Vec eq=vcmp_eq(p[i],vset(tgt[i]));Vec mm=vand(valid[i],vandnot(eq,_mm256_set1_epi8((char)-1)));uint32_t mb=bits(mm)&ab;
      uint32_t newany=mb&~foundAny;for(uint32_t z=newany;z;z&=z-1){int l=firstbit(z);firstAny[l]=i;}foundAny|=mb;
      if(i>=34){uint32_t neww=mb&~foundW;for(uint32_t z=neww;z;z&=z-1){int l=firstbit(z);firstW[l]=i;}foundW|=mb;}
    }
    for(int l=0;l<count;++l){
      ++c.tested;int code=start+l;V J=decode(code);
      if(firstW[l]>=0){++c.w9_mismatch;++c.hist[firstW[l]];if(firstW[l]<c.min_w){c.min_w=firstW[l];c.minJ=J;}if(firstW[l]>c.max_w){c.max_w=firstW[l];c.maxJ=J;}}
      else {++c.w9_same;c.survivors.push_back(code);}
      if(firstAny[l]>=0){++c.any_first_hist[firstAny[l]];c.min_any=std::min(c.min_any,firstAny[l]);c.max_any=std::max(c.max_any,firstAny[l]);}
    }
  }
 }
 for(const auto&x:locals){total.tested+=x.tested;total.clock_bad+=x.clock_bad;total.unknown+=x.unknown;total.valid_short+=x.valid_short;total.w9_mismatch+=x.w9_mismatch;total.w9_same+=x.w9_same;for(int i=0;i<160;++i){total.hist[i]+=x.hist[i];total.any_first_hist[i]+=x.any_first_hist[i];}if(x.min_w<total.min_w){total.min_w=x.min_w;total.minJ=x.minJ;}if(x.max_w>total.max_w){total.max_w=x.max_w;total.maxJ=x.maxJ;}if(x.min_any<total.min_any)total.min_any=x.min_any;if(x.max_any>total.max_any)total.max_any=x.max_any;total.survivors.insert(total.survivors.end(),x.survivors.begin(),x.survivors.end());total.short_codes.insert(total.short_codes.end(),x.short_codes.begin(),x.short_codes.end());total.clock_codes.insert(total.clock_codes.end(),x.clock_codes.begin(),x.clock_codes.end());}
 std::cout<<"U=";for(int x:U)std::cout<<x<<',';std::cout<<" tested="<<total.tested<<" expected="<<TOTAL<<" clock_bad="<<total.clock_bad<<" gamma_unknown="<<total.unknown<<" final_prefix_short_of_160="<<total.valid_short<<" W9_mismatch="<<total.w9_mismatch<<" W9_same_or_unresolved="<<total.w9_same<<" first_W_mismatch="<<total.min_w<<".."<<total.max_w<<" first_any_mismatch="<<total.min_any<<".."<<total.max_any<<"\n";
 std::cout<<"  minJ=";for(int x:total.minJ)std::cout<<x<<',';std::cout<<" maxJ=";for(int x:total.maxJ)std::cout<<x<<',';std::cout<<"\n  W_hist:";for(int i=0;i<160;++i)if(total.hist[i])std::cout<<' '<<i<<':'<<total.hist[i];std::cout<<"\n  any_hist:";for(int i=0;i<160;++i)if(total.any_first_hist[i])std::cout<<' '<<i<<':'<<total.any_first_hist[i];std::cout<<"\n";
 if(!total.survivors.empty()){std::cout<<"  W9_SAME_CODES";for(int x:total.survivors)std::cout<<' '<<x;std::cout<<"\n";}
 if(!total.short_codes.empty()){std::cout<<"  SHORT_CODES";for(int x:total.short_codes)std::cout<<' '<<x;std::cout<<"\n";}
 if(!total.clock_codes.empty()){std::cout<<"  CLOCK_BAD_CODES";for(int x:total.clock_codes)std::cout<<' '<<x;std::cout<<"\n";}
 if(total.tested!=TOTAL||total.clock_bad||total.unknown||total.valid_short||total.w9_mismatch!=(uint64_t)TOTAL||total.w9_same){std::cerr<<"CENSUS_INVARIANT_FAILED for U=";for(int x:U)std::cerr<<x<<',';std::cerr<<"\n";std::exit(4);}
}
static bool selftest(){
 const std::array<V,4> Cs={V{0,0},V{18,18},V{4,12,4},V{6,12,8,12,6}};
 for(const V&U:US)for(int caseNo=0;caseNo<32;++caseNo){int code=(caseNo*7919+13)%TOTAL;V J=decode(code);for(const V&C:Cs){
   Batch b;init_batch(b,U,code,1);Vec *p=b.p[0],*out=b.p[1],*valid=b.valid[0],*vout=b.valid[1];V full=full_source(J,C,U,14,100);bool clockok=true;
   int len=N;for(int t=0;t<120;++t){Vec gamma;step(p,valid,out,vout,b.seen,b.carryhi,gamma,len);--len;int gv=(bits(gamma)&1)?1:0;V next=full_step(full);int ga=(int)next.size()-(int)full.size();int expected=(t%4==0)?1:0;if(gv!=ga||gv!=expected)clockok=false;std::swap(p,out);std::swap(valid,vout);full=std::move(next);
     for(int i=0;i<N;++i)if(bits(valid[i])&1){if(i>=(int)full.size()||((unsigned char*)&p[i])[0]==255){std::cerr<<"SELFTEST internal failure\n";return false;} alignas(32) unsigned char bytes[32];_mm256_store_si256((Vec*)bytes,p[i]);if((int)bytes[0]!=full[i]){std::cerr<<"SELFTEST mismatch U=";for(int x:U)std::cerr<<x<<',';std::cerr<<" code="<<code<<" t="<<t<<" i="<<i<<" got="<<(int)bytes[0]<<" expected="<<full[i]<<"\n";return false;}}
   }
   if(!clockok){std::cerr<<"SELFTEST clock mismatch\n";return false;}
 }}
 std::cout<<"SELFTEST_PASS: SIMD carry/validity cone agrees coefficientwise with full pairword recurrence for 3 U x 32 J x 4 centres x 120 steps\n";return true;
}
int main(int argc,char**argv){if(argc>1&&std::string(argv[1])=="--selftest")return selftest()?0:1;for(const V&u:US)run_u(u);std::cout<<"Z11_BITPARALLEL_CENSUS_DONE\n";}
