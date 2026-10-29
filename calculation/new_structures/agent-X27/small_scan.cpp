#include <bits/stdc++.h>
using namespace std;
int main(int argc,char**argv){int T=argc>1?atoi(argv[1]):5000,K=argc>2?atoi(argv[2]):32;vector<int> survive;int best=0,bestseed=0;
for(int seed=10;seed<=999;seed++){
 vector<unsigned char>d;for(int n=seed;n;n/=10)d.push_back(n%10);
 int t=0;for(;t<=T;t++){int n=d.size(),i=0;for(;i<n/2&&i<K;i++){if((d[i]+d[n-1-i])&1)break;}if(i==min(K,n/2))break;if(t==T)break;vector<unsigned char>o(n);int c=0;for(int j=0;j<n;j++){int x=d[j]+d[n-1-j]+c;o[j]=x%10;c=x/10;}if(c)o.push_back(1);d.swap(o);}if(t==T)survive.push_back(seed);if(t>best){best=t;bestseed=seed;}
}cout<<"T="<<T<<" K="<<K<<" survivors="<<survive.size()<<" best="<<best<<" seed="<<bestseed<<"\n";for(auto v:survive)cout<<v<<" ";cout<<"\n";}
