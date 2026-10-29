// Independent decimal-digit implementation of a complete dyadic front profile.
#include <iostream>
#include <vector>
#include <cstdint>
using V=std::vector<uint8_t>;
V seed(int h,int central){V w{14};for(int i=0;i<h;i++){V next;next.reserve(w.size()*2);for(auto x:w){next.push_back(x==14?14:16);next.push_back(x==14?16:14);}w.swap(next);}V d{1};for(int x:w)d.push_back(x-9);d.push_back(central/2);for(size_t i=0;i<w.size();i++)d.push_back(9);d.push_back(3);return d;}
V step(const V&d){V s;s.reserve(d.size()+1);int c=0;for(size_t i=0;i<d.size();i++){int z=int(d[i])+int(d[d.size()-1-i])+c;s.push_back(z%10);c=z/10;}if(c)s.push_back(c);return s;}
int mismatch(const V&a,const V&b){if(a.size()!=b.size())return 0;for(size_t i=0;i<a.size();i++)if(int(a[i])+int(a[a.size()-1-i])!=int(b[i])+int(b[b.size()-1-i]))return i;return -1;}
int main(){for(int h=7;h<=12;h++){V a=seed(h,0),b=seed(h,18);int w=1<<h;for(int t=0;t<=5*w;t++){if(t%(w/2)==0)std::cout<<h<<","<<t<<","<<mismatch(a,b)<<"\n";if(t<5*w){a=step(a);b=step(b);}}}}
