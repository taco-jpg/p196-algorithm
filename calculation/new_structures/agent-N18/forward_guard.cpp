// Agent N18: exact pair-coefficient replay, independent of arbitrary-precision integer arithmetic.
// Source lattice data comes from first p=8 SCC in calculation/decimal_frontier/lattice_formats/p8_scc.txt.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
const int B0[]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
const string ROWS[]={"H31DHBE3I12073ECF97D","CB45CA78CA327A8895HB","639B51FH5174F0HGIBF4","A9D1767ED68BA68FGB8A","2073ECF97DH31DHBE3I1","327A8895HBCB45CA78CA","74F0HGIBF4639B51FH51","8BA68FGB8AA9D1767ED6"};
const int PATH[39][8]={{17,8,17,8,17,8,17,8},
{5,13,6,14,8,16,13,12},
{0,5,11,8,17,16,14,9},
{1,1,2,4,8,16,14,10},
{13,5,10,3,6,14,10,6},
{4,8,16,8,17,14,10,2},
{14,9,18,16,13,12,6,7},
{12,8,16,16,14,9,0,6},
{9,2,5,12,6,11,4,4},
{8,18,17,13,8,14,9,14},
{15,14,10,9,0,8,17,7},
{16,13,8,9,0,0,0,8},
{17,15,12,11,4,4,8,8},
{13,12,6,9,0,4,8,16},
{17,12,5,11,4,4,9,18},
{9,7,16,12,5,9,9,9},
{1,11,2,9,9,15,10,0},
{4,5,11,4,10,0,1,2},
{4,8,16,9,9,0,1,2},
{11,6,13,11,2,12,4,5},
{8,10,1,5,11,4,9,14},
{16,15,11,3,6,8,17,7},
{0,7,16,9,18,15,11,10},
{9,10,0,7,15,15,11,4},
{14,4,9,10,0,6,14,7},
{11,7,14,4,9,10,0,5},
{9,2,4,9,18,8,18,9},
{11,2,4,8,17,17,15,15},
{6,8,17,12,4,12,6,12},
{13,10,1,9,9,14,9,16},
{18,13,7,8,18,8,18,8},
{9,8,18,16,12,12,5,14},
{4,14,9,8,18,12,6,11},
{7,11,4,14,8,17,16,13},
{17,15,12,7,15,14,10,8},
{15,14,9,3,6,12,6,7},
{9,5,12,3,7,13,8,14},
{7,17,15,9,9,16,14,13},
{13,11,4,10,1,10,1,6}};
int val(char c){return c>='0'&&c<='9'?c-'0':c-'A'+10;}
vector<int> make_p(int q){
 vector<int> a(B0,B0+39);
 for(int j=0;j<20*q;j++)a.push_back(val(ROWS[0][j%20]));
 vector<int> p=a;p.push_back(0);
 for(int j=(int)a.size()-1;j>=0;j--)p.push_back(a[j]);
 return p;
}
vector<int> normalize(const vector<int>& p,int &g){
 vector<int> d;d.reserve(p.size()+1);int c=0;
 for(int x:p){int z=x+c;d.push_back(z%10);c=z/10;}
 g=c;if(c)d.push_back(c);
 assert(d.back()!=0);return d;
}
vector<int> pairs(const vector<int>& d){
 vector<int> p(d.size());
 for(size_t i=0;i<d.size();i++)p[i]=d[i]+d[d.size()-1-i];
 return p;
}
int main(int argc,char**argv){
 int q=argc>1?atoi(argv[1]):256,steps=argc>2?atoi(argv[2]):20000;
 auto p=make_p(q);int minBands=INT32_MAX,maxErosion=0,firstB=-1;long long ones=0;
 for(int t=0;t<=steps;t++){
  int phase=t%8;bool bmatch=true;
  for(int j=0;j<39;j++)if(p[j]!=PATH[j][phase]){bmatch=false;if(firstB<0)firstB=t;break;}
  if(!bmatch&&t<steps){cerr<<"B BREAK at "<<t<<"\n";return 2;}
  int matched=0;
  for(int j=39;j<(int)p.size()/2 && p[j]==val(ROWS[phase][(j-39)%20]);j++)matched++;
  minBands=min(minBands,matched/20);
  maxErosion=max(maxErosion,20*q-matched);
  bool oddWitness=false;for(int j=0;j<39;j++)if(p[j]%2){oddWitness=true;break;}
  if(!oddWitness){cerr<<"odd witness lost at "<<t<<"\n";return 3;}
  if(t==steps)break;
  int g;auto d=normalize(p,g);
  if(g!=((t%2)==0)){cerr<<"overflow mismatch "<<t<<"\n";return 4;}
  ones+=g;p=pairs(d);
 }
 cout<<"PASS q="<<q<<" steps="<<steps<<" first_B_break="<<firstB
     <<" min_complete_band="<<minBands<<" max_eroded_columns="<<maxErosion
     <<" final_width="<<p.size()<<" overflows="<<ones<<"\n";
}
