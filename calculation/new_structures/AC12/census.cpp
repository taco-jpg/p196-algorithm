#include <array>
#include <vector>
#include <map>
#include <algorithm>
#include <iostream>
#include <cstdlib>
#include <cstdint>
using namespace std;
using Byte=uint8_t;
const vector<Byte> B={5,2,3,12,16,2,15,10,9,7,18,8,15,9,1,14,0,3,10,0,17,17,9,3,3,15,8,7,9,4,3,3,9,2};
const vector<Byte> W={4,0,17,11,9,12,2,9,2};
const vector<vector<Byte>> Cs={{4,14,4},{4,4}};
const int q=14,k=100,steps=120;
vector<array<Byte,3>> U;
void init_u(){for(int a=0;a<=18;a+=2){array<Byte,3> u={(Byte)9,(Byte)a,(Byte)(18-a)};for(int rot=0;rot<3;rot++){U.push_back(u);rotate(u.begin(),u.begin()+1,u.end());}}}
vector<Byte> make(int jcode,int n,const array<Byte,3>& u,const vector<Byte>& c,int dk=0){
 vector<Byte> h;h.reserve(34+9*q+n+3*(k+dk));
 h.insert(h.end(),B.begin(),B.end());for(int i=0;i<q;i++)h.insert(h.end(),W.begin(),W.end());
 for(int i=0;i<n;i++){h.push_back(jcode%19);jcode/=19;}
 for(int i=0;i<k+dk;i++)for(Byte b:u)h.push_back(b);
 vector<Byte> p=h;p.insert(p.end(),c.begin(),c.end());p.insert(p.end(),h.rbegin(),h.rend());return p;
}
int step(vector<Byte>& p,vector<Byte>& digits,vector<Byte>& out){
 digits.clear();digits.reserve(p.size()+1);int carry=0;
 for(Byte b:p){int s=b+carry;digits.push_back(s%10);carry=s/10;}
 if(carry)digits.push_back(carry);
 out.resize(digits.size());int N=digits.size();
 for(int i=0;i<N;i++)out[i]=digits[i]+digits[N-1-i];
 p.swap(out);return carry;
}
struct Counts{uint64_t attempted=0,prefix_equal=0,all_equal=0,length_wrong=0,gamma_wrong=0;map<int,uint64_t> hist;};
int main(int argc,char**argv){
 int n=argc>1?atoi(argv[1]):3;long long begin=argc>2?atoll(argv[2]):0;long long end=argc>3?atoll(argv[3]):100;int ui=argc>4?atoi(argv[4]):-1;int ci=argc>5?atoi(argv[5]):-1;
 init_u();long long space=1;for(int i=0;i<n;i++)space*=19;begin=max(0LL,begin);end=min(space,end);
 int prefix=B.size()+W.size()*q;
 vector<Byte> target;target.reserve(prefix);target.insert(target.end(),B.begin(),B.end());for(int z=0;z<q;z++)target.insert(target.end(),W.begin(),W.end());
 Counts t; vector<Byte> p,digits,out;
 for(long long jc=begin;jc<end;jc++)for(int uix=0;uix<30;uix++){if(ui>=0&&ui!=uix)continue;
 for(int cix=0;cix<2;cix++){if(ci>=0&&ci!=cix)continue;
 p=make(jc,n,U[uix],Cs[cix]);int length=p.size(),gamma=0;
 for(int s=0;s<steps;s++)gamma+=step(p,digits,out);
 t.attempted++;
 if(int(p.size())!=length+30)t.length_wrong++;
 if(gamma!=30)t.gamma_wrong++;
 int mismatch=-1;
 for(int i=0;i<prefix;i++)if(p[i]!=target[i]){mismatch=i;break;}
 if(mismatch<0){t.prefix_equal++;auto expected=make(jc,n,U[uix],Cs[cix],5);if(expected==p)t.all_equal++;}
 else t.hist[mismatch-prefix]++;
 }}
 cout<<"n="<<n<<" j_start="<<begin<<" j_end="<<end<<" u="<<ui<<" c="<<ci<<" attempted="<<t.attempted<<" prefix_equal="<<t.prefix_equal<<" all_equal="<<t.all_equal<<" length_wrong="<<t.length_wrong<<" gamma_wrong="<<t.gamma_wrong<<" first_mismatch_offset=";
 for(auto [i,v]:t.hist)cout<<i<<":"<<v<<",";cout<<"\n";
 return 0;
}
