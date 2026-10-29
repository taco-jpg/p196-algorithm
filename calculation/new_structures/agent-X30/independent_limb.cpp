// Agent X30: base-1e9 arbitrary-precision arithmetic and a separate decimal
// schoolbook implementation, cross-checked on every state (not checkpoints).
// Run: g++ -O3 -std=c++17 independent_limb.cpp -o limbs; ./limbs 12000 4000 1 1 20000
#include <bits/stdc++.h>
using namespace std;
using u32=uint32_t;using u64=uint64_t;
const u64 RAD=1000000000ULL;
string seed(int Q,int at,int span,int kind){
 string s;s.reserve(4*Q);
 for(int k=0;k<Q;k++){
  string w="5346";
  if(k>=at&&k<at+span)
   w=kind==1?"3465":kind==2?"4653":kind==3?"6534":"5345";
  s+=w;
 }return s;
}
vector<u32> parse(const string&s){
 vector<u32>a;
 for(int i=(int)s.size();i>0;i-=9){
  int z=max(0,i-9);a.push_back(stoul(s.substr(z,i-z)));
 }
 while(a.size()>1&&a.back()==0)a.pop_back();
 return a;
}
string format(const vector<u32>&a){
 string s=to_string(a.back());
 for(int i=(int)a.size()-2;i>=0;i--){
  string w=to_string(a[i]);s.append(9-w.size(),'0');s+=w;
 }return s;
}
void add(vector<u32>&a,const vector<u32>&b){
 u64 c=0;size_t n=max(a.size(),b.size());a.resize(n,0);
 for(size_t i=0;i<n;i++){
  u64 z=u64(a[i])+(i<b.size()?b[i]:0)+c;
  a[i]=u32(z%RAD);c=z/RAD;
 }
 if(c)a.push_back(c);
}
string decimal_step(const string&s){
 int c=0,n=s.size();string out(n,'0');
 for(int i=n-1;i>=0;i--){
  int z=s[i]-'0'+s[n-1-i]-'0'+c;
  out[i]=char('0'+z%10);c=z/10;
 }
 if(c)out.insert(out.begin(),'1');
 return out;
}
int pair_p4(const string&s){
 int n=s.size(),r=0,best=0;
 for(int i=0;i<n/2;i++){
  int z=s[n-1-i]+s[i];
  r=(i>=4&&z==s[n-1-i+4]+s[i-4])?r+1:1;
  best=max(best,r);
 }return best;
}
u64 hash64(const string&s){
 u64 h=1469598103934665603ULL;
 for(char c:s){h^=(unsigned char)c;h*=1099511628211ULL;}
 return h;
}
int main(int argc,char**argv){
 int q=argc>1?atoi(argv[1]):12000,at=argc>2?atoi(argv[2]):4000,
     span=argc>3?atoi(argv[3]):1,kind=argc>4?atoi(argv[4]):1,
     T=argc>5?atoi(argv[5]):20000;
 if(q<=0||at<0||span<=0||at+span>q||kind<1||kind>4||T<0)return 1;
 string s=seed(q,at,span,kind);
 auto a=parse(s);
 int minrun=INT_MAX,tmin=-1,over=0;
 cout<<"t,digits,overflow,min_p4_so_far,fnv64_decimal_msb\n";
 for(int t=0;t<=T;t++){
  if(s!=format(a)){cerr<<"ERROR independent engines differ t="<<t<<"\n";return 2;}
  if(equal(s.begin(),s.begin()+s.size()/2,s.rbegin())){
   cerr<<"PALINDROME t="<<t<<"\n";return 3;
  }
  int r=pair_p4(s);
  if(r<minrun){minrun=r;tmin=t;}
  if(t%1000==0||t==T)
   cout<<t<<","<<s.size()<<","<<over<<","<<minrun<<","
       <<hex<<setw(16)<<setfill('0')<<hash64(s)<<dec<<"\n";
  if(t==T)break;
  string rev(s.rbegin(),s.rend());
  auto b=parse(rev);add(a,b);
  string next=decimal_step(s);
  if(next.size()>s.size())over++;
  s.swap(next);
 }
 cerr<<"PASS final_digits="<<s.size()<<" overflows="<<over
     <<" min_pair_p4_run="<<minrun<<" min_at="<<tmin
     <<" full_state_equivalence="<<T+1<<"\n";
 return 0;
}
