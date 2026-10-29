#include <bits/stdc++.h>
using namespace std;
using Row=array<int,6>;
Row norm(Row x,bool f){for(int c0=0;c0<2;c0++){int c=c0;Row y{};for(int k=0;k<6;k++){int i=f?k:5-k,z=x[i]+c;y[i]=z%10;c=z/10;}if(c==c0)return y;}abort();}
Row nxt(Row x,int g){Row a=norm(x,true),b=norm(x,false),z{};for(int i=0;i<6;i++)z[i]=a[i]+b[(i+6-g)%6];return z;}
int main(){map<int,int> periods;vector<tuple<int,int,Row>> hits;int n=0,ambiguous=0;
 for(int a=0;a<19;a++)for(int b=0;b<19;b++)for(int c=0;c<19;c++){
  if(a==9&&b==9&&c==9)continue;
  Row row{a,b,c,c,b,a};map<pair<int,Row>,int> seen;int t=0,mu=-1,period=0;
  for(;t<2000;t++){
   if(row==Row{9,9,9,9,9,9}){ambiguous++;break;}auto key=make_pair(t%2,row);if(seen.count(key)){mu=seen[key];period=t-mu;break;}seen[key]=t;row=nxt(row,1-t%2);
  }
  if(period==0)continue;periods[period]++;n++;if(period<=24&&period>=12)hits.push_back({period,mu,{a,b,c,c,b,a}});
 }
 cout<<"decided="<<n<<" neutral_ambiguous="<<ambiguous<<" periods:";for(auto [p,count]:periods)cout<<" "<<p<<":"<<count;cout<<"\n";
 sort(hits.begin(),hits.end());for(int i=0;i<min(50,(int)hits.size());i++){auto [p,mu,x]=hits[i];cout<<"p="<<p<<" mu="<<mu<<" r=";for(auto v:x)cout<<v<<",";cout<<"\n";}
}
