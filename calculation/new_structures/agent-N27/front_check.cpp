// N27 second result: an overflow-clocked shrinking central 18 plateau.
#define main n27_previous_replay_main
#include "replay.cpp"
#undef main
static int central18(const V &C) {
 int n=(int)C.size(),l=(n-1)/2,r=n/2;
 if(C[l]!=18||C[r]!=18)return 0;
 while(l>0&&C[l-1]==18)--l;
 while(r+1<n&&C[r+1]==18)++r;
 return r-l+1;
}
int main(int argc,char**argv) {
 int m=argc>1?atoi(argv[1]):3000,g=argc>2?atoi(argv[2]):12000,limit=argc>3?atoi(argv[3]):21000;
 S s{{12,9},{6},g,0,0,0,0,0};
 s.C.insert(s.C.end(),m,9);s.C.push_back(6);
 V d=seed_from_pairs(build(s.B,s.C,s.g));
 int totalGamma=0,equalCount=0,firstCollision=-1,firstFlipFail=-1,lastChecked=-1;
 for(int t=0;t<=limit;t++) {
  require(!palindrome(d),"palindrome",t);
  require(pairword(d)==build(s.B,s.C,s.g),"full pairword mismatch",t);
  int q=central18(s.C);
  if(t>0&&totalGamma<m) {
   require(q==m-totalGamma,"central18 != m-cumulative-overflows",t);
   ++equalCount;
  }
  if(t>0&&totalGamma>=m&&firstCollision<0)firstCollision=t;
  if(t==1||t==100||t==1000||t==5000||t==7000||t==7254||
     t==7256||t==20000||t==20629)
   printf("FRONT t=%d S=%d q=%d gap=%d digits=%zu\n",t,totalGamma,q,s.g,d.size());
  lastChecked=t;
  if(t==limit)break;
  V d2=integer_step(d);
  int gamma=(int)d2.size()-(int)d.size();
  bool ok=template_step(s);
  if(!ok){firstFlipFail=t;break;}
  require(s.gam==gamma,"gamma mismatch",t);
  require(s.g>0,"neutral gap exhausted",t);
  totalGamma+=gamma;
  d.swap(d2);
 }
 printf("FRONT RESULT m=%d checked_states=%d equalCount=%d firstCollision=%d firstFlipFailure=%d totalGamma=%d gap=%d\n",
        m,lastChecked+1,equalCount,firstCollision,firstFlipFail,totalGamma,s.g);
 if(m==3000) {
  require(firstCollision==7256,"unexpected first collision",0);
  require(firstFlipFail==20629,"unexpected first flip-fail",0);
  require(equalCount==7255,"unexpected plateau equality count",0);
 }
 return 0;
}
