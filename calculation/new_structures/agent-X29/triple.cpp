#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
using D=vector<uint8_t>;
const vector<int> B={8,13,5,1,5,8,9,8,2,18,14,13,15,12,12,7,11,5,8,6,10,15,7,10,4,7,2,2,8,10,13,8,14,11,15,14,5,17,11};
const vector<int> W={12,11,4,5,12,10,7,8,12,10,3,2,7,10,8,8,9,5,17,11};
D seed(int k,int m,int q,bool packet) {
 vector<int> half=B;
 for(int i=0;i<k;++i)half.insert(half.end(), W.begin(), W.end());
 int offset=half.size();
 for(int i=0;i<m;++i){half.push_back(5);half.push_back(5);half.push_back(2);}
 if(packet){int s=offset+3*50+1;assert(m>54);assert(half[s]==5 && half[s+1]==2 && half[s+2]==5);half[s]=half[s+1]=half[s+2]=7;}
 half.insert(half.end(),q,18);
 vector<int> p=half;p.push_back(18);for(int i=int(half.size())-1;i>=0;--i)p.push_back(half[i]);
 D a(p.size());for(int i=0;i<int(p.size()/2);++i){a[i]=p[i]/2;a[p.size()-1-i]=p[i]-a[i];}
 a[p.size()/2]=9;assert(a.back()!=0);return a;
}
inline int pairat(const D& a,int i){return int(a[i])+a[a.size()-1-i];}
D step(const D &d){D e(d.size()+1);int c=0;for(size_t i=0;i<d.size();++i){int s=int(d[i])+int(d[d.size()-1-i])+c;e[i]=s%10;c=s/10;}if(c){e[d.size()]=c;}else e.pop_back();return e;}
bool pal(const D& a){for(size_t i=0;i<a.size()/2;++i)if(a[i]!=a[a.size()-1-i])return false;return true;}
uint64_t fnv64(const D& a){uint64_t h=1469598103934665603ULL;for(size_t i=a.size();i--;) {h ^= uint64_t('0'+a[i]);h*=1099511628211ULL;}return h;}
int central(const D& a){int i=int(a.size()/2),j=int((a.size()-1)/2);while(i<int(a.size())&&j>=0&&pairat(a,j)==18&&pairat(a,i)==18){++i;--j;}return i-j-1;}
bool pumped(const D& a,const D& larger){int n=a.size();if(int(larger.size())!=n+2)return false;int mid=n/2;for(int i=0;i<n+2;++i){int v=pairat(larger,i);if(i>=mid&&i<mid+2){if(v!=18)return false;}else{int j=i>=mid+2?i-2:i;if(v!=pairat(a,j))return false;}}return true;}
int prefix(const D& a,const vector<int>&root,const vector<int>&band){int n=a.size()/2, r=0;for(;r<n;++r){int expected=r<int(root.size())?root[r]:band[(r-int(root.size()))%band.size()];if(pairat(a,r)!=expected)break;}return r;}
int main(int argc,char**argv){int k=argc>1?stoi(argv[1]):300,q=argc>2?stoi(argv[2]):6500,T=argc>3?stoi(argv[3]):20000,m=argc>4?stoi(argv[4]):80;assert(k>=2&&q>=1&&m>=60);
 D probe=seed(32,80,0,false);vector<vector<int>> roots,bands;
 for(int t=0;t<8;++t){vector<int>root,band;for(int i=0;i<39;++i)root.push_back(pairat(probe,i));for(int i=39;i<59;++i)band.push_back(pairat(probe,i));roots.push_back(root);bands.push_back(band);probe=step(probe);}
 D a=seed(k,m,q,false),b=seed(k,m,q,true),c=seed(k,m,q+1,false);uint64_t over=0,trajectory=1469598103934665603ULL;int mincentral=INT32_MAX,minprefix=INT32_MAX;int minpref_at=-1;
 for(int t=0;t<=T;++t){
  if(pal(a)||pal(b)||pal(c)){cerr<<"pal at "<<t<<"\n";return 2;}
  if(!pumped(a,c)){cerr<<"pump mismatch at "<<t<<"\n";return 3;}
  int cr=central(a);mincentral=min(mincentral,cr);
  int pr=prefix(a,roots[t%8],bands[t%8]);if(pr<minprefix){minprefix=pr;minpref_at=t;}
  if(t>=4){if(a.size()!=b.size())return 4;bool peq=true;for(size_t i=0;i<a.size();++i)if(pairat(a,i)!=pairat(b,i)){peq=false;break;}if(!peq){cerr<<"erase mismatch "<<t<<"\n";return 5;}}
  if(t>=5&&a!=b){cerr<<"merge mismatch "<<t<<"\n";return 6;}
  if(t==4&&a==b){cerr<<"premature n merger\n";return 7;}
  trajectory=(trajectory^fnv64(a))*1099511628211ULL;
  if(t%1000==0||t==T)cerr<<"t="<<t<<" n="<<a.size()<<" c18="<<cr<<" root="<<pr<<" hash="<<hex<<fnv64(a)<<" trajectory="<<trajectory<<dec<<"\n";
  if(t==T)break;
  D an=step(a),bn=step(b),cn=step(c);int gamma=int(an.size())-int(a.size());if(gamma!=(t%2)){cerr<<"clock mismatch "<<t<<" got "<<gamma<<"\n";return 8;}
  over+=gamma;a=move(an);b=move(bn);c=move(cn);
 }
 cout<<"PASS k="<<k<<" q="<<q<<" m="<<m<<" steps="<<T<<" n0="<<seed(k,m,q,false).size()<<" nT="<<a.size()<<" overflows="<<over<<" min_c18="<<mincentral<<" min_root="<<minprefix<<" at="<<minpref_at<<" hash="<<hex<<fnv64(a)<<" trajectory="<<trajectory<<dec<<"\n";
}
