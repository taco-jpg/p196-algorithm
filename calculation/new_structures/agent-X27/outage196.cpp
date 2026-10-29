// Independent literal decimal digit replay of 196: all-even pairword outages.
#include <bits/stdc++.h>
using namespace std;
int main(int argc,char**argv){int T=argc>1?atoi(argv[1]):100000;vector<unsigned char>d={6,9,1};int ct=0,rep=0,nohigh=0;
for(int t=0;t<=T;t++){
 int n=d.size();bool alleven=true;int j=-1;
 for(int i=0;i<(n+1)/2;i++){
    int p=d[i]+d[n-1-i];if(p&1)alleven=false;if(j<0&&p>=10)j=i;
 }
 if(alleven){
   ct++;
   vector<unsigned char>e(n);int c=0;
   for(int i=0;i<n;i++){int v=d[i]+d[n-1-i]+c;e[i]=v%10;c=v/10;}
   if(c)e.push_back(1);
   int ix=max(0,j-1);
   bool pal=true;for(int i=0;i<e.size()/2;i++)if(e[i]!=e[e.size()-1-i])pal=false;
   if(j<0){nohigh++;if(!pal){cerr<<"NOHIGH NOT PAL t="<<t<<"\n";return 2;}}
   else {rep++;if(ix>=e.size()/2||!((e[ix]+e[e.size()-1-ix])&1)){cerr<<"FAIL t="<<t<<" j="<<j<<"\n";return 3;}}
   cout<<"OUTAGE t="<<t<<" digits="<<n<<" firstHigh="<<j<<" successorOddIndex="<<ix<<" successorPal="<<pal<<"\n";
 }
 if(t==T)break;vector<unsigned char>o(n);int c=0;for(int i=0;i<n;i++){int v=d[i]+d[n-1-i]+c;o[i]=v%10;c=v/10;}if(c)o.push_back(1);d.swap(o);
}
cout<<"SUMMARY T="<<T<<" finalDigits="<<d.size()<<" allEven="<<ct<<" regenerated="<<rep<<" noHigh="<<nohigh<<"\n";
}
