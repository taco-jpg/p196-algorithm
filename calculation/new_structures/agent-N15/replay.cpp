#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using V=std::vector<uint8_t>;
static V pair(const V &d){
 V p(d.size());for(size_t i=0;i<d.size();++i)p[i]=d[i]+d[d.size()-1-i];return p;
}
static bool palindrome(const V &d){
 for(size_t i=0,j=d.size();i<j/2;++i){if(d[i]!=d[j-1-i])return false;}return true;
}
static V sum_reverse(const V &d,int b){
 V a; a.reserve(d.size()+1);int c=0;
 for(size_t i=0;i<d.size();++i){int s=d[i]+d[d.size()-1-i]+c;
 a.push_back(s%b);c=s/b;}
 if(c){a.push_back(c);}return a;
}
static V sum_pair(const V &p,int b){
 V a;a.reserve(p.size()+1);int c=0;
 for(auto x:p){int s=x+c;a.push_back(s%b);c=s/b;}
 if(c){a.push_back(c);}return a;
}
static V thue(int h,int A,int B){
 V w{(uint8_t)A};
 for(int k=0;k<h;++k){V v;v.reserve(w.size()*2);
 for(int x:w){if(x==A){v.push_back(A);v.push_back(B);}else {v.push_back(B);v.push_back(A);}}w.swap(v);}
 return w;
}
static V make_seed(int h){
 V w=thue(h,14,16);V H{4};H.insert(H.end(),w.begin(),w.end());
 V d(2*H.size());for(size_t i=0;i<H.size();++i){
 int a=(i==0?1:(int)H[i]-9);int z=(int)H[i]-a;
 if(a<0||a>9||z<0||z>9)throw std::runtime_error("bad decomposition");
 d[i]=a;d[d.size()-1-i]=z;}
 if(d.back()==0||d.front()==0)throw std::runtime_error("bad leading/trailing digit");
 return d;
}
static V predicted(int h){
 V w=thue(h,14,16);V H{9,(uint8_t)(2*w[0]-19)};
 for(size_t i=1;i<w.size();++i)H.push_back(2*(w[i]-9));
 V P=H;for(auto i=H.rbegin();i!=H.rend();++i)P.push_back(*i);
 return P;
}
static V predicted_second(int h){
 V q=thue(h,14,16); V Q{9,9};
 for(size_t i=1;i<q.size();++i)Q.push_back(2*(q[i]-9));
 // Q is the lower half at time 1.
 V R{10,9,(uint8_t)(Q[2]-10)};
 for(size_t i=3;i<Q.size();++i)R.push_back(Q[i]+Q[i-1]-18);
 R.push_back(2*(Q.back()-9));
 V out=R;for(size_t i=R.size()-1;i>0;--i)out.push_back(R[i-1]);
 return out;
}
static void replay(const V &seed,int b,int steps,bool check_morphic){
 V d=seed;int overflows=0;V P=pair(d);
 for(int t=0;t<steps;++t){
   if(palindrome(d))throw std::runtime_error("palindrome at t="+std::to_string(t));
   if(P!=pair(d))throw std::runtime_error("pairword invalid at t="+std::to_string(t));
   if(t==1&&check_morphic && P!=predicted(9))throw std::runtime_error("morphic step1 mismatch");
   if(t==2&&check_morphic && P!=predicted_second(9))throw std::runtime_error("morphic step2 mismatch");
   V expected=sum_pair(P,b);
   V actual=sum_reverse(d,b);
   if(expected!=actual)throw std::runtime_error("independent add mismatch t="+std::to_string(t));
   if(actual.size()>d.size())++overflows;
   V nextP=pair(actual);
   if(nextP.size()!=actual.size())throw std::runtime_error("length inconsistency");
   P.swap(nextP);d.swap(actual);
 }
 if(palindrome(d))throw std::runtime_error("palindrome at final step");
 std::cout<<"REPLAY_PASS base="<<b<<" steps="<<steps<<" seed_len="<<seed.size()
          <<" final_len="<<d.size()<<" overflows="<<overflows
          <<" final_first="<<(int)d.back()<<" final_last="<<(int)d.front()
          <<" final_pair_head="<<(int)P.front()<<"\n";
}
int main(int argc,char**argv){
 try{
  int steps=argc>1?std::atoi(argv[1]):20000;
  int h=argc>2?std::atoi(argv[2]):9;
  if(h<1||h>15)throw std::runtime_error("1<=h<=15");
  V d=make_seed(h);
  if(pair(d)!=([&](){V w=thue(h,14,16);V H{4};H.insert(H.end(),w.begin(),w.end());V P=H;for(auto i=H.rbegin();i!=H.rend();++i)P.push_back(*i);return P;}()))throw std::runtime_error("seed pairword");
  replay(d,10,steps,h==9);
 }catch(const std::exception &e){std::cerr<<"FAIL: "<<e.what()<<"\n";return 1;}
}
