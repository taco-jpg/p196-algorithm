// W09 independent base-1000 big-integer arithmetic; no pairword transition in the engine.
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <string>
using namespace std;
using Big=vector<uint16_t>;
static vector<int> L={7,12,16,10,7,4,12,8,15,13,17,1,17,18,16,3,5,0,2,12,18,10,1};
static const int PH[]={8,16,14,10,2,4};
string seed(int k){
 string s;for(int x:L)s+=char('0'+x-x/2);
 s+=string(2*k,'4');
 for(int i=int(L.size())-1;i>=0;i--)s+=char('0'+L[i]/2);
 return s;
}
Big parse(const string &s){
 Big b;for(int j=s.size();j>0;j-=3){
  int u=0;for(int i=max(0,j-3);i<j;i++)u=10*u+s[i]-'0';
  b.push_back(uint16_t(u));
 }
 while(b.size()>1&&b.back()==0)b.pop_back();
 return b;
}
string repr(const Big &b){
 string s=to_string(b.back());char buf[5];
 for(int i=(int)b.size()-2;i>=0;i--){
  snprintf(buf,sizeof(buf),"%03u",unsigned(b[i]));s+=buf;
 }
 return s;
}
Big add(const Big &a,const Big &b){
 Big c;int carry=0;
 for(size_t i=0;i<max(a.size(),b.size());i++){
  int v=carry;if(i<a.size())v+=a[i];if(i<b.size())v+=b[i];
  c.push_back(v%1000);carry=v/1000;
 }
 if(carry)c.push_back(carry);return c;
}
int width(const string &s,int x){
 int l=(int(s.size())-1)/2,r=s.size()/2;
 while(l>=0&&r<(int)s.size()&&s[l]-'0'+s[r]-'0'==x){--l;++r;}
 return r-l-1;
}
uint64_t hash_lsd(const string &s){
 uint64_t h=14695981039346656037ULL;
 for(int i=(int)s.size()-1;i>=0;i--){h^=s[i]-'0';h*=1099511628211ULL;}
 return h;
}
int main(int argc,char **argv){
 int k=argc>1?atoi(argv[1]):22000,T=argc>2?atoi(argv[2]):20000;
 if(argc>3){stringstream ss(argv[3]);string part;L.clear();while(getline(ss,part,','))if(!part.empty())L.push_back(stoi(part));if(L.empty()||L[0]<1)return 2;}
 Big a=parse(seed(k));int pal=0,bad=-1,minW=100000,maxGain=-100000;
 long long gam=0;int oldlen=0;
 for(int t=0;t<=T;t++){
  string s=repr(a);
  if(t>0)gam+=int(s.size())-oldlen;
  oldlen=s.size();
  int w=width(s,PH[t%6]);minW=min(minW,w);maxGain=max(maxGain,w-2*k);
  if(w<1 && bad<0)bad=t;
  bool ispal=equal(s.begin(),s.begin()+s.size()/2,s.rbegin());
  bool odd=false;
  for(int i=0;i<(int)s.size()/2;i++)
   if(((s[i]-'0')+(s[s.size()-1-i]-'0'))%2){odd=true;break;}
  pal+=ispal;
  if(t==0||t<=12||t==18||t==24||t==30||t==36||
     (argc>3&&t==60)||t==100||t==1000||t==5000||t==10000||t==15000||t==20000)
    cout<<"t="<<t<<" digits="<<s.size()<<" width="<<w<<" gain="<<w-2*k
        <<" odd="<<odd<<" pal="<<ispal<<" overflow="<<gam
        <<" fnv="<<hex<<hash_lsd(s)<<dec<<"\n";
  if(t<T){string r(s.rbegin(),s.rend());a=add(a,parse(r));}
 }
 cout<<"TOTAL "<<T<<" pal="<<pal<<" firstShapeFailure="<<bad
     <<" minCentral="<<minW<<" maxGain="<<maxGain<<" gammas="<<gam<<"\n";
 return (pal||bad>=0)?1:0;
}
