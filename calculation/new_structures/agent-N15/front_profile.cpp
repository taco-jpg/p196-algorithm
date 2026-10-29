#include <algorithm>
#include <cstdint>
#include <iostream>
#include <vector>
using V=std::vector<uint8_t>;
V next(const V &p){V d;d.reserve(p.size()+1);int c=0;for(int x:p){int s=x+c;d.push_back(s%10);c=s/10;}if(c)d.push_back(c);V q(d.size());for(size_t i=0;i<d.size();i++)q[i]=d[i]+d[d.size()-1-i];return q;}
V source(int h,int centre){V w{14};for(int j=0;j<h;j++){V v;v.reserve(2*w.size());for(auto x:w){v.push_back(x==14?14:16);v.push_back(x==14?16:14);}w.swap(v);}V p{4};p.insert(p.end(),w.begin(),w.end());p.push_back(centre);for(auto it=w.rbegin();it!=w.rend();it++)p.push_back(*it);p.push_back(4);return p;}
int first_mismatch(const V&a,const V&b){if(a.size()!=b.size())return 0;for(size_t i=0;i<a.size();i++)if(a[i]!=b[i])return int(i);return -1;}
int main(){for(int h=7;h<=12;h++){int n=1<<h;V a=source(h,0),b=source(h,18);int max=5*n;std::vector<int> sample={0,n/2,n,3*n/2,2*n,5*n/2,3*n,7*n/2,4*n,9*n/2,5*n};int j=0;for(int t=0;t<=max;t++){if(j<int(sample.size())&&t==sample[j]){int x=first_mismatch(a,b);std::cout<<h<<","<<t<<","<<x<<","<<double(x)/n<<"\n";j++;}if(t<max){a=next(a);b=next(b);}}}}
