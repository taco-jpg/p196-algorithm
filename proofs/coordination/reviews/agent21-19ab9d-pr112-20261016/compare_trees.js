const repo="taco-jpg/p196-algorithm";
const seen=[];
async function getTree(sha){
 let p=load("tree_"+sha);
 if(!p){const v=await tools.mcp__codex_apps__github_fetch({url:"https://api.github.com/repos/"+repo+"/git/trees/"+sha});if(v.isError)throw new Error("Tree read failed "+sha);p=JSON.parse(v.structuredContent.content);if(p.truncated)throw new Error("Truncated tree "+sha);store("tree_"+sha,p);}
 seen.push({sha,count:p.tree.length,truncated:p.truncated});return p.tree;
}
const diffs=[],equal=[];
async function walk(oldSha,newSha,prefix){
 if(oldSha===newSha){equal.push({path:prefix,sha:oldSha});return;}
 const rs=await Promise.allSettled([oldSha?getTree(oldSha):Promise.resolve([]),newSha?getTree(newSha):Promise.resolve([])]);
 if(rs.some(r=>r.status!=="fulfilled"))throw new Error("Tree comparison read failed");
 const old=new Map(rs[0].value.map(e=>[e.path,e])),now=new Map(rs[1].value.map(e=>[e.path,e]));
 for(const name of new Set([...old.keys(),...now.keys()])){
  const a=old.get(name),b=now.get(name),path=prefix?prefix+"/"+name:name;
  if(a?.sha===b?.sha&&a?.mode===b?.mode&&a?.type===b?.type){equal.push({path,sha:a.sha,type:a.type,mode:a.mode});continue;}
  if((!a||a.type==="tree")&&(!b||b.type==="tree"))await walk(a?.sha,b?.sha,path);
  else diffs.push({path,before:a??null,after:b??null});
 }
}
const base=load("main112_commit_parsed"),expected=load("combined112_elements"),tree=load("combined112_tree_create").structuredContent.sha;
await walk(base.tree.sha,tree,"");
if(diffs.length!==expected.length||diffs.some(d=>d.before!==null||!expected.some(e=>e.path===d.path&&e.sha===d.after?.sha&&e.mode===d.after?.mode)))throw new Error("Unexpected combined-tree delta");
const record={status:"PASS_ADDITIVE_COMBINED_TREE_MERKLE_COMPARISON",method:"Read-only GitHub Git-tree comparison; descend only changed subtrees and require all other entries to preserve their mode/type/SHA.",source_head:"01ecb6aa6bc555335ff6cb628d08e84133888307",base:base.sha,base_tree:base.tree.sha,combined_tree:tree,added_files:diffs.map(d=>({path:d.path,sha:d.after.sha,mode:d.after.mode})),changed_existing_files:0,deleted_files:0,unchanged_entries:equal,trees_read:seen,source_bindings:load("source112_mapping"),archive_tree_identity:load("main112_proofs_parsed").tree.find(e=>e.path==="archive").sha,ci_checkout_commit:"4d10aa839c074cb2d04013ed8d3aee967677c09a",ci_archive_and_flat_dependency_blobs_identical:true,new_lean_execution:"NOT_RUN",source_branch_writes:"NONE",main_write_slot:"NOT_HELD"};
store("combined112_verification",record);text({status:record.status,base:record.base,combined_tree:record.combined_tree,added_files:record.added_files.length,unchanged_entries:equal.length,trees_read:seen.length});
