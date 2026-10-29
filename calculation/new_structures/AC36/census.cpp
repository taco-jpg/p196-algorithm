// AC36 phase-3 p12/m9; genuine 120-step decimal pairword arithmetic.
// Correct on all canonical source integers: P = pair(N+reverse(N)).
// This checks endpoints only; no strict-W9 pruning.
#include <algorithm>
#include <array>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
const vector<int> B={5,2,3,12,16,2,15,10,9,7,18,8,15,9,1,14,0,3,10,0,17,17,9,3,3,15,8,7,9,4,3,3,9,2};
const vector<int> W={4,0,17,11,9,12,2,9,2};
vector<array<int,3>> rotations(){
 vector<array<int,3>> v;
 for(int a=0;a<=18;a+=2){
  array<int,3> x={9,a,18-a};
  for(int r=0;r<3;r++){v.push_back(x);rotate(x.begin(),x.begin()+1,x.end());}
 }
 sort(v.begin(),v.end());return v;
}
vector<int> tpl(const array<int,6>& j,const array<int,3>& u,bool odd,int q,int k){
 vector<int> h=B;
 for(int t=0;t<q;t++)h.insert(h.end(),W.begin(),W.end());
 h.insert(h.end(),j.begin(),j.end());
 for(int t=0;t<k;t++)h.insert(h.end(),u.begin(),u.end());
 vector<int> p=h;
 if(odd)p.insert(p.end(),{4,14,4});
 else p.insert(p.end(),{4,4});
 p.insert(p.end(),h.rbegin(),h.rend());
 return p;
}
struct Check {int first,firstW,overflows;bool clock;};
Check check(const array<int,6>& j,const array<int,3>& u,bool odd,int q=14,int k=100){
 vector<int> p=tpl(j,u,odd,q,k),target=tpl(j,u,odd,q,k+5);
 int overflow=0;bool clock=true;
 vector<int> digit, next;
 digit.reserve(target.size()+1);next.reserve(target.size()+1);
 for(int t=0;t<120;t++){
  digit.clear();int carry=0;
  for(int x:p){int y=x+carry;digit.push_back(y%10);carry=y/10;}
  if(carry)digit.push_back(carry);
  overflow+=int(digit.size())-int(p.size());
  if((digit.size()>p.size())!=(t%4==1))clock=false;
  next.resize(digit.size());
  for(size_t i=0;i<digit.size();i++)next[i]=digit[i]+digit[digit.size()-1-i];
  p.swap(next);
 }
 int first=-1;
 for(size_t i=0;i<min(p.size(),target.size());i++)if(p[i]!=target[i]){first=int(i);break;}
 if(first<0&&p.size()!=target.size())first=int(min(p.size(),target.size()));
 int firstW=-1;
 for(int i=34;i<34+9*q;i++)if(i>=int(p.size())||p[i]!=target[i]){firstW=i;break;}
 return {first,firstW,overflow,clock};
}
int main(int argc,char**argv){
 const auto U=rotations();
 if(argc==2&&string(argv[1])=="control"){
  array<int,6> j={0,0,0,0,0,0};
  for(int rank:{1,13,25})for(int odd:{0,1}){
   auto c=check(j,U[rank-1],odd);
   cout<<"rank="<<rank<<" odd="<<odd<<" first="<<c.first<<" W="<<c.firstW
       <<" gamma="<<c.overflows<<" clock="<<c.clock<<"\n";
  }return 0;
 }
 if(argc!=5){cerr<<"usage: ./census control | ./census U_rank(1-based) J4 J5\n";return 2;}
 int rank=atoi(argv[1]),s4=atoi(argv[2]),s5=atoi(argv[3]);
 // Accept a fourth argument as the fixed first junction symbol, for explicit disjoint slices.
 int s0=atoi(argv[4]);
 if(rank<1||rank>30||s4<0||s4>18||s5<0||s5>18||s0<0||s0>18)return 2;
 long total=0,returns=0,wall=0,correctClock=0;int minW=100000,maxW=-1;
 for(int a=0;a<19;a++)for(int b=0;b<19;b++)for(int c=0;c<19;c++)
  for(int odd=0;odd<2;odd++){
   array<int,6> j={s0,a,b,c,s4,s5};
   auto x=check(j,U[rank-1],odd);
   total++;returns+=(x.first==-1);wall+=(x.firstW==-1);correctClock+=x.clock;
   if(x.firstW>=0){minW=min(minW,x.firstW);maxW=max(maxW,x.firstW);}
  }
 cout<<"rank="<<rank<<" J0="<<s0<<" suffix="<<s4<<","<<s5<<" total="<<total
     <<" returns="<<returns<<" W_repaired="<<wall<<" clock="<<correctClock
     <<" W_mismatch_range="<<minW<<","<<maxW<<"\n";
}