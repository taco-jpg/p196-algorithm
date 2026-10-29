// Independent GMP carry gates derived from actual N(t+1) decimal digits.
#define main x25_collision_unused_main
#include "collision.cpp"
#undef main
#include <gmpxx.h>
using Gates=array<int,4>;
mpz_class realize(const Word &p){int n=p.size();string d(n,'0');for(int i=0;i<n/2;i++){int z=p[i], hi=i?max(0,z-9):max(1,z-9);d[i]='0'+z-hi;d[n-1-i]='0'+hi;}if(n%2){if(p[n/2]%2)abort();d[n/2]='0'+p[n/2]/2;}reverse(d.begin(),d.end());return mpz_class(d,10);}
Word pairs(const mpz_class& n){string s=n.get_str();Word p(s.size());for(int i=0;i<(int)s.size();i++)p[i]=(s[i]-'0')+(s[s.size()-1-i]-'0');return p;}
mpz_class add(const mpz_class&n){string s=n.get_str();reverse(s.begin(),s.end());return n+mpz_class(s,10);}
vector<int> actualcarry(const Word &p,const mpz_class &nnext){string s=nnext.get_str();reverse(s.begin(),s.end());int size=p.size();vector<int> c(size+1);for(int i=0;i<size;i++){int digit=s[i]-'0';int z=p[i]+c[i]-digit;if(z%10||z<0||z>10){cerr<<"carry fail i="<<i<<" z="<<z<<"\n";abort();}c[i+1]=z/10;}if(c[size]!=(int)s.size()-size)abort();return c;}
struct Gate {int r;Gates ports;};
Gate snap(const Word &p,const Word &background,const mpz_class &nnext){int r=-1;for(int i=0;i<(int)p.size()/2;i++)if(p[i]!=background[i])r=i;int n=p.size(),l=r-20,h=r+80;auto c=actualcarry(p,nnext);if(l<0||h>=n/2)abort();return {r,{c[l],c[h+1],c[n-1-h],c[n-l]}};}
int main(int argc,char**argv){int q=argc>1?atoi(argv[1]):140,x=argc>2?atoi(argv[2]):960,H=argc>3?atoi(argv[3]):1792;
Word b=seed(q),a=patch(b,x,A),d=patch(b,x,D);mpz_class nb=realize(b),na=realize(a),nd=realize(d);vector<Gate> aa,dd;
for(int t=0;t<=H;t++){
  if(pairs(nb)!=b||pairs(na)!=a||pairs(nd)!=d){cerr<<"full pair mismatch "<<t<<"\n";return 2;}
  string sa=na.get_str(),sd=nd.get_str(),sb=nb.get_str();if(equal(sa.begin(),sa.begin()+sa.size()/2,sa.rbegin())||equal(sd.begin(),sd.begin()+sd.size()/2,sd.rbegin())||equal(sb.begin(),sb.begin()+sb.size()/2,sb.rbegin())){cerr<<"palindrome\n";return 2;}
  mpz_class nbnext=add(nb),nanext=add(na),ndnext=add(nd);
  aa.push_back(snap(a,b,nanext));dd.push_back(snap(d,b,ndnext));
  if(t<H){int cb=step(b),ca=step(a),cd=step(d);if(cb!=ca||cb!=cd||cb!=(t%2==0))abort();nb=nbnext;na=nanext;nd=ndnext;}
}
for(auto [name,v,lastexpected]:vector<tuple<string,const vector<Gate>*,int>>{{"A",&aa,421},{"D",&dd,496}}){int good=0,last=-1;for(int t=0;t+792<=H;t++){bool ok=((*v)[t+792].r-(*v)[t].r==540 && (*v)[t+792].ports==(*v)[t].ports);if(ok)good++;else last=t;}cout<<name<<" actual-number carry-port recurrence good="<<good<<"/"<<H+1-792<<" lastfailure="<<last<<" stable_from="<<last+1<<"\n";if(q==140&&x==960&&H==1792&&last!=lastexpected)abort();}
cout<<"GMP_DECIMAL_DIGIT_CARRY_PASS three seeds, "<<H+1<<" time states each\n";
}
