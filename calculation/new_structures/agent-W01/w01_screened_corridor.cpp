// W01 experimental three-body interaction: 8 literal decimal reverse-add orbits.
#include <bits/stdc++.h>
using namespace std;using V=vector<unsigned char>;
constexpr int ROOT[39]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
constexpr int BULK[20]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
V seed(int h,int mask,int X,int Y,int Z){V a(2*h);for(int j=0;j<h;j++){
 int q=j<39?ROOT[j]:BULK[(j-39)%20];
 if(mask&1 && j>=X&&j<X+50)q=(7*j+11)%19;
 if(mask&2 && j>=Y&&j<Y+50)q=(3*(j-Y)+10)%19;
 if(mask&4 && j>=Z&&j<Z+50)q=(5*(j-Z)+3)%19;
 a[j]=min(q,9);a[2*h-1-j]=q-a[j];}return a;}
void step(V&a){int n=a.size(),carry=0;V b(n+1);for(int j=0;j<n;j++){int s=a[j]+a[n-1-j]+carry;b[j]=s%10;carry=s/10;}if(carry)b[n]=1;else b.pop_back();a.swap(b);}
// signed Mobius coefficient (-1)^(3-popcount(mask))
constexpr int SG[8]={-1,+1,+1,-1,+1,-1,-1,+1};
string hx(int v){constexpr char h[]="0123456789ABCDEF";if(v<-36||v>36){cerr<<"DELTA_RANGE "<<v<<"\n";exit(2);} v+=36;return string({h[(v>>4)&15],h[v&15]});}
int main(int argc,char**argv){int T=argc>1?atoi(argv[1]):8000,H=argc>2?atoi(argv[2]):12000,X=6000,Y=8000,Z=10000;
 array<V,8>a;for(int i=0;i<8;i++)a[i]=seed(H,i,X,Y,Z);
 cout<<"t,front,back,count,low,high,shield_front,shield_gap\n";
 for(int t=0;t<=T;t++){
  int n=a[0].size(),h=n/2;
  for(int k=0;k<8;k++){
   if((int)a[k].size()!=n){cerr<<"MISMATCH_LENGTH "<<t<<" ";return 3;}
   bool odd=0;for(int j=0;j<39;j++)if((a[k][j]+a[k][n-1-j])%2){odd=1;break;}
   if(!odd){cerr<<"NO_ODD_WITNESS t="<<t<<" k="<<k;return 4;}
  }
  auto val=[&](int j,int side){int sum=0;for(int k=0;k<8;k++){int p=side?n-1-j:j;sum+=SG[k]*(int)a[k][p];}return sum;};
  int front=-1,back=-1,count=0;
  for(int j=0;j<h;j++)if(val(j,0)+val(j,1)){
    if(front<0)front=j;back=j;count++;
  }
  int shield=-1;
  for(int j=0;j<h;j++){
   int xl=int(a[7][j])-int(a[5][j])-int(a[3][j])+int(a[1][j]);
   int xh=int(a[7][n-1-j])-int(a[5][n-1-j])-int(a[3][n-1-j])+int(a[1][n-1-j]);
   if(xl||xh){shield=j;break;}
  }
  if(t>=1500){string low,high;
   for(int r=-20;r<=40;r++){
    int j=front+r;
    if(j<0||j>=h){low+="??";high+="??";}else {low+=hx(val(j,0));high+=hx(val(j,1));}
   }
   cout<<t<<","<<front<<","<<back<<","<<count<<","<<low<<","<<high<<","<<shield<<","<<(front>=0&&shield>=0?shield-front:-1)<<"\n";
  }
  if(t<T)for(auto &v:a)step(v);
 }
}
