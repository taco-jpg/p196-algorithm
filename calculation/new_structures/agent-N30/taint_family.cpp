#include <bits/stdc++.h>
using namespace std;
static uint64_t rng=0x9a702f4ed37008c5ULL;
uint64_t xrand(){rng^=rng<<13;rng^=rng>>7;rng^=rng<<17;return rng;}
struct Norm {uint16_t digs;uint8_t carries;};
Norm norm(uint32_t p, uint8_t c){
  uint16_t ds=0;uint8_t cs=0;
  if(p==0) return {0,0};
  if(p==0x7ffff && c==3)return {0x3ff,3};
  while(p){int j=__builtin_ctz(p);p&=p-1;
    if(c&1){int z=j;ds|=1u<<(z%10);cs|=1u<<(z/10);}
    if(c&2){int z=j+1;ds|=1u<<(z%10);cs|=1u<<(z/10);}
  }
  return {ds,cs};
}
uint32_t pairmask(uint16_t a,uint16_t b){
 if(a==0x3ff && b==0x3ff)return 0x7ffff;
 uint32_t p=0;while(a){int i=__builtin_ctz(a);a&=a-1;p|=uint32_t(b)<<i;}return p;
}
int main(int argc,char**argv){
 int K=argc>1?atoi(argv[1]):5800;
 int T=argc>2?atoi(argv[2]):20000;
 int M=argc>3?atoi(argv[3]):37;
 char centre=argc>4?argv[4][0]:'3';
 if(K<1||T<1||M<1||centre<'0'||centre>'9')return 2;
 struct BigInt {
   vector<uint32_t> limbs;
   explicit BigInt(const string& s) {
     for(int end=(int)s.size();end>0;end-=9){
       int begin=max(0,end-9);
       limbs.push_back((uint32_t)stoul(s.substr(begin,end-begin)));
     }
     while(limbs.size()>1&&limbs.back()==0)limbs.pop_back();
   }
   string str()const{
     string ans=to_string(limbs.back());
     for(int i=(int)limbs.size()-2;i>=0;i--){
       string part=to_string(limbs[i]);ans+=string(9-part.size(),'0')+part;
     }
     return ans;
   }
   void add(const BigInt& rhs){
     size_t n=max(limbs.size(),rhs.limbs.size());limbs.resize(n,0);
     uint64_t c=0;
     for(size_t j=0;j<n;j++){
       uint64_t z=limbs[j]+c+(j<rhs.limbs.size()?rhs.limbs[j]:0);
       limbs[j]=z%1000000000U;c=z/1000000000U;
     }
     if(c)limbs.push_back((uint32_t)c);
   }
 };
 string seed;
 seed.reserve(2*K+M);
 vector<unsigned char> init_lo(K),init_hi(K);
 vector<uint16_t> lo(K),hi(K),nlo(K),nhi(K),lowdig(K),highdig(K);
 vector<uint32_t> pm(K);
 for(int j=0;j<K;j++){
  init_lo[j]=xrand()%10;init_hi[j]=xrand()%10;
  lo[j]=1u<<init_lo[j];hi[j]=1u<<init_hi[j];
 }
 init_hi[0]=1+(init_hi[0]%9);hi[0]=1u<<init_hi[0];
 for(int j=0;j<K;j++)seed.push_back('0'+init_hi[j]);
 seed.append(M,centre);
 for(int j=K-1;j>=0;j--)seed.push_back('0'+init_lo[j]);
 BigInt N(seed);
 int max_first=0,last_w=-1,full_unequal=0;
 long long uncertainty_total=0;
 for(int t=0;t<=T;t++){
  string actual=N.str();
  if(actual.size()<size_t(2*K+1)){cerr<<"FAIL length at "<<t<<"\n";return 3;}
  if(equal(actual.begin(),actual.end(),actual.rbegin())){cerr<<"FAIL palindrome at "<<t<<"\n";return 4;}
  full_unequal++;
  int w=-1,uncertain=0;
  for(int j=0;j<K;j++){
    int a=actual[actual.size()-1-j]-'0';
    int b=actual[j]-'0';
    if(!(lo[j]&(1u<<a)) || !(hi[j]&(1u<<b))){
       cerr<<"FAIL symbolic membership at step="<<t<<" index="<<j<<"\n";return 5;
    }
    if(w<0 && (lo[j]&hi[j])==0)w=j;
    uncertain+=((lo[j]&(lo[j]-1))!=0 || (hi[j]&(hi[j]-1))!=0);
  }
  if(w<0){cout<<"FAIL stage="<<t<<" K="<<K<<"\n";return 1;}
  uncertainty_total+=uncertain;
  last_w=w;max_first=max(max_first,w);
  if(t==0||t==1||t==10||t==100||t==1000||t==5000||t==10000||t==15000||t==T)
    cout<<"SAMPLE stage="<<t<<" digits="<<actual.size()<<" witness="<<w<<" max_first="<<max_first<<" uncertain="<<uncertain<<"\n";
  if(t==T)break;
  for(int j=0;j<K;j++)pm[j]=pairmask(lo[j],hi[j]);
  uint8_t c=1;
  for(int j=0;j<K;j++){
    auto n=norm(pm[j],c);lowdig[j]=n.digs;c=n.carries;
  }
  c=3;
  for(int j=K-1;j>=0;j--){
    auto n=norm(pm[j],c);highdig[j]=n.digs;c=n.carries;
  }
  for(int j=0;j<K;j++){
    nlo[j]=lowdig[j];nhi[j]=0;
    if(c&1)nhi[j]|=highdig[j];
    if(c&2)nhi[j]|=(j?highdig[j-1]:(1u<<1));
  }
  lo.swap(nlo);hi.swap(nhi);
  string reversed=actual;reverse(reversed.begin(),reversed.end());
  BigInt R(reversed);N.add(R);
 }
 cout<<"PASS steps="<<T<<" checked_integers="<<full_unequal
   <<" K="<<K<<" max_first_witness="<<max_first
   <<" last_witness="<<last_w<<" centre_length="<<M
   <<" centre_digit="<<centre<<" uncertainty_cell_total="<<uncertainty_total<<"\n";
}
