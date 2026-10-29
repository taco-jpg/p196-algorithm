// W13: independent base10 vector and GMP integer replay, nonlocal charge-neutral dipole corridors.
#include <bits/stdc++.h>
#include <gmpxx.h>
using namespace std;using V=vector<unsigned char>;
V source(int h,int M,bool altered){assert(h>50 && M>=0);V half;half.reserve(h);half.push_back(17);for(int i=1;i<h;i++)half.push_back(i%3==1?4:1);
 if(altered)for(int m=0;m<M;m++){
  int a=200+198*m,k=1,b=a+6*k+3;assert(b+20<=h);
  const int left[]={3,4,3},corridor[]={2,0,5,0,2,3},right[]={4,3,4};
  for(int j=0;j<3;j++)half[a+j]=left[j];for(int j=0;j<6*k;j++)half[a+3+j]=corridor[j%6];for(int j=0;j<3;j++)half[b+j]=right[j];
 }
 V p=half;for(int i=h-1;i>=0;i--)p.push_back(half[i]);return p;
}
V pairs(const V&d){V r(d.size());for(size_t i=0;i<d.size();i++)r[i]=d[i]+d[d.size()-1-i];return r;}
V digits(const V&p){assert(p.size()%2==0);V d(p.size());for(size_t i=0;i<p.size()/2;i++){d[i]=min(9,int(p[i]));d[p.size()-1-i]=p[i]-d[i];}assert(d.back() && pairs(d)==p);return d;}
V addrev(const V&d){V z;z.reserve(d.size()+1);int c=0;for(size_t i=0;i<d.size();i++){int u=d[i]+d[d.size()-1-i]+c;z.push_back(u%10);c=u/10;}if(c)z.push_back(c);return z;}
bool ispal(const V&d){return equal(d.begin(),d.begin()+d.size()/2,d.rbegin());}
string spell(const V&d){string s;s.reserve(d.size());for(auto it=d.rbegin();it!=d.rend();it++)s+=char('0'+*it);return s;}
string fnv(const V&d){uint64_t h=1469598103934665603ull;for(unsigned v:d){h^=v;h*=1099511628211ull;}char out[32];snprintf(out,sizeof(out),"%016llx",(unsigned long long)h);return out;}
int main(int argc,char**argv){int h=argc>1?atoi(argv[1]):6000,M=argc>2?atoi(argv[2]):20,steps=argc>3?atoi(argv[3]):20000;
 V A=digits(source(h,M,false)),B=digits(source(h,M,true));
 for(int t=0;t<=6;t++){
  if(ispal(A)||ispal(B))throw runtime_error("palindrome in initial six");
  if(t==5 && pairs(A)!=pairs(B))throw runtime_error("pairword 5 merger failed");
  if(t==6 && A!=B)throw runtime_error("integer 6 merger failed");
  if(t<6){A=addrev(A);B=addrev(B);}
 }
 A=digits(source(h,M,false));mpz_class n(spell(A),10);int overflows=0;int first16_odd=0,first32_odd=0;long max_length=0;int failedclock=-1;int lastgamma=-1;
 for(int t=0;t<=steps;t++){
  string s=n.get_str();if(s!=spell(A))throw runtime_error("GMP/vector integer disagreement at "+to_string(t));
  if(ispal(A)||equal(s.begin(),s.begin()+s.size()/2,s.rbegin()))throw runtime_error("palindrome at "+to_string(t));
  V p=pairs(A);
  bool odd16=false,odd32=false;for(int i=0;i<16;i++)odd16|=p[i]&1;for(int i=0;i<32;i++)odd32|=p[i]&1;
  first16_odd+=odd16;first32_odd+=odd32;
  max_length=max(max_length,long(A.size()));
  if(t==steps)break;
  auto old=A.size();A=addrev(A);int g=int(A.size()>old);overflows+=g;
  if(failedclock<0 && g!=(t%2==0))failedclock=t;
  lastgamma=g;
  reverse(s.begin(),s.end());n+=mpz_class(s,10);
 }
 cout<<"W13_CHARGE_DIPOLE_PASS h="<<h<<" M="<<M<<" variants=2^"<<M<<" steps="<<steps
     <<" source_digits="<<2*h<<" final_digits="<<A.size()<<" overflows="<<overflows
     <<" odd_first16_states="<<first16_odd<<" odd_first32_states="<<first32_odd
     <<" first_overflow_clock_failure="<<failedclock<<" fnv64="<<fnv(A)<<"\n";
}
