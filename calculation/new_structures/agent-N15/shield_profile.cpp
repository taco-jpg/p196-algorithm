// First passage of a dyadic core perturbation into nested exterior windows.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <vector>
#include <array>
using V=std::vector<uint8_t>;
V step(const V&p){V d;d.reserve(p.size()+1);int c=0;for(auto x:p){int s=x+c;d.push_back(s%10);c=s/10;}if(c)d.push_back(1);V q(d.size());for(size_t i=0;i<d.size();i++)q[i]=d[i]+d[d.size()-1-i];return q;}
V seed(int h,int c){V w{14};for(int i=0;i<h;i++){V next;next.reserve(2*w.size());for(int z:w){next.push_back(z==14?14:16);next.push_back(z==14?16:14);}w.swap(next);}V p{4};p.insert(p.end(),w.begin(),w.end());p.push_back(c);for(int i=int(w.size())-1;i>=0;i--)p.push_back(w[i]);p.push_back(4);return p;}
int main(){for(int h=6;h<=12;h++){V a=seed(h,0),b=seed(h,18);const int K[]={4,8,16,32,64};int crossing[5]={-1,-1,-1,-1,-1},limit=std::min(26000,12*(1<<h));for(int t=0;t<=limit;t++){int ix=0;if(a.size()!=b.size())ix=0;else{int mx=std::min(64,int(a.size()));while(ix<mx&&a[ix]==b[ix])ix++;}for(int j=0;j<5;j++)if(crossing[j]<0&&ix<K[j])crossing[j]=t;if(crossing[0]>=0&&crossing[1]>=0&&crossing[2]>=0&&crossing[3]>=0&&crossing[4]>=0)break;if(t<limit){a=step(a);b=step(b);}}std::cout<<h;for(auto x:crossing)std::cout<<","<<x;std::cout<<"\n";}}
