#include <bits/stdc++.h>
using namespace std;
static const int path[]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
static const int cyc[]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
vector<uint8_t> seed(int h,int reserve){vector<uint8_t>a(h*2);
  for(int i=0;i<h;i++){
    int q=i<39?path[i]:cyc[(i-39)%20];
    if(reserve && i>=h-reserve)q=(7*i+11)%19;
    a[i]=min(9,q);a[2*h-1-i]=q-a[i];
  }return a;
}
vector<uint8_t>step(const vector<uint8_t>&a){vector<uint8_t>b(a.size()+1);int c=0;for(int i=0;i<(int)a.size();i++){int s=a[i]+a[a.size()-1-i]+c;b[i]=s%10;c=s/10;}if(c)b[a.size()]=c;else b.pop_back();return b;}
int main(int argc,char**argv){int h=argc>1?atoi(argv[1]):5200,steps=argc>2?atoi(argv[2]):20000,k=argc>3?atoi(argv[3]):100;auto a=seed(h,0),b=seed(h,k);ofstream raw("front_dense.tsv");
for(int t=0;t<=steps;t++){
 int len=min(a.size(),b.size());int j=0;
 for(;j<len/2;j++) if(a[j]+a[a.size()-1-j]!=b[j]+b[b.size()-1-j])break;
 raw<<t<<"\t"<<j<<"\n";
 if(t==0 || t==steps || t%1000==0)cout<<"t="<<t<<" min_digit_len="<<len<<" first_pair_difference="<<j<<" count_to_mid="<<len/2-j<<"\n";
 if(t<steps){a=step(a);b=step(b);}
}}
