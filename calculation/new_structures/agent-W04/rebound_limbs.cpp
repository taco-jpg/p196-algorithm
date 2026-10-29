// W04 independent big-integer engine: ordinary base-1e9 limbs plus decimal reversal.
// No digit-array addition and no symmetric-pairword transition is used.
#include <bits/stdc++.h>
using namespace std;
static constexpr uint64_t BASE=1000000000ULL;
struct Big{
 vector<uint32_t> limbs;
 explicit Big(const string&s){
  for(int i=(int)s.size();i>0;i-=9){uint32_t z=0;int j=max(0,i-9);for(;j<i;j++)z=z*10+(s[j]-'0');limbs.push_back(z);}
  while(limbs.size()>1&&!limbs.back())limbs.pop_back();
 }
 string str()const{
  string o=to_string(limbs.back());
  for(int i=(int)limbs.size()-2;i>=0;i--){string x=to_string(limbs[i]);o.append(9-x.size(),'0');o+=x;}
  return o;
 }
 void add(const Big&x){
  size_t k=max(limbs.size(),x.limbs.size());limbs.resize(k,0);
  uint64_t carry=0;
  for(size_t i=0;i<k;i++){
   uint64_t z=limbs[i]+carry+(i<x.limbs.size()?x.limbs[i]:0);
   limbs[i]=uint32_t(z%BASE);carry=z/BASE;
  }
  if(carry)limbs.push_back(uint32_t(carry));
 }
};
static string seed(int m,int n){
 vector<int>h{11,9,8,17};h.insert(h.end(),m,8);h.push_back(17);h.push_back(7);h.insert(h.end(),n,16);h.push_back(8);
 string upper,lower;for(int x:h){int q=min(9,x);upper.push_back(char('0'+q));lower.push_back(char('0'+x-q));}
 reverse(lower.begin(),lower.end());return upper+lower;
}
static bool bands(const string&s,int a,int b,int threshold,int&outA,int&outB){
 int half=(s.size()+1)/2;vector<int>B(half+1),suffix(half+1);outA=outB=0;
 auto p=[&](int i){return (s[i]-'0')+(s[s.size()-1-i]-'0');};
 for(int i=half-1;i>=0;i--){B[i]=p(i)==b?B[i+1]+1:0;suffix[i]=max(suffix[i+1],B[i]);}
 int run=0;
 for(int i=0;i<half;i++){
   run=p(i)==a?run+1:0;
   if(run>=threshold&&suffix[i+1]>=threshold){outA=max(outA,run);outB=max(outB,suffix[i+1]);}
 }
 return outA>=threshold&&outB>=threshold;
}
static uint64_t wordfnv(const string&s){uint64_t h=1469598103934665603ULL;for(char x:s){h^=uint8_t(x);h*=1099511628211ULL;}return h;}
int main(int argc,char**argv){
 if(argc!=5)return 1;
 int m=stoi(argv[1]),n=stoi(argv[2]),steps=stoi(argv[3]),threshold=stoi(argv[4]);
 Big N(seed(m,n));const int A[6]={8,16,14,10,2,4},B[6]={16,14,10,2,4,8};
 uint64_t trace=1469598103934665603ULL;int minA=INT_MAX,minB=INT_MAX;
 for(int t=0;t<=steps;t++){
  string s=N.str();if(s.front()=='0')return 7;
  if(equal(s.begin(),s.begin()+s.size()/2,s.rbegin())){cerr<<"PAL "<<t<<"\n";return 2;}
  int a=0,b=0;if(!bands(s,A[t%6],B[t%6],threshold,a,b)){cerr<<"BAND FAIL "<<t<<" "<<a<<" "<<b<<"\n";return 3;}
  minA=min(minA,a);minB=min(minB,b);
  for(uint64_t v:{uint64_t(t),uint64_t(s.size()),uint64_t(a),uint64_t(b)}){trace^=v;trace*=1099511628211ULL;}
  if(t%5000==0||t==steps)cout<<"CHECKPOINT "<<t<<" digits="<<s.size()<<" A="<<a<<" B="<<b<<" digest="<<hex<<trace<<" numeric_fnv="<<wordfnv(s)<<dec<<"\n"<<flush;
  if(t==steps)break;
  reverse(s.begin(),s.end());N.add(Big(s));
 }
 cout<<"LIMB_20000_PASS states="<<steps+1<<" m="<<m<<" n="<<n<<" minA="<<minA<<" minB="<<minB<<" digest="<<hex<<trace<<dec<<"\n";
}
