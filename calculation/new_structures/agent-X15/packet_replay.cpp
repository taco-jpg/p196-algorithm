// X15: paired-centre soft defect witness; independent GMP and digit arithmetic.
// Build: g++ -std=c++17 -O3 packet_replay.cpp -lgmpxx -lgmp -o packet_replay
#include <gmpxx.h>
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
using namespace std;using V=vector<int>;
static const string BRAW[8]={
"H501D4EC98FGHDH9144B8G09EB9B6DI947HF97D",
"8D5158982IEDFCC7B586AF7A47228AD8EBFE5HB",
"H6B2AGIG5HA8C65G2BGD1BG09E44H17I94C9CF4",
"8E8438GGCD99B9BC949B5397A498C98G8E7339A",
"H8H86HDE680040459A92B6IF09IH49ICI8F6791",
"8GGGEEC9BE804449F00C48FF6A8HCE8CCHECDGA",
"HDEEAA6049H08899A1149HBBE0IF69I56GA68E1",
"8C9A62764E788GI90225E7A4759FCG8EBD87ED6"};
static const string WRAW[8]={
"H31DHBE3I12073ECF97D","CB45CA78CA327A8895HB",
"639B51FH5174F0HGIBF4","A9D1767ED68BA68FGB8A",
"2073ECF97DH31DHBE3I1","327A8895HBCB45CA78CA",
"74F0HGIBF4639B51FH51","8BA68FGB8AA9D1767ED6"};
V decode(const string&s){V p;for(char c:s)p.push_back(c>='A'?c-'A'+10:c-'0');return p;}
V centre(bool optimized){V u(40,1);u[13]=7;u[20]=7;u[30]=6;
 if(optimized){u[30]=4;u[33]=3;u[34]=4;u[38]=8;u[39]=3;}
 V c={8,0,0};c.insert(c.end(),u.begin(),u.end());c.push_back(16);
 c.insert(c.end(),u.rbegin(),u.rend());c.insert(c.end(),{0,0,8});return c;}
V pairs_seed(int q,bool pulse,bool optimized){V B=decode(BRAW[0]),W=decode(WRAW[0]),C=centre(optimized),P=B;
 for(int k=0;k<q;k++)P.insert(P.end(),W.begin(),W.end());
 P.insert(P.end(),C.begin(),C.end());for(int k=0;k<q;k++)P.insert(P.end(),W.rbegin(),W.rend());
 P.insert(P.end(),B.rbegin(),B.rend());
 if(pulse){if(q<6){cerr<<"q must be >=6\n";exit(2);}
  const int pos[4]={129,132,135,145}, val[4]={9,18,0,1};
  for(int j=0;j<4;j++){int i=pos[j]+20*(q-6);P[i]=P[P.size()-1-i]=val[j];}
 }
 return P;
}
V digits_from_pairs(const V&P){int n=P.size();V d(n);
 for(int i=0;i<n/2;i++){d[i]=min(9,P[i]);d[n-1-i]=P[i]-d[i];}
 if(n%2){if(P[n/2]&1){cerr<<"odd midpoint\n";exit(3);}d[n/2]=P[n/2]/2;}
 if(d.back()==0){cerr<<"leading zero\n";exit(4);}return d;
}
V pair_from_digits(const V&d){V p(d.size());for(int i=0,n=d.size();i<n;i++)p[i]=d[i]+d[n-1-i];return p;}
V digit_step(const V&d){int n=d.size(),c=0;V out;out.reserve(n+1);for(int i=0;i<n;i++){int k=d[i]+d[n-1-i]+c;out.push_back(k%10);c=k/10;}if(c)out.push_back(c);return out;}
V pair_step(const V&p){int c=0;V d;d.reserve(p.size()+1);for(int v:p){int z=v+c;d.push_back(z%10);c=z/10;}if(c)d.push_back(c);return pair_from_digits(d);}
string decimal(const V&d){string s;s.reserve(d.size());for(auto it=d.rbegin();it!=d.rend();++it)s.push_back('0'+*it);return s;}
uint64_t hashword(uint64_t h,uint64_t z){for(int j=0;j<8;j++){h^=(z>>(8*j))&255;h*=1099511628211ULL;}return h;}
int main(int argc,char**argv){int q=argc>1?atoi(argv[1]):6,H=argc>2?atoi(argv[2]):352;
 int variant=argc>3?atoi(argv[3]):1;bool pulse=variant==1,optimized=variant!=0;
 V P=pairs_seed(q,pulse,optimized),d=digits_from_pairs(P);
 mpz_class big(decimal(d));uint64_t h=14695981039346656037ULL;
 int minPrefix=1<<30,minB=1<<30,firstFail=-1,last=0;
 for(int t=0;t<=H;t++){
  string s=big.get_str();if(s!=decimal(d)){cerr<<"BIGINT MISMATCH at "<<t<<"\n";return 10;}
  if(equal(s.begin(),s.begin()+s.size()/2,s.rbegin())){cerr<<"PALINDROME at "<<t<<"\n";return 11;}
  if(pair_from_digits(d)!=P){cerr<<"PAIR MISMATCH at "<<t<<"\n";return 12;}
  V B=decode(BRAW[t%8]),W=decode(WRAW[t%8]);int k=0;
  while(k<d.size()/2 && P[k]==(k<39?B[k]:W[(k-39)%20]))k++;
  minPrefix=min(minPrefix,k);minB=min(minB,min(k,39));
  if(k<39 && firstFail<0)firstFail=t;
  if(t==88||t==176||t==264||t==352){int at=39+20*(q-1),bad=0,pref=0;
    for(int j=0;j<20;j++)bad+=(P[at+j]!=W[j]);
    while(pref<20&&P[at+pref]==W[pref])pref++;
    cout<<"checkpoint t="<<t<<" digit_length="<<d.size()<<" prefix="<<k<<" site="<<at<<" mismatches="<<bad<<" site_prefix="<<pref<<"\n";
  }
  h=hashword(h,(uint64_t)k);h=hashword(h,(uint64_t)d.size());h=hashword(h,(uint64_t)(t%8));
  last=d.size();if(t==H)break;
  V nd=digit_step(d),np=pair_step(P);
  if(pair_from_digits(nd)!=np){cerr<<"INDEPENDENT DIGIT/PAIR UPDATE MISMATCH at "<<t<<"\n";return 13;}
  if((int)nd.size()!=(int)d.size()+(t%2==0)){cerr<<"OVERFLOW PATTERN FAILURE at "<<t<<"\n";return 14;}
  string rev=s;reverse(rev.begin(),rev.end());big+=mpz_class(rev);
  d.swap(nd);P.swap(np);
 }
 cout<<"PASS q="<<q<<" H="<<H<<" variant="<<variant<<" initial_digits="<<pairs_seed(q,pulse,optimized).size()<<" final_digits="<<last<<" minPrefix="<<minPrefix<<" firstBadB="<<firstFail<<" fnv64="<<hex<<h<<dec<<"\n";
}