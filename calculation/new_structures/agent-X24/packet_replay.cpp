// Agent X24: independent GMP and decimal digit-vector replay of a two-step inverse fibre.
// g++ -O3 -std=c++17 packet_replay.cpp -lgmp -o packet_replay
// ./packet_replay 234 20000 200
#include <gmp.h>
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
static vector<int> B={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
static vector<int> W={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
vector<int> step_pair(const vector<int>&p,int *gamma=nullptr){
 vector<int>d;d.reserve(p.size()+1);int c=0;
 for(int x:p){int z=x+c;d.push_back(z%10);c=z/10;}
 if(gamma)*gamma=c;
 if(c)d.push_back(c);
 vector<int>q;q.reserve(d.size());
 for(size_t i=0;i<d.size();i++)q.push_back(d[i]+d[d.size()-1-i]);
 return q;
}
vector<int> exterior_half(int r){vector<int> h=B;for(int j=0;j<r;j++)h.insert(h.end(),W.begin(),W.end());return h;}
vector<int> pair_seed(int r,int k,int which){
 vector<int>half=exterior_half(r),p=half,ca;
 ca.push_back(0);
 for(int j=0;j<k;j++)ca.push_back(which?10:1);
 for(int j=k-1;j>=0;j--)ca.push_back(which?10:1);
 ca.push_back(0);
 p.insert(p.end(),ca.begin(),ca.end());
 p.insert(p.end(),half.rbegin(),half.rend());return p;
}
string numeric_seed(int r,int k,int which){
 auto p=pair_seed(r,k,which);size_t n=p.size();string s(n,'0');
 for(size_t i=0;i<n/2;i++){
  int lo=p[i]/2,hi=p[i]-lo;
  if(lo>9||hi>9){cerr<<"unrealizable coefficient\n";exit(2);}
  s[n-1-i]=char('0'+lo);s[i]=char('0'+hi);
 }
 if(s[0]=='0'){cerr<<"leading zero\n";exit(2);}return s;
}
string add_reverse_string(const string &s){
 int n=(int)s.size(),carry=0;string out(n,'0');
 for(int i=n-1;i>=0;--i){int sum=(s[i]-'0')+(s[n-1-i]-'0')+carry;out[i]=char('0'+sum%10);carry=sum/10;}
 if(carry)out.insert(out.begin(),char('0'+carry));
 if(out[0]=='0'){cerr<<"leading zero unexpectedly\n";exit(3);}return out;
}
void gmp_step(const string &s,string &output,mpz_t x,mpz_t y){
 mpz_set_str(x,s.c_str(),10);string rev=s;reverse(rev.begin(),rev.end());
 if(mpz_set_str(y,rev.c_str(),10)){cerr<<"mpz parse error\n";exit(4);}
 mpz_add(x,x,y);char *z=mpz_get_str(NULL,10,x);
 output.assign(z);void(*freefn)(void*,size_t);
 mp_get_memory_functions(NULL,NULL,&freefn);freefn(z,strlen(z)+1);
}
uint64_t hash64(const string &s){
 uint64_t h=1469598103934665603ULL;
 for(char c:s){h^=(unsigned char)c;h*=1099511628211ULL;}return h;
}
vector<vector<int>> phase_B,phase_W;
void build_phase(){
 auto h=exterior_half(20);vector<int>p=h;p.insert(p.end(),h.rbegin(),h.rend());
 for(int t=0;t<16;t++){
  vector<int>bb(p.begin(),p.begin()+39),ww(p.begin()+39,p.begin()+59);
  if(t<8){phase_B.push_back(bb);phase_W.push_back(ww);}
  else if(bb!=phase_B[t-8]||ww!=phase_W[t-8]){cerr<<"phase did not close\n";exit(5);}
  int gamma=0;p=step_pair(p,&gamma);
  if(gamma!=(t%2==0)){cerr<<"bad gamma phase\n";exit(6);}
 }
}
int check_exterior(const string &s,int phase,int band_max=20){
 int n=(int)s.size(),minmatch=0;
 for(int j=0;j<39;j++)
  if(s[n-1-j]-'0'+s[j]-'0'!=phase_B[phase][j])return -1;
 for(int k=0;k<band_max;k++){
  bool good=true;
  for(int j=0;j<20;j++){
   int i=39+k*20+j;
   if(i>=n/2||s[n-1-i]-'0'+s[i]-'0'!=phase_W[phase][j]){good=false;break;}
  }
  if(!good)break;
  minmatch++;
 }
 return minmatch;
}
int main(int argc,char**argv){
 if(argc<3){cerr<<"usage: packet_replay <band_copies> <steps> [centre_bits=1]\n";return 1;}
 int r=atoi(argv[1]),steps=atoi(argv[2]),k=(argc>3?atoi(argv[3]):1);build_phase();
 string a=numeric_seed(r,k,0),b=numeric_seed(r,k,1);int n0=a.size();
 cerr<<"seed_digits="<<n0<<" r="<<r<<" k="<<k<<" hA="<<hex<<hash64(a)<<" hB="<<hash64(b)<<dec<<"\n";
 mpz_t x,y;mpz_inits(x,y,NULL);string gm;
 gmp_step(a,gm,x,y);string a1=gm;
 gmp_step(b,gm,x,y);string b1=gm;
 if(a1==b1){cerr<<"FAILED distinct first successors\n";return 10;}
 gmp_step(a1,gm,x,y);string a2=gm;
 gmp_step(b1,gm,x,y);string b2=gm;
 if(a2!=b2){cerr<<"FAILED second-step coalescence\n";return 11;}
 cerr<<"PASS distinct first values then exact second-step coalescence; h2="<<hex<<hash64(a2)<<dec<<"\n";
 int minbands=100000,break_step=-1;long long pal=0;
 for(int t=0;t<=steps;t++){
  if(equal(a.begin(),a.end(),a.rbegin()))++pal;
  int match=check_exterior(a,t%8,20);
  if(match<minbands)minbands=match;
  if(match<1&&break_step<0)break_step=t;
  if(t%1000==0||t==steps)
   cout<<"step="<<t<<" length="<<a.size()<<" bands="<<match<<" pal_count="<<pal
       <<" hash64="<<hex<<hash64(a)<<dec<<"\n"<<flush;
  if(t==steps)break;
  string stringresult=add_reverse_string(a);
  gmp_step(a,gm,x,y);
  if(gm!=stringresult){cerr<<"DIVERGENCE engines at step "<<t<<"\n";return 12;}
  a.swap(stringresult);
 }
 mpz_clears(x,y,NULL);
 cout<<"RESULT r="<<r<<" k="<<k<<" steps="<<steps<<" no_pal="<<(pal==0)
     <<" min_band_matches="<<minbands<<" first_no_band="<<break_step<<"\n";
 return pal==0&&break_step<0?0:13;
}
