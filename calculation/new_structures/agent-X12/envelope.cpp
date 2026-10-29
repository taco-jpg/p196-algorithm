// Agent-X12. Finite exact two-counter carry-envelope experiment, NOT an infinite certificate.
#include <bits/stdc++.h>
using namespace std;
using u8=uint8_t;
const vector<int> B={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
const vector<int> W={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
const char *bs[8]={"H501D4EC98FGHDH9144B8G09EB9B6DI947HF97D", "8D5158982IEDFCC7B586AF7A47228AD8EBFE5HB", "H6B2AGIG5HA8C65G2BGD1BG09E44H17I94C9CF4", "8E8438GGCD99B9BC949B5397A498C98G8E7339A", "H8H86HDE680040459A92B6IF09IH49ICI8F6791", "8GGGEEC9BE804449F00C48FF6A8HCE8CCHECDGA", "HDEEAA6049H08899A1149HBBE0IF69I56GA68E1", "8C9A62764E788GI90225E7A4759FCG8EBD87ED6"};
vector<u8> seed(int q,int r){vector<int> a=B,u(40,1);u[13]=7;u[20]=7;u[30]=6;for(int j=0;j<q;j++)a.insert(a.end(),W.begin(),W.end());vector<int> c={8,0,0};c.insert(c.end(),u.begin(),u.end());c.insert(c.end(),r,1);c.push_back(16);c.insert(c.end(),r,1);c.insert(c.end(),u.rbegin(),u.rend());c.insert(c.end(),{0,0,8});vector<u8> p;for(int v:a)p.push_back(v);for(int v:c)p.push_back(v);for(auto z=a.rbegin();z!=a.rend();z++)p.push_back(*z);return p;}
int step(vector<u8>&p){int c=0;vector<u8> d;d.reserve(p.size()+1);for(int v:p){int z=v+c;d.push_back(z%10);c=z/10;}if(c)d.push_back(1);int n=d.size();p.resize(n);for(int i=0;i<n;i++)p[i]=d[i]+d[n-1-i];return c;}
int splice(const vector<u8>&p,const vector<u8>&z){int n=p.size();if(z.size()!=n+2)return -1;int k=0,h=n/2;while(k<h&&p[k]==z[k])k++;if(z[n-k+1]!=z[k])return -2;for(int i=k;i<n-k;i++)if(p[i]!=z[i+1])return -3;for(int i=n-k;i<n;i++)if(p[i]!=z[i+2])return -4;return k;}
int normL(int r){int a[5]={13,15,16,16,17};return 6*((r-1)/5)+a[(r-1)%5];}
int eclock(int q){return 88*q+276;}
int minq(int r){return max(1,(normL(r)-276)/88 +1);}
struct Stats {int firstB=-1,firstClock=-1,firstSplice=-1,returnAfter=0;};
Stats scan(int q,int r,int end){auto p=seed(q,r),z=seed(q,r+1);Stats ans;for(int t=0;t<=end;t++){
 int k=splice(p,z);if(k<0){if(ans.firstSplice<0)ans.firstSplice=t;}else if(ans.firstSplice>=0)ans.returnAfter++;
 if(ans.firstB<0)for(int i=0;i<39;i++){char x=bs[t%8][i];int v=isdigit(x)?x-'0':x-'A'+10;if(int(p[i])!=v||int(z[i])!=v){ans.firstB=t;break;}}
 if(t==end)break;int g=step(p),h=step(z);if(ans.firstClock<0&&(g!=(t%2==0)||h!=(t%2==0)))ans.firstClock=t;
 }return ans;}
int main(int argc,char**argv){bool full=argc>1 && string(argv[1])=="--full";
 vector<int> qvals=full ? vector<int>{1,2,3,4,5,7,10,16,20,30,50,65} : vector<int>{1,5,10};
 vector<int> rvals=full ? vector<int>{100,250,500,850,1000,1500,2000,3000,5000,10000,15000,20000} : vector<int>{100,250,500,850,1000};
 for(int q:qvals){
  int end=eclock(q)+2;auto x=scan(q,12000,end);
  if(x.firstB!=eclock(q)||x.firstSplice!=-1||x.firstClock!=-1)throw runtime_error("outer clock regression");
  cout<<"OUTER q="<<q<<" r=12000 firstB="<<x.firstB<<" firstClock=none firstSplice=none through="<<end<<"\n";
 }
 for(int r:rvals){
  int L=normL(r),q=minq(r);auto x=scan(q,r,L);
  if(x.firstSplice!=L||x.firstB!=-1||x.firstClock!=-1)throw runtime_error("inner protected failure regression");
  int preB=-1;if(q>1){auto y=scan(q-1,r,L);preB=y.firstB;if(preB!=eclock(q-1))throw runtime_error("threshold minus one regression");}
  cout<<"INNER r="<<r<<" q_min="<<q<<" L="<<L<<" qprev_firstB="<<preB<<" firstB=none firstClock=none\n";
 }
 cout<<"X12_DUAL_CLOCK_FINITE_CONTROLS_PASS\n";
}
