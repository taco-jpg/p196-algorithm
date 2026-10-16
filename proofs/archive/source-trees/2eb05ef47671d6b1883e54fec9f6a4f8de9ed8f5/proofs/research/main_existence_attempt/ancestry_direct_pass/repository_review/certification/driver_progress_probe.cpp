// Small mock-backend probe. It does not run a production/emulator executable,
// load a checkpoint, launch CUDA, or modify upstream files.
#include <iostream>
#include <stdexcept>
#include "driver8.h"

struct Mock {
  int backups=0,zeroSteps=0,n=3;
  bool stopSecondBackup=false,stopSecondZero=false;
  int numSMs(){return 1;}
  int tbBlocksPerSM(size_t){return 1;}
  void init(const std::vector<bits::u32>&,int nn,int,const tb::Conf&,int){n=nn;}
  void backup(int){if(++backups==2&&stopSecondBackup)throw std::runtime_error("bounded_probe_stop");}
  void restore(){}
  int currentN(){return n;}
  void stepRun(int count,std::vector<unsigned>& bad,int){
    bad.assign(count,1u);
    if(count==0&&++zeroSteps==2&&stopSecondZero)throw std::runtime_error("bounded_probe_stop");
  }
  void tbLaunch(int,long long,int){}
  d5::TBResult tbSync(){return {0,-1,n};}
};

int main(){
  d5::Opts opts;opts.K=1;opts.tile=4;opts.mode="step";opts.window=-1;
  Mock a;a.stopSecondBackup=true;
  d5::Engine<Mock> x(a,opts);x.setup("196",0,8);
  bool stopped=false;try{x.advance(1);}catch(const std::runtime_error&){stopped=true;}
  if(!stopped||a.backups!=2||x.it!=-1)return 1;
  std::cout<<"{\"case\":\"negative_window\",\"accepted_by_setup\":true,\"window\":"
    <<x.o.window<<",\"iteration_after_one_outer_pass\":"<<x.it<<",\"backup_calls\":"<<a.backups<<"}\n";

  opts.window=4;opts.batch=0;
  Mock b;b.stopSecondZero=true;
  d5::Engine<Mock> y(b,opts);y.setup("196",0,8);
  stopped=false;try{y.stepAdvance(1);}catch(const std::runtime_error&){stopped=true;}
  if(!stopped||b.zeroSteps!=2||y.it!=0)return 2;
  std::cout<<"{\"case\":\"zero_batch_setup_used_by_run_mode\",\"accepted_by_setup\":true,\"zero_step_calls\":"
    <<b.zeroSteps<<",\"iteration\":"<<y.it<<"}\n";

  opts.batch=4;opts.halo=-4;
  Mock c;d5::Engine<Mock> z(c,opts);z.setup("196",0,8);
  if(z.conf.HW!=-4)return 3;
  std::cout<<"{\"case\":\"negative_halo\",\"accepted_by_setup\":true,\"halo_words\":"<<z.conf.HW<<"}\n";
}
