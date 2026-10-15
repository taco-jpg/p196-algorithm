#include <bits/stdc++.h>
using namespace std;
// digits little-endian
static int first_hit(vector<int> d, int cap){
  for(int t=1;t<=cap;t++){
    int n=d.size(); vector<int> e(n+1,0); int c=0;
    for(int i=0;i<n;i++){int s=d[i]+d[n-1-i]+c; e[i]=s%10; c=s/10;}
    if(c){e[n]=c;} else e.pop_back();
    d.swap(e); int m=d.size(); bool p=true;
    for(int i=0;i<m/2;i++) if(d[i]!=d[m-1-i]){p=false;break;}
    if(p) return t;
  }
  return -1;
}
static vector<int> mk(const string& s){ vector<int> d(s.rbegin(),s.rend()); for(auto&x:d)x-='0'; return d;}
int main(int argc,char**argv){
  int maxA=atoi(argv[1]), maxC=atoi(argv[2]), cap=atoi(argv[3]);
  vector<int> rs={4,8,12,16,20,24,32};
  vector<string> As,Cs;
  for(int l=1;l<=maxA;l++){int lo=1; for(int i=1;i<l;i++)lo*=10; for(int v=lo;v<lo*10;v++)As.push_back(to_string(v));}
  for(int l=1;l<=maxC;l++){int hi=1; for(int i=0;i<l;i++)hi*=10; for(int v=0;v<hi;v++){string s=to_string(v); while((int)s.size()<l)s="0"+s; Cs.push_back(s);}}
  long cnt=0;
  for(auto&A:As) for(char B='0';B<='9';B++) for(auto&C:Cs){
    cnt++;
    int h4=first_hit(mk(A+string(4,B)+C),cap); if(h4<0) continue;
    int h24=first_hit(mk(A+string(24,B)+C),cap); if(h24<0||h24-h4<8) continue;
    vector<int> hs; bool ok=true;
    for(int r:rs){int h=first_hit(mk(A+string(r,B)+C),cap); if(h<0){ok=false;break;} hs.push_back(h);}
    if(!ok) continue;
    bool inc=true; for(size_t i=0;i+1<hs.size();i++) if(hs[i]>=hs[i+1]) inc=false;
    if(!inc) continue;
    printf("%s [%c]^r %s :",A.c_str(),B,C.c_str()); for(int h:hs)printf(" %d",h); printf("\n");
  }
  fprintf(stderr,"patterns %ld\n",cnt);
}
