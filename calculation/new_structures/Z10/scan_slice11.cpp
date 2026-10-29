#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <memory>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>
using namespace std;
using U64=uint64_t; static constexpr U64 ALL=~U64(0); static constexpr size_t FULL=2476099;
struct Planes { array<vector<U64>,5> b; explicit Planes(size_t n){for(auto&x:b)x.assign(n,0);} };
struct Cell { int v=0; shared_ptr<Planes> p; Cell()=default; explicit Cell(int x):v(x){if(x<0||x>18)throw runtime_error("bad coefficient");} explicit Cell(shared_ptr<Planes>x):p(move(x)){} bool constant()const{return !p;} };
struct Mask { bool c=true,v=false; shared_ptr<vector<U64>> p; static Mask con(bool x){Mask m;m.v=x;return m;} static Mask var(shared_ptr<vector<U64>>x){Mask m;m.c=false;m.p=move(x);return m;} };
struct Lattice{vector<int> gamma;vector<vector<int>>W,B;};
static U64 cb(const Cell&x,int b,size_t w){return x.p?x.p->b[b][w]:(((x.v>>b)&1)?ALL:0);}
static U64 mb(const Mask&x,size_t w){return x.c?(x.v?ALL:0):(*x.p)[w];}
static bool any(const vector<U64>&a){for(auto x:a)if(x)return true;return false;}
static size_t cnt(const vector<U64>&a){size_t n=0;for(auto x:a)n+=__builtin_popcountll(x);return n;}
static void mask_alive(vector<U64>&a,const Mask&m,bool expect){if(m.c){if(m.v!=expect)fill(a.begin(),a.end(),0);return;}for(size_t w=0;w<a.size();++w)a[w]&=expect?(*m.p)[w]:~(*m.p)[w];}
static pair<Cell,Mask> norm(const Cell&x,const Mask&carry,size_t words){
 if(x.constant()&&carry.c){int z=x.v+(carry.v?1:0);return {Cell(z%10),Mask::con(z>=10)};}
 auto y=make_shared<Planes>(words);shared_ptr<vector<U64>>g;
 if(x.p)g=make_shared<vector<U64>>(words,0);
 for(size_t w=0;w<words;++w){U64 x0=cb(x,0,w),x1=cb(x,1,w),x2=cb(x,2,w),x3=cb(x,3,w),x4=cb(x,4,w),c=mb(carry,w);
  U64 s0=x0^c,c1=x0&c; U64 s1=x1^c1,c2=x1&c1; U64 s2=x2^c2,c3=x2&c2; U64 s3=x3^c3,c4=x3&c3; U64 s4=x4^c4;
  U64 ge10=x4|(x3&(x2|x1)); U64 eq9=x3&~x2&~x1&x0; U64 gg=ge10|(c&eq9);
  U64 b2=gg&~s1,b3=b2&~s2; U64 y0=s0,y1=s1^gg,y2=s2^b2,y3=s3^gg^b3;
  U64 b4=(gg&~s3)|(b3&~s3)|(gg&b3); U64 y4=s4^b4;
  y->b[0][w]=y0;y->b[1][w]=y1;y->b[2][w]=y2;y->b[3][w]=y3;y->b[4][w]=y4;if(g)(*g)[w]=gg;
 }
 Mask gout;if(x.constant()){if(x.v==9)gout=carry;else gout=Mask::con(x.v>=10);}else gout=Mask::var(move(g));return {Cell(move(y)),move(gout)};
}
static Cell addc(const Cell&a,const Cell&b,size_t words){if(a.constant()&&b.constant())return Cell(a.v+b.v);auto s=make_shared<Planes>(words);for(size_t w=0;w<words;++w){U64 c=0;for(int bit=0;bit<5;++bit){U64 x=cb(a,bit,w),y=cb(b,bit,w);s->b[bit][w]=x^y^c;c=(x&y)|(x&c)|(y&c);}}return Cell(move(s));}
static Lattice load(const string&path){ifstream f(path);if(!f)throw runtime_error("cannot open lattice");int p,nb,m,base;f>>p>>nb>>m>>base;if(p!=12||nb!=34||m!=9||base!=10)throw runtime_error("bad lattice header");Lattice x;x.gamma.resize(12);for(int&v:x.gamma)f>>v;x.W.assign(12,vector<int>(9));for(int t=0;t<12;++t)for(int i=0;i<9;++i)f>>x.W[t][i];for(int t=0;t<12;++t)for(int i=0;i<9;++i){int d;f>>d;}x.B.assign(12,vector<int>(34));for(int t=0;t<12;++t)for(int i=0;i<34;++i)f>>x.B[t][i];if(!f)throw runtime_error("truncated lattice");return x;}
static array<int,5> decode(size_t i){array<int,5>d{};for(int j=4;j>=0;--j){d[j]=int(i%19);i/=19;}return d;}
static array<shared_ptr<Planes>,5> jplanes(size_t n,size_t words){array<shared_ptr<Planes>,5>jp;for(auto&p:jp)p=make_shared<Planes>(words);for(size_t i=0;i<n;++i){auto d=decode(i);size_t w=i/64;U64 bit=U64(1)<<(i%64);for(int j=0;j<5;++j)for(int b=0;b<5;++b)if((d[j]>>b)&1)jp[j]->b[b][w]|=bit;}return jp;}
static vector<Cell> templ(const vector<int>&B,const vector<int>&W,const vector<int>&U,const array<shared_ptr<Planes>,5>&jp,int q,int k){vector<Cell>h;h.reserve(B.size()+W.size()*q+5+U.size()*k);for(int x:B)h.emplace_back(x);for(int r=0;r<q;++r)for(int x:W)h.emplace_back(x);for(int j=0;j<5;++j)h.emplace_back(Cell(jp[j]));for(int r=0;r<k;++r)for(int x:U)h.emplace_back(x);vector<Cell>P;P.reserve(2*h.size()+1);for(auto&x:h)P.push_back(x);P.emplace_back(2);for(auto it=h.rbegin();it!=h.rend();++it)P.push_back(*it);return P;}
static void step(vector<Cell>&P,vector<U64>&alive,size_t words,bool ov){vector<Cell>D;D.reserve(P.size()+1);Mask c=Mask::con(false);for(auto&x:P){auto z=norm(x,c,words);D.push_back(move(z.first));c=move(z.second);}mask_alive(alive,c,ov);size_t n=P.size()+(ov?1:0);if(ov)D.emplace_back(1);vector<Cell>N(n);for(size_t i=0;i<(n+1)/2;++i){Cell z=addc(D[i],D[n-1-i],words);N[i]=z;N[n-1-i]=z;}P=move(N);}
static size_t mismatch_mask(const Cell&x,int want,const vector<U64>&alive,size_t words){size_t n=0;for(size_t w=0;w<words;++w){U64 eq=ALL;for(int b=0;b<5;++b)eq&=((want>>b)&1)?cb(x,b,w):~cb(x,b,w);n+=__builtin_popcountll(alive[w]&~eq);}return n;}
static string js(array<int,5>d){ostringstream o;for(int i=0;i<5;++i){if(i)o<<',';o<<d[i];}return o.str();}
int main(int argc,char**argv)try{string path="calculation/new_structures/Z10/input_lat_p12m9.txt";int q=14,k=100;size_t lim=FULL;for(int i=1;i<argc;++i){string a=argv[i];if(a=="--lattice"&&i+1<argc)path=argv[++i];else if(a=="--q"&&i+1<argc)q=stoi(argv[++i]);else if(a=="--k"&&i+1<argc)k=stoi(argv[++i]);else if(a=="--limit"&&i+1<argc)lim=stoull(argv[++i]);else throw runtime_error("bad argument");}Lattice L=load(path);if(q<14||k<100)throw runtime_error("reference width requires q>=14,k>=100");lim=min(lim,FULL);size_t words=(lim+63)/64;vector<U64>base(words,ALL);if(lim%64)base.back()=(U64(1)<<(lim%64))-1;
 vector<array<int,3>>Uall={{0,9,18},{0,18,9},{2,9,16},{2,16,9},{4,9,14},{4,14,9},{6,9,12},{6,12,9},{8,9,10},{8,10,9},{9,0,18},{9,2,16},{9,4,14},{9,6,12},{9,8,10},{9,10,8},{9,12,6},{9,14,4},{9,16,2},{9,18,0},{10,8,9},{10,9,8},{12,6,9},{12,9,6},{14,4,9},{14,9,4},{16,2,9},{16,9,2},{18,0,9},{18,9,0}};
 vector<int>chosen={11,23};cout<<"SPACE "<<FULL<<" explored_per_U "<<lim<<" fraction "<<double(lim)/FULL<<" q="<<q<<" k="<<k<<" C=[2]\n";
 for(int rank:chosen){auto U=Uall[rank-1];auto jp=jplanes(lim,words);vector<Cell>P=templ(L.B[0],L.W[0],vector<int>(U.begin(),U.end()),jp,q,k);vector<U64>alive=base;for(int t=0;t<120;++t)step(P,alive,words,L.gamma[t%12]!=0);size_t clocks=cnt(alive),pref=L.B[0].size()+q*L.W[0].size();map<long long,size_t>hist;map<long long,size_t>ex;
  for(size_t i=0;i<pref&&any(alive);++i){int want=i<L.B[0].size()?L.B[0][i]:L.W[0][(i-L.B[0].size())%9];if(P[i].constant()){if(P[i].v!=want){long long off=(long long)i-(long long)pref;hist[off]+=cnt(alive);for(size_t w=0;w<words;++w)if(alive[w]){ex.emplace(off,w*64+__builtin_ctzll(alive[w]));break;}fill(alive.begin(),alive.end(),0);}}else{size_t fail=0,first=lim;for(size_t w=0;w<words;++w){U64 eq=ALL;for(int b=0;b<5;++b)eq&=((want>>b)&1)?P[i].p->b[b][w]:~P[i].p->b[b][w];U64 bad=alive[w]&~eq;fail+=__builtin_popcountll(bad);if(bad&&first==lim)first=w*64+__builtin_ctzll(bad);alive[w]&=eq;}if(fail){long long off=(long long)i-(long long)pref;hist[off]+=fail;ex.emplace(off,first);}}}
  size_t survivors=cnt(alive),tot=0;for(auto&x:hist)tot+=x.second;if(tot!=clocks-survivors)throw runtime_error("histogram does not partition candidate set");cout<<"U_RANK "<<rank<<" U="<<U[0]<<","<<U[1]<<","<<U[2]<<" clock_survivors="<<clocks<<" W9_prefix_survivors="<<survivors<<" mismatch_hist_total="<<tot<<" first_mismatch_from_cut=";bool first=true;for(auto&x:hist){if(!first)cout<<',';first=false;cout<<x.first<<':'<<x.second;}cout<<" examples=";first=true;for(auto&x:ex){if(!first)cout<<',';first=false;cout<<x.first<<'@'<<x.second<<"["<<js(decode(x.second))<<"]";}cout<<"\n";
 }
 return 0;}catch(const exception&e){cerr<<"ERROR: "<<e.what()<<"\n";return 2;}
