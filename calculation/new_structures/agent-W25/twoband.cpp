// Agent W25: decimal rooted p8/m20 + independently synthesized p8/m4 bulk.
// From repository root:
// g++ -O3 -std=c++17 calculation/new_structures/agent-W25/twoband.cpp -lgmpxx -lgmp -o /tmp/w25_twoband
// /tmp/w25_twoband 500 9000 20000
// Full ordinary decimal digit replay and independent pair-normalization agree at every step.
// GMP independently checks the first 20 full steps; this is NOT an infinite certificate.
#include <bits/stdc++.h>
#include <gmpxx.h>
using namespace std;
using V=vector<unsigned char>;
static const int B[]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
static const int W[]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
static const int U[]={9,18,9,0};
static V from_pair(const vector<int>&half){
 int n=2*(int)half.size();V a(n);
 for(int i=0;i<(int)half.size();i++){a[i]=min(half[i],9);a[n-1-i]=half[i]-a[i];}
 if(a.back()==0)throw runtime_error("leading zero");return a;
}
static string as_string(const V&d){
 string s;s.reserve(d.size());for(auto it=d.rbegin();it!=d.rend();it++)s.push_back(char('0'+*it));return s;
}
static V schoolbook(const V&d,int&gamma){
 V e;e.reserve(d.size()+1);int carry=0;
 for(int i=0;i<(int)d.size();i++){int v=d[i]+d[d.size()-1-i]+carry;e.push_back(v%10);carry=v/10;}
 gamma=carry;if(carry)e.push_back(carry);return e;
}
static V pair_coeff(const V&d){
 V p(d.size());for(int i=0;i<(int)d.size();i++)p[i]=d[i]+d[d.size()-1-i];return p;
}
static V normalized_from_pairs(const V&p,int&overflow){
 V out;out.reserve(p.size()+1);int carry=0;
 for(auto x:p){int z=x+carry;out.push_back(z%10);carry=z/10;}
 overflow=carry;if(carry)out.push_back(carry);return out;
}
static V bulk(const V&w,int gam){
 int m=w.size(),c0=-1,hm=-1;V lo(m),hi(m),out(m);
 for(int init=0;init<2;init++){
  int cr=init;for(int i=0;i<m;i++)cr=(w[i]+cr)/10;
  if(cr==init){c0=init;break;}
 }
 for(int init=0;init<2;init++){
  int cr=init;for(int i=m-1;i>=0;i--)cr=(w[i]+cr)/10;
  if(cr==init){hm=init;break;}
 }
 if(c0<0||hm<0)throw runtime_error("cyclic carry not found");
 int cr=c0;
 for(int i=0;i<m;i++){lo[i]=(w[i]+cr)%10;cr=(w[i]+cr)/10;}
 cr=hm;
 for(int i=m-1;i>=0;i--){hi[i]=(w[i]+cr)%10;cr=(w[i]+cr)/10;}
 for(int i=0;i<m;i++)out[i]=lo[i]+hi[(i+m-gam)%m];
 return out;
}
static uint64_t fnv(const V&a){
 uint64_t h=1469598103934665603ull;
 for(auto x:a){h^=x;h*=1099511628211ull;}return h;
}
static mpz_class reversed(const mpz_class&n){
 string s=n.get_str(10);reverse(s.begin(),s.end());return mpz_class(s,10);
}
int main(int argc,char**argv){
 int k=argc>1?atoi(argv[1]):500,r=argc>2?atoi(argv[2]):9000,steps=argc>3?atoi(argv[3]):20000;
 if(k<10||r<10||steps<1)throw runtime_error("invalid parameters");
 vector<int> half;
 for(auto b:B)half.push_back(b);
 for(int i=0;i<k;i++)for(auto w:W)half.push_back(w);
 for(int i=0;i<r;i++)for(auto u:U)half.push_back(u);
 V a=from_pair(half),w(begin(W),end(W)),u(begin(U),end(U));
 const int xw=39+20*(k/2),xu=39+20*k+4*(r/2);
 mpz_class n(as_string(a),10);
 cout<<"INIT digits="<<a.size()<<" W_window="<<xw<<" U_window="<<xu<<"\n"<<flush;
 int survivedW=0,survivedU=0,badW=-1,badU=-1,badClock=-1,pals=0;
 for(int t=0;t<=steps;t++){
  if(a.size()<2||a.back()==0)throw runtime_error("invalid ordinary integer");
  if(equal(a.begin(),a.begin()+a.size()/2,a.rbegin()))pals++;
  V pp=pair_coeff(a);
  bool okW=true,okU=true;
  for(int j=0;j<80;j++){
   if(xw+j>=(int)pp.size()/2||pp[xw+j]!=w[(xw+j-39)%w.size()])okW=false;
   if(xu+j>=(int)pp.size()/2||pp[xu+j]!=u[(xu+j-39-20*k)%u.size()])okU=false;
  }
  if(okW)survivedW++;else if(badW<0)badW=t;
  if(okU)survivedU++;else if(badU<0)badU=t;
  if(t==steps)break;
  int gamma=0;V next=schoolbook(a,gamma);
  if(gamma!=(t%2==0)&&badClock<0)badClock=t;
  int norm_gamma=0;V cross=normalized_from_pairs(pp,norm_gamma);
  if(norm_gamma!=gamma||cross!=next)throw runtime_error("independent normalizer mismatch at t="+to_string(t));
  if(t<20){
   n+=reversed(n);
   if(n.get_str(10)!=as_string(next))throw runtime_error("GMP mismatch at t="+to_string(t));
  }
  w=bulk(w,gamma);u=bulk(u,gamma);a.swap(next);
 }
 cout<<"RESULT k="<<k<<" r="<<r<<" steps="<<steps<<" digits="<<a.size()
 <<" pal="<<pals<<" first_clock_failure="<<badClock<<" first_W_failure="<<badW
 <<" first_U_failure="<<badU<<" W_matching_states="<<survivedW
 <<" U_matching_states="<<survivedU<<" FNV64="<<hex<<fnv(a)<<dec<<"\n";
 if(k==500&&r==9000&&steps==20000 &&
 (pals||badClock!=-1||badW!=-1||badU!=-1||
 a.size()!=102078||fnv(a)!=0x3f6aaae5052be7bcULL))
  throw runtime_error("20,000-step W25 regression failed");
}
