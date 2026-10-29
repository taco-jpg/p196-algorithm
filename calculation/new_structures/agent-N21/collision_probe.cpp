#include <bits/stdc++.h>
using namespace std;using V=vector<uint8_t>;
const array<int,34> B={2,11,1,6,8,1,7,15,9,3,9,4,7,9,10,16,9,11,4,10,8,8,9,11,11,7,4,3,9,12,1,1,9,11};
const array<int,9> W={1,10,8,5,9,16,0,9,11};
const array<int,11> K={6,1,0,1,11,14,10,6,11,16,1};
V base(){int n=70000;V p(n);for(int i=0;i<n/2;i++)p[i]=p[n-1-i]=i<34?B[i]:W[(i-34)%9];return p;}
V patch(V p,initializer_list<int> sites){int n=p.size();for(int a:sites)for(int j=0;j<11;j++)p[a+j]=p[n-1-a-j]=K[j];return p;}
V next(const V &p){int n=p.size(),c=0;V d(n+1),q;for(int i=0;i<n;i++){int z=p[i]+c;d[i]=z%10;c=z/10;}if(!c)d.pop_back();else d[n]=c;int m=d.size();q.resize(m);for(int i=0;i<m;i++)q[i]=d[i]+d[m-1-i];return q;}
void dump(int t,int j,const V &p){cout<<"SNAP "<<t<<" "<<j<<" ";const char*hex="0123456789";for(auto x:p){cout<<hex[x/10]<<hex[x%10];}cout<<'\n';}
int main(){V p=base();array<V,4> a={p,patch(p,{8000}),patch(p,{22000}),patch(p,{8000,22000})};int first_overlap=-1,first_nonlinear=-1;int final_bad=-1;
 for(int t=0;t<=22644;t++){if(t%2000==0)cerr<<"PROGRESS "<<t<<"\n";
  int n=a[0].size(),maxl=-1,minr=INT_MAX,bad=0;vector<int> positions;
  for(int i=0;i<n/2;i++){
   if(a[1][i]!=a[0][i])maxl=i;
   if(a[2][i]!=a[0][i] && i<minr)minr=i;
   if(int(a[0][i])+int(a[3][i])!=int(a[1][i])+int(a[2][i])){bad++;if(bad<=4)positions.push_back(i);}
  }
  if(maxl>=minr && first_overlap<0)first_overlap=t;
  if(bad && first_nonlinear<0){first_nonlinear=t;assert(t==22506);assert(bad==3);assert((positions==vector<int>{17781,17782,17783}));
   for(int i=17781;i<=17783;i++)cerr<<"CORRECTION i="<<i<<" predicted="<<int(a[1][i])+int(a[2][i])-int(a[0][i])<<" actual="<<int(a[3][i])<<"\n";
  }
  if(t==22500||t==22506)for(int j=0;j<4;j++)dump(t,j,a[j]);
  if(t==22502||t==22503||t==22505||t==22506||t==22507||t==22508||t==22536||t==22644)
   cerr<<"TRACE t="<<t<<" gap="<<minr-maxl-1<<" nonlinear="<<bad<<"\n";
  if(t==22644)final_bad=bad;
  if(t<22644)for(auto &q:a)q=next(q);
 }
 assert(first_overlap==22503&&first_nonlinear==22506&&final_bad==86);
 cout<<"SUMMARY first_overlap=22503 first_nonlinear=22506 initial_residual=3 residual_22644=86\n";
}
