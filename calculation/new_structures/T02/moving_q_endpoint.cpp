#include <boost/multiprecision/cpp_int.hpp>
#include <algorithm>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>
using boost::multiprecision::cpp_int;
using V=std::vector<int>;
static const V B={10,4,7,5,13,6,11,1,9,16,16,18,10,9,4,8,1,7,0,2,15,15,9,7,7,10,17,14,18,8,6,6,18,4};
static const V W={8,1,15,4,0,5,5,18,4};
static const V J={17,5,5,9,6,6,6,14,5,11,7,10,14,7,8,15,9,6,4,18,9,10,17,2};
static const V C={4,14,4};
static V reverse(V x){std::reverse(x.begin(),x.end());return x;}
static V repeat(const V&w,int k){V r;r.reserve(w.size()*k);for(int i=0;i<k;i++)r.insert(r.end(),w.begin(),w.end());return r;}
static V rotate(V u,int n){n=(n%int(u.size())+int(u.size()))%int(u.size());std::rotate(u.begin(),u.begin()+n,u.end());return u;}
static std::vector<V> all_u(){std::vector<V> out;for(int a=0;a<=18;a+=2){V w={9,a,18-a};for(int s=0;s<3;s++){V u=rotate(w,s);if(std::find(out.begin(),out.end(),u)==out.end())out.push_back(u);}}return out;}
static V templ(int q,int k,const V&u){V h=B;V w=repeat(W,q),v=repeat(u,k);h.insert(h.end(),w.begin(),w.end());h.insert(h.end(),J.begin(),J.end());h.insert(h.end(),v.begin(),v.end());V p=h;p.insert(p.end(),C.begin(),C.end());V rh=reverse(h);p.insert(p.end(),rh.begin(),rh.end());return p;}
static V realize(const V&p){int n=p.size();V d(n);for(int i=0;i<n/2;i++){d[i]=std::max(0,p[i]-9);d[n-1-i]=std::min(9,p[i]);}if(n%2){if(p[n/2]%2)throw std::runtime_error("odd centre coefficient");d[n/2]=p[n/2]/2;}if(d.back()==0)throw std::runtime_error("leading zero");return d;}
static bool palindrome(const V&d){return std::equal(d.begin(),d.begin()+d.size()/2,d.rbegin());}
static V digit_step(const V&d){int n=d.size(),carry=0;V out(n);for(int i=0;i<n;i++){int z=d[i]+d[n-1-i]+carry;out[i]=z%10;carry=z/10;}if(carry)out.push_back(carry);return out;}
static cpp_int from_digits(const V&d){cpp_int n=0;for(auto i=d.rbegin();i!=d.rend();++i){n*=10;n+=*i;}return n;}
static V to_digits(const cpp_int&n){std::string s=n.str();V d;d.reserve(s.size());for(auto i=s.rbegin();i!=s.rend();++i)d.push_back(*i-'0');return d;}
static cpp_int bigint_step(const cpp_int&n){std::string s=n.str();std::reverse(s.begin(),s.end());size_t z=0;while(z+1<s.size()&&s[z]=='0')++z;return n+cpp_int(s.substr(z));}
static V pairword(const V&d){V p(d.size());for(size_t i=0;i<d.size();i++)p[i]=d[i]+d[d.size()-1-i];return p;}
static bool slice_eq(const V&p,size_t s,const V&w,size_t n){if(s+n>p.size())return false;for(size_t i=0;i<n;i++)if(p[s+i]!=w[i%w.size()])return false;return true;}
static int endpoint_hits(const V&p,int q,int k,const std::vector<V>&targets){int hits=0;for(int a=1;a<=10&&a<q;a++){int qp=q-a,kp=k+10+3*a;size_t cut=B.size()+W.size()*size_t(qp);if(!std::equal(B.begin(),B.end(),p.begin())||!slice_eq(p,B.size(),W,W.size()*size_t(qp)))continue;for(int jl=0;jl<=25;jl++){int cl=51-2*jl;size_t us=cut+jl,half=us+3*size_t(kp);if(2*half+size_t(cl)!=p.size())continue;V center(p.begin()+half,p.end()-half);if(center.size()!=size_t(cl)||!std::equal(center.begin(),center.end(),center.rbegin()))continue;for(const V&u:targets)if(slice_eq(p,us,u,u.size()*size_t(kp)))hits++;}}return hits;}
int main(){auto words=all_u();if(words.size()!=30)return 2;long long trajectories=0,steps=0,palindromes=0,clock_errors=0,engine_mismatches=0;int hits=0;for(int q:{20,40,80,160}){int k=4*q;for(const V&u:words){V p=templ(q,k,u),d=realize(p);cpp_int n=from_digits(d);bool any_pal=palindrome(d);if(any_pal)palindromes++;int overflow_sum=0;for(int t=1;t<=240;t++){V d2=digit_step(d);cpp_int n2=bigint_step(n);if(to_digits(n2)!=d2){engine_mismatches++;std::cerr<<"ENGINE_MISMATCH q="<<q<<" t="<<t<<"\n";return 3;}int g=int(d2.size()>d.size());overflow_sum+=g;if(g!=(t%4==1?1:0))clock_errors++;if(palindrome(d2)){any_pal=true;palindromes++;}d.swap(d2);n.swap(n2);steps++;}if(overflow_sum!=60)clock_errors++;hits+=endpoint_hits(pairword(d),q,k,words);trajectories++;std::cout<<"DONE q="<<q<<" k="<<k<<" U="<<u[0]<<","<<u[1]<<","<<u[2]<<" digits="<<d.size()<<" palindrome="<<any_pal<<"\n";}}
std::cout<<"SUMMARY U=30 trajectories="<<trajectories<<" steps="<<steps<<" engine_mismatches="<<engine_mismatches<<" clock_errors="<<clock_errors<<" palindrome_occurrences="<<palindromes<<" endpoint_hits_all_Uprime_a1_to10="<<hits<<"\n";return(engine_mismatches||clock_errors||hits)?4:0;}
