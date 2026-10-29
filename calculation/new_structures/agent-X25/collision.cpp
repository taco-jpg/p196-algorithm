// X25. Finite-horizon p8-carrier / transplanted-p12-symbol collision table.
// C++17; exact decimal coefficient normalization, not floating point.
#include <bits/stdc++.h>
using namespace std;
using Word=vector<unsigned char>;
const int B[]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
const int W[]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
const int C[]={8,0,0,16,0,0,8};
const int A[]={6,1,0,1,11,14,10,6,11,16,1};
const int D[]={16,0,9,11,1,10,8,5,14,18,0};
Word seed(int q){Word h;for(int x:B)h.push_back(x);for(int i=0;i<q;i++)for(int x:W)h.push_back(x);Word p=h;for(int x:C)p.push_back(x);reverse(h.begin(),h.end());p.insert(p.end(),h.begin(),h.end());return p;}
Word patch(Word p,int a,const int*code,int b=-1,const int*code2=nullptr){int n=p.size();for(int j=0;j<11;j++)p[a+j]=p[n-1-a-j]=code[j];if(code2)for(int j=0;j<11;j++)p[b+j]=p[n-1-b-j]=code2[j];return p;}
int step(Word &p){int n=p.size(),c=0;Word d(n+1);for(int i=0;i<n;i++){int z=p[i]+c;d[i]=z%10;c=z/10;}if(c)d[n]=c;else d.pop_back();int m=d.size();Word next(m);for(int i=0;i<m;i++)next[i]=d[i]+d[m-i-1];p.swap(next);return c;}
struct Event{int t=-1,j=-1,count=0;};
void trial(int q,int gap,int limit,int a=960){
 Word bg=seed(q);int b=a+gap;
 vector<Word> ps={bg,patch(bg,a,A),patch(bg,a,D),patch(bg,b,A),patch(bg,b,D),patch(bg,a,A,b,D),patch(bg,a,D,b,A)};
 Event ad,da,ad_new,da_new;
 for(int t=0;t<=limit;t++){
  int n=ps[0].size();
  for(const auto &p:ps)if((int)p.size()!=n){cerr<<"length mismatch\n";exit(2);}
  auto collision=[&](Event &out,int k,int l,int r){if(out.t>=0)return;for(int j=0;j<n/2;j++)if((int)ps[k][j]+ps[0][j]-ps[l][j]-ps[r][j]){if(out.j<0)out.j=j;out.count++;}if(out.count)out.t=t;else out.j=-1;};
  auto daughter=[&](Event &out,int k,int l,int r){if(out.t>=0)return;for(int j=0;j<n/2;j++)if(ps[k][j]!=ps[0][j]&&ps[l][j]==ps[0][j]&&ps[r][j]==ps[0][j]){if(out.j<0)out.j=j;out.count++;}if(out.count)out.t=t;else out.j=-1;};
  collision(ad,5,1,4);collision(da,6,2,3);
  daughter(ad_new,5,1,4);daughter(da_new,6,2,3);
  if(ad.t>=0&&da.t>=0&&ad_new.t>=0&&da_new.t>=0)break;
  if(t==limit)break;
  int ref=-1;for(auto &p:ps){int g=step(p);if(ref<0)ref=g;else if(g!=ref){cerr<<"overflow mismatch gap="<<gap<<" t="<<t<<"\n";exit(2);}}
 }
 if(ad.t<0||da.t<0||ad_new.t<0||da_new.t<0){cerr<<"unfinished gap "<<gap<<"\n";exit(2);}
 cout<<"{\"gap\":"<<gap<<",\"AD\":["<<ad.t<<","<<ad.j<<","<<ad.count
     <<"],\"DA\":["<<da.t<<","<<da.j<<","<<da.count
     <<"],\"AD_new\":["<<ad_new.t<<","<<ad_new.j<<","<<ad_new.count
     <<"],\"DA_new\":["<<da_new.t<<","<<da_new.j<<","<<da_new.count<<"]}"<<endl;
}
int main(int argc,char**argv){int q=argc>1?atoi(argv[1]):220;int limit=argc>2?atoi(argv[2]):2200;for(int gap:{180,360,540,720,900,1080,1260,1440})trial(q,gap,limit);}
