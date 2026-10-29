// Independently checks W05 exact base-10 orbit, using GMP decimal arithmetic
// AND an independently implemented schoolbook least-significant digit engine.
// Reproduce: g++ -std=c++17 -O3 w05_replay.cpp -lgmpxx -lgmp -o w05_replay
//            ./w05_replay 230 20000
#include <gmpxx.h>
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
using V=vector<int>;
const string Braw[8]={
"H501D4EC98FGHDH9144B8G09EB9B6DI947HF97D",
"8D5158982IEDFCC7B586AF7A47228AD8EBFE5HB",
"H6B2AGIG5HA8C65G2BGD1BG09E44H17I94C9CF4",
"8E8438GGCD99B9BC949B5397A498C98G8E7339A",
"H8H86HDE680040459A92B6IF09IH49ICI8F6791",
"8GGGEEC9BE804449F00C48FF6A8HCE8CCHECDGA",
"HDEEAA6049H08899A1149HBBE0IF69I56GA68E1",
"8C9A62764E788GI90225E7A4759FCG8EBD87ED6"};
const string Wraw[8]={
"H31DHBE3I12073ECF97D","CB45CA78CA327A8895HB",
"639B51FH5174F0HGIBF4","A9D1767ED68BA68FGB8A",
"2073ECF97DH31DHBE3I1","327A8895HBCB45CA78CA",
"74F0HGIBF4639B51FH51","8BA68FGB8AA9D1767ED6"};
V decode(string s){V p;for(char c:s)p.push_back(c>='A' ? c-'A'+10 : c-'0');return p;}
V initial(int q){
 V b=decode(Braw[0]),w=decode(Wraw[0]),u(40,1);
 u[13]=7;u[20]=7;u[30]=6;
 V c={8,0,0};c.insert(c.end(),u.begin(),u.end());c.push_back(16);
 c.insert(c.end(),u.rbegin(),u.rend());c.insert(c.end(),{0,0,8});
 V p=b;for(int i=0;i<q;i++)p.insert(p.end(),w.begin(),w.end());
 p.insert(p.end(),c.begin(),c.end());for(int i=0;i<q;i++)p.insert(p.end(),w.rbegin(),w.rend());
 p.insert(p.end(),b.rbegin(),b.rend());return p;
}
V digitsFromPairs(const V &p){
 int n=p.size();V d(n);
 for(int i=0;i<n/2;i++){d[i]=min(9,p[i]);d[n-1-i]=p[i]-d[i];}
 if(n%2) {if(p[n/2]%2)abort();d[n/2]=p[n/2]/2;}
 if(d.back()==0)abort();return d;
}
string decimal(const V &d){string s;s.reserve(d.size());for(auto i=d.rbegin();i!=d.rend();i++)s.push_back(char('0'+*i));return s;}
V schoolbook(const V &d){V out;out.reserve(d.size()+1);int c=0,n=d.size();for(int i=0;i<n;i++){int x=d[i]+d[n-1-i]+c;out.push_back(x%10);c=x/10;}if(c)out.push_back(c);return out;}
int main(int argc,char**argv){int q=argc>1?atoi(argv[1]):230;int H=argc>2?atoi(argv[2]):20000;V d=digitsFromPairs(initial(q));mpz_class g(decimal(d));uint64_t hash=14695981039346656037ULL;
 int minMatch=2147483647,firstFailure=-1,lastL=0;
 for(int t=0;t<=H;t++){
  string s=g.get_str();if(s!=decimal(d)){cerr<<"INTEGER ENGINE DISAGREEMENT "<<t<<"\n";return 2;}
  string rs=s;reverse(rs.begin(),rs.end());if(s==rs){cerr<<"PALINDROME "<<t<<"\n";return 3;}
  int phase=t%8;V b=decode(Braw[phase]),w=decode(Wraw[phase]);int n=d.size(),h=n/2;
  int matched=0;
  for(int i=0;i<h;i++){
    int x=d[i]+d[n-1-i],expected=i<39?b[i]:w[(i-39)%20];
    if(x!=expected)break;
    matched++;
  }
  if(matched<39+20 && firstFailure<0)firstFailure=t;
  minMatch=min(minMatch,matched);lastL=n;
  for(uint64_t k: {(uint64_t)matched,(uint64_t)n,(uint64_t)(t%8)}){
   for(int j=0;j<8;j++){hash^=(k>>(8*j))&255;hash*=1099511628211ULL;}
  }
  if(t==H)break;
  V next=schoolbook(d);
  g+=mpz_class(rs);
  if((int)next.size()!=n+(t%2==0)){cerr<<"OVERFLOW FAIL "<<t<<"\n";return 4;}
  d.swap(next);
  if(t>0 && t%5000==0)cerr<<"checkpoint "<<t<<" prefix="<<matched<<" len="<<n<<"\n";
 }
 cout<<"W05 PASS q="<<q<<" H="<<H<<" initial_digits="<<initial(q).size()<<" final_digits="<<lastL<<" min_prefix="<<minMatch<<" first_prefix_under_59="<<firstFailure<<" FNV64="<<hex<<hash<<dec<<"\n";
 return 0;
}
