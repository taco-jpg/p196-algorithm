// An intentionally finite padding identity is checked until and after root collision.
// /tmp/n17_control 250 1200 20 => first shifted-tail mismatch 951
#include <bits/stdc++.h>
using namespace std;using W=vector<uint8_t>;
int pre[]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
int cyc[]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
W seed(int h){W z(2*h);for(int i=0;i<h;i++){int p=i<39?pre[i]:cyc[(i-39)%20];z[i]=max(0,p-9);z[2*h-1-i]=p-z[i];}return z;}
int step(W&z){W y(z.size()+1);int n=z.size(),c=0;for(int i=0;i<n;i++){int s=z[i]+z[n-i-1]+c;y[i]=s%10;c=s/10;}if(c)y[n]=c;else y.resize(n);z.swap(y);return c;}
int main(int argc,char**argv){
 int h=argc>1?atoi(argv[1]):250,T=argc>2?atoi(argv[2]):1200,m=argc>3?atoi(argv[3]):20;
 W a=seed(h),b=seed(h+m);int first=-1,root=-1,gamma=-1;
 for(int t=0;t<=T;t++){
  int n=a.size();for(int i=0;i<n/2;i++){
   int x=a[i]+a[n-1-i],j=i<39?i:i+m,y=b[j]+b[b.size()-1-j];
   if(i<39&&x!=y&&root<0)root=t;
   if(i>=39&&x!=y&&first<0)first=t;
  }
  if(t<T){int g=step(a),q=step(b);if(g!=q&&gamma<0)gamma=t;}
 }
 cout<<"control h="<<h<<" T="<<T<<" m="<<m<<" first_shift_failure="<<first<<" first_root_difference="<<root<<" first_gamma_difference="<<gamma<<"\n";
 return (h==250&&m==20&&T==1200&&first==951&&root==940&&gamma==-1)?0:1;
}
