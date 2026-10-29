#include <bits/stdc++.h>
using namespace std; using V=vector<uint8_t>;
const int F[6]={8,16,14,10,2,4}, G[6]={10,2,4,8,16,14};
V makepair(int A,int L,int C){V p;p.insert(p.end(),A,8);p.insert(p.end(),L,9);p.insert(p.end(),C,10);p.insert(p.end(),L,9);p.insert(p.end(),A,8);return p;}
string frompair(const V&p){int n=p.size();string s(n,'0');for(int i=0;i<n/2;i++){int lo=min(int(p[i]),9),hi=int(p[i])-lo;if(i==0){hi=8;lo=int(p[i])-hi;}s[n-1-i]='0'+lo;s[i]='0'+hi;}if(n%2)s[n/2]='0'+int(p[n/2])/2;assert(s[0]!='0');return s;}
V getpair(const string&s){int n=s.size();V p(n);for(int i=0;i<n;i++)p[i]=s[i]+s[n-1-i]-2*'0';return p;}
string stepint(const string&s){int n=s.size(),carry=0;string out(n,'0');for(int i=0;i<n;i++){int z=(s[n-1-i]-'0')+(s[i]-'0')+carry;out[n-1-i]='0'+z%10;carry=z/10;}if(carry)out.insert(out.begin(),'1');return out;}
V steppair(const V&p,int&carry){V o;o.reserve(p.size()+1);carry=0;for(auto x:p){int z=x+carry;o.push_back(z%10);carry=z/10;}if(carry)o.push_back(carry);int n=o.size();V q(n);for(int i=0;i<n;i++)q[i]=o[i]+o[n-1-i];return q;}
pair<int,int> runpos(const V&v,int q){int n=0,m=0,start=0,cur=0;for(int i=0;i<int(v.size())/2;i++){auto x=v[i];if(x==q){if(!n)cur=i;n++;if(n>m){m=n;start=cur;}}else n=0;}return {start,m};}
int main(int argc,char**argv){int A=argc>1?atoi(argv[1]):14000,L=argc>2?atoi(argv[2]):8000,C=argc>3?atoi(argv[3]):16000,H=argc>4?atoi(argv[4]):20000;
 V p=makepair(A,L,C);string s=frompair(p);int total=0,min9=INT_MAX,minx=INT_MAX,miny=INT_MAX;
 cout<<"CONFIG "<<A<<" "<<L<<" "<<C<<" "<<H<<"\n";
 for(int t=0;t<=H;t++){
  if(getpair(s)!=p){cerr<<"PAIR MISMATCH "<<t<<"\n";return 2;}
  auto rp9=runpos(p,9),rpx=runpos(p,F[t%6]),rpy=runpos(p,G[t%6]);
  int a=rp9.second,x=rpx.second,y=rpy.second;
  if(!(rpx.first+x<=rp9.first && rp9.first+a<=rpy.first)){cerr<<"ORDER FAIL t="<<t<<"\n";return 6;}
  min9=min(min9,a);minx=min(minx,x);miny=min(miny,y);
  if(!a || (A==14000&&L==8000&&C==16000&&H==20000&&(a<1100||x<600||y<1300))){cerr<<"SHAPE FAIL t="<<t<<"\n";return 3;}
  if(s==string(s.rbegin(),s.rend())){cerr<<"PALINDROME t="<<t<<"\n";return 4;}
  if(t<=6||t%1000==0||t==H){cout<<"t="<<t<<" n="<<s.size()<<" g="<<total<<" 9="<<a<<" x="<<x<<" y="<<y<<" seamL="<<rp9.first-rpx.first-x<<" seamR="<<rpy.first-rp9.first-a<<"\n";}
  if(t==H)break;
  int gamma;V p2=steppair(p,gamma);string s2=stepint(s);
  if(int(s2.size())-int(s.size())!=gamma){cerr<<"OVERFLOW MISMATCH "<<t<<"\n";return 5;}
  s.swap(s2);p.swap(p2);total+=gamma;
 }
 cout<<"PASS min9="<<min9<<" minx="<<minx<<" miny="<<miny<<" final="<<s.size()<<" totalgamma="<<total<<"\n";
 ofstream("w22_final_digits.txt")<<s;return 0;
}
