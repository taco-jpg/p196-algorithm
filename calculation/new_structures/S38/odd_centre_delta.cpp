// S38: parity-complete extension of the T* mod-101 carry-source delta.
// Build: g++ -O3 -std=c++17 odd_centre_delta.cpp -o odd_centre_delta
#include <algorithm>
#include <array>
#include <cassert>
#include <boost/multiprecision/cpp_int.hpp>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>
using namespace std;
using boost::multiprecision::cpp_int;
using Word = vector<int>;
static const Word B={10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5};
static const Word W={5,18,4,8,1,15,4,0,5};
int md(long long x){x%=101;if(x<0)x+=101;return (int)x;}
int px(int n){static const int a[4]={1,91,100,10};return a[n%4];} // (-10)^n mod 101
int p10(int n){static const int a[4]={1,10,100,91};return a[n%4];}
int geom10(int n){int r=0;for(int i=0;i<n%4;i++)r=md(r+p10(i));return r;}
Word repeat(const Word&a,int n){Word z;z.reserve(a.size()*n);for(int i=0;i<n;i++)z.insert(z.end(),a.begin(),a.end());return z;}
Word rev(Word a){reverse(a.begin(),a.end());return a;}
Word pairword(int q,int k,const Word&J,const Word&U,const Word&C){Word H=B;auto w=repeat(W,q),u=repeat(U,k);H.insert(H.end(),w.begin(),w.end());H.insert(H.end(),J.begin(),J.end());H.insert(H.end(),u.begin(),u.end());Word P=H;P.insert(P.end(),C.begin(),C.end());auto rh=rev(H);P.insert(P.end(),rh.begin(),rh.end());return P;}
struct Norm{int K=0,gamma=0;Word carryOut,digits;};
Norm normalize(const Word&P){Norm n;int c=0;n.carryOut.reserve(P.size());n.digits.reserve(P.size()+1);for(size_t i=0;i<P.size();i++){int v=P[i]+c;n.digits.push_back(v%10);c=v/10;n.carryOut.push_back(c);n.K=md(n.K+1LL*c*px((int)i+1));}n.gamma=c;if(c)n.digits.push_back(c);return n;}
Word sourceDigits(const Word&P){if(P.empty()||!equal(P.begin(),P.end(),P.rbegin()))throw runtime_error("nonpalindromic coefficient word");for(int x:P)if(x<0||x>18)throw runtime_error("coefficient outside 0..18");int n=P.size(),h=n/2;Word d(n);for(int i=0;i<h;i++){d[i]=max(P[i]-9,0);d[n-1-i]=P[i]-d[i];}if(n%2){if(P[h]%2)throw runtime_error("odd midpoint coefficient in odd-length pairword");d[h]=P[h]/2;}if(d.back()==0)throw runtime_error("noncanonical source digits");for(int i=0;i<n;i++)if(d[i]<0||d[i]>9||d[i]+d[n-1-i]!=P[i])throw runtime_error("source pairword mismatch");return d;}
string decimal(const Word&ds){string s;s.reserve(ds.size());for(auto it=ds.rbegin();it!=ds.rend();++it)s.push_back(char('0'+*it));while(s.size()>1&&s.front()=='0')s.erase(s.begin());return s;}
string reverseAddBig(const Word&ds){string s=decimal(ds),r(s.rbegin(),s.rend());cpp_int n(s),nr(r);return (n+nr).convert_to<string>();}
string schoolbookStep(const Word&ds){int c=0;Word out;out.reserve(ds.size()+1);for(size_t i=0;i<ds.size();i++){int v=ds[i]+ds[ds.size()-1-i]+c;out.push_back(v%10);c=v/10;}if(c)out.push_back(c);return decimal(out);}
pair<int,int> block(const Word&u,int c0){int c=c0,A=0;for(size_t i=0;i<u.size();i++){c=(u[i]+c)/10;A=md(A+1LL*c*px((int)i+1));}return {c,A};}
int segmentK(const Word&carries,int lo,int hi){int r=0;for(int i=lo;i<hi;i++)r=md(r+1LL*carries[i]*px(i+1));return r;}
int predictDeltaK(int q,int k,const Word&J,const Word&U,const Word&C,const Norm&old){Word V=rev(U);int a=(int)B.size()+9*q+(int)J.size(),c=(int)C.size(),s=a+3*k,t=s+c,z=t+3*k;int betaU=block(U,0).first,betaU1=block(U,1).first,betaV=block(V,0).first,betaV1=block(V,1).first;if(betaU!=betaU1||betaV!=betaV1)throw runtime_error("U/V carry map did not reset");int AU=block(U,betaU).second;int b=old.carryOut.at(t-1);int AV0=block(V,b).second,AVstar=block(V,betaV).second;if(block(V,b).first!=betaV||block(V,betaV).first!=betaV)throw runtime_error("reverse band carry reset mismatch");int KC=segmentK(old.carryOut,s,s+c),KZ=segmentK(old.carryOut,z,(int)old.carryOut.size());int pred=md(1LL*px(s)*AU+9LL*KC+1LL*px(t)*md(9LL*AV0+1LL*md(1-2LL*geom10(k))*AVstar)-2LL*KZ);return pred;}
vector<Word> motifs(){set<Word> out;for(int a=0;a<=18;a+=2){Word u={9,a,18-a};for(int r=0;r<3;r++){Word v=u;rotate(v.begin(),v.begin()+r,v.end());out.insert(v);}}return vector<Word>(out.begin(),out.end());}
void physicalControl(const Word&P,const Norm&norm,const string&tag){Word ds=sourceDigits(P);string big=reverseAddBig(ds),school=schoolbookStep(ds),normal=decimal(norm.digits);if(big!=school||big!=normal)throw runtime_error("cpp_int / schoolbook / coefficient-normalization mismatch at "+tag);}
int main(){try{auto Us=motifs();if(Us.size()!=30)throw runtime_error("expected 30 U motifs");vector<Word> Js={{5},{0,9,18},{4,12,4,12}};vector<Word> Cs={{10},{2,4,2},{2,18,2}};vector<int> widths;for(int base:{20,40,80,160})for(int phase=0;phase<4;phase++)widths.push_back(base+phase);long long checked=0;for(const auto&U:Us)for(const auto&J:Js)for(const auto&C:Cs)for(int q:widths)for(int k:widths){Word P=pairword(q,k,J,U,C),P5=pairword(q,k+5,J,U,C);Norm old=normalize(P),next=normalize(P5);if(old.gamma!=1||next.gamma!=1)throw runtime_error("rooted phase-zero overflow not 1");if(C.size()%2!=1||!equal(C.begin(),C.end(),C.rbegin())||C[C.size()/2]%2)throw runtime_error("invalid odd palindrome centre");physicalControl(P,old,"source q="+to_string(q)+" k="+to_string(k));physicalControl(P5,next,"target q="+to_string(q)+" k="+to_string(k+5));int predicted=predictDeltaK(q,k,J,U,C,old),actual=md(next.K-old.K);if(predicted!=actual){cerr<<"FAIL q="<<q<<" k="<<k<<" Jlen="<<J.size()<<" C="<<decimal(C)<<" U="<<U[0]<<","<<U[1]<<","<<U[2]<<" predicted="<<predicted<<" actual="<<actual<<"\n";return 1;}checked++;}cout<<"PASS: "<<checked<<" parity-complete carry-source cases (30 U motifs x 3 J x 3 odd palindromic C x 256 independent q,k pairs).\n";cout<<"Each source and k+5 target is a genuine canonical integer; cpp_int n+reverse(n), fresh-buffer schoolbook digit addition, and coefficient normalization agree.\n";cout<<"Exact five-copy delta formula agrees with directly accumulated K(P(q,k+5))-K(P(q,k)) in every case.\n";}catch(const exception&e){cerr<<"FAIL: "<<e.what()<<"\n";return 2;} }
