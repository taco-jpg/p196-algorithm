// Computed first defect birth for 256 adjacent centre-padding decimal seeds.
#include <bits/stdc++.h>
using namespace std;
using D=vector<uint8_t>;
D seed(int gap){string s="39"+string(gap,'0')+"43";D d;for(auto it=s.rbegin();it!=s.rend();it++)d.push_back(*it-'0');return d;}
void step(D&d){int n=d.size(),c=0;D e(n+1);for(int i=0;i<n;i++){int p=d[i]+d[n-1-i]+c;e[i]=p%10;c=p/10;}if(c)e[n]=c;else e.pop_back();d.swap(e);}
int width(const D&d){int n=d.size();for(int i=n/2-1;i>=0;--i)if(d[i]+d[n-1-i])return i+1;return 0;}
int zeros(const D&d){return d.size()-2*width(d);}
D unpad(const D&m,int delta){int n=m.size(),j=(n-delta+1)/2;D s;for(int t=j;t<j+delta;t++)if(m[t])abort();s.insert(s.end(),m.begin(),m.begin()+j);s.insert(s.end(),m.begin()+j+delta,m.end());return s;}
int diff(const D&a,const D&b,int *rad){int n=a.size(),s=(n+1)/2;if(b.size()!=n+1)return -2;int count=0;*rad=0;for(int i=0;i<(int)b.size();i++){int x=i<s?a[i]:(i==s?0:a[i-1]);if(x!=b[i]){++count;*rad=max(*rad,abs(i-s));}}return count;}
int main(){
 const int maxk=256,limit=52000,guard=100;
 D master=seed(31000+maxk);
 vector<D>x(maxk+1);
 vector<int>active(maxk+1,-1),firstzero(maxk+1,-1),firstdiff(maxk,-1),birthcount(maxk,0),birthrad(maxk,0),birthzlo(maxk,0),birthzhi(maxk,0),first16(maxk,1);
 int numpairs=0;
 for(int t=0;t<=limit;t++){
  int zm=zeros(master);
  for(int k=0;k<=maxk;k++){
   int delta=maxk-k;
   if(active[k]<0&&zm<=delta+guard){
    if(zm-delta<4){cerr<<"broken guard";return 3;}
    x[k]=unpad(master,delta);active[k]=t;
   }
   if(active[k]>=0&&firstzero[k]<0&&zeros(x[k])==0)firstzero[k]=t;
  }
  for(int k=0;k<maxk;k++)if(active[k]>=0&&active[k+1]>=0&&firstdiff[k]<0){
   int rad=0,ds=diff(x[k],x[k+1],&rad);
   if(ds==-2){cerr<<"length gap changed before first divergence t="<<t<<" k="<<k<<"\n";return 2;}
   if(ds){
    firstdiff[k]=t;birthcount[k]=ds;birthrad[k]=rad;
    birthzlo[k]=zeros(x[k]);birthzhi[k]=zeros(x[k+1]);numpairs++;
    int n=x[k].size(),m=x[k+1].size();
    for(int j=0;j<16;j++)if(x[k][j]+x[k][n-1-j]!=x[k+1][j]+x[k+1][m-1-j])first16[k]=0;
   }
  }
  if(t<limit){
   step(master);
   for(int k=0;k<=maxk;k++){
    if(active[k]<0)continue;
    bool needed=(k>0&&firstdiff[k-1]<0)||(k<maxk&&firstdiff[k]<0)||firstzero[k]<0;
    if(needed)step(x[k]);
   }
  }
 }
 if(numpairs!=maxk){cerr<<"missing pairs: "<<numpairs<<"\n";return 2;}
 cout<<"k,short_gap,long_gap,collision_short,collision_long,first_divergence,lag_from_earlier_collision,hamming_at_birth,radius_at_birth,z_short_at_birth,z_long_at_birth,first16_pair_equal\n";
 for(int k=0;k<maxk;k++){
  int c=min(firstzero[k],firstzero[k+1]);
  cout<<k<<','<<31000+k<<','<<31001+k<<','<<firstzero[k]<<','<<firstzero[k+1]<<','<<firstdiff[k]<<','<<firstdiff[k]-c<<','<<birthcount[k]<<','<<birthrad[k]<<','<<birthzlo[k]<<','<<birthzhi[k]<<','<<first16[k]<<'\n';
 }
}
