#include <bits/stdc++.h>
using namespace std;
struct Norm {uint16_t digs;uint8_t carries;};
Norm norm(uint32_t p,uint8_t c) {
  uint16_t ds=0;uint8_t cs=0;
  while(p){int j=__builtin_ctz(p);p&=p-1;
    if(c&1){ds|=1u<<(j%10);cs|=1u<<(j/10);}
    if(c&2){int z=j+1;ds|=1u<<(z%10);cs|=1u<<(z/10);}
  }
  return {ds,cs};
}
uint32_t pairmask(uint16_t a,uint16_t b){
  uint32_t p=0;
  while(a){int i=__builtin_ctz(a);a&=a-1;p|=uint32_t(b)<<i;}
  return p;
}
struct BigInt {
  vector<uint32_t> v;
  explicit BigInt(const string& s){
    for(int j=(int)s.size();j>0;j-=9)v.push_back(stoul(s.substr(max(0,j-9),min(j,9))));
    while(v.size()>1&&v.back()==0)v.pop_back();
  }
  string str() const {
    string s=to_string(v.back());
    for(int j=(int)v.size()-2;j>=0;j--){string x=to_string(v[j]);s+=string(9-x.size(),'0')+x;}
    return s;
  }
  void add(const BigInt& rhs){
    size_t n=max(v.size(),rhs.v.size());v.resize(n,0);
    uint64_t carry=0;
    for(size_t j=0;j<n;j++){
      uint64_t z=uint64_t(v[j])+carry+(j<rhs.v.size()?rhs.v[j]:0);
      v[j]=z%1000000000U;carry=z/1000000000U;
    }
    if(carry)v.push_back((uint32_t)carry);
  }
};
int main(int argc,char**argv){
  int K=argc>1?atoi(argv[1]):5500;
  int T=argc>2?atoi(argv[2]):20000;
  int M=argc>3?atoi(argv[3]):37;
  char centre=argc>4?argv[4][0]:'3';
  if(K<2||T<1||M<1||centre<'0'||centre>'9')return 2;
  vector<uint16_t> lo(K),hi(K),nlo(K),nhi(K),lowdig(K),highdig(K);
  vector<uint32_t> pm(K);
  string seed;seed.reserve(2*K+M);
  for(int j=0;j<K;j++){lo[j]=1u<<((j%2==0)?2:6);hi[j]=1u<<((j==0)?1:((j%2==0)?9:8));}
  for(int j=0;j<K;j++)seed.push_back('0'+__builtin_ctz(hi[j]));
  seed.append(M,centre);
  for(int j=K-1;j>=0;j--)seed.push_back('0'+__builtin_ctz(lo[j]));
  BigInt N(seed);int max_first=0,last_w=-1;
  long long uncertainty_total=0;
  for(int t=0;t<=T;t++){
    string a=N.str();
    if(a.size()<(size_t)(2*K+1)){cerr<<"FAIL length at step "<<t<<"\n";return 3;}
    if(equal(a.begin(),a.end(),a.rbegin())){cerr<<"FAIL palindrome at "<<t<<"\n";return 4;}
    int w=-1,uncertain=0;
    for(int j=0;j<K;j++){
      int x=a[a.size()-1-j]-'0',y=a[j]-'0';
      if(!(lo[j]&(1u<<x))||!(hi[j]&(1u<<y))){
        cerr<<"FAIL mask membership step="<<t<<" index="<<j<<"\n";return 5;
      }
      if(w<0&&!(lo[j]&hi[j]))w=j;
      if((lo[j]&(lo[j]-1))||(hi[j]&(hi[j]-1)))uncertain++;
    }
    if(w<0){cout<<"FAIL envelope guard step="<<t<<"\n";return 1;}
    max_first=max(max_first,w);last_w=w;uncertainty_total+=uncertain;
    if(t==0||t==1||t==10||t==100||t==1000||t==5000||t==10000||t==15000||t==T)
      cout<<"SAMPLE stage="<<t<<" digits="<<a.size()<<" witness="<<w
          <<" max_first="<<max_first<<" uncertain="<<uncertain<<"\n";
    if(t==T)break;
    for(int j=0;j<K;j++)pm[j]=pairmask(lo[j],hi[j]);
    uint8_t c=1;
    for(int j=0;j<K;j++){auto r=norm(pm[j],c);lowdig[j]=r.digs;c=r.carries;}
    c=3;
    for(int j=K-1;j>=0;j--){auto r=norm(pm[j],c);highdig[j]=r.digs;c=r.carries;}
    for(int j=0;j<K;j++){
      nlo[j]=lowdig[j];nhi[j]=0;
      if(c&1)nhi[j]|=highdig[j];
      if(c&2)nhi[j]|=j?highdig[j-1]:(1u<<1);
    }
    lo.swap(nlo);hi.swap(nhi);
    string reversed=a;reverse(reversed.begin(),reversed.end());
    N.add(BigInt(reversed));
  }
  cout<<"PASS steps="<<T<<" checked_integers="<<T+1<<" K="<<K
      <<" max_first_witness="<<max_first<<" last_witness="<<last_w
      <<" centre_length="<<M<<" centre_digit="<<centre
      <<" uncertainty_cell_total="<<uncertainty_total<<"\n";
}