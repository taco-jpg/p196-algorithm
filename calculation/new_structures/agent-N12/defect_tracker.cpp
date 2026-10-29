// Exact two-orbit decimal replay and aligned one-extra-zero defect support.
#include <bits/stdc++.h>
using namespace std;
using D=vector<uint8_t>;
D init(int g){string s="39"+string(g,'0')+"43";D d;for(auto it=s.rbegin();it!=s.rend();it++)d.push_back(*it-'0');return d;}
void step(D& d){int n=d.size(),c=0;D e(n+1);for(int i=0;i<n;i++){int v=d[i]+d[n-1-i]+c;e[i]=v%10;c=v/10;}if(c)e[n]=c;else e.pop_back();d.swap(e);}
int main(int argc,char **argv){int maxstep=argc>1?atoi(argv[1]):60000;D d=init(31000),e=init(31001);
cout<<"t,n,ne,mismatch_count,max_distance_center,min_distance_center,leftmost,rightmost,first16equal\n";
int seen=0;bool any16=false;
for(int t=0;t<=maxstep;t++){
  int n=d.size(),ne=e.size(),s=(n+1)/2;int diffs=0,maxdist=0,mindist=INT_MAX,leftmost=INT_MAX,rightmost=-1;
  if(ne!=n+1){cerr<<"length shift changed at "<<t<<"\n";return 3;}
  for(int i=0;i<ne;i++){
   int v=(i<s?d[i]:(i==s?0:d[i-1]));
   if(v!=e[i]){diffs++;maxdist=max(maxdist,abs(i-s));mindist=min(mindist,abs(i-s));leftmost=min(leftmost,i);rightmost=max(rightmost,i);}
  }
  int p16=1;for(int j=0;j<16;j++)if(d[j]+d[n-1-j]!=e[j]+e[ne-1-j])p16=0;
  if(!p16)any16=true;
  if(diffs)seen++;
  if(t==0||t==51450||t==51460||t==51462||t==51463||t==51464||t==51465||t==51466||t==51467||t==51468||t==51469||t==51470||t==51500||t==51600||t==52000||t==52500||t==53000||t==54000||t==55000||t==57500||t==60000 || (t>=51464 && t%100==0))
   cout<<t<<','<<n<<','<<ne<<','<<diffs<<','<<maxdist<<','<<(diffs?mindist:-1)<<','<<(diffs?leftmost:-1)<<','<<rightmost<<','<<p16<<'\n';
  if(t<maxstep){step(d);step(e);}
}
cerr<<"steps_with_nonzero_aligned_defect="<<seen<<"\n";
if(maxstep==60000&&(seen!=8536||any16)){cerr<<"DEFECT_CONTROL_FAILED\n";return 1;}
}
