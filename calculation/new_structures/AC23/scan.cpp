// Agent AC23: unpruned, 64-lane exact decimal folded-pairword step engine.
// Scope: finite reference-width diagnostics, NOT an all-time certificate.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
using V=uint64_t;
struct B {V a[5];};
static B constant(int x){B r{};for(int j=0;j<5;j++)r.a[j]=(x&(1<<j))?~V(0):0;return r;}
static B add(const B &x,const B &y){B z;V c=0;for(int i=0;i<5;i++){z.a[i]=x.a[i]^y.a[i]^c;c=(x.a[i]&y.a[i])|(x.a[i]&c)|(y.a[i]&c);}return z;}
static B norm(const B &x,V carry,V &next){
    V z[5],c=carry;
    for(int i=0;i<5;i++){z[i]=x.a[i]^c;c=x.a[i]&c;}
    V ge=z[4]|(z[3]&(z[2]|z[1]));
    next=ge;
    // z-10 = z+22 modulo 32 when z>=10.
    B y{};
    y.a[0]=z[0];
    y.a[1]=z[1]^ge;
    V c2=z[1]&ge;
    y.a[2]=z[2]^ge^c2;
    V c3=(z[2]&ge)|(z[2]&c2)|(ge&c2);
    y.a[3]=z[3]^c3;
    V c4=z[3]&c3;
    y.a[4]=z[4]^ge^c4;
    return y;
}
static V eq(const B &x,int v){V m=~V(0);for(int i=0;i<5;i++)m &= (v&(1<<i))?x.a[i]:~x.a[i];return m;}
static void read_lat(const string &file, vector<vector<int>>&Bv,vector<vector<int>>&Wv,vector<int>&g){
    ifstream f(file);int p,n,m,base;f>>p>>n>>m>>base;if(!f||p!=12||n!=34||m!=9||base!=10)throw runtime_error("bad lattice header");
    g.resize(12);for(int &v:g)f>>v;
    Wv.resize(12,vector<int>(m));for(auto &r:Wv)for(int&v:r)f>>v;
    for(int t=0;t<12*m;t++){int z;f>>z;}
    Bv.resize(12,vector<int>(n));for(auto &r:Bv)for(int &v:r)f>>v;
    if(!f)throw runtime_error("truncated lattice");
}
static vector<array<int,3>> make_us(){vector<array<int,3>> u;for(int a=0;a<=18;a+=2){array<int,3>b={9,a,18-a};for(int t=0;t<3;t++)u.push_back({b[t%3],b[(t+1)%3],b[(t+2)%3]});}sort(u.begin(),u.end());return u;}
static array<int,5> decode(uint64_t code){array<int,5>j;for(int i=4;i>=0;i--){j[i]=code%19;code/=19;}return j;}
static B junction(int digit,uint64_t start){B r{};for(unsigned lane=0;lane<64;lane++){auto j=decode(start+lane);for(int bit=0;bit<5;bit++)if(j[digit]&(1<<bit))r.a[bit]|=V(1)<<lane;}return r;}
static vector<B> make(const vector<int>&b,const vector<int>&w,const array<int,3>&u,int q,int k,int clen,uint64_t start){
    vector<B> half;half.reserve(b.size()+9*q+5+3*k);
    for(int x:b)half.push_back(constant(x));
    for(int r=0;r<q;r++)for(int x:w)half.push_back(constant(x));
    for(int i=0;i<5;i++)half.push_back(junction(i,start));
    for(int r=0;r<k;r++)for(int x:u)half.push_back(constant(x));
    vector<B> p=half;
    if(clen==2){p.push_back(constant(4));p.push_back(constant(4));}
    else {p.push_back(constant(4));p.push_back(constant(14));p.push_back(constant(4));}
    for(int i=(int)half.size()-1;i>=0;i--)p.push_back(half[i]);
    return p;
}
static V step(vector<B>&p,vector<B>&digit,vector<B>&nxt,int gamma){
    const size_t n=p.size();digit.resize(n);V carry=0;
    for(size_t i=0;i<n;i++) digit[i]=norm(p[i],carry,carry);
    V endcarry=carry;
    if(gamma)digit.push_back(constant(1));
    const size_t m=digit.size();nxt.resize(m);
    for(size_t i=0;i<(m+1)/2;i++){B x=add(digit[i],digit[m-1-i]);nxt[i]=x;nxt[m-1-i]=x;}
    p.swap(nxt);return endcarry;
}
static int mismatch(const vector<B>&p,const vector<int>&b,const vector<int>&w,size_t lane,int cut){
    for(int i=0;i<cut;i++){int want=i<(int)b.size()?b[i]:w[(i-(int)b.size())%9];
       if(!(eq(p[i],want)&(V(1)<<lane)))return i;
    }return cut;
}
int main(int argc,char**argv){
 try{
    if(argc<3){cerr<<"usage: scan LAT FILE --phase 2 --u RANK|all --start N --count N --centre 2|3\n";return 2;}
    string lat=argv[1],out=argv[2];int phase=2,urank=-1,centre=2;uint64_t start=0,count=64;
    for(int i=3;i<argc;i++){
      string a=argv[i];if(i+1>=argc)throw runtime_error("missing arg");string v=argv[++i];
      if(a=="--phase")phase=stoi(v);else if(a=="--u")urank=(v=="all"?-1:stoi(v));
      else if(a=="--start")start=stoull(v);else if(a=="--count")count=stoull(v);
      else if(a=="--centre")centre=stoi(v);else throw runtime_error("unknown arg "+a);
    }
    if(phase<0||phase>=12||(centre!=2&&centre!=3)||start+count>2476099)throw runtime_error("invalid scope");
    vector<vector<int>>b,w;vector<int>g;read_lat(lat,b,w,g);
    vector<array<int,3>>us=make_us();
    ofstream f(out);if(!f)throw runtime_error("cannot write output");
    f<<"phase="<<phase<<" centre="<<centre<<" start="<<start<<" count="<<count<<"\n";
    for(int ui=0;ui<30;ui++){
      if(urank>=0&&ui!=urank)continue;
      map<int,uint64_t>hist;uint64_t clock_ok=0,prefix_ok=0;
      for(uint64_t code=start;code<start+count;code+=64){
        vector<B>p=make(b[phase],w[phase],us[ui],14,100,centre,code),digit,next;
        V live=~V(0);auto valid=min<uint64_t>(64,start+count-code);
        if(valid<64)live=(V(1)<<valid)-1;
        for(int t=0;t<120;t++){int gm=g[(phase+t)%12];V endcarry=step(p,digit,next,gm);live &= gm?endcarry:~endcarry;}
        clock_ok+=__builtin_popcountll(live);
        for(unsigned lane=0;lane<valid;lane++)if(live&(V(1)<<lane)){
          int m=mismatch(p,b[phase],w[phase],lane,34+9*14);hist[m]++;prefix_ok+=(m==160);
        }
      }
      f<<"U_RANK_1BASED="<<ui+1<<" U="<<us[ui][0]<<','<<us[ui][1]<<','<<us[ui][2]
       <<" CLOCK="<<clock_ok<<" PREFIX="<<prefix_ok<<" HIST";
      for(auto [i,n]:hist)f<<" "<<i<<":"<<n;
      f<<"\n";f.flush();
      cerr<<"U="<<ui+1<<" clock="<<clock_ok<<" prefix="<<prefix_ok<<" done\n";
    }
 }catch(exception&e){cerr<<e.what()<<"\n";return 2;}return 0;
}
