// Actual functions.exec orchestration; requires tools, load, store, and text supplied by that runtime.
// Hydrate the exact input keys from STACK_INPUTS.json. No branch/ref mutations are present.

async function preflightStack154(){
 function u(r){const s=r.structuredContent;if(s?.content){try{return JSON.parse(s.content)}catch{return s}}return s??r}
 const repo="taco-jpg/p196-algorithm",api="https://api.github.com/repos/"+repo,B=load("stack154_main").object.sha,BT=load("comb132_current").BT;
 if(B!==load("comb132_current").B)throw new Error("Base changed before source preflight");
 const pending=new Map(),used=new Set();
 async function tree(sha){
  used.add(sha);const cached=load("gt_"+sha);if(cached)return cached;
  if(!pending.has(sha))pending.set(sha,(async()=>{const r=u(await tools.mcp__codex_apps__github_fetch({url:api+"/git/trees/"+sha}));if(r.truncated||!r.tree||r.sha!==sha)throw new Error("Invalid tree "+sha);store("gt_"+sha,r);return r;})());
  return pending.get(sha);
 }
 async function lookup(root,path){const ps=path.split("/");let t=root;for(let i=0;i<ps.length;i++){const e=(await tree(t)).tree.find(x=>x.path===ps[i]);if(!e)return null;if(i===ps.length-1)return e;if(e.type!=="tree")throw new Error("Non-directory ancestor "+path);t=e.sha;}}
 const stages=[],seen=new Map();
 for(const s of load("stack154_specs")){
  const rows=[];
  for(let j=0;j<s.files.length;j+=8){
   const out=await Promise.allSettled(s.files.slice(j,j+8).map(async f=>{
    if(f.status!=="added"||f.deletions!==0)throw new Error("Non-additive source "+f.filename);
    const [h,b]=await Promise.all([lookup(s.tree,f.filename),lookup(BT,f.filename)]);
    if(!h||h.sha!==f.sha||h.type!=="blob"||h.mode!=="100644")throw new Error("Source entry mismatch "+f.filename);
    if(b)throw new Error("Existing current-main path requires reconciliation "+f.filename);
    if(seen.has(f.filename))throw new Error("Overlapping stack path "+f.filename);
    seen.set(f.filename,s.pr);
    return {path:f.filename,sha:f.sha,mode:h.mode,type:h.type,size:h.size,status:"EXACT_SOURCE_AND_ABSENT_FROM_CURRENT_MAIN"};
   }));
   for(const x of out){if(x.status!=="fulfilled")throw x.reason;rows.push(x.value);}
  }
  stages.push({pr:s.pr,H:s.H,HT:s.tree,count:rows.length,entries:rows});
 }
 const result={B,BT,status:"PASS_ADDITIVE_STACK_SOURCE_PREFLIGHT",stages,total_new_paths:seen.size,unique_paths:seen.size,used_tree_hashes:[...used],fresh_lean:"NOT_RUN",integration:"UNATTACHED_CANDIDATE_PREPARATION_ONLY"};
 store("stack154_preflight",result);
 return {B,BT,status:result.status,stages:stages.map(x=>({pr:x.pr,H:x.H,count:x.count})),total_new_paths:seen.size,trees_read_or_reused:used.size};
}

async function constructStack154(){
 function u(r){const s=r.structuredContent;if(s?.content){try{return JSON.parse(s.content)}catch{return s}}return s??r}
 const p=load("stack154_preflight"),repo="taco-jpg/p196-algorithm";
 if(p.status!=="PASS_ADDITIVE_STACK_SOURCE_PREFLIGHT")throw new Error("Preflight did not pass");
 let base=p.BT;const stages=[];
 for(const s of p.stages){
  const r=u(await tools.mcp__codex_apps__github_create_tree({repository_full_name:repo,base_tree_sha:base,tree_elements:s.entries.map(({path,mode,type,sha})=>({path,mode,type,sha}))}));
  if(!r.sha)throw new Error("Missing tree receipt");
  stages.push({pr:s.pr,H:s.H,HT:s.HT,input_tree:base,output_tree:r.sha,additions:s.count,construction:"UNATTACHED_GIT_TREE_ONLY"});
  base=r.sha;
 }
 const result={B:p.B,BT:p.BT,stages,T:base,files:p.total_new_paths,status:"CONSTRUCTED_PENDING_INDEPENDENT_TREE_READBACK",fresh_lean:"NOT_RUN",branch_mutations:0,commit_objects_created:0};
 store("stack154_constructed",result);return result;
}

