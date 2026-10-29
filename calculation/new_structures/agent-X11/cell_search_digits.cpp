// Independent exhaustive ordinary-decimal digit-array scan for X11's cell.
// Realizes each canonical source and applies fresh-buffer decimal n+reverse(n).
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <map>
#include <stdexcept>
#include <vector>
#include <omp.h>
using namespace std;
using V=vector<uint8_t>;
static const V B={10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5};
static const V W={5,18,4,8,1,15,4,0,5};
static const V U={9,10,8};
static void append(V&a,const V&b){a.insert(a.end(),b.begin(),b.end());}
static void repeat(V&a,const V&b,int n){for(int i=0;i<n;i++)append(a,b);}
static V rev(V a){reverse(a.begin(),a.end());return a;}
static V templ(const V&J,int q,int k,int clen){V h=B;repeat(h,W,q);append(h,J);repeat(h,U,k);V p=h;p.insert(p.end(),clen,0);append(p,rev(h));return p;}
static V realize(const V&p){V d(p.size());for(size_t i=0;i<p.size()/2;i++){int hi=min(9,int(p[i])),lo=int(p[i])-hi;if(lo<0||lo>9)throw runtime_error("unrealizable coefficient");d[i]=lo;d[p.size()-1-i]=hi;}if(p.size()%2)throw runtime_error("expected even pairword length");if(d.back()==0)throw runtime_error("noncanonical source");return d;}
static int step_digits(const V&d,V&out){out.resize(d.size());int carry=0;for(size_t i=0;i<d.size();++i){int z=int(d[i])+int(d[d.size()-1-i])+carry;out[i]=z%10;carry=z/10;}if(carry)out.push_back((uint8_t)carry);return int(out.size())-int(d.size());}
static V decode(uint64_t n,int len){V j(len);for(int i=0;i<len;i++){j[i]=n%19;n/=19;}return j;}
static int first_prefix_mismatch(const V&d,const V&target){for(size_t i=0;i<target.size();++i){if(i>=d.size())return int(i);int pair=int(d[i])+int(d[d.size()-1-i]);if(pair!=target[i])return int(i);}return -1;}
int main(int argc,char**argv){
 int q=14,k=100,clen=14;if(argc>1)q=stoi(argv[1]);if(argc>2)k=stoi(argv[2]);if(argc>3)clen=stoi(argv[3]);
 if(q!=14||k!=100||clen!=14){cerr<<"defined at T12 reference width q=14,k=100,C_len=14\n";return 2;}
 V target=B;repeat(target,W,q);const uint64_t n3=19ULL*19*19,n4=n3*19,total=n3+n4;uint64_t checked=0,clockok=0,returns=0;vector<map<int,uint64_t>>hists(omp_get_max_threads());
 #pragma omp parallel for schedule(dynamic,32) reduction(+:checked,clockok,returns)
 for(long long raw=0;raw<(long long)total;++raw){
  uint64_t idx=uint64_t(raw);int len=idx<n3?3:4;uint64_t local=idx<n3?idx:idx-n3;V J=decode(local,len);V p=templ(J,q,k,clen);V d=realize(p),out;bool clock=true;
  for(int t=0;t<120;++t){int g=step_digits(d,out);if(g!=(t%4==0))clock=false;d.swap(out);}
  ++checked;clockok+=clock;int mm=first_prefix_mismatch(d,target);hists[omp_get_thread_num()][mm]++;if(mm==-1)++returns;
 }
 cerr<<"ENGINE=digit-array U=9,10,8 q="<<q<<" k="<<k<<" C_len="<<clen<<" checked="<<checked<<" clock="<<clockok<<" prefix_returns="<<returns<<" domain="<<total<<"\n";
 map<int,uint64_t>hist;for(const auto&hm:hists)for(auto[m,n]:hm)hist[m]+=n;for(auto[m,n]:hist)cerr<<"first_mismatch="<<m<<" count="<<n<<"\n";
 return checked==total&&clockok==total&&returns==0?0:1;
}