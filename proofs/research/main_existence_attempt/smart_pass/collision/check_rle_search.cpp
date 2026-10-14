// Literal positive-integer controls for the C++ compressed search engine.
#define main rle_search_main
#include "rle_phase_search.cpp"
#undef main
#include <cassert>
string decimal_step(const string&s){
  string low;int carry=0;
  for(int i=int(s.size())-1;i>=0;i--){
    int v=(s[i]-'0')+(s[s.size()-1-i]-'0')+carry;
    low.push_back('0'+v%10);carry=v/10;
  }
  if(carry)low.push_back('0'+carry);
  return string(low.rbegin(),low.rend());
}
string realize_string(const Word&q){
  vector<int>x;for(auto[v,n]:q)for(int i=0;i<n;i++)x.push_back(v);
  vector<int>d(x.size());for(int i=0;i<int(x.size()/2);i++){
    d[i]=max(0,x[i]-9);d[x.size()-1-i]=x[i]-d[i];
  }
  if(x.size()%2){assert(x[x.size()/2]%2==0);d[x.size()/2]=x[x.size()/2]/2;}
  string s;for(auto it=d.rbegin();it!=d.rend();it++)s.push_back('0'+*it);
  assert(s[0]!='0');return s;
}
long long verify(Word q,int horizon){
  string s=realize_string(q);long long count=0;
  for(int t=0;t<horizon;t++){
    auto[out,pal]=step(q);s=decimal_step(s);string backwards(s.rbegin(),s.rend());
    assert(pal==(s==backwards));++count;if(pal)break;
    Word literal;for(int i=0;i<int(s.size());i++)append(literal,s[i]+s[s.size()-1-i]-2*'0',1);
    assert(out==literal);q=out;
  }
  return count;
}
int main(){
  long long count=0,seeds=0;
  for(int a=1;a<=18;a++)for(int b=0;b<=18;b++)for(int x=0;x<=18;x++){
    Word q=canonical({{a,1},{x,3},{b,2},{x,3},{a,1}});
    count+=verify(q,32);++seeds;
  }
  for(int M:{8,9,16})for(int N:{7,13,32}){
    Word q={{9,2},{18,5},{9,2},{0,N},{9,2},{18,M},{9,2},{0,N},{9,2},{18,5},{9,2}};
    count+=verify(q,200);++seeds;
  }
  cout<<"{\"status\":\"C++ RLE search agrees with literal decimal integer arithmetic\",\"seeds\":"<<seeds<<",\"transitions\":"<<count<<"}\n";
}
