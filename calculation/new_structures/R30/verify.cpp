// R30 independent GMP-free decimal digit checker; no in-place overwrites.
#include <algorithm>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
using V=std::vector<int>;
V csv(const std::string&s){V v;std::istringstream ss(s);std::string t;while(std::getline(ss,t,','))if(!t.empty()){int n=std::stoi(t);if(n<0||n>18)throw std::runtime_error("bad coefficient");v.push_back(n);}return v;}
void append(V&a,const V&b){a.insert(a.end(),b.begin(),b.end());}
void power(V&a,const V&w,int n){for(int i=0;i<n;i++)append(a,w);}
V mirror(V a){std::reverse(a.begin(),a.end());return a;}
V templ(const V&B,const V&W,const V&J,const V&U,const V&C,int q,int k){
 V h;append(h,B);power(h,W,q);append(h,J);power(h,U,k);
 V p=h;append(p,C);append(p,mirror(h));return p;
}
V realize(const V&p){
 if(p.empty()||p!=mirror(p))throw std::runtime_error("invalid pairword");
 V d(p.size());for(size_t i=0;i<p.size()/2;i++){
  int hi=std::min(9,p[i]),lo=p[i]-hi;
  if(lo<0||lo>9)throw std::runtime_error("nonrealizable coefficient");
  d[i]=lo;d[p.size()-1-i]=hi;
 }
 if(p.size()%2){int z=p[p.size()/2];if(z%2)throw std::runtime_error("odd midpoint");d[p.size()/2]=z/2;}
 if(d.back()==0)throw std::runtime_error("noncanonical source");
 return d;
}
V step(const V&d){
 V next;next.reserve(d.size()+1);int carry=0;
 for(size_t i=0;i<d.size();i++){
  int s=d[i]+d[d.size()-1-i]+carry;
  next.push_back(s%10);carry=s/10;
 }
 if(carry)next.push_back(carry);
 return next;
}
V pairword(const V&d){V p(d.size());for(size_t i=0;i<d.size();i++)p[i]=d[i]+d[d.size()-1-i];return p;}
int main(int argc,char**argv){
 if(argc!=8){std::cerr<<"usage: verify lattice.txt q k J_csv U_csv C_csv steps\n";return 2;}
 std::ifstream f(argv[1]);if(!f)throw std::runtime_error("lattice missing");
 int p,nb,m,base;f>>p>>nb>>m>>base;
 if(p!=12||nb!=34||m!=9||base!=10)throw std::runtime_error("bad lattice header");
 V gam(12),B(34),W(9);for(int&i:gam)f>>i;
 // File layout: 12 W rows, 12 auxiliary 9-column rows, then 12 B rows.
 for(int t=0;t<12;t++)for(int i=0,x;i<9;i++){f>>x;if(t==0)W[i]=x;}
 for(int t=0;t<12;t++)for(int i=0,x;i<9;i++)f>>x; // skip auxiliary carry/phase table
 for(int t=0;t<12;t++)for(int i=0,x;i<34;i++){f>>x;if(t==0)B[i]=x;}
 if(!f)throw std::runtime_error("truncated lattice data");
 int q=std::stoi(argv[2]),k=std::stoi(argv[3]);
 if(q<0||k<0)throw std::runtime_error("negative exponent");
 V J=csv(argv[4]),U=csv(argv[5]),C=csv(argv[6]);
 if(U.size()!=3||C!=mirror(C))throw std::runtime_error("bad U or C");
 V source=templ(B,W,J,U,C,q,k),wanted=templ(B,W,J,U,C,q,k+5);
 V d=realize(source);int pal_time=-1;std::string overflows;
 for(int t=0;t<std::stoi(argv[7]);t++){
  if(d==mirror(d)&&pal_time<0)pal_time=t;
  V next=step(d);
  overflows+=std::to_string(next.size()-d.size());
  d.swap(next);
 }
 V got=pairword(d);
 size_t first=0;while(first<std::min(got.size(),wanted.size())&&got[first]==wanted[first])first++;
 bool equal=got==wanted;
 int total=0;for(char c:overflows)total+=c-'0';
 std::cout<<"{\"q\":"<<q<<",\"k\":"<<k<<",\"return\":"<<(equal?"true":"false")<<",\"first_mismatch\":";
 if(equal)std::cout<<"null";else std::cout<<first;
 std::cout<<",\"gamma\":\""<<overflows<<"\",\"sum_gamma\":"<<total<<",\"palindrome_at\":"<<pal_time
          <<",\"digits\":"<<d.size()<<",\"expected_digits\":"<<wanted.size()<<"}\n";
}
