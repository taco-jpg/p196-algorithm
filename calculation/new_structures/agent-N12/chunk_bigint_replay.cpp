// Independent arbitrary-precision decimal integer: base 10^9 positional limbs.
// Reverse is reconstructed numerically from the canonical decimal representation.
#include <bits/stdc++.h>
using namespace std;
using U=uint32_t;
constexpr uint64_t base=1000000000ULL;
struct Big {
 vector<U> a; // little-endian radix-1e9 limbs
 static Big parse(string s) {
  Big x;for(int k=(int)s.size();k>0;k-=9){int j=max(0,k-9);U v=0;for(int i=j;i<k;i++)v=v*10+(s[i]-'0');x.a.push_back(v);}x.trim();return x;
 }
 void trim(){while(a.size()>1&&a.back()==0)a.pop_back();}
 string show() const{
   string s=to_string(a.back());
   for(int i=(int)a.size()-2;i>=0;i--){string v=to_string(a[i]);s.append(9-v.size(),'0');s+=v;}
   return s;
 }
 Big operator+(const Big& r) const{
  Big b;size_t n=max(a.size(),r.a.size());b.a.resize(n+1,0);uint64_t c=0;
  for(size_t i=0;i<n;i++){uint64_t v=c+(i<a.size()?a[i]:0)+(i<r.a.size()?r.a[i]:0);b.a[i]=v%base;c=v/base;}
  b.a[n]=c;b.trim();return b;
 }
};
int main(int argc,char **argv){
 if(argc!=7){cerr<<"Usage: chunk_bigint_replay LEFT GAP RIGHT STEPS MIN_ZERO TRACE.csv\n";return 2;}
 string L=argv[1],R=argv[3];int g=atoi(argv[2]),steps=atoi(argv[4]),floor=atoi(argv[5]);
 Big n=Big::parse(L+string(g,'0')+R);
 ofstream f(argv[6]); if(!f)return 2;
 f<<"t,length,width,central_zeros,mismatch,fnv64,first16pairs\n";
 constexpr uint64_t FNV_OFFSET=14695981039346656037ULL,FNV_PRIME=1099511628211ULL;
 int minz=INT_MAX,maxw=0,overflow=0;
 for(int t=0;t<=steps;t++){
  string s=n.show();int len=s.size(),width=0,mismatch=-1;string head;uint64_t h=FNV_OFFSET;
  for(int i=len-1;i>=0;i--)h=(h^(uint8_t)(s[i]-'0'))*FNV_PRIME;
  for(int i=0;i<len/2;i++){
   int lo=s[len-1-i]-'0',hi=s[i]-'0';
   if(lo||hi)width=i+1;
   if(mismatch==-1&&lo!=hi)mismatch=i;
  }
  int z=len-2*width;
  for(int i=0;i<min(width,16);i++){int p=(s[len-1-i]-'0')+(s[i]-'0');if(p<10)head+='0';head+=to_string(p);}
  if(mismatch<0||z<floor){cerr<<"FAIL t="<<t<<" mismatch="<<mismatch<<" z="<<z<<"\n";return 1;}
  f<<t<<','<<len<<','<<width<<','<<z<<','<<mismatch<<','<<hex<<h<<dec<<','<<head<<'\n';
  minz=min(minz,z);maxw=max(maxw,width);
  if(t<steps){reverse(s.begin(),s.end());Big rev=Big::parse(s);n=n+rev;overflow+=int(n.show().size())-len;}
 }
 cout<<"CHUNK_BIGINT_PASS seed="<<L<<"+0^"<<g<<"+"<<R<<" steps="<<steps<<" min_center_zero="<<minz<<" max_halfwidth="<<maxw<<" final_length="<<n.show().size()<<" total_overflow="<<overflow<<"\n";
}
