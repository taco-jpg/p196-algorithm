// Locate real 196 orbit's 9^7 -> 0^6 event and print surrounding 21 steps.
// Letters A..S encode symmetric pair coefficients 0..18.
#include <bits/stdc++.h>
using namespace std;
static int advance(vector<uint8_t>&d,vector<uint8_t>&o){int n=d.size(),c=0;o.resize(n+1);for(int i=0;i<n;i++){int x=d[i]+d[n-i-1]+c;o[i]=x%10;c=x/10;}o[n]=c;d.swap(o);d.resize(n+(c!=0));return c;}
int main(int argc,char**argv){int target=argc>1?atoi(argv[1]):96400,lead=argc>2?atoi(argv[2]):10,tail=argc>3?atoi(argv[3]):10;
 vector<uint8_t>d={6,9,1},o;vector<string>rows;vector<int>lens;int loc=-1;
 for(int t=0;t<=target+tail;t++){
  int m=d.size()/2;vector<uint8_t>p(m);for(int i=0;i<m;i++)p[i]=d[i]+d[d.size()-1-i];
  if(t==target){for(int i=0;i+7<=m;i++){bool hit=true;for(int j=0;j<7;j++)if(p[i+j]!=9)hit=false;if(hit){loc=i;break;}}if(loc<0){cerr<<"no 9^7 at requested step\n";return 2;}}
  if(t>=target-lead){string s;for(auto x:p)s.push_back(char('A'+x));rows.push_back(move(s));lens.push_back(d.size());}
  if(t==target+tail)break;
  advance(d,o);
 }
 cout<<"source_t="<<target<<" chain_start_i="<<loc<<" pairword_char_J_means_9; A=0..S=18\n";
 cout<<"t\tlen\tP[i-12:i+26]\n";int start=max(0,loc-12),end=loc+26;
 for(int t=target-lead;t<=target+tail;t++){string &s=rows[t-(target-lead)];cout<<t<<'\t'<<lens[t-(target-lead)]<<'\t'<<s.substr(start,min((int)s.size(),end)-start)<<'\n';}
}
