// N25 paired-firewall scan: maximal *reflection-matched* zero sectors (not independent maximal zero runs).
#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>
using namespace std;
static string next10(const string &s){string q(s.size(),'0');int c=0;for(size_t i=0;i<s.size();++i){int x=s[i]-'0'+s[s.size()-1-i]-'0'+c;q[q.size()-1-i]=char('0'+x%10);c=x/10;}if(c)q.insert(q.begin(),'1');return q;}
int main(int argc,char**argv){int steps=argc>1?atoi(argv[1]):20000;int gap=argc>2?atoi(argv[2]):40001;
 if(gap<=2*steps)throw runtime_error("need gap>2*steps");
 string s="1789"+string(gap,'0')+"3141"+string(gap,'0')+"5926"+string(gap,'0')+"5358";
 int cum=0,prevGamma=0,prevWidth[2]={gap,gap},prevEta[2]={0,0};int deposits[2]={},growth[2]={},bestJump[2]={};
 cout<<"t,G,nominal,outer_paired,central_symmetric,outer_eta,central_eta\n";
 for(int t=0;t<=steps;++t){
  int N=(int)s.size(),w=gap-2*t+cum;
  int l0=4+t,r0=l0+w-1,l1=8+gap+t,r1=l1+w-1;
  if(w<=0||s[l0]!='0'||s[r0]!='0'||s[l1]!='0'||s[r1]!='0')throw runtime_error("nominal firewall lost");
  int extL=0,extR=0,extC=0;
  while(l0-1-extL>=0 && N-l0+extL<N && s[l0-1-extL]=='0' && s[N-l0+extL]=='0')++extL;
  while(r0+1+extR<N && N-r0-2-extR>=0 && s[r0+1+extR]=='0' && s[N-r0-2-extR]=='0')++extR;
  while(l1-1-extC>=0 && r1+1+extC<N && s[l1-1-extC]=='0' && s[r1+1+extC]=='0')++extC;
  int widths[2]={w+extL+extR,w+2*extC};
  for(int j=0;j<2;j++){
   int eta=widths[j]-w;
   if(eta<prevEta[j])throw runtime_error("paired firewall regeneration counter decreased at t="+to_string(t));
   if(t){
    int regen=eta-prevEta[j];deposits[j]+=regen;
    int dw=widths[j]-prevWidth[j];if(dw>0)growth[j]++;
    bestJump[j]=max(bestJump[j],dw);
   }
   prevEta[j]=eta;prevWidth[j]=widths[j];
  }
  if(t%1000==0||t==1848)cout<<t<<','<<cum<<','<<w<<','<<widths[0]<<','<<widths[1]<<','<<widths[0]-w<<','<<widths[1]-w<<'\n';
  if(t==steps)break;
  string q=next10(s);cum+=(q.size()>s.size());prevGamma=cum;s.swap(q);
 }
 cerr<<"FINAL deposits_outer="<<deposits[0]<<" deposits_central="<<deposits[1]<<" width_growth_events_outer="<<growth[0]<<" central="<<growth[1]<<" best_jump_outer="<<bestJump[0]<<" central="<<bestJump[1]<<"\n";
}
