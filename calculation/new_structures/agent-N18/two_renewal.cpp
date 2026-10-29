// Agent N18: constructive two-renewal search, exact decimal pair-coefficient arithmetic.
// Run from this directory: g++ -std=c++17 -O3 two_renewal.cpp -o two_renewal && ./two_renewal
#include <algorithm>
#include <cassert>
#include <fstream>
#include <iostream>
#include <vector>
using namespace std;
int ext[39][8],row[8][20]; vector<int>B,W;
vector<int> templ(const vector<int>&C,int q){
 vector<int>a=B;
 for(int k=0;k<q;k++)a.insert(a.end(),W.begin(),W.end());
 vector<int>p=a;p.insert(p.end(),C.begin(),C.end());
 p.insert(p.end(),a.rbegin(),a.rend());return p;
}
void step(vector<int>&p,int expectedCarry){
 vector<int>d;d.reserve(p.size()+1);int c=0;
 for(int x:p){int t=x+c;d.push_back(t%10);c=t/10;}
 assert(c==expectedCarry);
 if(c)d.push_back(c);
 assert(d.back()!=0);
 vector<int>np(d.size());
 for(size_t i=0;i<np.size();i++)np[i]=d[i]+d[np.size()-1-i];
 p.swap(np);
}
vector<int> advance(vector<int>p){
 for(int t=0;t<88;t++){
  bool odd=false;
  for(int j=0;j<39;j++){
   assert(p[j]==ext[j][t%8]);
   odd|=(p[j]%2!=0);
  }
  assert(odd);
  step(p,(t%2)==0);
 }
 for(int j=0;j<39;j++)assert(p[j]==B[j]);
 return p;
}
vector<int> makeCore(int mut){
 vector<int>U(20,1);U[13]=mut;
 vector<int>C={8,0,0};
 C.insert(C.end(),U.begin(),U.end());C.push_back(16);
 C.insert(C.end(),U.rbegin(),U.rend());
 C.insert(C.end(),{0,0,8});return C;
}
int prefix(const vector<int>&C){
 int k=0;while(k<20&&k<(int)C.size()&&C[k]==W[k])k++;return k;
}
vector<int> nextCore(const vector<int>&C,int q,int&matched){
 vector<int>p=advance(templ(C,q));
 int a=39+20*(q-1);
 vector<int>fixed=B;for(int i=0;i<q-1;i++)fixed.insert(fixed.end(),W.begin(),W.end());
 assert(equal(fixed.begin(),fixed.end(),p.begin()));
 assert(equal(fixed.begin(),fixed.end(),p.rbegin()));
 vector<int>R(p.begin()+a,p.end()-a);
 assert((int)R.size()==(int)C.size()+84);
 matched=prefix(R);
 if(matched==20)R=vector<int>(R.begin()+20,R.end()-20);
 return R;
}
int main(){
 ifstream f("lattice.txt");assert(f);
 for(auto& a:ext)for(int&x:a)f>>x;
 for(auto& a:row)for(int&x:a)f>>x;
 for(auto& a:ext)B.push_back(a[0]);
 for(int x:row[0])W.push_back(x);
 vector<int>success;
 for(int v=0;v<19;v++){
  vector<int>C=makeCore(v);int k0,k1;
  C=nextCore(C,1,k0);
  if(k0!=20)continue;
  C=nextCore(C,1,k1);
  if(k1==20)success.push_back(v);
 }
 assert((success==vector<int>{7,16}));
 cout<<"scan U[13]=0..18: exactly two consecutive renewals for 7,16\n";
 vector<int>expectedC1,expectedC2;
 for(int q=1;q<=4;q++){
  auto C=makeCore(7);int k0,k1,k2;
  auto C1=nextCore(C,q,k0),C2=nextCore(C1,q,k1),C3=nextCore(C2,q,k2);
  assert(k0==20&&k1==20&&k2==8);
  assert(C1.size()==91&&C2.size()==135&&C3.size()==219);
  if(q==1){expectedC1=C1;expectedC2=C2;}
  else assert(C1==expectedC1&&C2==expectedC2);
  cout<<"q="<<q<<" PASS 264 exact steps, renewal prefixes 20,20,8, centre lengths 47,91,135,219\n";
 }
 cout<<"PASS TWO EXACT RENEWALS (264-step third failure characterized)\n";
}
