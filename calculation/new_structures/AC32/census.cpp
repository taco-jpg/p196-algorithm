#include <array>
#include <vector>
#include <string>
#include <algorithm>
#include <iostream>
#include <cstdlib>
#include <cstdint>
using namespace std;
// Genuine decimal reverse-and-add; no strict W9 phase pruning.
const vector<int> B={5,2,3,3,3,16,9,7,18,6,0,1,5,8,13,9,18,12,12,8,12,8,17,9,6,14,5,18,14,11,12,11,9,12};
const vector<int> W={2,9,2,4,0,17,11,9,12};
void build(const int J[5],const int U[3],int ci,int q,int k,vector<uint8_t>&d,vector<uint8_t>&target){
 vector<int> h;h.reserve(34+9*q+5+3*k);h.insert(h.end(),B.begin(),B.end());
 for(int i=0;i<q;i++)h.insert(h.end(),W.begin(),W.end());
 for(int i=0;i<5;i++)h.push_back(J[i]);
 for(int i=0;i<k;i++)for(int u=0;u<3;u++)h.push_back(U[u]);
 int n=h.size()*2+(ci==0?3:2);d.resize(n);target.resize(n+30);
 auto coeff=[&](int index)->int{
  int j=min(index,n-1-index);
  if(j<(int)h.size())return h[j];
  return ci==0?(j==(int)h.size()?4:14):4;
 };
 for(int i=0;i<n/2;i++){
  int v=coeff(i),hi=min(v,9),lo=v-hi;d[i]=lo;d[n-1-i]=hi;
 }
 if(n%2)d[n/2]=7;
 vector<int> h2;h2.reserve(h.size()+15);
 h2.insert(h2.end(),B.begin(),B.end());
 for(int i=0;i<q;i++)h2.insert(h2.end(),W.begin(),W.end());
 for(int i=0;i<5;i++)h2.push_back(J[i]);
 for(int i=0;i<k+5;i++)for(int u=0;u<3;u++)h2.push_back(U[u]);
 int t=n+30;
 for(int i=0;i<t;i++){
  int j=min(i,t-1-i);
  target[i]=j<(int)h2.size()?h2[j]:(ci==0?(j==(int)h2.size()?4:14):4);
 }
}
void orbit(vector<uint8_t>&d,vector<uint8_t>&buf,int&len,int steps=120){
 for(int t=0;t<steps;t++){
  int c=0;
  for(int i=0;i<len;i++){
   int z=d[i]+d[len-1-i]+c;buf[i]=z%10;c=z/10;
  }
  if(c)buf[len++]=c;
  d.swap(buf);
 }
}
int main(int argc,char**argv){
 int q=argc>1?atoi(argv[1]):14,k=argc>2?atoi(argv[2]):100;
 int count=argc>3?atoi(argv[3]):10000,start=argc>4?atoi(argv[4]):0;
 int oddgate=argc>5?atoi(argv[5]):0,considered=0;
 vector<uint8_t>d,tgt,buf;d.reserve(4096);tgt.reserve(4096);buf.reserve(4096);
 array<long long,2048>hist{};int gate=0,shortBad=0,equal=0,firstmin=10000,firstmax=-1;
 auto mod11=[](int a){return (a%11+11)%11;};
 for(int i0=start;i0<start+count;i0++){
  int rank=(i0/(2*2476099))%30,ci=(i0/2476099)%2,jword=i0%2476099;
  int a=(rank/3)*2;int U[3]={9,a,18-a};rotate(U,U+rank%3,U+3);
  int J[5];for(int i=0;i<5;i++){J[i]=jword%19;jword/=19;}
  if(oddgate){
   if(ci!=0)continue;
   int au=U[0]-U[1]+U[2],aj=J[0]-J[1]+J[2]-J[3]+J[4];
   // For phase 11, C=[4,14,4], uniform all-q,k mod-11 constraints:
   // A(U)=-6 (mod11) and 2*A(J)+18=0 (mod11).
   if(mod11(au+6)!=0||mod11(2*aj+18)!=0)continue;
  }
  considered++;build(J,U,ci,q,k,d,tgt);
  int n=d.size();buf.resize(n+200);d.resize(n+200);
  orbit(d,buf,n);
  if(n!=(int)tgt.size())shortBad++;
  int first=0;
  while(first<n&&first<(int)tgt.size()){
   if(d[first]+d[n-1-first]!=tgt[first])break;
   first++;
  }
  if(first>=n||first>=(int)tgt.size()){
   if(n==(int)tgt.size())equal++;
   continue;
  }
  hist[min(first,2047)]++;firstmin=min(firstmin,first);firstmax=max(firstmax,first);
  if(first>=34+9*q)gate++;
 }
 cout<<"COUNT "<<count<<" start="<<start<<" q="<<q<<" k="<<k<<" tested="<<considered
     <<" equal="<<equal<<" W9_survivors="<<gate<<" length_mismatches="<<shortBad
     <<" first_range="<<firstmin<<":"<<firstmax<<"\n";
 for(int i=0;i<(int)hist.size();i++)if(hist[i])cout<<i<<":"<<hist[i]<<" ";
 cout<<"\n";
}
