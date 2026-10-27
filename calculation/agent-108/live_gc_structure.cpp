// Focused structural checks of the actual exterior MDD's live arena.
// No exterior search or mathematical negative result is claimed here.
// Build/run from the repository root:
//   c++ -std=c++17 -O2 calculation/agent-108/live_gc_structure.cpp -o /tmp/p196-live-gc-check
//   /tmp/p196-live-gc-check
// Sanitizers:
//   c++ -std=c++17 -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer calculation/agent-108/live_gc_structure.cpp -o /tmp/p196-live-gc-sanitize
//   ASAN_OPTIONS=detect_leaks=0 /tmp/p196-live-gc-sanitize
// LeakSanitizer is excluded: it cannot inspect /proc under container ptrace.
#define main agent108_exterior_search_main
#include "exterior_mdd.cpp"
#undef main
#include <set>

namespace {
using Word=vector<int>;
using Language=set<Word>;
struct Statistics {
  size_t checks=0,languages=0,collections=0,stale_throws=0,cap_checks=0;
} statistics;

void require(bool condition,const string &message){
  ++statistics.checks;
  if(!condition)throw runtime_error(message);
}

Language enumerate(const Arena &arena,Id root){
  if(!root)return {};
  const int start_level=arena.nodes[root].level;
  Language words;Word word;
  function<void(Id,int)> visit=[&](Id id,int level){
    const Node &node=arena.nodes[id];
    require(node.level==level,"wrong node level while enumerating");
    if(id==1){
      require(level==arena.G&&int(word.size())==arena.G-start_level,"wrong terminal depth");
      require(words.insert(word).second,"duplicate represented word");return;
    }
    require(level>=0&&level<arena.G&&!node.arcs.empty(),"invalid internal node");
    int previous=-1;
    for(Arc arc:node.arcs){
      require(arc.first>previous&&arc.first<10*(1<<(2*arena.lengths[level])),"invalid arc labels");
      require(arc.second!=0&&arena.nodes.contains(arc.second),"missing nonempty child");
      previous=arc.first;word.push_back(arc.first);visit(arc.second,level+1);word.pop_back();
    }
  };
  visit(root,start_level);return words;
}

bool terminal_suffix(const Arena &arena,int level,const Word &word){
  for(int symbol:word){
    const int width=arena.lengths[level],radix=1<<width;
    const int low=symbol%radix,high=(symbol/radix)%radix,digit=symbol/(radix*radix);
    if(low+high!=radix-1||digit!=9*(low%2))return false;
    if(arena.required_low[level]>=0&&low!=arena.required_low[level])return false;
    ++level;
  }
  return level==arena.G;
}

void check_language(const Arena &arena,Id root,const Language &expected){
  ++statistics.languages;
  require(enumerate(arena,root)==expected,"represented language changed");
  require(arena.nodes[root].count.decimal()==to_string(expected.size()),"wrong language count");
  size_t accepts=0;
  if(root)for(const Word &word:expected)accepts+=terminal_suffix(arena,arena.nodes[root].level,word);
  require(arena.nodes[root].accepts.decimal()==to_string(accepts),"wrong accepting count");
}

Id build(Arena &arena,const Language &words){
  Id root=0;
  for(const Word &word:words)root=arena.unite(root,arena.singleton(word));
  check_language(arena,root,words);return root;
}

void check_arena(const Arena &arena){
  require(arena.live&&arena.nodes.sparse&&arena.nodes.dense.empty(),"live arena retained a dense history");
  require(arena.nodes.contains(0)&&arena.nodes.contains(1),"permanent nodes disappeared");
  require(arena.nodes.size()==arena.nodes.resident.size(),"resident size mismatch");
  require(arena.nodes.size()<=arena.cap,"resident node cap exceeded");
  set<Id> interned;
  set<pair<int,vector<Arc>>> descriptions;
  for(const auto &bucket:arena.unique)for(Id id:bucket.second){
    require(id>=2&&arena.nodes.contains(id),"intern table names a dead/permanent node");
    require(interned.insert(id).second,"duplicate intern-table ID");
    const Node &node=arena.nodes[id];
    uint64_t hash=1469598103934665603ULL;
    hash=(hash^uint64_t(node.level))*1099511628211ULL;
    for(Arc arc:node.arcs){hash=(hash^uint64_t(arc.first))*1099511628211ULL;hash=(hash^uint64_t(arc.second))*1099511628211ULL;}
    require(hash==bucket.first,"intern node is in the wrong hash bucket");
  }
  for(const auto &entry:arena.nodes.resident){
    const Id id=entry.first;const Node &node=entry.second;
    require(uint64_t(id)<arena.nodes.created,"ID exceeds monotone address counter");
    if(id<2)continue;
    require(interned.count(id)==1,"live node missing from intern table");
    require(descriptions.emplace(node.level,node.arcs).second,"duplicate canonical live node");
    check_language(arena,id,enumerate(arena,id));
  }
  for(const auto &entry:arena.union_memo){
    Id a=Id(entry.first>>32),b=Id(entry.first);
    require(arena.nodes.contains(a)&&arena.nodes.contains(b)&&arena.nodes.contains(entry.second),
            "union memo names a dead node");
  }
}

set<Id> reachable(const Arena &arena,const vector<Id> &roots){
  set<Id> reached{0,1};vector<Id> todo=roots;
  while(!todo.empty()){
    Id id=todo.back();todo.pop_back();const Node &node=arena.nodes[id];
    if(!reached.insert(id).second)continue;
    for(Arc arc:node.arcs)todo.push_back(arc.second);
  }
  return reached;
}

void checked_collect(Arena &arena,const vector<Id> &roots){
  const set<Id> expected=reachable(arena,roots);
  map<Id,Node> retained;
  size_t removed_arcs=0;
  for(const auto &entry:arena.nodes.resident){
    if(expected.count(entry.first))retained.emplace(entry.first,entry.second);
    else removed_arcs+=entry.second.arcs.size();
  }
  const size_t before_size=arena.nodes.size();
  const uint64_t before_created=arena.nodes.created,before_nodes=arena.collected_nodes,before_arcs=arena.collected_arcs;
  arena.collect(roots,true);++statistics.collections;
  require(arena.nodes.created==before_created,"GC allocated or recycled an ID");
  require(arena.nodes.size()==expected.size(),"GC did not reclaim exactly the unreachable objects");
  require(arena.collected_nodes-before_nodes==before_size-expected.size(),"wrong reclaimed-node count");
  require(arena.collected_arcs-before_arcs==removed_arcs,"wrong reclaimed-arc count");
  require(arena.union_memo.empty(),"GC failed to clear union memo");
  for(const auto &entry:retained){
    const Node &before=entry.second,&after=arena.nodes[entry.first];
    require(before.level==after.level&&before.arcs==after.arcs
            &&before.count.decimal()==after.count.decimal()
            &&before.accepts.decimal()==after.accepts.decimal(),"GC mutated a retained node");
    require(after.marked,"retained node was not marked");
  }
  check_arena(arena);
}

void stale_throws(const Arena &arena,Id dead){
  require(!arena.nodes.contains(dead),"stale-ID control is still resident");
  bool threw=false;
  try{(void)arena.nodes[dead];}catch(const out_of_range &){threw=true;}
  require(threw,"stale ID did not throw out_of_range");++statistics.stale_throws;
}

void language_and_alias_controls(){
  Pattern p=pattern("1101000"); // block lengths 1,2,4
  Arena arena(p,"",1000,1000000,30,true);
  const Language a{{0,0,0},{1,0,0}},b{{0,1,0},{1,1,0}};
  const Language diagonal{{0,0,0},{1,1,0}};
  const Language all{{0,0,0},{1,0,0},{0,1,0},{1,1,0}};
  const Language terminals{{2,12,240},{37,153,2499}};
  const Language garbage{{3,4,5},{6,7,8}};
  Id physical=arena.singleton(p.initial),ra=build(arena,a),rb=build(arena,b);
  Id rd=build(arena,diagonal),ru=arena.unite(ra,rb),rt=build(arena,terminals),dead=build(arena,garbage);
  check_language(arena,ru,all);
  require(ra!=rb&&rd!=ru,"different correlated languages collapsed");
  require(arena.nodes[ra].arcs.size()==2&&arena.nodes[ra].arcs[0].second==arena.nodes[ra].arcs[1].second,
          "shared suffix was not canonicalized");
  require(arena.nodes[rt].accepts.decimal()=="2","manual all-e terminal language should accept twice");
  require(!arena.union_memo.empty(),"union-cache clearing control was vacuous");
  check_arena(arena);
  checked_collect(arena,{physical,ra,ra,ru,rt});
  stale_throws(arena,dead);stale_throws(arena,rb);stale_throws(arena,rd);
  const uint64_t next=arena.nodes.created;
  Id fresh_b=build(arena,b),fresh_garbage=build(arena,garbage);
  require(fresh_b>=next&&fresh_b!=rb&&fresh_garbage>dead,"reconstruction reused a dead address");
  require(arena.unite(ra,fresh_b)==ru,"retained equal language lost its canonical ID");
  require(build(arena,all)==ru,"rebuilding a retained language changed its root ID");
  const uint64_t stable_created=arena.nodes.created;
  require(arena.intern(arena.nodes[ru].level,arena.nodes[ru].arcs)==ru
          &&arena.nodes.created==stable_created,"reinterning a retained node allocated a duplicate");
  // Releasing one alias keeps ra pinned; releasing the last allows its root
  // object to disappear even though its suffixes remain shared with ru.
  checked_collect(arena,{physical,ra,ru,rt});
  check_language(arena,ra,a);stale_throws(arena,fresh_b);stale_throws(arena,fresh_garbage);
  checked_collect(arena,{physical,ru,rt});stale_throws(arena,ra);
  check_language(arena,ru,all);check_language(arena,rt,terminals);
  checked_collect(arena,{});
  require(arena.nodes.size()==2&&arena.unique.empty()&&arena.nodes.created>2,"empty pin set retained history");

  Arena fixed(p,"0000000",1000,1000000,30,true);
  Id rf=build(fixed,terminals);
  require(fixed.nodes[rf].accepts.decimal()=="1","manual fixed-e terminal language should accept once");
  checked_collect(fixed,{rf,rf});check_language(fixed,rf,terminals);
}

void cadence_and_capacity_controls(){
  Pattern p=pattern("1101000");
  Arena cadence(p,"",1000,1000000,30,true,3);
  Id kept=cadence.singleton({0,0,0}),dead=cadence.singleton({1,1,1});
  size_t before=cadence.nodes.size();
  cadence.collect({kept});cadence.collect({kept});
  require(cadence.collections==0&&cadence.nodes.size()==before&&cadence.nodes.contains(dead),
          "collection cadence swept too early");
  cadence.collect({kept});++statistics.collections;
  require(cadence.collections==1&&cadence.boundaries==3,"collection cadence missed its boundary");
  stale_throws(cadence,dead);check_language(cadence,kept,{{0,0,0}});check_arena(cadence);

  Arena capped(p,"",8,1000000,30,true);
  Id first=capped.singleton({0,0,0});
  (void)capped.singleton({1,1,1});
  require(capped.nodes.size()==8,"resident-cap setup has the wrong size");
  bool failed=false;
  try{(void)capped.singleton({2,2,2});}
  catch(const Limit &limit){require(limit.reason=="node_cap","wrong resident-cap reason");failed=true;}
  require(failed,"resident cap did not fire");++statistics.cap_checks;
  checked_collect(capped,{first});
  Id later=capped.singleton({2,2,2});
  require(capped.nodes.size()==8&&capped.nodes.created==11&&later==10,
          "resident cap incorrectly charged historical IDs");
  check_language(capped,later,{{2,2,2}});check_arena(capped);

  // Model a long history already reclaimed: this allocates only three nodes.
  NodeStore addresses(true);
  addresses.append({-1,{},0,0});addresses.append({0,{},1,1});
  addresses.created=numeric_limits<Id>::max();
  Id last=addresses.append({0,{},1,1});
  require(last==numeric_limits<Id>::max()&&addresses.contains(last),"last valid ID was lost");
  failed=false;
  try{(void)addresses.append({0,{},1,1});}
  catch(const Limit &limit){require(limit.reason=="node_id_cap","wrong address-cap reason");failed=true;}
  require(failed&&addresses.size()==3&&addresses.created==uint64_t(numeric_limits<Id>::max())+1,
          "ID address wrapped or changed after its cap");++statistics.cap_checks;
}
} // namespace

int main(){
  try{
    language_and_alias_controls();cadence_and_capacity_controls();
    cout<<"PASS LIVE_GC_STRUCTURE language_checks="<<statistics.languages
        <<" collections="<<statistics.collections<<" stale_throws="<<statistics.stale_throws
        <<" cap_checks="<<statistics.cap_checks<<" invariant_checks="<<statistics.checks<<'\n';
    cout<<"ALL STRUCTURAL LIVE-GC CHECKS PASSED\n";return 0;
  }catch(const Limit &limit){cerr<<"unexpected limit: "<<limit.reason<<'\n';return 1;}
  catch(const exception &error){cerr<<error.what()<<'\n';return 1;}
}
