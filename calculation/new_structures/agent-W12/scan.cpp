// Reproduce the 2..6 motif discovery; fixed caps 12 and 34, q=45.
#include <algorithm>
#include <iostream>
#include <map>
#include <string>
using namespace std;
string step(const string&s){
 int n=(int)s.size(),c=0;string t(n+1,'0');
 for(int i=0;i<n;i++){int x=s[i]-'0'+s[n-1-i]-'0'+c;t[n-i]='0'+x%10;c=x/10;}
 t[0]='0'+c;if(!c)t.erase(t.begin());return t;
}
string canon(const string&s){
 int n=(int)s.size(),l=n/2-20,r=n/2+20;
 for(int p=1;p<=6;p++){
  bool ok=true;for(int i=l+p;i<r;i++)if(s[i]!=s[i-p]){ok=false;break;}
  if(ok){string w=s.substr(l,p),best=w;
   for(int j=1;j<p;j++)best=min(best,w.substr(j)+w.substr(0,j));
   return best;
  }
 }
 return "?";
}
int main(){
 map<string,int> first;
 for(int m=2;m<=6;m++){
  int total=1,recurrent=0,nontrivial=0;
  for(int j=0;j<m;j++)total*=10;
  for(int x=0;x<total;x++){
   int v=x;string w(m,'0');
   for(int j=m-1;j>=0;j--){w[j]='0'+v%10;v/=10;}
   string s="12";for(int j=0;j<45;j++)s+=w;s+="34";
   string start=canon(s),last;bool pal=false;
   for(int j=0;j<=3;j++){
    if(equal(s.begin(),s.end(),s.rbegin()))pal=true;
    if(j<3)s=step(s);
   }
   last=canon(s);
   if(start==last&&start!="?"){
    recurrent++;
    if(start.size()>1&&!pal){nontrivial++;if(!first.count(start))first[start]=x;}
   }
  }
  cout<<"m="<<m<<" total="<<total<<" returned="<<recurrent
      <<" nonconstant_nonpal="<<nontrivial<<"\n";
 }
 for(auto [w,x]:first)cout<<"bulk_return="<<w<<" example="<<x<<"\n";
}
