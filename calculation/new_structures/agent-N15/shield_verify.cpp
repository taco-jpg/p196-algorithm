// Independent ordinary decimal digit-list replay. Does not use pairword normalisation.
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <vector>
using V=std::vector<uint8_t>;
V seed(int h,int centre){
 V word{14};
 for(int j=0;j<h;j++){
  V next;next.reserve(word.size()*2);
  for(auto v:word){if(v==14){next.push_back(14);next.push_back(16);}else{next.push_back(16);next.push_back(14);}}
  word.swap(next);
 }
 V lo{1},hi{3};
 for(int v:word){lo.push_back(v-9);hi.push_back(9);}
 V d=lo;d.push_back(centre/2);
 for(auto it=hi.rbegin();it!=hi.rend();it++)d.push_back(*it);
 if(d.front()==0||d.back()==0)throw std::runtime_error("not a positive canonical number");
 return d;
}
V step(const V&d){
 V output;output.reserve(d.size()+1);int carry=0;
 for(size_t i=0;i<d.size();i++){
  int s=int(d[i])+int(d[d.size()-1-i])+carry;
  output.push_back(s%10);carry=s/10;
 }
 if(carry)output.push_back(carry);
 return output;
}
bool equal_exterior(const V&a,const V&b,int k){
 if(a.size()!=b.size())return false;
 for(int i=0;i<k;i++)if(int(a[i])+int(a[a.size()-1-i])!=int(b[i])+int(b[b.size()-1-i]))return false;
 return true;
}
int main(){
 const int K[5]={4,8,16,32,64};
 const int times[7][5]={{337,317,280,187,6}, {648,629,587,508,364},
 {1450,1433,1355,1267,1097}, {3222,3199,3160,3032,2774},
 {5865,5839,5796,5715,5527}, {11614,11586,11546,11456,11257},
 {23289,23263,23223,23143,22999}};
 for(int h=6;h<=12;h++){
   V x=seed(h,0),y=seed(h,18);
   if(x==y)throw std::runtime_error("same seeds");
   int max_t=times[h-6][0];
   for(int t=0;t<=max_t;t++){
     for(int j=0;j<5;j++){
       const bool same=equal_exterior(x,y,K[j]);
       if(same!=(t<times[h-6][j]))
         throw std::runtime_error("wrong window crossing h="+std::to_string(h)+" t="+std::to_string(t)+" k="+std::to_string(K[j]));
     }
     if(t<max_t){x=step(x);y=step(y);}
   }
   std::cout<<"DIGIT_REPLAY_SHIELD_PASS h="<<h<<" outer4="<<times[h-6][0]<<" outer64="<<times[h-6][4]<<"\n";
 }
}
