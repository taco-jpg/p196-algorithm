// N06 exact cross-family core pump, ordinary digit-vector arithmetic.
#include <bits/stdc++.h>
using namespace std;
const int path[]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
const int cycle[]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
const string entrance[]={
"H501D4EC98FGHDH9144B8G09EB9B6DI947HF97D",
"8D5158982IEDFCC7B586AF7A47228AD8EBFE5HB",
"H6B2AGIG5HA8C65G2BGD1BG09E44H17I94C9CF4",
"8E8438GGCD99B9BC949B5397A498C98G8E7339A",
"H8H86HDE680040459A92B6IF09IH49ICI8F6791",
"8GGGEEC9BE804449F00C48FF6A8HCE8CCHECDGA",
"HDEEAA6049H08899A1149HBBE0IF69I56GA68E1",
"8C9A62764E788GI90225E7A4759FCG8EBD87ED6"};
const string lattice[]={
"H31DHBE3I12073ECF97D","CB45CA78CA327A8895HB",
"639B51FH5174F0HGIBF4","A9D1767ED68BA68FGB8A",
"2073ECF97DH31DHBE3I1","327A8895HBCB45CA78CA",
"74F0HGIBF4639B51FH51","8BA68FGB8AA9D1767ED6"};
const string alphabet="0123456789ABCDEFGHI";
vector<unsigned char>seed(int L){
 vector<int>q(begin(path),end(path));
 for(int j=0;j<L;j++)q.insert(q.end(),begin(cycle),end(cycle));
 int h=q.size();vector<unsigned char>d(2*h);
 for(int i=0;i<h;i++){d[i]=min(9,q[i]);d[2*h-1-i]=q[i]-d[i];}
 return d;
}
int main(int argc,char**argv){
 int L=argc>1?atoi(argv[1]):224,T=argc>2?atoi(argv[2]):20200;
 auto d=seed(L),e=seed(L+1);vector<unsigned char>x,y;
 int count=0,failedFront=0,failedCore=0,firstFront=-1,firstCore=-1;
 for(int t=0;t<=T;t++){
  int n=d.size(),m=e.size();
  auto frontier=[&](const vector<unsigned char>&v){
   int z=v.size(),k=0;
   while(k<z/2){
    int want=alphabet.find(k<39?entrance[t%8][k]:lattice[t%8][(k-39)%20]);
    if(v[k]+v[z-1-k]!=want)break;k++;
   }return k;
  };
  int f=frontier(d),g=frontier(e);
  bool same=(m==n+40&&g==f+20),core=same;
  if(core)for(int i=f;i<n/2;i++)
   if(d[i]+d[n-1-i]!=e[i+20]+e[m-1-(i+20)]){core=false;break;}
  count++;
  if(!same){failedFront++;if(firstFront<0)firstFront=t;}
  if(!core){failedCore++;if(firstCore<0)firstCore=t;}
  if(t%2000==0||t==firstFront||t==firstCore||t==T)
   cout<<"t="<<t<<" F0="<<f<<" F1="<<g<<" fronts="<<same<<" core="<<core<<" n0="<<n<<" n1="<<m<<"\n";
  if(t==T)break;
  x.resize(n);y.resize(m);int c=0,k=0;
  for(int i=0;i<n;i++){int u=d[i]+d[n-1-i]+c;x[i]=u%10;c=u/10;}
  for(int i=0;i<m;i++){int u=e[i]+e[m-1-i]+k;y[i]=u%10;k=u/10;}
  if(c)x.push_back(c);if(k)y.push_back(k);d.swap(x);e.swap(y);
 }
 cout<<"RESULT trials="<<count<<" failedfront="<<failedFront<<" failedcore="<<failedCore
     <<" firstfront="<<firstFront<<" firstcore="<<firstCore<<"\n";
 return !(firstCore==11+88*L&&firstFront==12+88*L);
}