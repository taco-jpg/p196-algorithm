#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
using U64=uint64_t;
// Bit-sliced specialization of R30's exact folded-pairword transition. The T12
// protected cut lets us retain only the last 12 W9 copies, J, and a guarded U3 collar.
static constexpr int JLEN=5, LEFT_W=108, UC=180, M=LEFT_W+JLEN+UC;
static constexpr uint64_t NJ=19ULL*19*19*19*19;
static_assert(NJ==2476099ULL);
static_assert(UC%3==0); // align the far-side carry seed to a U3 word boundary
struct Lattice { array<int,12> g{}; array<array<int,9>,12> W{}; array<array<int,34>,12> B{}; };
Lattice load(const string& path){ifstream f(path);if(!f)throw runtime_error("lattice missing");int p,nb,m,b;f>>p>>nb>>m>>b;if(p!=12||nb!=34||m!=9||b!=10)throw runtime_error("bad lattice header");Lattice x;for(int&z:x.g)f>>z;for(auto&row:x.W)for(int&z:row)f>>z;for(int t=0;t<12;t++)for(int i=0;i<9;i++){int z;f>>z;}for(auto&row:x.B)for(int&z:row)f>>z;if(!f)throw runtime_error("truncated lattice");return x;}
vector<array<int,3>> allU(){vector<array<int,3>> v;for(int a=0;a<=18;a+=2){array<int,3>b{9,a,18-a};for(int r=0;r<3;r++)v.push_back({b[r],b[(r+1)%3],b[(r+2)%3]});}sort(v.begin(),v.end());v.erase(unique(v.begin(),v.end()),v.end());if(v.size()!=30)throw runtime_error("U count !=30");return v;}
array<int,3> bulkStep(array<int,3>w,int g){int a[4]{},b[4]{};bool ok=false;for(int s=0;s<=1&&!ok;s++){a[0]=s;for(int i=0;i<3;i++)a[i+1]=(w[i]+a[i])/10;ok=a[3]==s;}if(!ok)throw runtime_error("no low cyclic carry");ok=false;for(int s=0;s<=1&&!ok;s++){b[3]=s;for(int i=2;i>=0;i--)b[i]=(w[i]+b[i+1])/10;ok=b[0]==s;}if(!ok)throw runtime_error("no high cyclic carry");array<int,3> z{};for(int i=0;i<3;i++){int lo=(w[i]+a[i])%10;int hi=g?((w[(i+2)%3]+b[i])%10):((w[i]+b[i+1])%10);z[i]=lo+hi;}return z;}
struct Planes{int m;size_t nw;vector<U64>a;Planes(int M_,size_t nw_):m(M_),nw(nw_),a((size_t)5*M_*nw_){} U64* p(int bit,int i){return a.data()+((size_t)bit*m+i)*nw;} const U64* p(int bit,int i)const{return a.data()+((size_t)bit*m+i)*nw;} void clear(){fill(a.begin(),a.end(),0);} };
struct Low{int m;size_t nw;vector<U64>a;Low(int M_,size_t nw_):m(M_),nw(nw_),a((size_t)4*M_*nw_){} U64* p(int bit,int i){return a.data()+((size_t)bit*m+i)*nw;} const U64* p(int bit,int i)const{return a.data()+((size_t)bit*m+i)*nw;} };
inline void digit(U64 b0,U64 b1,U64 b2,U64 b3,U64 b4,U64 c,U64&d0,U64&d1,U64&d2,U64&d3,U64&co){U64 s0=b0^c,c1=b0&c;U64 s1=b1^c1,c2=b1&c1;U64 s2=b2^c2,c3=b2&c2;U64 s3=b3^c3,c4=b3&c3;U64 s4=b4^c4;co=s4|(s3&(s2|s1));U64 br1=co&~s1,br2=br1&~s2;d0=s0;d1=s1^co;d2=s2^br1;d3=s3^co^br2;}
inline U64 carryOnly(U64 b0,U64 b1,U64 b2,U64 b3,U64 b4,U64 c){U64 c1=b0&c;U64 s1=b1^c1,c2=b1&c1;U64 s2=b2^c2,c3=b2&c2;U64 s3=b3^c3,c4=b3&c3;U64 s4=b4^c4;return s4|(s3&(s2|s1));}
inline U64 maj(U64 a,U64 b,U64 c){return (a&b)|(a&c)|(b&c);}
inline void sumDigits(U64 l0,U64 l1,U64 l2,U64 l3,U64 h0,U64 h1,U64 h2,U64 h3,U64&y0,U64&y1,U64&y2,U64&y3,U64&y4){y0=l0^h0;U64 c1=l0&h0;y1=l1^h1^c1;U64 c2=maj(l1,h1,c1);y2=l2^h2^c2;U64 c3=maj(l2,h2,c2);y3=l3^h3^c3;U64 c4=maj(l3,h3,c3);y4=c4;}
uint64_t maskFor(size_t w,size_t nw,size_t count){if(w+1<nw)return ~U64(0);size_t rem=count%64;return rem?((U64(1)<<rem)-1):~U64(0);}
void initFixed(Planes& h,int pos,int x,const vector<U64>&valid){for(int b=0;b<5;b++){U64* dst=h.p(b,pos);if((x>>b)&1)copy(valid.begin(),valid.end(),dst);else fill(dst,dst+h.nw,0);}}
void initAll(const Lattice& lat,const array<int,3>&U,const vector<U64>&jm,Planes& h,const vector<U64>&valid){h.clear();size_t nw=h.nw;for(int i=0;i<M;i++){if(i<LEFT_W){int x=lat.W[0][i%9];initFixed(h,i,x,valid);}else if(i<LEFT_W+JLEN){int j=i-LEFT_W;for(int b=0;b<5;b++)copy(jm.begin()+((size_t)b*JLEN+j)*nw,jm.begin()+((size_t)b*JLEN+j+1)*nw,h.p(b,i));}else{int x=U[(i-LEFT_W-JLEN)%3];initFixed(h,i,x,valid);}}}
vector<U64> makeJMasks(size_t start,size_t count,size_t nw,const vector<U64>&valid){vector<U64> jm((size_t)5*JLEN*nw,0);for(size_t w=0;w<nw;w++){array<array<U64,5>,JLEN> m{};for(int bit=0;bit<64;bit++){size_t idx=start+w*64+bit;if(idx>=start+count)break;size_t z=idx;for(int j=0;j<JLEN;j++){int d=z%19;z/=19;for(int p=0;p<5;p++)if((d>>p)&1)m[j][p]|=U64(1)<<bit;}}for(int j=0;j<JLEN;j++)for(int p=0;p<5;p++)jm[((size_t)p*JLEN+j)*nw+w]=m[j][p]&valid[w];}return jm;}
vector<int> decodeJ(size_t id){vector<int> j(JLEN);for(int i=0;i<JLEN;i++){j[i]=id%19;id/=19;}return j;}
void scalarStep(const vector<int>&H,int g,int lowIn,int prev,int seed,vector<int>&out){int n=H.size();vector<int>lo(n),hi(n);int c=lowIn;for(int i=0;i<n;i++){int z=H[i]+c;lo[i]=z%10;c=z/10;}int state=seed;for(int i=n-1;i>=0;i--){if(!g){hi[i]=(H[i]+state)%10;state=(H[i]+state)/10;}else{state=(H[i]+state)/10;int x=i?H[i-1]:prev;hi[i]=(x+state)%10;}}out.resize(n);for(int i=0;i<n;i++)out[i]=lo[i]+hi[i];}
int getLane(const Planes&h,int pos,size_t word,int bit){int x=0;for(int p=0;p<5;p++)if((h.p(p,pos)[word]>>bit)&1)x|=1<<p;return x;}
int main(int argc,char**argv){string latticePath="calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt",outPath="calculation/new_structures/Z03/census_range.tsv";size_t chunkSize=32768,jStart=0,jLimit=NJ;int onlyRank=0;bool selftest=true;for(int i=1;i<argc;i++){string a=argv[i];if(a=="--lattice"&&i+1<argc)latticePath=argv[++i];else if(a=="--out"&&i+1<argc)outPath=argv[++i];else if(a=="--chunk"&&i+1<argc)chunkSize=stoull(argv[++i]);else if(a=="--j-start"&&i+1<argc)jStart=stoull(argv[++i]);else if(a=="--j-limit"&&i+1<argc)jLimit=stoull(argv[++i]);else if(a=="--u-rank"&&i+1<argc)onlyRank=stoi(argv[++i]);else if(a=="--no-selftest")selftest=false;else throw runtime_error("bad arg: "+a);}if(chunkSize==0||jStart>jLimit||jLimit>NJ)throw runtime_error("invalid range/chunk");if(onlyRank && onlyRank!=3 && onlyRank!=15 && onlyRank!=27)throw runtime_error("--u-rank must be 3, 15, 27, or omitted");Lattice lat=load(latticePath);auto Us=allU();if(Us[2]!=array<int,3>{2,9,16}||Us[14]!=array<int,3>{9,8,10}||Us[26]!=array<int,3>{16,2,9})throw runtime_error("lexicographic U slice mismatch");array<int,12> lowIn{},prev{};for(int ph=0;ph<12;ph++){int c=0;for(int x:lat.B[ph])c=(x+c)/10;for(int i=0;i<18;i++)c=(lat.W[ph][i%9]+c)/10;lowIn[ph]=c;prev[ph]=lat.W[ph][8];}
vector<array<array<int,3>,121>> ur(Us.size());for(size_t ui=0;ui<Us.size();ui++){ur[ui][0]=Us[ui];for(int t=0;t<120;t++)ur[ui][t+1]=bulkStep(ur[ui][t],lat.g[t%12]);if(ur[ui][120]!=Us[ui])throw runtime_error("U not periodic after 120");}
ofstream out(outPath);if(!out)throw runtime_error("cannot open output");out<<"# Z03 phase0 Jlen5 bit-parallel endpoint W9 census; N="<<NJ<<"; range=["<<jStart<<","<<min(NJ,jLimit)<<"); chunk="<<chunkSize<<"; M="<<M<<"\n";
for(size_t ui=0;ui<Us.size();ui++){if(ui!=2 && ui!=14 && ui!=26)continue; if(onlyRank && onlyRank!=(int)ui+1)continue; // lex ranks 3,15,27 only
 const auto U=Us[ui];array<uint64_t,109> firstHist{};uint64_t total=0,endpoint=0,strict=0;vector<size_t> survivors;survivors.reserve(1000);array<size_t,8> sampleIds={0,1,2,19,361,123456,987654,(size_t)NJ-1};
 for(size_t start=jStart;start<min(NJ,jLimit);start+=chunkSize){if((start-jStart)% (chunkSize*10)==0)cerr<<"PROGRESS U rank "<<(ui+1)<<" start="<<start<<"\n";size_t count=min(chunkSize,min(NJ,jLimit)-start),nw=(count+63)/64;vector<U64> valid(nw);for(size_t w=0;w<nw;w++)valid[w]=maskFor(w,nw,count);auto jm=makeJMasks(start,count,nw,valid);Planes cur(M,nw),nxt(M,nw);Low lows(M,nw);initAll(lat,U,jm,cur,valid);vector<U64> carry(nw),state(nw),strictAlive=valid,active=valid;
 vector<pair<size_t,vector<int>>> scalar;
 if(selftest){for(size_t sid:sampleIds)if(sid>=start&&sid<start+count){size_t rel=sid-start,word=rel/64;int bit=rel%64;vector<int> h(M);for(int i=0;i<M;i++)h[i]=getLane(cur,i,word,bit);scalar.push_back({sid,h});}}
 for(int t=0;t<120;t++){int ph=t%12,g=lat.g[ph];auto urow=ur[ui][t];int seed=0;bool found=false;for(int z:urow){if(z!=9){seed=(z>=10);found=true;break;}}if(!found)throw runtime_error("all-nine U row");
  fill(carry.begin(),carry.end(),0);if(lowIn[ph])carry=valid;
  for(int i=0;i<M;i++){U64*b0=cur.p(0,i),*b1=cur.p(1,i),*b2=cur.p(2,i),*b3=cur.p(3,i),*b4=cur.p(4,i);U64*l0=lows.p(0,i),*l1=lows.p(1,i),*l2=lows.p(2,i),*l3=lows.p(3,i);for(size_t w=0;w<nw;w++){U64 d0,d1,d2,d3,co;digit(b0[w],b1[w],b2[w],b3[w],b4[w],carry[w],d0,d1,d2,d3,co);l0[w]=d0;l1[w]=d1;l2[w]=d2;l3[w]=d3;carry[w]=co;}}
  if(seed)state=valid;else fill(state.begin(),state.end(),0);
  for(int i=M-1;i>=0;i--){U64*b0=cur.p(0,i),*b1=cur.p(1,i),*b2=cur.p(2,i),*b3=cur.p(3,i),*b4=cur.p(4,i);for(size_t w=0;w<nw;w++){U64 d0,d1,d2,d3,co; if(!g){digit(b0[w],b1[w],b2[w],b3[w],b4[w],state[w],d0,d1,d2,d3,co);state[w]=co;
      U64 l0=lows.p(0,i)[w],l1=lows.p(1,i)[w],l2=lows.p(2,i)[w],l3=lows.p(3,i)[w],y0,y1,y2,y3,y4;sumDigits(l0,l1,l2,l3,d0,d1,d2,d3,y0,y1,y2,y3,y4);nxt.p(0,i)[w]=y0;nxt.p(1,i)[w]=y1;nxt.p(2,i)[w]=y2;nxt.p(3,i)[w]=y3;nxt.p(4,i)[w]=y4;
    }else{U64 cnew=carryOnly(b0[w],b1[w],b2[w],b3[w],b4[w],state[w]);state[w]=cnew;U64 x0,x1,x2,x3,x4;if(i>0){x0=cur.p(0,i-1)[w];x1=cur.p(1,i-1)[w];x2=cur.p(2,i-1)[w];x3=cur.p(3,i-1)[w];x4=cur.p(4,i-1)[w];}else{x0=(prev[ph]&1)?valid[w]:0;x1=(prev[ph]&2)?valid[w]:0;x2=(prev[ph]&4)?valid[w]:0;x3=(prev[ph]&8)?valid[w]:0;x4=(prev[ph]&16)?valid[w]:0;}digit(x0,x1,x2,x3,x4,state[w],d0,d1,d2,d3,co);U64 l0=lows.p(0,i)[w],l1=lows.p(1,i)[w],l2=lows.p(2,i)[w],l3=lows.p(3,i)[w],y0,y1,y2,y3,y4;sumDigits(l0,l1,l2,l3,d0,d1,d2,d3,y0,y1,y2,y3,y4);nxt.p(0,i)[w]=y0;nxt.p(1,i)[w]=y1;nxt.p(2,i)[w]=y2;nxt.p(3,i)[w]=y3;nxt.p(4,i)[w]=y4;}}}
  // Strict-per-phase lane: retain candidates whose complete protected W9 suffix agrees at every phase.
  int nph=(ph+1)%12;for(int i=0;i<LEFT_W;i++){int ex=lat.W[nph][i%9];for(size_t w=0;w<nw;w++){U64 same=valid[w];for(int p=0;p<5;p++){U64 bits=nxt.p(p,i)[w];same &= ((ex>>p)&1)?bits:~bits;}strictAlive[w]&=same;}}
  // Validate selected lanes against an independent scalar local recurrence at every phase.
  if(selftest&&!scalar.empty()){for(auto&sv:scalar){size_t rel=sv.first-start,word=rel/64;int bit=rel%64;vector<int> expected;scalarStep(sv.second,g,lowIn[ph],prev[ph],seed,expected);for(int i=0;i<M;i++){int got=getLane(nxt,i,word,bit);if(got!=expected[i]){cerr<<"BITSLICE_SCALAR_MISMATCH U-rank="<<(ui+1)<<" id="<<sv.first<<" t="<<t<<" i="<<i<<" got="<<got<<" expected="<<expected[i]<<"\n";return 3;}}sv.second.swap(expected);}}
  cur.a.swap(nxt.a);
 }
 // Final endpoint mismatch histogram over W segment (global positions 52..159).
 for(int i=0;i<LEFT_W;i++){int ex=lat.W[0][i%9];for(size_t w=0;w<nw;w++){U64 same=valid[w];for(int p=0;p<5;p++){U64 bits=cur.p(p,i)[w];same &= ((ex>>p)&1)?bits:~bits;}U64 mismatch=active[w]&~same;uint64_t n=popcount(mismatch);if(n)firstHist[i]+=n;active[w]&=same;}}
 // active is cleared at each earlier mismatch, so this is the first-mismatch histogram.
 for(size_t w=0;w<nw;w++){endpoint+=popcount(active[w]);strict+=popcount(strictAlive[w]);}
 for(size_t w=0;w<nw;w++){U64 bits=active[w];while(bits){int b=countr_zero(bits);size_t id=start+w*64+b;if(id<NJ && survivors.size()<1000)survivors.push_back(id);bits&=bits-1;}}
 total+=count;
 }
 out<<"U_RANK="<<(ui+1)<<" U="<<U[0]<<","<<U[1]<<","<<U[2]<<" range=["<<jStart<<","<<min(NJ,jLimit)<<") total="<<total<<" endpoint_W9="<<endpoint<<" strict_W9="<<strict<<"\n";
 uint64_t histSum=accumulate(firstHist.begin(),firstHist.begin()+LEFT_W,uint64_t(0));if(histSum+endpoint!=total)throw runtime_error("first-mismatch histogram does not partition the domain");if(strict>endpoint)throw runtime_error("strict lane not subset of endpoint lane");out<<"endpoint_first_mismatch_by_offset_from_W9_cut:";for(int i=0;i<LEFT_W;i++)out<<" "<<(i-LEFT_W)<<":"<<firstHist[i];out<<"\n";
 out<<"survivor_ids_first_1000:";for(auto id:survivors){auto j=decodeJ(id);out<<" "<<id<<"="<<j[0]<<","<<j[1]<<","<<j[2]<<","<<j[3]<<","<<j[4];}out<<"\n";out.flush();
 cerr<<"DONE U rank "<<(ui+1)<<" endpoint="<<endpoint<<" strict="<<strict<<" total="<<total<<"\n";
 }
 out<<"END\n";out.close();cout<<"DONE output="<<outPath<<" M="<<M<<" total per U="<<NJ<<"\n";
}
