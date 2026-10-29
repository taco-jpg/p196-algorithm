// Exact two-step coalescence: choose 5632 four-digit mirror pair symbols independently.
// C++17: g++ -O3 -std=c++17 multicolour_dipoles.cpp -o /tmp/x30multi
// /tmp/x30multi 8000 2 20000;  mode=0 first symbol,1 last symbol,2 seeded random symbols.
#include <bits/stdc++.h>
using namespace std;
using u32=uint32_t;using u64=uint64_t;const u64 RAD=1000000000ULL;
int rev4(int x){int r=0;for(int i=0;i<4;i++){r=10*r+x%10;x/=10;}return r;}
struct Pair {int u,v,k;};
vector<Pair> alphabet(){
 vector<Pair>a;
 for(int k=0;k<=1;k++)for(int U=1000;U<10000;U++){
  int vrev=11781+90*k-U;
  if(vrev<0||vrev>9999)continue;
  int V=rev4(vrev);
  if(rev4(V)!=vrev||V+rev4(U)!=11781+900*k||U/1000==V%10)continue;
  a.push_back({U,V,k});
 }return a;
}
string fmt4(int x){auto s=to_string(x);return string(4-s.size(),'0')+s;}
u32 shift(u32 &r){r^=r<<13;r^=r>>17;r^=r<<5;return r;}
string seed(int q,int mode,const vector<Pair>&al){
 vector<string>blocks(q,"5346");u32 r=0x0badf00d;
 for(int a=0;a<q/2;a++){
  const Pair &p=al[mode==0?0:mode==1?al.size()-1:shift(r)%al.size()];
  blocks[a]=fmt4(p.u);blocks[q-1-a]=fmt4(p.v);
 }
 string s;s.reserve(4*q);for(const auto&block:blocks)s+=block;return s;
}
string school(const string&s){
 int c=0,n=s.size();string z(n,'0');
 for(int i=n-1;i>=0;i--){int v=s[i]+s[n-1-i]-96+c;z[i]='0'+v%10;c=v/10;}
 if(c)z.insert(z.begin(),'1');return z;
}
vector<u32> parse(const string&s){
 vector<u32>a;
 for(int i=s.size();i>0;i-=9){
  int z=max(0,i-9);a.push_back(stoul(s.substr(z,i-z)));
 }
 while(a.size()>1&&a.back()==0)a.pop_back();return a;
}
string out(const vector<u32>&a){
 string s=to_string(a.back());
 for(int i=(int)a.size()-2;i>=0;i--){
  string z=to_string(a[i]);s+=string(9-z.size(),'0')+z;
 }return s;
}
void add(vector<u32>&a,const vector<u32>&b){
 u64 c=0;size_t n=max(a.size(),b.size());a.resize(n);
 for(size_t i=0;i<n;i++){
  u64 z=u64(a[i])+(i<b.size()?b[i]:0)+c;
  a[i]=z%RAD;c=z/RAD;
 }if(c)a.push_back(c);
}
u64 fnv(const string&s){
 u64 h=1469598103934665603ULL;
 for(unsigned char c:s){h^=c;h*=1099511628211ULL;}
 return h;
}
int main(int argc,char**argv){
 int q=argc>1?atoi(argv[1]):8000,mode=argc>2?atoi(argv[2]):2,
     T=argc>3?atoi(argv[3]):20000;
 if(q<2||mode<0||mode>2||T<2)return 1;
 auto al=alphabet();int k0=0,k1=0;
 for(auto p:al){k0+=p.k==0;k1+=p.k==1;}
 cout<<"alphabet_k0="<<k0<<" alphabet_k1="<<k1<<" total="<<al.size()<<"\n";
 if(al.size()!=5632||k0!=4096||k1!=1536)return 6;
 string x;for(int j=0;j<q;j++)x+="5346";
 string y=seed(q,mode,al);auto n=parse(y);int ov=0;
 cout<<"t,length,overflow,fnv64\n";
 for(int t=0;t<=T;t++){
  if(out(n)!=y){cerr<<"BIGINT DISAGREEMENT at "<<t<<"\n";return 2;}
  if(equal(y.begin(),y.begin()+y.size()/2,y.rbegin())){
   cerr<<"PAL t="<<t<<"\n";return 3;
  }
  if(t>=2&&y!=x){cerr<<"NO COALESCENCE t="<<t<<"\n";return 4;}
  if(t%1000==0||t<=2||t==T)
   cout<<t<<","<<y.size()<<","<<ov<<","<<hex<<setw(16)
       <<setfill('0')<<fnv(y)<<dec<<"\n";
  if(t==T)break;
  string rev(y.rbegin(),y.rend());add(n,parse(rev));
  string yy=school(y),xx=school(x);
  if(yy.size()>y.size())ov++;
  y.swap(yy);x.swap(xx);
 }
 cerr<<"PASS Q="<<q<<" mode="<<mode<<" complete states="<<T+1
     <<" end_length="<<y.size()<<" overflow="<<ov<<"\n";
 return 0;
}
