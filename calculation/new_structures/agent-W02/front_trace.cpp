#include <bits/stdc++.h>
using namespace std;
const int G[]={1,0,0,0,1,0,0,0,1,0,0,0};
const int W[12][9]={{5,18,4,8,1,15,4,0,5},{10,14,13,12,9,7,10,4,5},{1,10,8,5,9,16,0,9,11},{4,0,17,11,9,12,2,9,2},{8,1,15,4,0,5,5,18,4},{12,9,7,10,4,5,10,14,13},{5,9,16,0,9,11,1,10,8},{11,9,12,2,9,2,4,0,17},{4,0,5,5,18,4,8,1,15},{10,4,5,10,14,13,12,9,7},{0,9,11,1,10,8,5,9,16},{2,9,2,4,0,17,11,9,12}};
const int C[12][9]={{0,0,1,0,0,0,1,0,0},{0,1,1,1,1,1,0,1,0},{1,0,1,0,0,0,1,0,0},{0,0,0,1,1,1,1,0,0},{0,0,0,1,0,0,0,0,1},{1,1,1,0,1,0,0,1,1},{0,0,0,1,0,0,1,0,1},{1,1,1,1,0,0,0,0,0},{1,0,0,0,0,1,0,0,0},{0,1,0,0,1,1,1,1,1},{1,0,0,1,0,1,0,0,0},{1,0,0,0,0,0,1,1,1}};
const int A[]={6,1,0,1,11,14,10,6,11,16,1};
const int B[]={16,0,9,11,1,10,8,5,14,18,0};
const int XX=16000;
int mod9(int x){int a=(x-34)%9;return a>=0?a:a+9;}
int bulk(int phase,int x){return W[phase%12][mod9(x)];}
int cup(int phase,int x){return C[phase%12][mod9(x)];}
struct Patch {vector<signed char> p;int mi=INT_MAX,ma=INT_MIN;Patch():p(XX,-1){}void put(int t,int x,int v){if(v==bulk(t,x))return;p[x]=v;mi=min(mi,x);ma=max(ma,x);}int get(int t,int x)const{int v=p[x];return v<0?bulk(t,x):v;}bool empty()const{return ma<mi;}void assign(int t,int x,const int*sym){for(int j=0;j<11;j++)put(t,x+j,sym[j]);}};
Patch evolve(const Patch&p,int t){Patch out;if(p.empty())return out;int lo=p.mi-18,hi=p.ma+18;assert(lo>=2 && hi+40<XX);vector<signed char> lower(hi-lo+5),upper(hi-lo+5);int c=cup(t,lo-1);for(int x=lo-1;x<=hi+1;x++){int v=p.get(t,x)+c;lower[x-lo+1]=v%10;c=v/10;}c=0;for(int x=hi+30;x>=lo-3;x--){int v=p.get(t,x)+c;if(x>=lo-1&&x<=hi+1)upper[x-lo+1]=v%10;c=v/10;}for(int x=lo+1;x<hi;x++){int v=int(lower[x-lo+1])+int(upper[x-G[t%12]-lo+1]);out.put(t+1,x,v);}return out;}
const int B2[]={2,11,1,6,8,1,7,15,9,3,9,4,7,9,10,16,9,11,4,10,8,8,9,11,11,7,4,3,9,12,1,1,9,11};
uint64_t hashPatch(const Patch&p,int t,int half){uint64_t h=14695981039346656037ULL;for(int i=0;i<half;i++){int d=(p.p[i]<0?0:int(p.p[i])-bulk(t,i));h=(h ^ uint8_t(d+18)) * 1099511628211ULL;}return h;}
int main(int argc,char**argv){for(int ph=0;ph<12;ph++)for(int j=0;j<9;j++){int x=34+j;assert(bulk(ph+76,x+33)==bulk(ph,x));assert(cup(ph+76,x+33)==cup(ph,x));assert(G[(ph+76)%12]==G[ph]);}int maxT=argc>1?atoi(argv[1]):5000;int n=20000;int anchor=2100;Patch a,b;a.assign(2,anchor,A);b.assign(2,anchor,B);int matchA=0,matchB=0, badA=-1,badB=-1, bad2A=-1,bad2B=-1;deque<Patch>qa,qb;int len=n;cout<<"step len Aleft Aright Aedge AfHash Bleft Bright Bedge BfHash\n";for(int k=0;k<=maxT;k++){int half=len/2;auto h1=hashPatch(a,k+2,half),h2=hashPatch(b,k+2,half);cout<<k<<" "<<len<<" "<<a.mi<<" "<<a.ma<<" "<<a.get(k+2,a.ma)<<" "<<h1<<" "<<b.mi<<" "<<b.ma<<" "<<b.get(k+2,b.ma)<<" "<<h2<<"\n";if(k>=76){auto &pa=qa.front(),&pb=qb.front();if(a.ma-pa.ma!=33)badA=k-76;else matchA++;if(b.ma-pb.ma!=33)badB=k-76;else matchB++;if(a.get(k+2,a.ma-1)!=pa.get(k+2-76,pa.ma-1))bad2A=k-76;if(b.get(k+2,b.ma-1)!=pb.get(k+2-76,pb.ma-1))bad2B=k-76;qa.pop_front();qb.pop_front();}qa.push_back(a);qb.push_back(b);if(k<maxT){a=evolve(a,2+k);b=evolve(b,2+k);len+=G[(k+2)%12];}}
cerr<<"FRONT_LOCK A_right_last_failure="<<badA<<" B_right_last_failure="<<badB<<" A_second_site_last_failure="<<bad2A<<" B_second_site_last_failure="<<bad2B<<" checks="<<maxT-75<<" matches="<<matchA<<","<<matchB<<"\n";if(maxT==5000)assert(badA==336&&badB==154&&bad2A==4592&&bad2B==4644);
}
