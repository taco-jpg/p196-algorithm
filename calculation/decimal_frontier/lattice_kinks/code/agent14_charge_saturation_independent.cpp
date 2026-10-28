// Independent exhaustive check of the three-site congruence map.
// g++ -O2 -std=c++17 calculation/decimal_frontier/lattice_kinks/code/agent14_charge_saturation_independent.cpp -o /tmp/p196_agent14_charge && /tmp/p196_agent14_charge
#include <cassert>
#include <cstdio>
#include <set>
#include <tuple>
using namespace std;
int mod(int a,int m){return (a%m+m)%m;}
int main(){
 set<tuple<int,int,int>> got;
 for(int u=0;u<=18;++u)for(int v=0;v<=18;++v)for(int r=0;r<=9;++r)
  got.emplace(mod(u+v+2*r,3),mod(-2*u-2*v-3*r,9),mod(2*u-2*v+2*r,11));
 assert(got.size()==297);
 for(int a=0;a<3;++a)for(int b=0;b<9;++b)for(int c=0;c<11;++c)
  assert(got.count({a,b,c})==1);
 printf("INDEPENDENT 3610-ASSIGNMENT RESIDUE COVERAGE: 297/297 PASSED\n");
}
