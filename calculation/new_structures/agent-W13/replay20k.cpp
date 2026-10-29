// W13: independent ordinary decimal digit vector and GMP integer replay.
#include <bits/stdc++.h>
#include <gmpxx.h>
using namespace std;
using V=vector<unsigned char>;
const int B[]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
const int W[]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
const int repl[9][3]={{11,14,3},{6,6,7},{6,6,16},{6,15,7},{6,15,16},{15,6,7},{15,6,16},{15,15,7},{15,15,16}};
V coefficients(int q,int M,bool altered){
 assert(q>=30+10*M && M>=0);
 V half(begin(B),end(B));
 for(int j=0;j<q;j++)half.insert(half.end(),begin(W),end(W));
 half.push_back(0);
 if(altered)for(int m=0;m<M;m++){
   int j=39+20*(30+10*m)+5;int choice=1+(m%8);
   for(int k=0;k<3;k++)half[j+k]=repl[choice][k];
 }
 V p=half;
 for(int j=int(half.size())-2;j>=0;j--)p.push_back(half[j]);
 return p;
}
V digits(const V &p){
 assert((p.size()&1) && p[p.size()/2]%2==0);V d(p.size(),0);
 for(size_t i=0;i<p.size()/2;i++){d[i]=min(9,int(p[i]));d[p.size()-i-1]=p[i]-d[i];}
 d[p.size()/2]=p[p.size()/2]/2; assert(d.back()!=0);return d;
}
V pairword(const V&d){V p(d.size());for(size_t i=0;i<d.size();i++)p[i]=d[i]+d[d.size()-i-1];return p;}
V add_reverse(const V&d){V out;out.reserve(d.size()+1);int carry=0;
 for(size_t i=0;i<d.size();i++){int s=d[i]+d[d.size()-i-1]+carry;out.push_back(s%10);carry=s/10;}
 if(carry)out.push_back(carry);assert(out.back());return out;
}
string spelling(const V&d){string s; s.reserve(d.size());for(auto it=d.rbegin();it!=d.rend();it++)s.push_back(char('0'+*it));return s;}
bool pal(const V&d){return equal(d.begin(),d.begin()+d.size()/2,d.rbegin());}
string checksum(const V&d){uint64_t h=1469598103934665603ull;
 for(int v:d){h^=uint64_t(v);h*=1099511628211ull;}char buf[32];snprintf(buf,sizeof(buf),"%016llx",(unsigned long long)h);return buf;}
int main(int argc,char**argv){int q=argc>1?atoi(argv[1]):300;int M=argc>2?atoi(argv[2]):25;int steps=argc>3?atoi(argv[3]):20000;
 V origin=digits(coefficients(q,M,false)),pert=digits(coefficients(q,M,true));
 V a=origin,b=pert;assert(pairword(a)!=pairword(b));
 for(int t=0;t<=4;t++){
  if(pal(a)||pal(b))throw runtime_error("palindrome in first 4");
  if(t==3&&pairword(a)!=pairword(b))throw runtime_error("no coalescence at pair t3");
  if(t==4&&a!=b)throw runtime_error("no integer coalescence at t4");
  if(t<4){a=add_reverse(a);b=add_reverse(b);}
 }
 a=origin;mpz_class n(spelling(origin));int overflows=0;V phase[8];constexpr int keep=39+20*60;
 for(int t=0;t<=steps;t++){
  if(pal(a))throw runtime_error("palindrome digit-array");
  V pw=pairword(a); if(int(pw.size())<keep)throw runtime_error("short band");
  if(t<8){phase[t]=V(pw.begin(),pw.begin()+keep);
    for(int j=0;j<60;j++)for(int k=0;k<20;k++)
      if(pw[39+20*j+k]!=pw[39+k])throw runtime_error("initial bulk");
  }else if(!equal(phase[t%8].begin(),phase[t%8].end(),pw.begin()))
    throw runtime_error("phase-8 bulk lost at "+to_string(t));
  bool odd=false;for(int j=0;j<39;j++)odd|=pw[j]&1;
  if(!odd)throw runtime_error("odd exterior witness lost");
  string s=n.get_str();
  if(s!=spelling(a))throw runtime_error("GMP / digit-vector mismatch at "+to_string(t));
  if(equal(s.begin(),s.begin()+s.size()/2,s.rbegin()))throw runtime_error("palindrome GMP");
  if(t==steps)break;
  auto len=a.size();a=add_reverse(a);overflows+=int(a.size()>len);
  reverse(s.begin(),s.end());mpz_class rev(s);n+=rev;
 }
 cout<<"W13_PASS q="<<q<<" packets="<<M<<" variants="<<"9^"<<M
     <<" steps="<<steps<<" initial_digits="<<origin.size()
     <<" final_digits="<<a.size()<<" overflows="<<overflows
     <<" fnv64="<<checksum(a)<<"\n";
}
