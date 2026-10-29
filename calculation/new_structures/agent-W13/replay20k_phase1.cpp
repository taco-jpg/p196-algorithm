// W13 independent ordinary-integer replay of four-step p8 precursor family.
#include <bits/stdc++.h>
#include <gmpxx.h>
using namespace std;using V=vector<unsigned char>;
const int B[]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
const int W[]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
const int repl[3][3]={{3,2,7},{5,16,0},{1,6,5}};
V pairword(const V&d){V p(d.size());for(size_t i=0;i<d.size();i++)p[i]=d[i]+d[d.size()-1-i];return p;}
V norm(V p){V d;int c=0;d.reserve(p.size()+1);for(int v:p){int z=v+c;d.push_back(z%10);c=z/10;}if(c)d.push_back(c);return pairword(d);}
V source(int q,int M,bool altered){assert(q>=30+10*M);V h(begin(B),end(B));for(int k=0;k<q;k++)h.insert(h.end(),begin(W),end(W));h.push_back(0);
 V p=h;for(int i=int(h.size())-2;i>=0;i--)p.push_back(h[i]);p=norm(p);
 if(altered)for(int m=0;m<M;m++){int j=39+20*(30+10*m)+10;assert(p[j]==3 && p[j+1]==2 && p[j+2]==7);int which=1+m%2;for(int k=0;k<3;k++)p[j+k]=p[p.size()-1-j-k]=repl[which][k];}
 return p;}
V digits(const V&p){assert(p.size()%2==0);V d(p.size());for(size_t i=0;i<p.size()/2;i++){d[i]=min(9,int(p[i]));d[p.size()-1-i]=p[i]-d[i];}if(d.back()==0){assert(d.front());d.front()--;d.back()++;}assert(d.back());assert(pairword(d)==p);return d;}
V addreverse(const V&d){V r;int c=0;for(size_t i=0;i<d.size();i++){int z=d[i]+d[d.size()-1-i]+c;r.push_back(z%10);c=z/10;}if(c)r.push_back(c);return r;}
string spell(const V&d){string s;for(auto i=d.rbegin();i!=d.rend();i++)s+=char('0'+*i);return s;}
bool pal(const V&d){return equal(d.begin(),d.begin()+d.size()/2,d.rbegin());}
string fnv(const V&d){uint64_t h=1469598103934665603ULL;for(int x:d){h^=x;h*=1099511628211ULL;}char buff[40];snprintf(buff,sizeof(buff),"%016llx",(unsigned long long)h);return buff;}
int main(int argc,char**argv){int q=argc>1?atoi(argv[1]):300;int M=argc>2?atoi(argv[2]):25;int steps=argc>3?atoi(argv[3]):20000;
 V a=digits(source(q,M,false)),b=digits(source(q,M,true));assert(a!=b);
 for(int t=0;t<=5;t++){
  if(pal(a)||pal(b))throw runtime_error("early palindrome");
  if(t==4&&pairword(a)!=pairword(b))throw runtime_error("pairword fails four-step erasure");
  if(t==5&&a!=b)throw runtime_error("integers fail five-step merge");
  if(t<5){a=addreverse(a);b=addreverse(b);}
 }
 a=digits(source(q,M,false));mpz_class n(spell(a));int overflows=0;V phase[8];constexpr int keep=39+20*60;
 for(int t=0;t<=steps;t++){
  V p=pairword(a);if(int(p.size())<keep)throw runtime_error("band exhausted");
  bool odd=false;for(int i=0;i<39;i++)odd|=p[i]&1;if(!odd)throw runtime_error("nonpalindrome witness exhausted");
  if(t<8){phase[t]=V(p.begin(),p.begin()+keep);for(int j=1;j<60;j++)for(int k=0;k<20;k++)if(p[39+20*j+k]!=p[39+k])throw runtime_error("not spatial periodic");}
  else if(!equal(phase[t%8].begin(),phase[t%8].end(),p.begin()))throw runtime_error("temporal bulk lost at "+to_string(t));
  string s=n.get_str();if(s!=spell(a))throw runtime_error("GMP/digit discrepancy");
  if(pal(a)||equal(s.begin(),s.begin()+s.size()/2,s.rbegin()))throw runtime_error("palindrome");
  if(t==steps)break;
  auto len=a.size();a=addreverse(a);overflows+=a.size()>len;
  reverse(s.begin(),s.end());n+=mpz_class(s);
 }
 cout<<"W13_PHASE1_PASS q="<<q<<" M="<<M<<" seeds=3^"<<M<<" steps="<<steps
     <<" start_digits="<<source(q,M,false).size()<<" final_digits="<<a.size()
     <<" overflows="<<overflows<<" final_fnv="<<fnv(a)<<"\n";
}
