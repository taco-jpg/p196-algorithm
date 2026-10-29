// W20 constructive three-level delay gate: exhaustive q=1 census and finite q-clock sample.
// g++ -std=c++17 -O3 -Wall -Wextra -Werror clock_lifetimes.cpp -o clock_lifetimes
// clock_lifetimes lattice_n18.txt
#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
using Bytes=vector<unsigned char>;
array<array<int,8>,39> E;array<int,20>W;array<int,39>B;
Bytes seed(int x,int y,int z,int copies){
  vector<int>u(43,1);u[13]=7;u[20]=7;u[30]=6;u[40]=x;u[41]=y;u[42]=z;
  Bytes c={8,0,0};for(int a:u)c.push_back(a);c.push_back(16);
  for(auto it=u.rbegin();it!=u.rend();++it)c.push_back(*it);
  c.insert(c.end(),{0,0,8});
  Bytes a;for(int b:B)a.push_back(b);for(int j=0;j<copies;j++)for(int b:W)a.push_back(b);
  Bytes p=a;p.insert(p.end(),c.begin(),c.end());p.insert(p.end(),a.rbegin(),a.rend());return p;
}
int lifetime(Bytes p,int horizon){
  Bytes d;d.reserve(p.size()+horizon+1);
  for(int t=0;t<=horizon;t++){
    for(int j=0;j<39;j++)if(p[j]!=E[j][t%8])return t;
    if(t==horizon)break;
    d.clear();int carry=0;
    for(int a:p){int v=a+carry;d.push_back(v%10);carry=v/10;}
    if(carry)d.push_back(carry);
    int n=d.size();p.resize(n);
    for(int i=0;i<n;i++)p[i]=d[i]+d[n-1-i];
  }
  throw runtime_error("horizon insufficient for the first mismatch");
}
int main(int argc,char**argv){
  try{
    if(argc!=2)throw runtime_error("usage: clock_lifetimes lattice.txt");
    ifstream f(argv[1]);if(!f)throw runtime_error("missing fixture");
    for(auto&r:E)for(int&x:r)if(!(f>>x))throw runtime_error("incomplete exterior");
    for(int t=0;t<8;t++)for(int i=0;i<20;i++){
      int v;if(!(f>>v))throw runtime_error("incomplete spatial period");if(t==0)W[i]=v;
    }
    for(int i=0;i<39;i++)B[i]=E[i][0];
    map<int,int> hist;map<int,array<int,3>>representatives;
    for(int x=0;x<19;x++)for(int y=0;y<19;y++)for(int z=0;z<19;z++){
      int t=lifetime(seed(x,y,z,1),500);
      hist[t]++;if(!representatives.count(t))representatives[t]={x,y,z};
    }
    if(hist.size()!=3||hist[300]!=64||hist[324]!=603||hist[364]!=6192)
      throw runtime_error("unexpected q=1 gate classification");
    for(auto [t,n]:hist){auto a=representatives[t];
      cout<<"EXHAUSTIVE q=1 first_break="<<t<<" count="<<n<<" representative="<<a[0]<<","<<a[1]<<","<<a[2]<<"\n";
    }
    int sample[]={1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,32,64,128,240};
    for(auto [t,n]:hist){auto a=representatives[t];
      for(int q:sample){int observed=lifetime(seed(a[0],a[1],a[2],q),88*q+400);
        int expected=88*q+t-88;
        if(observed!=expected)throw runtime_error("affine delay mismatch for representative");
      }
      cout<<"CLOCK_PASS class="<<t<<" q_samples=20 slope=88 intercept="<<t-88<<" largest_q=240 first_break="<<88*240+t-88<<"\n";
    }
    cout<<"PASS\n";
  }catch(const exception&e){cerr<<"FAIL "<<e.what()<<"\n";return 1;}
}
