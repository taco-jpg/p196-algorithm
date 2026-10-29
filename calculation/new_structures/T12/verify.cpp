#include <algorithm>
#include <cassert>
#include <chrono>
#include <fstream>
#include <sstream>
#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <boost/multiprecision/cpp_int.hpp>
using namespace std;
using boost::multiprecision::cpp_int;
using Dig=vector<int>;
using Row=vector<int>;
static Row W[12],B[12];
static Row J={8,3,14}, C={8,8};
static int gamma_t(int t){return t%4==0;}
static string str_digits(const Dig& d){ string s; s.reserve(d.size()); for(auto it=d.rbegin();it!=d.rend();++it)s.push_back(char('0'+*it)); return s; }
static Dig source_digits(const Row& p){
  int n=(int)p.size(); Dig d(n,0);
  for(int i=0;i<n/2;i++){int v=min(9,p[i]);d[i]=p[i]-v;d[n-1-i]=v;}
  if(n%2){if(p[n/2]%2)throw runtime_error("odd central pair coefficient");d[n/2]=p[n/2]/2;}
  if(d.back()==0)throw runtime_error("leading zero source"); return d;
}
static Row pairword(const Dig& d){int n=(int)d.size();Row p(n);for(int i=0;i<n;i++)p[i]=d[i]+d[n-1-i];return p;}
static Dig step_digits(const Dig& d){int n=(int)d.size(),c=0;Dig out;out.reserve(n+1);for(int i=0;i<n;i++){int z=d[i]+d[n-1-i]+c;out.push_back(z%10);c=z/10;}if(c)out.push_back(c);return out;}
static Dig make_digits(int q,int k,const Row& U){Row h=B[0];for(int i=0;i<q;i++)h.insert(h.end(),W[0].begin(),W[0].end());h.insert(h.end(),J.begin(),J.end());for(int i=0;i<k;i++)h.insert(h.end(),U.begin(),U.end());Row p=h;p.insert(p.end(),C.begin(),C.end());p.insert(p.end(),h.rbegin(),h.rend());return source_digits(p);}
static Row insert_pair(const Row& p,const Row& w,int c){int n=(int)p.size();if(c<0||c>(n/2)||c+(int)w.size()>n-c)throw runtime_error("bad cut");Row o;o.reserve(n+2*w.size());o.insert(o.end(),p.begin(),p.begin()+c);o.insert(o.end(),w.begin(),w.end());o.insert(o.end(),p.begin()+c,p.end()-c);o.insert(o.end(),w.rbegin(),w.rend());o.insert(o.end(),p.end()-c,p.end());return o;}
static bool has_odd(const Row& p){for(int x:p)if(x&1)return true;return false;}
static string stripzero(string s){size_t i=s.find_first_not_of('0');return i==string::npos?string("0"):s.substr(i);}
static void check_big_step(const Dig& d,const Dig& next){string ns=str_digits(d),rs;rs.reserve(d.size());for(int x:d)rs.push_back(char('0'+x));rs=stripzero(rs);cpp_int n(ns),r(rs),sum=n+r,expected(str_digits(next));if(sum!=expected)throw runtime_error("cpp_int mismatch");}
static int modp(int x,int m){x%=m;return x<0?x+m:x;}
static Row bulk_next(const Row& w,int g){
 int m=(int)w.size();Row alpha(m),beta(m);int z=0;
 for(int x:w)z=(x+z)/10;alpha[0]=z;
 for(int i=1;i<m;i++)alpha[i]=(w[i-1]+alpha[i-1])/10;
 z=0;for(auto it=w.rbegin();it!=w.rend();++it)z=(*it+z)/10;beta[0]=z;
 for(int i=m-1;i>=1;i--)beta[i]=(w[i]+beta[(i+1)%m])/10;
 for(int i=0;i<m;i++)if((w[i]+alpha[i])/10!=alpha[(i+1)%m]||(w[i]+beta[(i+1)%m])/10!=beta[i])throw runtime_error("bulk carry loop not closed");
 Row out(m);for(int i=0;i<m;i++){int low=(w[i]+alpha[i])%10;int high=g? (w[modp(i-1,m)]+beta[i])%10:(w[i]+beta[(i+1)%m])%10;out[i]=low+high;}return out;
}
static vector<Row> phase_rows(Row u){vector<Row> v;v.push_back(u);for(int t=0;t<120;t++)v.push_back(bulk_next(v.back(),gamma_t(t)));return v;}
static pair<int,int> cone(const vector<Row>& v){int l=0,r=0,m=(int)v[0].size();for(int t=0;t<120;t++){const Row&w=v[t];int lh=(w[l%m]==9);int rh=(w[modp(-r-1,m)]==9);l+=1+lh;r+=1+rh-gamma_t(t);}return {l,r};}
static int w_cone(){int m=34+9*14,total=0;for(int t=0;t<120;t++){int run=0;while(W[t%12][modp(m-35-run,9)]==9)run++;int d=1+run-gamma_t(t);if(d<0)throw runtime_error("negative W cone step");m-=d;total+=d;}return total;}
static Row make_U(int a,int rot){Row u={9,a,18-a};rotate(u.begin(),u.begin()+rot,u.end());return u;}
static void run_one(int q,int k,const Row& U,bool ucut,bool checkcpp){
 Dig x=make_digits(q,k,U), y=make_digits(q+(ucut?0:1),k+(ucut?1:0),U);
 int c=ucut?34+9*q+(int)J.size()+165:52,m=ucut?3:9;
 Row start=ucut?U:W[0];
 for(int t=0;t<=120;t++){
   Row px=pairword(x),py=pairword(y); if(py!=insert_pair(px,Row(px.begin()+c,px.begin()+c+m),c))throw runtime_error("paired insertion fails q="+to_string(q)+" k="+to_string(k)+" t="+to_string(t)+" U="+to_string(U[0])+","+to_string(U[1])+","+to_string(U[2])+" cut="+to_string(ucut));
   if(!has_odd(px)||!has_odd(py))throw runtime_error("odd-pair guard fails");
   if(t==120){if(Row(px.begin()+c,px.begin()+c+m)!=start)throw runtime_error("bulk row not restored at t=120");break;}
   Dig xn=step_digits(x),yn=step_digits(y);
   if((int)xn.size()-(int)x.size()!=gamma_t(t)||(int)yn.size()-(int)y.size()!=gamma_t(t))throw runtime_error("overflow clock fails");
   if(checkcpp){check_big_step(x,xn);check_big_step(y,yn);}
   x.swap(xn);y.swap(yn);
 }
}
int main(int argc,char**argv){
 string path=argc>1?argv[1]:"calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt";
 ifstream f(path);if(!f)throw runtime_error("cannot open data file");vector<Row>a;string line;while(getline(f,line)){if(line.empty())continue;istringstream iss(line);Row r;int x;while(iss>>x)r.push_back(x);a.push_back(r);}if(a.size()!=38)throw runtime_error("expected 38 rows");
 for(int i=0;i<12;i++)W[i]=a[2+i];for(int i=0;i<12;i++)B[i]=a[26+i];
 auto start=chrono::steady_clock::now();long long cases=0,cppcases=0;int uLmin=999,uLmax=0,uRmin=999,uRmax=0;map<pair<int,int>,int> hist;
 for(int aa=0;aa<=18;aa+=2)for(int rot=0;rot<3;rot++){Row U=make_U(aa,rot);auto v=phase_rows(U);if(v.back()!=U)throw runtime_error("U phase fails 120-return");for(const auto& row:v){int n9=0;for(int z:row)n9+=(z==9);if(n9!=1)throw runtime_error("U phase lost unique 9");}auto [cl,cr]=cone(v);uLmin=min(uLmin,cl);uLmax=max(uLmax,cl);uRmin=min(uRmin,cr);uRmax=max(uRmax,cr);hist[{cl,cr}]++;
  for(int q:{20,40,80,160}){int k=q+80;bool cpp=(aa==0&&rot==0);run_one(q,k,U,false,cpp);run_one(q,k,U,true,cpp);cases+=2;if(cpp)cppcases+=2;}}
 if(w_cone()!=91)throw runtime_error("W cone differs from 91");
 cout<<"PASS cases="<<cases<<" q=20,40,80,160 k=q+80; U-words=30; each insertion identity checked at t=0..120; exact digit-vector orbit; cpp_int cross-check cases="<<cppcases<<"\n";cout<<"CONE exact worst-case carry-port radii: W=91, U-junction-side="<<uLmax<<" (min "<<uLmin<<"), U-centre-side="<<uRmax<<" (min "<<uRmin<<")\n";for(auto [v,n]:hist)cout<<"  U cone ("<<v.first<<","<<v.second<<"): "<<n<<" words\n";cout<<"  Fixed-phase W retreat: 89 steps of 1, 30 of 0, 1 of 2 = 91 columns\n";
}
