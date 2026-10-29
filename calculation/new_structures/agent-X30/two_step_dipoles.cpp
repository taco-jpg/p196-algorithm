// X30: independent base-1e9 and decimal digit arithmetic for all-mask
// two-step anti-mirror dipoles in a repeated 5346 decimal crystal.
// g++ -O3 -std=c++17 two_step_dipoles.cpp -o dipoles
// ./dipoles 8000 2 20000  # mode 0:none, 1:all, 2:PRNG subset, 3:one
#include <bits/stdc++.h>
using namespace std;
using u32=uint32_t;using u64=uint64_t;const u64 BASE=1000000000ULL;
vector<u32> parse(const string&s){
 vector<u32>a;for(int i=(int)s.size();i>0;i-=9){
  int j=max(0,i-9);a.push_back(stoul(s.substr(j,i-j)));
 }while(a.size()>1&&a.back()==0)a.pop_back();return a;
}
string fmt(const vector<u32>&a){
 string s=to_string(a.back());for(int i=(int)a.size()-2;i>=0;i--){
  string z=to_string(a[i]);s+=string(9-z.size(),'0')+z;
 }return s;
}
void add(vector<u32>&a,const vector<u32>&b){
 u64 c=0;size_t n=max(a.size(),b.size());a.resize(n);
 for(size_t i=0;i<n;i++){
  u64 s=u64(a[i])+(i<b.size()?b[i]:0)+c;
  a[i]=s%BASE;c=s/BASE;
 }if(c)a.push_back(c);
}
string step(const string&s){
 int n=s.size(),c=0;string z(n,'0');
 for(int i=n-1;i>=0;i--){
  int v=(s[i]-48)+(s[n-1-i]-48)+c;
  z[i]='0'+v%10;c=v/10;
 }if(c)z.insert(z.begin(),'1');return z;
}
u64 fnv(const string&s){
 u64 h=1469598103934665603ULL;
 for(char c:s){h^=(unsigned char)c;h*=1099511628211ULL;}
 return h;
}
string family(int q,int mode){
 vector<string>blocks(q,"5346");uint32_t r=0x1a2b3c4d;
 for(int a=0;a<q/2;a++){
  bool on=false;
  if(mode==1)on=true;
  if(mode==2){r^=r<<13;r^=r>>17;r^=r<<5;on=(r&1)!=0;}
  if(mode==3)on=(a==q/3);
  if(on){blocks[a]="2497";blocks[q-1-a]="4739";}
 }
 string s;s.reserve(4*q);for(const auto&b:blocks)s+=b;
 return s;
}
int main(int argc,char**argv){
 int q=argc>1?atoi(argv[1]):8000,mode=argc>2?atoi(argv[2]):2,
     T=argc>3?atoi(argv[3]):20000;
 if(q<2||mode<0||mode>3||T<2)return 1;
 string x;for(int j=0;j<q;j++)x+="5346";
 string y=family(q,mode);vector<u32>n=parse(y);int over=0;
 cout<<"t,length,overflows,fnv64_MSB\n";
 for(int t=0;t<=T;t++){
  if(fmt(n)!=y){cerr<<"BIGINT MISMATCH t="<<t<<"\n";return 2;}
  if(equal(y.begin(),y.begin()+y.size()/2,y.rbegin())){
   cerr<<"PALINDROME t="<<t<<"\n";return 3;
  }
  if(t==1&&mode!=0&&y==x){cerr<<"EARLY coalescence\n";return 4;}
  if(t>=2&&y!=x){cerr<<"NOT COALESCED t="<<t<<"\n";return 5;}
  if(t%1000==0||t<=2||t==T)
   cout<<t<<","<<y.size()<<","<<over<<","<<hex
       <<setw(16)<<setfill('0')<<fnv(y)<<dec<<"\n";
  if(t==T)break;
  string rev(y.rbegin(),y.rend());add(n,parse(rev));
  auto next=step(y),nextx=step(x);
  if(next.size()>y.size())over++;
  y.swap(next);x.swap(nextx);
 }
 cerr<<"PASS q="<<q<<" mode="<<mode<<" states="<<T+1
     <<" final_length="<<y.size()<<" overflow="<<over<<"\n";
 return 0;
}
