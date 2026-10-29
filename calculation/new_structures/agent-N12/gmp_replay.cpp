// Independent literal arbitrary-precision GMP decimal reverse-and-add.
// No shared code, no pair-word arithmetic used to evolve the integer.
#include <gmpxx.h>
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>
using namespace std;
static const uint64_t Offset=14695981039346656037ULL,Prime=1099511628211ULL;
int main(int argc,char**argv){
 if(argc!=7){cerr<<"Usage: gmp_replay LEFT GAP RIGHT STEPS MIN_ZERO TRACE.csv\n";return 2;}
 string left=argv[1],right=argv[3];int gap=atoi(argv[2]),steps=atoi(argv[4]),floor=atoi(argv[5]);
 string seed=left+string(gap,'0')+right;mpz_class n;if(n.set_str(seed,10)!=0){cerr<<"bad seed\n";return 2;}
 ofstream f(argv[6]);if(!f)return 2;
 f<<"t,length,width,central_zeros,mismatch,fnv64,first16pairs\n";
 int minz=1000000000,maxw=0,overflow_count=0;
 for(int t=0;t<=steps;t++){
   string s=n.get_str(10);int len=s.size(),width=0,mismatch=-1;string head;
   uint64_t h=Offset;
   for(int i=len-1;i>=0;--i)h=(h^(uint8_t)(s[i]-'0'))*Prime;
   for(int i=0;i<len/2;i++){
     int a=s[len-1-i]-'0',b=s[i]-'0';
     if(a||b)width=i+1;
     if(mismatch<0 && a!=b)mismatch=i;
   }
   int z=len-2*width;
   for(int i=0;i<min(width,16);i++){
     int p=(s[len-1-i]-'0')+(s[i]-'0');
     if(p<10)head+='0';head+=to_string(p);
   }
   if(mismatch<0||z<floor){cerr<<"FAIL t="<<t<<" mismatch="<<mismatch<<" zeros="<<z<<"\n";return 1;}
   f<<t<<','<<len<<','<<width<<','<<z<<','<<mismatch<<','<<hex<<h<<dec<<','<<head<<'\n';
   minz=min(minz,z);maxw=max(maxw,width);
   if(t<steps){
      string reversed(s.rbegin(),s.rend());mpz_class r;
      if(r.set_str(reversed,10)!=0)abort();
      n+=r; overflow_count+=int(n.get_str(10).size())-len;
   }
 }
 cout<<"GMP_PASS seed="<<left<<"+0^"<<gap<<"+"<<right<<" steps="<<steps<<" min_center_zero="<<minz<<" max_halfwidth="<<maxw<<" final_length="<<n.get_str(10).size()<<" total_overflow="<<overflow_count<<"\n";
}
