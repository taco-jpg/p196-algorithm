// W23 dense-packet physical radix-10 digit-vector independent control.
// g++ -O3 -std=c++17 packed_digit.cpp -o /tmp/w23_packed && /tmp/w23_packed
#include <vector>
#include <iostream>
#include <cassert>
#include <algorithm>
using namespace std;using V=vector<int>;
const V B={17,5,0,2,1,9,15,18,14,9,3};
const V W={4,4,14,1,5,11,7,1,15,12,7,9,9,12,14,4,0,6,5,17,13,9,7,3,13,10,4,13,5,1,9,4,11,6,16,3,7,7,12,4,2,13,2,15,10,10,9,3};
V seed(int q,int mode){
 V h=B;for(int i=0;i<q;i++)h.insert(h.end(),W.begin(),W.end());
 h.insert(h.end(),{10,14,1,10});
 int M=q-4;
 for(int j=0;j<M;j++)if(mode==2||(mode==1&&j%2==0)){
  int pos=11+48*(2+j)+20;assert(h[pos]==13 && h[pos+1]==9);
  h[pos]=8;h[pos+1]=5;
 }
 int n=(int)h.size()*2-1;V d(n);
 for(int i=0;i<(int)h.size()-1;i++){
  int p=h[i];d[i]=max(0,p-9);d[n-1-i]=min(9,p);
 }
 d[h.size()-1]=5;return d;
}
void step(V&d){
 int n=d.size(),carry=0;V z;z.reserve(n+1);
 for(int i=0;i<n;i++){
  int s=d[i]+d[n-1-i]+carry;z.push_back(s%10);carry=s/10;
 }
 if(carry)z.push_back(carry);d.swap(z);
}
V pairword(const V&d){
 V p(d.size());for(int i=0;i<(int)d.size();i++)p[i]=d[i]+d[d.size()-1-i];
 return p;
}
bool palindrome(const V&d){
 for(int i=0,j=d.size()-1;i<j;i++,j--)if(d[i]!=d[j])return false;
 return true;
}
int main(){
 int q=100;V a=seed(q,0),b=seed(q,1),c=seed(q,2);
 assert(a!=b &&b!=c &&a!=c);
 for(int t=0;t<4;t++){
  assert(!palindrome(a)&&!palindrome(b)&&!palindrome(c));
  if(t==3)assert(pairword(a)==pairword(b)&&pairword(a)==pairword(c));
  step(a);step(b);step(c);
 }
 assert(a==b&&b==c);
 cout<<"PASS q=100 M=96: none/alternating/all of 96 dense patches coalesce at t=4 (physical decimal digits)\n";
}
