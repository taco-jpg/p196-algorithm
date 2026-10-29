// Independent GNU GMP integer checker. No call to W01's digit-array step.
#include <gmpxx.h>
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
static const int ROOT[39]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
static const int BULK[20]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
string seed(int h,int flags){string s(2*h,'0');for(int j=0;j<h;j++){
 int q=j<39?ROOT[j]:BULK[(j-39)%20];
 if((flags&1)&&j>=6000&&j<6050)q=(7*j+11)%19;
 if((flags&2)&&j>=8000&&j<8050)q=(3*j+7)%19;
 int a=min(q,9),b=q-a;s[2*h-1-j]=char('0'+a);s[j]=char('0'+b);}
 return s;}
int coef(const string&s,int j){return s[j]-'0'+s[s.size()-1-j]-'0';}
uint64_t hashstr(const string&s){uint64_t h=1469598103934665603ULL;for(unsigned char a:s){h^=a;h*=1099511628211ULL;}return h;}
int main(int argc,char**argv){int T=argc>1?atoi(argv[1]):20000;int flags=argc>2?atoi(argv[2]):3;bool wrong_phase=argc>3;mpz_class n(seed(12000,flags),10);
 array<array<int,59>,8> tile{};long long checks=0;string s;
 for(int t=0;t<=T;t++){
  s=n.get_str(10);if(t<8)for(int j=0;j<59;j++)tile[t][j]=coef(s,j);
  for(int j=0;j<1456;j++){int phase=(t>=8 && wrong_phase)?(t+1)%8:t%8;int expected=j<39?tile[phase][j]:tile[phase][39+(j-39)%20];
    if(coef(s,j)!=expected){cerr<<"GMP_SHAPE_FAIL t="<<t<<" j="<<j<<" got="<<coef(s,j)<<" expected="<<expected<<"\n";return 2;}checks++;}
  int odd=-1;for(int j=0;j<39;j++){if(coef(s,j)%2){odd=j;break;}}
  if(odd<0){cerr<<"GMP_ODD_WITNESS_FAIL t="<<t<<"\n";return 3;}
  if(t==0||t==1000||t==2154||t==2161||t==8000||t==20000)
    cout<<"W01_GMP_CHECKPOINT t="<<t<<" len="<<s.size()<<" fnv64="<<hashstr(s)<<" odd="<<odd<<"\n";
  if(t<T){string r=s;reverse(r.begin(),r.end());mpz_class backwards(r,10);n+=backwards;}
 }
 cout<<"W01_GMP_PASS flags="<<flags<<" steps="<<T<<" prefix_checks="<<checks<<"\n";
}
