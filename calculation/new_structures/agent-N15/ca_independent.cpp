// Independent ordinary decimal integer digit-list controls for the dyadic 7-edge identities.
#include <cassert>
#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdint>
using V=std::vector<int>;
static V morph(int h){V w{14};for(int k=0;k<h;++k){V v;v.reserve(w.size()*2);for(int x:w){v.push_back(x);v.push_back(30-x);}w.swap(v);}return w;}
static V seed(int h){auto w=morph(h);int n=2*(int(w.size())+1);V d(n,0);d.front()=0;d.back()=4;for(int i=1;i<n/2;++i){d[i]=w[i-1]-9;d[n-1-i]=9;}return d;}
static V addrev(const V &d){int n=d.size(),c=0;V q;q.reserve(n+1);for(int i=0;i<n;++i){int z=d[i]+d[n-1-i]+c;q.push_back(z%10);c=z/10;}if(c)q.push_back(c);while(q.size()>1&&q.back()==0)q.pop_back();return q;}
static V pair(const V &d){V p(d.size());for(size_t i=0;i<d.size();++i)p[i]=d[i]+d[d.size()-1-i];return p;}
static int hi(int p){return p>=10;}
static V predict_third(int h){auto w=morph(h);const int L=w.size(),m=L+1;V q(m),r(m+1);q[0]=9;q[1]=9;for(int i=2;i<m;++i)q[i]=2*(w[i-1]-9);r[0]=10;r[1]=9;r[2]=q[2]-10;for(int i=3;i<m;++i)r[i]=q[i]+q[i-1]-18;r[m]=2*(q[m-1]-9);V g{1,0,14,5};for(int i=4;i<=m;++i)g.push_back(r[i]+r[i-1]-9*(hi(r[i])+hi(r[i-1])));V p=g;for(auto it=g.rbegin();it!=g.rend();++it)p.push_back(*it);return p;}
static V ca(V p){assert(std::count(p.begin(),p.end(),9)==0);V out(p.size());for(int i=0;i<int(p.size());++i)out[i]=2*(p[i]%10)+(i?hi(p[i-1]):0)+(i+1<int(p.size())?hi(p[i+1]):0);return out;}
static bool pal(const V &d){return std::equal(d.begin(),d.end(),d.rbegin());}
int main(){long checks=0;for(int h=2;h<=15;++h){V d=seed(h);assert(!pal(d));for(int t=1;t<=7;++t){d=addrev(d);assert(!pal(d));V got=pair(d);if(t==3){V exp=predict_third(h);if(got!=exp){std::cerr<<"third failure h="<<h<<"\n";return 1;}V corrupt=exp;corrupt[5]=(corrupt[5]+1)%19;assert(corrupt!=got);for(int s=4;s<=7;++s){exp=ca(exp);d=addrev(d);assert(!pal(d));if(pair(d)!=exp){std::cerr<<"CA mismatch h="<<h<<" step="<<s<<"\n";return 1;}++checks;}break;}}}
std::cout<<"INDEPENDENT_ORDINARY_DECIMAL_PASS levels=2..15 exact_edges=3..7 checks="<<checks<<" mutation_rejected=14\n";}
