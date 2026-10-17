async function validateSupport104(){
 function u(r){const s=r.structuredContent;if(s?.content){try{return JSON.parse(s.content)}catch{return s}}return s??r}
 const api="https://api.github.com/repos/taco-jpg/p196-algorithm",T="2765245df1124e30f3148c4a96dce3228e8605dc",BT="ba552a911841c2f2654cb4481c92e559e42d2a9b",H="c9a86a40ffd478f7c01ac68688896cba91f94dd1",HT=load("s104_source_commit").tree.sha,used=new Set();
 async function tree(s){used.add(s);const c=load("gt_"+s);if(c?.tree)return c;const r=u(await tools.mcp__codex_apps__github_fetch({url:api+"/git/trees/"+s}));if(r.sha!==s||!r.tree||r.truncated)throw new Error("Invalid tree "+s);store("gt_"+s,r);return r;}
 async function lookup(root,path){let s=root;const ps=path.split("/");for(let i=0;i<ps.length;i++){const e=(await tree(s)).tree.find(x=>x.path===ps[i]);if(!e)return null;if(i===ps.length-1)return e;if(e.type!=="tree")throw new Error("Non-directory ancestor");s=e.sha;}}
 const preserved=[],added=[];
 async function leaves(s,prefix){for(const e of(await tree(s)).tree){const path=prefix+e.path;if(e.type==="tree")await leaves(e.sha,path+"/");else added.push({path,sha:e.sha,type:e.type,mode:e.mode,size:e.size});}}
 async function diff(a,b,prefix){const aa=(await tree(a)).tree,bb=(await tree(b)).tree,bm=new Map(bb.map(x=>[x.path,x])),am=new Map(aa.map(x=>[x.path,x]));
 for(const e of aa){const f=bm.get(e.path),path=prefix+e.path;if(!f||e.type!==f.type||e.mode!==f.mode)throw new Error("Removed/mode changed "+path);if(e.sha===f.sha)preserved.push({path,mode:e.mode,type:e.type,sha:e.sha});else if(e.type==="tree")await diff(e.sha,f.sha,path+"/");else throw new Error("Overwritten "+path);}
 for(const e of bb)if(!am.has(e.path)){const path=prefix+e.path;if(e.type==="tree")await leaves(e.sha,path+"/");else added.push({path,sha:e.sha,type:e.type,mode:e.mode,size:e.size});}}
 await diff(BT,T,"");
 const em=new Map(load("s104_files").map(x=>[x.filename,x]));
 if(added.length!==21||em.size!==21)throw new Error("Wrong addition count");
 const sources=[];
 for(const e of added){const ex=em.get(e.path),h=await lookup(HT,e.path),b=await lookup(BT,e.path);if(!ex||e.sha!==ex.sha||e.mode!=="100644"||e.type!=="blob"||!h||h.sha!==e.sha||h.mode!==e.mode||h.type!==e.type||b)throw new Error("Addition/source/base mismatch "+e.path);sources.push({...e,status:"EXACT_H_AND_ABSENT_FROM_B"});}
 const reg=load("s104_registry"),modules=[];
 for(const pj of Object.values(reg.projects))for(const [name,m]of Object.entries(pj.modules)){const e=await lookup(T,m.path);if(!e||e.sha!==m.git_blob||e.mode!=="100644"||e.type!=="blob")throw new Error("Module mismatch "+name);modules.push({name,path:m.path,git_blob:e.sha,registry_sha256:m.sha256,status:"EXACT_BLOB_MATCH"});}
 const p=reg.provenance,verifier=await lookup(T,p.verifier_path);if(!verifier||verifier.sha!==p.verifier_git_blob)throw new Error("Verifier mismatch");
 store("s104_preserved",preserved);
 const out={status:"PASS_EXACT_CURRENT_BASE_COMBINATION",B:"74a1c3922eb7af438fe40b23d2105ad07556e3f5",BT,H,HT,T,source_additions:sources,preserved_entries_or_subtrees:preserved.length,full_base_preserved:true,modules,verifier:{path:p.verifier_path,git_blob:verifier.sha},tree_hashes_read_or_reused:[...used],root_tree_readback:"HTTP200 public credential-free GET via authorized exec_command after connector404/transport failures",root_tree_expected_matches_create_receipt:true,fresh_lean:"NOT_RUN",scope:"Current-tree/source-identity support only; Agent31 keeps PR104 delivery and main ownership. No replacement independent mathematical review or actual merge."};
 store("s104_validated",out);return{status:out.status,B:out.B,H,T,additions:sources.length,preserved_entries_or_subtrees:preserved.length,modules:modules.length,verifier:verifier.sha,tree_reads:used.size};
}
