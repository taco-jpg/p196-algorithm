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
int main(int argc,char**argv){int steps=argc>1?atoi(argv[1]):2400;vector<int>ds;for(int i=2;i<argc;i++)ds.push_back(atoi(argv[i]));if(ds.empty())for(int k=15;k<150;k++)ds.push_back(k*9);for(int gap:ds){Patch aa,bb,ab;aa.assign(2,1200,A);bb.assign(2,1200+gap,B);ab.assign(2,1200,A);ab.assign(2,1200+gap,B);int first=-1,at=-1,loA=-1,hiA=-1,loB=-1,hiB=-1;for(int k=0;k<=steps;k++){int t=2+k;if(!aa.empty()&&!bb.empty()&&aa.ma>=bb.mi){int lo=min({aa.mi,bb.mi,ab.mi}),hi=max({aa.ma,bb.ma,ab.ma});for(int x=lo;x<=hi;x++){int d=ab.get(t,x)-aa.get(t,x)-bb.get(t,x)+bulk(t,x);if(d){first=k;at=x;loA=aa.mi;hiA=aa.ma;loB=bb.mi;hiB=bb.ma;break;}}}if(first>=0||k==steps)break;aa=evolve(aa,t);bb=evolve(bb,t);ab=evolve(ab,t);}cout<<gap<<" "<<first<<" "<<at<<" "<<loA<<":"<<hiA<<" "<<loB<<":"<<hiB<<"\n"<<flush;}}
