// Agent X06. Build: c++ -O3 -std=c++17 twist.cpp -lgmpxx -lgmp -o twist
// Run: ./twist 500 20000   (two entirely independent decimal replay algorithms)
#include <gmpxx.h>
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <random>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
using U=uint8_t;
static const vector<U> B={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
static const vector<U> W={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
static const vector<U> V={4,4,14,1,5,11,7,1,15,12,7,9,9,12,14,4,0,6,5,17,13,9,7,3,13,10,4,13,5,1,9,4,11,6,16,3,7,7,12,4,2,13,2,15,10,10,9,3};
static void req(bool ok,const string &why){if(!ok)throw runtime_error(why);}
static vector<U> complement(vector<U> w){for(auto &a:w)a=18-a;return w;}
static vector<U> cyclic(const vector<U>&w){
  for(int c0=0;c0<=1;c0++){int c=c0;vector<U>d;
    for(U x:w){int y=x+c;d.push_back(y%10);c=y/10;}
    if(c==c0)return d;
  }throw runtime_error("cyclic carry absent");
}
static vector<U> bulk(const vector<U>&w,int g){
  vector<U> low=cyclic(w),rev=w;reverse(rev.begin(),rev.end());
  vector<U> high=cyclic(rev);reverse(high.begin(),high.end());
  vector<U> out(w.size());int m=int(w.size());
  for(int i=0;i<m;i++)out[i]=low[i]+high[(i-g+m)%m];
  return out;
}
static vector<U> coeffnorm(const vector<U>&p){
  vector<U>d;int c=0;d.reserve(p.size()+1);
  for(U x:p){int y=x+c;d.push_back(y%10);c=y/10;}
  if(c)d.push_back(c);return d;
}
static vector<U> ordinary(const vector<U>&d){
  vector<U>z;int c=0,n=int(d.size());z.reserve(n+1);
  for(int i=0;i<n;i++){int x=d[i]+d[n-1-i]+c;z.push_back(x%10);c=x/10;}
  if(c)z.push_back(c);return z;
}
static vector<U> pairs(const vector<U>&d){
  vector<U>p(d.size());int n=int(d.size());
  for(int i=0;i<n;i++)p[i]=d[i]+d[n-1-i];return p;
}
static vector<U> seed(int k){
  vector<U>h=B;h.reserve(B.size()+(W.size()+V.size())*k+1);
  for(int i=0;i<k;i++)h.insert(h.end(),W.begin(),W.end());
  h.push_back(9);auto cv=complement(V);
  for(int i=0;i<k;i++)h.insert(h.end(),cv.begin(),cv.end());
  vector<U>p=h;p.push_back(9);p.insert(p.end(),h.rbegin(),h.rend());return p;
}
static void local_controls(){
  mt19937 rng(6006);
  for(int m=1;m<=32;m++)for(int rep=0;rep<150;rep++){
    vector<U>w(m);bool nonneutral=false;
    for(auto &x:w){x=rng()%19;if(x!=9)nonneutral=true;}
    if(!nonneutral)continue;
    for(int g=0;g<=1;g++){
      auto left=bulk(complement(w),g),right=complement(bulk(w,g));
      req(left==right,"complement-cyclic failure");
    }
  }
  for(const auto&w:{W,V}){
    auto a=w;
    for(int t=0;t<8;t++){
      req(bulk(complement(a),1-t%2)==complement(bulk(a,1-t%2)),"phase complement failure");
      a=bulk(a,1-t%2);
    }
    req(a==w,"8-phase temporal closure absent");
  }
}
static vector<U> pairs_of_integer_string(const string&s){
  int n=int(s.size());vector<U>p(n);
  for(int i=0;i<n;i++)p[i]=(s[i]-'0')+(s[n-1-i]-'0');
  return p;
}
int main(int argc,char**argv){
  try{
    int k=argc>1?atoi(argv[1]):500,steps=argc>2?atoi(argv[2]):20000;
    req(k>=400 && steps>=0,"require k>=400, nonnegative steps");local_controls();
    vector<U>p=seed(k),d=coeffnorm(p),w=W,v=V;
    // Different representation and arithmetic: GMP builds the number directly from coefficients.
    mpz_class N=0;
    for(auto it=p.rbegin();it!=p.rend();++it){N*=10;N+=static_cast<unsigned long>(*it);}
    string prev;uint64_t hash=1469598103934665603ULL;
    size_t base=B.size()+W.size()*k+1;
    size_t ws=B.size()+400,we=B.size()+1400;
    size_t vs=base+15000,ve=base+15960;
    req(ve<base+V.size()*k,"selected V window outside the bulk");
    for(int t=0;t<=steps;t++){
      string s=N.get_str(10);
      req(s.size()==d.size(),"GMP and digit-array lengths disagree at "+to_string(t));
      for(size_t i=0;i<d.size();i++)if(d[i]!=s[s.size()-1-i]-'0')throw runtime_error("GMP vs digit-array digits at "+to_string(t));
      req(!equal(s.begin(),s.begin()+s.size()/2,s.rbegin()),"PALINDROME at "+to_string(t));
      if(t)req(p==pairs_of_integer_string(prev),"GMP previous-number pairword differs at "+to_string(t));
      req(int(d.size())-int(p.size())==1-t%2,"alternating overflow lost at "+to_string(t));
      req(we<p.size()/2 && ve<p.size()/2,"windows leave half-word at "+to_string(t));
      for(size_t j=ws;j<we;j++)if(p[j]!=w[(j-B.size())%w.size()])throw runtime_error("W bulk mismatch t="+to_string(t));
      for(size_t j=vs;j<ve;j++)if(p[j]!=18-v[(j-base)%v.size()])throw runtime_error("COMPLEMENTED V bulk mismatch t="+to_string(t));
      if(t==steps){for(U x:d){hash^=x;hash*=1099511628211ULL;}break;}
      prev=move(s);
      string rev(prev.rbegin(),prev.rend());
      N+=mpz_class(rev,10); // independent high-precision integer reverse-and-add
      auto nd=ordinary(d),np=pairs(d);d.swap(nd);p.swap(np);
      w=bulk(w,1-t%2);v=bulk(v,1-t%2);
      if((t+1)%4000==0)cerr<<"checked="<<t+1<<" digits="<<d.size()<<"\n";
    }
    cout<<"PASS k="<<k<<" steps="<<steps<<" initial_digits="<<seed(k).size()+1
        <<" final_digits="<<d.size()<<" 8-phase W and complemented-V bands intact at EVERY step;"
        <<" independent GMP/digit checks PASS; hash="<<hex<<hash<<dec<<"\n";
  }catch(const exception&e){cerr<<"FAIL: "<<e.what()<<"\n";return 1;}
}