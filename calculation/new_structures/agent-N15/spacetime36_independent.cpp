// Independent ordinary digit-vector decimal RAA checks of 36-state 16-row macrotiles.
#include <algorithm>
#include <cassert>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>
#include <cstdint>
using V=std::vector<uint8_t>;
struct Cell{std::string f;int cls,left,right;std::vector<int> out;};
static std::string morph(int h,std::string w="0"){for(int k=0;k<h;++k){std::string v;v.reserve(2*w.size());for(char x:w){v.push_back(x);v.push_back(x=='0'?'1':'0');}w.swap(v);}return w;}
static V seed(const std::string&w){int n=2*(int(w.size())+1);V d(n,0);d[0]=0;d[n-1]=4;for(int i=1;i<n/2;i++){d[i]=w[i-1]=='0'?5:7;d[n-1-i]=9;}return d;}
static V raa(const V&d){V v;v.reserve(d.size()+1);int c=0,n=d.size();for(int i=0;i<n;++i){int s=d[i]+d[n-1-i]+c;v.push_back(s%10);c=s/10;}if(c)v.push_back(c);return v;}
static V pair(const V&d){V p(d.size());for(int i=0;i<int(d.size());++i)p[i]=d[i]+d[d.size()-1-i];return p;}
static bool palindrome(const V&d){return std::equal(d.begin(),d.end(),d.rbegin());}
static int max9(const V&p){int n=0,m=0;for(auto x:p){n=x==9?n+1:0;m=std::max(m,n);}return m;}
int main(int argc,char**argv){if(argc!=2){std::cerr<<"need state TSV\n";return 2;}
std::ifstream f(argv[1]);assert(f);std::string line;std::vector<Cell> states;std::unordered_map<std::string,int> idx;
while(std::getline(f,line)){if(line.empty()||line[0]=='#')continue;std::istringstream iss(line);Cell x;int id;std::string csv;iss>>id>>x.f>>x.cls>>x.left>>x.right>>csv;assert(id==int(states.size()));assert(x.f.size()==125);std::istringstream values(csv);std::string token;while(std::getline(values,token,','))x.out.push_back(std::stoi(token));assert(x.out.size()==16);idx[x.f]=id;states.push_back(x);}assert(states.size()==376);assert(idx.size()==376);
std::vector<int> reps(36,-1);for(int i=0;i<int(states.size());i++){auto &x=states[i];assert(x.cls>=0&&x.cls<36);assert(x.left>=0&&x.left<376&&x.right>=0&&x.right<376);if(reps[x.cls]<0)reps[x.cls]=i;else{auto &v=states[reps[x.cls]];assert(x.out==v.out);assert(states[x.left].cls==states[v.left].cls);assert(states[x.right].cls==states[v.right].cls);}std::string s=morph(1,x.f);assert(idx.at(s.substr(62,125))==x.left);assert(idx.at(s.substr(63,125))==x.right);}
assert(std::count_if(reps.begin(),reps.end(),[](int x){return x>=0;})==36);
std::string gamma="011000010101001001";std::vector<std::vector<V>> pByH(15);
std::vector<std::vector<int>> observed(376);int sites=0,cross=0,actualPairs=0;for(int h=2;h<=14;++h){std::string w=morph(h);V d=seed(w);assert(!palindrome(d));std::vector<V> temporal(19);
for(int t=0;t<=18;t++){temporal[t]=pair(d);if(t>=3&&t<=17)assert(max9(temporal[t])<=2);if(t<18){V q=raa(d);if(int(q.size())-int(d.size())!=gamma[t]-'0'){std::cerr<<"gamma mismatch at h="<<h<<" t="<<t<<"\n";return 1;}if(palindrome(q)){std::cerr<<"palindrome h="<<h<<" t="<<t<<"\n";return 1;}d.swap(q);}}
pByH[h]=std::move(temporal);
if(h>=7){for(int c=62;c<int(w.size())-62;++c){int state=idx.at(w.substr(c-62,125));auto &out=states[state].out;if(observed[state].empty())observed[state]=std::vector<int>(16,-1);for(int t=3;t<=18;t++){int actual=pByH[h][t][c+2];if(actual!=out[t-3]){std::cerr<<"incorrect integer value h="<<h<<" t="<<t<<" c="<<c<<"\n";return 1;}observed[state][t-3]=actual;++actualPairs;}++sites;}}
if(h>=9)std::cout<<"DECIMAL_SPACETIME_LEVEL h="<<h<<" word="<<w.size()<<" active_pairword="<<pByH[h][18].size()<<"\n";}
for(int h=7;h<=12;++h){std::string w=morph(h);for(int c=62;c<int(w.size())-62;++c){auto &s=states[idx.at(w.substr(c-62,125))];for(int t=3;t<=18;++t){assert(pByH[h+1][t][2*c+2]==states[s.left].out[t-3]);assert(pByH[h+1][t][2*c+3]==states[s.right].out[t-3]);cross+=2;}}}
int tampered=0;for(int i=0;i<376;++i){assert(observed[i].size()==16);assert(observed[i]==states[i].out);int corrupted=(states[i].out[12]+1)%19;assert(corrupted!=observed[i][12]);++tampered;}
std::cout<<"SPACETIME_ORDINARY_DECIMAL_PASS states=376 classes=36 actual_pair_checks="<<actualPairs<<" cross_scale_children="<<cross<<" state_mutations_rejected="<<tampered<<"\n";}
