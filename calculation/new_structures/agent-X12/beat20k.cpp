// Agent X12: genuine base-ten digit arithmetic vs independent base-1000-limb integer RAA.
// A finite computation, never an infinite Lychrel proof.
#include <bits/stdc++.h>
using namespace std;
using U8=uint8_t;
const vector<int> B={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
const vector<int> W={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
const char *bs[8]={"H501D4EC98FGHDH9144B8G09EB9B6DI947HF97D", "8D5158982IEDFCC7B586AF7A47228AD8EBFE5HB", "H6B2AGIG5HA8C65G2BGD1BG09E44H17I94C9CF4", "8E8438GGCD99B9BC949B5397A498C98G8E7339A", "H8H86HDE680040459A92B6IF09IH49ICI8F6791", "8GGGEEC9BE804449F00C48FF6A8HCE8CCHECDGA", "HDEEAA6049H08899A1149HBBE0IF69I56GA68E1", "8C9A62764E788GI90225E7A4759FCG8EBD87ED6"};
vector<U8> make_number(int q,int r){
 vector<int> u(40,1);u[13]=7;u[20]=7;u[30]=6;
 vector<int> a=B;for(int i=0;i<q;i++)a.insert(a.end(),W.begin(),W.end());
 vector<int> c={8,0,0};c.insert(c.end(),u.begin(),u.end());c.insert(c.end(),r,1);c.push_back(16);c.insert(c.end(),r,1);
 c.insert(c.end(),u.rbegin(),u.rend());c.insert(c.end(),{0,0,8});
 vector<int> p=a;p.insert(p.end(),c.begin(),c.end());p.insert(p.end(),a.rbegin(),a.rend());
 vector<U8> d(p.size());int n=p.size();
 for(int i=0;i<(n+1)/2;i++){int j=n-1-i;
  if(i==j){if(p[i]%2)throw runtime_error("odd midpoint");d[i]=p[i]/2;}
  else{d[i]=min(p[i],9);d[j]=p[i]-d[i];}
 }
 if(d.back()==0)throw runtime_error("zero leading digit");return d;
}
struct Big1000{
 vector<int> limb;
 explicit Big1000(const vector<U8>&d){for(int i=0;i<(int)d.size();i+=3){int v=d[i];if(i+1<(int)d.size())v+=10*d[i+1];if(i+2<(int)d.size())v+=100*d[i+2];limb.push_back(v);}}
 static vector<int> parse(string s){vector<int> a;for(int i=(int)s.size();i>0;i-=3){int l=max(0,i-3);a.push_back(stoi(s.substr(l,i-l)));}while(a.size()>1&&a.back()==0)a.pop_back();return a;}
 string dec()const{string s=to_string(limb.back());for(int i=(int)limb.size()-2;i>=0;i--){int v=limb[i];s+=char('0'+v/100);s+=char('0'+(v/10)%10);s+=char('0'+v%10);}return s;}
 void advance(){string s=dec();reverse(s.begin(),s.end());vector<int> y=parse(s);int c=0;for(size_t i=0;i<max(limb.size(),y.size());i++){if(i>=limb.size())limb.push_back(0);int z=limb[i]+(i<y.size()?y[i]:0)+c;limb[i]=z%1000;c=z/1000;}if(c)limb.push_back(c);}
};
string decimal(const vector<U8>&d){string s; s.reserve(d.size());for(auto i=d.rbegin();i!=d.rend();i++)s.push_back('0'+*i);return s;}
bool ispal(const vector<U8>&d){for(int i=0,n=d.size();i<n/2;i++)if(d[i]!=d[n-1-i])return false;return true;}
int step(vector<U8>&d){int n=d.size();vector<U8> o(n+1);int c=0;
 for(int i=0;i<n;i++){int s=d[i]+d[n-1-i]+c;o[i]=s%10;c=s/10;}if(c)o[n]=1;else o.resize(n);d.swap(o);return c;}
vector<U8> pairs(const vector<U8>&d){int n=d.size();vector<U8> p(n);for(int i=0;i<n;i++)p[i]=d[i]+d[n-1-i];return p;}
int splice(const vector<U8>&p,const vector<U8>&z){
 if(z.size()!=p.size()+2)return -1;int n=p.size(),h=n/2,k=0;
 while(k<h&&p[k]==z[k])k++;if(k>h)return -2;
 int s=z[k];if(z[n-k+1]!=s)return -3;
 for(int i=k;i<n-k;i++)if(p[i]!=z[i+1])return -4;
 for(int i=n-k;i<n;i++)if(p[i]!=z[i+2])return -5;
 return k;
}
uint64_t hash_digits(const vector<U8>&d){uint64_t x=14695981039346656037ULL;for(U8 v:d){x^=v;x*=1099511628211ULL;}return x;}
int main(int argc,char**argv){
 int q=argc>1?atoi(argv[1]):300,r=argc>2?atoi(argv[2]):20000,T=argc>3?atoi(argv[3]):20000;
 vector<U8> a=make_number(q,r),b=make_number(q,r+1);
 Big1000 x(a),y(b);vector<int> ks;ks.reserve(T+1);long long over=0;int minB=40;
 for(int t=0;t<=T;t++){
  if(decimal(a)!=x.dec()||decimal(b)!=y.dec()){cerr<<"INTEGER DIFFERENCE t="<<t<<"\n";return 2;}
  if(ispal(a)||ispal(b)){cerr<<"PALINDROME t="<<t<<"\n";return 3;}
  vector<U8> p=pairs(a),z=pairs(b);
  for(int i=0;i<39;i++){int target=(isdigit(bs[t%8][i])?bs[t%8][i]-'0':bs[t%8][i]-'A'+10);if(p[i]!=target||z[i]!=target){cerr<<"EXTERIOR FAILURE t="<<t<<" i="<<i<<"\n";return 4;}}
  int k=splice(p,z);if(k<0){cerr<<"SPLICE FAILURE t="<<t<<" error="<<k<<"\n";return 5;}
  if(t>0){const int cycle[6]={2,4,8,16,14,10};if(z[k]!=cycle[(t-1)%6]){cerr<<"INNER PHASE FAIL t="<<t<<"\n";return 6;}}
  ks.push_back(k);if(t>=264&&ks[t]-ks[t-264]!=-44){cerr<<"264 DRIFT FAIL t="<<t<<" delta="<<ks[t]-ks[t-264]<<"\n";return 7;}
  if(t>0&&t%1000==0)cerr<<"checkpoint "<<t<<" digits="<<a.size()<<" cut="<<k<<"\n";
  if(t==T){cout<<"PASS q="<<q<<" r="<<r<<" steps="<<T<<" seed_digits="<<make_number(q,r).size()<<" final_digits="<<a.size()<<" final_cut="<<k<<" overflow_ones="<<over<<" hashA="<<hex<<hash_digits(a)<<" hashB="<<hash_digits(b)<<dec<<"\n";break;}
  x.advance();y.advance();int ca=step(a),cb=step(b);if(ca!=cb){cerr<<"OVERFLOW DIVERGENCE t="<<t<<"\n";return 8;}
  if(ca!=((t%2)==0)){cerr<<"OVERFLOW CLOCK FAIL t="<<t<<"\n";return 9;}over+=ca;
 }
}
