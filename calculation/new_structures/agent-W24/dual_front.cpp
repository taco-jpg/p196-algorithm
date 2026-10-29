// W24: exact 9-complement dual of the first p8/m20 lattice; paired GMP/digit oracle.
// Build: g++ -std=c++17 -O3 -Wall -Wextra dual_front.cpp -lgmpxx -lgmp -o dual_front
// Run: ./dual_front 900 20000
#include <gmpxx.h>
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
static const int B[] = {17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
static const int W[] = {17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
static_assert(sizeof(B)/sizeof(B[0])==39 && sizeof(W)/sizeof(W[0])==20,"phase source");
vector<unsigned char> initial(int q){
    vector<unsigned char> half;half.reserve(39+20*q);
    for(int x:B)half.push_back(18-x);
    for(int k=0;k<q;k++)for(int x:W)half.push_back(18-x);
    vector<unsigned char> d(2*half.size());
    for(int i=0;i<(int)half.size();i++){
        int p=half[i];d[i]=max(0,p-9);d[d.size()-1-i]=p-d[i];
    }
    if(d.back()==0)throw runtime_error("leading zero");
    return d;
}
string str(const vector<unsigned char>&d){
    string s;s.reserve(d.size());
    for(auto it=d.rbegin();it!=d.rend();++it)s+=char('0'+*it);
    return s;
}
void step_vector(vector<unsigned char>&d){
    int n=d.size(),carry=0;vector<unsigned char> out;out.reserve(n+1);
    for(int i=0;i<n;i++){
        int z=d[i]+d[n-1-i]+carry;out.push_back(z%10);carry=z/10;
    }
    if(carry)out.push_back(carry);
    d.swap(out);
}
void step_gmp(mpz_class &n){
    string s=n.get_str(10),rs=s;reverse(rs.begin(),rs.end());
    mpz_class r;
    if(r.set_str(rs,10)!=0)throw runtime_error("bad GMP reverse");
    n+=r;
}
struct Run{int start,stop,length,half;};
Run longest_period20(const vector<unsigned char>&d){
    int n=d.size(),half=n/2,best_start=0,best_stop=0,st=-1;
    auto coeff=[&](int i){return int(d[i])+int(d[n-1-i]);};
    for(int i=0;i<=half-20;i++){
        bool eq=(i+20<half && coeff(i)==coeff(i+20));
        if(eq && st<0)st=i;
        if(!eq && st>=0){
            if(i-st>best_stop-best_start){best_start=st;best_stop=i;}
            st=-1;
        }
    }
    if(st>=0 && half-20-st>best_stop-best_start){
        best_start=st;best_stop=half-20;
    }
    return {best_start,best_stop,best_stop-best_start,half};
}
uint64_t fnv_hash(const vector<unsigned char>&d){
    uint64_t h=1469598103934665603ULL;
    for(unsigned char c:d){h^=c;h*=1099511628211ULL;}
    return h;
}
int main(int argc,char**argv){
 try{
    int q=argc>1?atoi(argv[1]):900,steps=argc>2?atoi(argv[2]):20000;
    if(q<1||q>100000||steps<0||steps>200000)throw runtime_error("bounds");
    auto d=initial(q);mpz_class n(str(d),10);
    int min_bulk=1000000000,min_at=-1,min_odd=0,all_pals=0,checks=0;
    cout<<"{\"q\":"<<q<<",\"steps\":"<<steps<<",\"initial_digits\":"<<d.size()<<",\"checkpoints\":[";
    bool first=true;
    for(int t=0;t<=steps;t++){
      auto run=longest_period20(d);
      if(run.length<min_bulk){min_bulk=run.length;min_at=t;}
      int p0=int(d[0])+int(d.back());if(p0&1)min_odd++;
      bool pal=true;
      for(int j=0;j<(int)d.size()/2;j++){
          if(d[j]!=d[d.size()-1-j]){pal=false;break;}
      }
      if(pal)all_pals++;
      if(t==0||t==1||t==2||t==8||t==88||t==500||t==1000||
          t==2000||t==5000||t==10000||t==15000||t==steps){
        if(!first)cout<<",";
        first=false;
        cout<<"{\"t\":"<<t<<",\"digits\":"<<d.size()
            <<",\"front_left\":"<<run.start<<",\"front_right\":"<<run.stop
            <<",\"repeat20\":"<<run.length<<",\"p0\":"<<p0
            <<",\"pal\":"<<(pal?"true":"false")<<",\"fnv64\":"<<fnv_hash(d)<<"}";
      }
      if(t==steps)break;
      step_vector(d);step_gmp(n);
      if(str(d)!=n.get_str(10))
          throw runtime_error("independent integer mismatch at "+to_string(t+1));
      checks++;
      if(run.length<100)throw runtime_error("lost 100-site bulk at "+to_string(t));
      if(pal)throw runtime_error("palindrome at "+to_string(t));
    }
    cout<<"],\"min_bulk\":"<<min_bulk<<",\"min_bulk_at\":"<<min_at
        <<",\"odd_pair0_count\":"<<min_odd<<",\"palindromes\":"<<all_pals
        <<",\"independent_gmp_checks\":"<<checks<<"}"<<endl;
    if(min_bulk<100||all_pals)return 2;
  }catch(const exception&e){cerr<<"ERROR "<<e.what()<<"\n";return 1;}
}