async function validateStack154(){
 function u(r){const s=r.structuredContent;if(s?.content){try{return JSON.parse(s.content)}catch{return s}}return s??r}
 const repo="taco-jpg/p196-algorithm",api="https://api.github.com/repos/"+repo,used=new Set(),pending=new Map();
 async function tree(sha){used.add(sha);const c=load("gt_"+sha);if(c)return c;if(!pending.has(sha))pending.set(sha,(async()=>{const r=u(await tools.mcp__codex_apps__github_fetch({url:api+"/git/trees/"+sha}));if(r.truncated||!r.tree||r.sha!==sha)throw new Error("Invalid tree "+sha);store("gt_"+sha,r);return r;})());return pending.get(sha);}
 async function lookup(root,path){const ps=path.split("/");let t=root;for(let i=0;i<ps.length;i++){const e=(await tree(t)).tree.find(x=>x.path===ps[i]);if(!e)return null;if(i===ps.length-1)return e;if(e.type!=="tree")throw new Error("Non-tree ancestor "+path);t=e.sha;}}
 async function leaves(sha,prefix,out){for(const e of(await tree(sha)).tree){const path=prefix+e.path;if(e.type==="tree")await leaves(e.sha,path+"/",out);else out.push({...e,path});}}
 async function diff(a,b,prefix,preserved,added){
  const [aa,bb]=await Promise.all([tree(a),tree(b)]),bm=new Map(bb.tree.map(x=>[x.path,x])),am=new Map(aa.tree.map(x=>[x.path,x]));
  for(const e of aa.tree){const f=bm.get(e.path),path=prefix+e.path;if(!f)throw new Error("Deleted "+path);if(e.mode!==f.mode||e.type!==f.type)throw new Error("Mode/type changed "+path);if(e.sha===f.sha){preserved.push({path,mode:e.mode,type:e.type,sha:e.sha});}else if(e.type==="tree"){await diff(e.sha,f.sha,path+"/",preserved,added);}else throw new Error("Overwritten "+path);}
  for(const f of bb.tree)if(!am.has(f.path)){const path=prefix+f.path;if(f.type==="tree")await leaves(f.sha,path+"/",added);else added.push({...f,path});}
 }
 const c=load("stack154_constructed"),p=load("stack154_preflight"),result=[];
 for(const s of c.stages){
  const expected=p.stages.find(x=>x.pr===s.pr).entries,em=new Map(expected.map(x=>[x.path,x])),preserved=[],added=[];
  await diff(s.input_tree,s.output_tree,"",preserved,added);
  if(added.length!==expected.length)throw new Error("Unexpected addition count "+s.pr);
  for(const e of added){const x=em.get(e.path);if(!x||e.sha!==x.sha||e.mode!==x.mode||e.type!==x.type)throw new Error("Unexpected addition "+e.path);}
  const reg=load("stack154_registry_"+s.pr),modules=[];
  for(const [project,pj]of Object.entries(reg.projects))for(const [name,m]of Object.entries(pj.modules)){
   const e=await lookup(s.output_tree,m.path);if(!e||e.sha!==m.git_blob||e.type!=="blob"||e.mode!=="100644")throw new Error("Module binding mismatch "+name);
   modules.push({project,name,path:m.path,git_blob:e.sha,registry_sha256:m.sha256,mode:e.mode,status:"EXACT_GIT_BLOB_MATCH"});
  }
  store("stack154_preserved_"+s.pr,preserved);
  result.push({...s,status:"PASS_EXACT_ADDITIVE_TREE_AND_REGISTRY_BINDING",preserved_entries_or_subtrees:preserved.length,additions:added.map(({path,mode,type,sha,size})=>({path,mode,type,sha,size})),modules});
 }
 const allPreserved=[],allAdded=[];
 await diff(c.BT,c.T,"",allPreserved,allAdded);
 const allExpected=new Map(p.stages.flatMap(x=>x.entries).map(x=>[x.path,x]));
 if(allAdded.length!==p.total_new_paths)throw new Error("Final addition count mismatch");
 for(const e of allAdded){const x=allExpected.get(e.path);if(!x||x.sha!==e.sha||x.mode!==e.mode||x.type!==e.type)throw new Error("Final set mismatch "+e.path);}
 store("stack154_final_preserved",allPreserved);
 const out={...c,status:"PASS_COMBINED_TREE_AND_SOURCE_BINDING",stages:result,all_original_base_preserved:true,preserved_entries_or_subtrees:allPreserved.length,total_new_paths:allAdded.length,used_tree_hashes:[...used],new_lean:"NOT_RUN",ownership:"Read-only integration support for existing prerequisite owners; no source branch, target, PR state or main role mutated.",limitations:"Conditional future stack tree. Actual prerequisite merges and then-current base/head must be refreshed before retargeting or merging. Retained mathematical execution must be separately qualified; no independent review of prerequisites is claimed here."};
 store("stack154_validated",out);
 return{B:out.B,BT:out.BT,T:out.T,status:out.status,preserved_entries_or_subtrees:allPreserved.length,additions:allAdded.length,stages:result.map(x=>({pr:x.pr,input_tree:x.input_tree,output_tree:x.output_tree,additions:x.additions.length,preserved_entries_or_subtrees:x.preserved_entries_or_subtrees,modules:x.modules.length})),tree_reads_or_cache_reuse:used.size};
}

// Executed in this order, with output inspected after each invocation:
// await preflightStack154();
// await constructStack154();
// await validateStack154();
