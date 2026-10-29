// N06 full matched-prefix frontier against the 8-phase decimal p8 lattice.
#include <bits/stdc++.h>
using namespace std;
const string entr[]={
"H501D4EC98FGHDH9144B8G09EB9B6DI947HF97D",
"8D5158982IEDFCC7B586AF7A47228AD8EBFE5HB",
"H6B2AGIG5HA8C65G2BGD1BG09E44H17I94C9CF4",
"8E8438GGCD99B9BC949B5397A498C98G8E7339A",
"H8H86HDE680040459A92B6IF09IH49ICI8F6791",
"8GGGEEC9BE804449F00C48FF6A8HCE8CCHECDGA",
"HDEEAA6049H08899A1149HBBE0IF69I56GA68E1",
"8C9A62764E788GI90225E7A4759FCG8EBD87ED6"};
const string cyc[]={
"H31DHBE3I12073ECF97D","CB45CA78CA327A8895HB",
"639B51FH5174F0HGIBF4","A9D1767ED68BA68FGB8A",
"2073ECF97DH31DHBE3I1","327A8895HBCB45CA78CA",
"74F0HGIBF4639B51FH51","8BA68FGB8AA9D1767ED6"};
const string alpha="0123456789ABCDEFGHI";
int main(int argc,char**argv){
 int L=argc>1?atoi(argv[1]):225,T=argc>2?atoi(argv[2]):20000;
 vector<int>q;for(char c:entr[0])q.push_back(alpha.find(c));
 for(int j=0;j<L;j++)for(char c:cyc[0])q.push_back(alpha.find(c));
 int h=q.size();vector<unsigned char>d(2*h),nxt;
 for(int i=0;i<h;i++){d[i]=min(9,q[i]);d[2*h-1-i]=q[i]-d[i];}
 vector<int> fronts;int prev=0;
 for(int t=0;t<=T;t++){
  int n=d.size(),upto=n/2,front=0;
  while(front<upto){
   int e=alpha.find(front<39?entr[t%8][front]:cyc[t%8][(front-39)%20]);
   if(d[front]+d[n-1-front]!=e)break;front++;
  }
  fronts.push_back(front);
  if(t<=20||t%1000==0||front<8||t==T)
   cout<<"t="<<t<<" len="<<n<<" frontier="<<front<<" delta="<<front-prev<<"\n";
  prev=front;
  if(t==T)break;
  int carry=0;nxt.resize(n);
  for(int i=0;i<n;i++){int p=d[i]+d[n-1-i]+carry;nxt[i]=p%10;carry=p/10;}
  if(carry)nxt.push_back(carry);d.swap(nxt);
 }
 int bad=0;for(int t=100;t<=19000&&t+88<(int)fronts.size();t++)
  if(fronts[t+88]!=fronts[t]-20)bad++;
 cout<<"SHIFT88 minus20 mismatches="<<bad<<" checked="<<max(0,min(19000,T-88)-99)<<"\n";
}