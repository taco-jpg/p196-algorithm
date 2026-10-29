// Agent N18: constructive decimal three-renewal mechanism; exact coefficient replay.
#include <algorithm>
#include <cassert>
#include <fstream>
#include <iostream>
#include <vector>
using namespace std;
int ext[39][8],row[8][20];vector<int>B,W;
vector<int> seed(const vector<int>&C,int q){
 vector<int>a=B;for(int k=0;k<q;k++)a.insert(a.end(),W.begin(),W.end());
 vector<int>P=a;P.insert(P.end(),C.begin(),C.end());P.insert(P.end(),a.rbegin(),a.rend());
 return P;
}
void step(vector<int>&P,int t){
 int c=0;vector<int>d;
 for(int x:P){int y=x+c;d.push_back(y%10);c=y/10;}
 assert(c==((t%2)==0));
 if(c)d.push_back(c);
 assert(d.back()!=0);
 vector<int>np(d.size());
 for(size_t i=0;i<d.size();i++)np[i]=d[i]+d[d.size()-1-i];
 P.swap(np);
}
vector<int> run88(vector<int>P){
 for(int t=0;t<88;t++){
  bool odd=false;
  for(int j=0;j<39;j++){assert(P[j]==ext[j][t%8]);odd|=P[j]%2;}
  assert(odd);step(P,t);
 }
 for(int j=0;j<39;j++)assert(P[j]==B[j]);
 return P;
}
vector<int> candidate(int x,int y){
 vector<int>U(40,1);U[13]=7;U[20]=x;U[30]=y;
 vector<int>C={8,0,0};
 C.insert(C.end(),U.begin(),U.end());C.push_back(16);
 C.insert(C.end(),U.rbegin(),U.rend());
 C.insert(C.end(),{0,0,8});return C;
}
int matchW(const vector<int>&a){int k=0;while(k<20&&k<(int)a.size()&&a[k]==W[k])k++;return k;}
vector<int> transform(const vector<int>&C,int q,int&score){
 auto P=run88(seed(C,q));
 vector<int>fixed=B;
 for(int k=0;k<q-1;k++)fixed.insert(fixed.end(),W.begin(),W.end());
 assert(equal(fixed.begin(),fixed.end(),P.begin()));
 assert(equal(fixed.begin(),fixed.end(),P.rbegin()));
 vector<int>R(P.begin()+fixed.size(),P.end()-fixed.size());
 assert(R.size()==C.size()+84);
 score=matchW(R);
 if(score==20)return vector<int>(R.begin()+20,R.end()-20);
 return R;
}
int main(){
 ifstream f("lattice.txt");assert(f);
 for(auto&v:ext)for(int&x:v)f>>x;
 for(auto&v:row)for(int&x:v)f>>x;
 for(auto&v:ext)B.push_back(v[0]);
 for(int x:row[0])W.push_back(x);
 vector<pair<int,int>> winners;
 for(int x=0;x<=18;x++)for(int y=0;y<=18;y++){
  vector<int>C=candidate(x,y);int k[3]={};
  for(int i=0;i<3;i++){C=transform(C,1,k[i]);if(k[i]!=20)break;}
  if(k[0]==20&&k[1]==20&&k[2]==20)winners.emplace_back(x,y);
 }
 assert((winners==vector<pair<int,int>>{{7,6},{7,15},{16,6},{16,15}}));
 cout<<"361 parameter grid: exact 3-renewal hits (U20,U30)=(7,6),(7,15),(16,6),(16,15)\n";
 vector<int>ref[3];
 for(int q=1;q<=4;q++){
  vector<int>C=candidate(7,6);int s;
  for(int j=0;j<3;j++){
   C=transform(C,q,s);assert(s==20);
   assert(C.size()==(size_t)(131+44*j));
   if(q==1)ref[j]=C;else assert(ref[j]==C);
  }
  C=transform(C,q,s);assert(s==2);
  assert(C.size()==303);
  cout<<"q="<<q<<" PASS 352 steps; 3 renewals, 4th prefix=2/20\n";
 }
 cout<<"PASS independent q-invariant core identities for q=1,2,3,4\n";
}
