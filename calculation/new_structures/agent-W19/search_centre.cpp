// Finite width-four exact hash join; filters non-gauge collisions.
#include <bits/stdc++.h>
using namespace std;
using Word=vector<uint8_t>;
static constexpr int B[]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
static constexpr int W[]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
static Word step_pair(const Word&p){
 Word d;d.reserve(p.size()+1);int c=0;
 for(auto x:p){int y=x+c;d.push_back(y%10);c=y/10;}
 if(c)d.push_back(c);
 Word out(d.size());for(size_t i=0;i<d.size();i++)out[i]=d[i]+d[d.size()-i-1];
 return out;
}
static array<int,4> decode(int z){array<int,4> v{};for(auto&x:v){x=z%19;z/=19;}return v;}
static bool nongauge(int a,int b){auto x=decode(a),y=decode(b);
 for(int i=0;i<4;i++)if(x[i]%9!=y[i]%9)return true;
 return false;
}
static string encode(const Word&w){return string(w.begin(),w.end());}
int main(){
 Word base;for(int v:B)base.push_back(v);for(int v:W)base.push_back(v);
 unordered_map<string,int> seen;seen.reserve(150000);
 for(int z=0;z<19*19*19*19;z++){
  auto c=decode(z);Word h=base;for(int x:c)h.push_back(x);
  Word p=h;for(auto it=h.rbegin();it!=h.rend();++it)p.push_back(*it);
  Word p1=step_pair(p),p2=step_pair(p1);
  string key=encode(p2);auto found=seen.find(key);
  if(found!=seen.end()&&nongauge(found->second,z)){
   int old=found->second;auto oc=decode(old);
   Word hh=base;for(int x:oc)hh.push_back(x);
   Word pp=hh;for(auto it=hh.rbegin();it!=hh.rend();++it)pp.push_back(*it);
   if(step_pair(pp)==p1)continue;
   cout<<"HASH_JOIN_PASS states_considered="<<z+1
       <<" distinct_two_step_keys="<<seen.size()
       <<" old_index="<<old<<" new_index="<<z<<" C0=";
   for(auto x:oc)cout<<x<<",";
   cout<<" C1=";for(auto x:c)cout<<x<<",";
   cout<<" non_gauge=true first_images_distinct=true second_images_equal=true\n";
   return 0;
  }
  if(found==seen.end())seen.emplace(move(key),z);
 }
 cerr<<"no collision found\n";return 1;
}
