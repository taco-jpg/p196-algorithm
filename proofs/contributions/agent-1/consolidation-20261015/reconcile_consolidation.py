#!/usr/bin/env python3
"""Agent #1: deterministic contribution mapping and complete byte-index repair.

Adapts the existing Agent110/Agent116 incremental publication reconciliation.
No research source edits, network access, proof acceptance inference or Git writes.
Run from an exact clean candidate with all archived source objects available.
The caller stages reviewed outputs before --verify; no main mutation occurs here.
"""
from __future__ import annotations
import argparse, collections, copy, hashlib, json, re, subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
ROOT = REPO / 'proofs'
OWN = 'contributions/agent-1/consolidation-20261015'
OUT = ROOT / OWN / 'index'
ARCHIVE = 'eef3ecc100ae1038f6556c1600b85bf0200914f6'
INITIAL = 'b6f827418576027b1cff89746ee8077217963fce'
MAP = '59f7f540d107a7d35b27c4a00cc0e5075ec6fc8a5bf6a8114eeb34855e75e931'
SHARED = {'README.md','FINDINGS.md','REPRODUCE.md','REPORTS.md','PUBLICATION_SCOPE.md',
          'INVENTORY.json','INVENTORY.tsv','FILES.md','MANIFEST.sha256','release_stats.json','VALIDATION.json'}
MARK = '<!-- AGENT1 CONSOLIDATION 20261015 -->'

def git(*args):
    return subprocess.check_output(['git',*args],cwd=REPO)

def text(*args): return git(*args).decode()
def sha(data): return hashlib.sha256(data).hexdigest()
def load(path): return json.loads(path.read_text())
def put(path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def source(ref,path): return git('show',ref+':'+path)
def tree(ref):
    return {path:meta.split()[2] for line in text('ls-tree','-r',ref).splitlines()
            for meta,path in [line.split('\t',1)] if meta.split()[1]=='blob'}
def ancestor(a,b):
    return subprocess.run(['git','merge-base','--is-ancestor',a,b],cwd=REPO).returncode==0

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--initial-metadata',type=Path,required=True)
    p.add_argument('--resumption-metadata',type=Path,required=True)
    p.add_argument('--integrated-main',required=True)
    p.add_argument('--verify',action='store_true')
    a=p.parse_args()
    for ref in [INITIAL,ARCHIVE,a.integrated_main]:
        if not re.fullmatch('[0-9a-f]{40}',ref): raise ValueError('Full source commit required')
        git('cat-file','-e',ref+'^{commit}')
    target=a.integrated_main; tgt=tree(target)
    generator_path = ROOT / OWN / 'make_accepted_registry.py'
    original_generator = source(target, str(generator_path.relative_to(REPO))).decode()
    old_blocker = "       {'id':'BASELINE_BYTE_COVERAGE','status':'OPEN','description':'Initial main b6f8274 has 478 tracked proof files absent from its legacy manifest, including132 Lean files. Regeneration and complete tracked-file coverage verification remain required.'}"
    if old_blocker not in original_generator:
        raise ValueError('Publication-blocker reconciliation anchor changed')
    repaired_generator = original_generator.replace(old_blocker, '')
    # A trailing comma inside the blocker list is legal Python. Keep the legacy
    # accepted-scope blocker, and require byte verification as a separate check.
    repaired_generator = repaired_generator.replace("      'projects':", "      'publication_integrity':{'baseline':'b6f827418576027b1cff89746ee8077217963fce','historical_omissions':'contributions/agent-1/consolidation-20261015/index/baseline-coverage.json','verification_command':'python3 -B proofs/verify_release.py','scope':'Complete byte coverage is checked separately on each current snapshot; not mathematical acceptance.'},\n      'projects':")
    generator_path.write_text(repaired_generator)
    subprocess.run(['python3','-B',str(generator_path)],cwd=REPO,check=True)
    core=load(ROOT/'ACCEPTED_BUILD.json')
    if core['reviewed_source_map_sha256']!=MAP or core['catalogue_complete']:
        raise ValueError('Unreviewed accepted registry or complete-catalogue assertion')
    accepted={r['path']:r for pr in core['projects'].values() for r in pr['modules'].values()}
    for path,rec in accepted.items():
        if sha(source(target,path))!=rec['sha256'] or sha((REPO/path).read_bytes())!=rec['sha256']:
            raise ValueError('Accepted source changed: '+path)
    original=load(a.initial_metadata/'capture.json'); current=load(a.resumption_metadata/'capture.json')
    branches=load(a.initial_metadata/'branches.json'); now=load(a.resumption_metadata/'branches.json')
    prs=load(a.initial_metadata/'pull_requests.json'); latest_pr={x['number']:x for x in load(a.resumption_metadata/'pull_requests.json')}
    if original['starting_main']!=INITIAL: raise ValueError('Wrong bounded snapshot')
    snapshot=json.loads(source(ARCHIVE,'SNAPSHOT.json'))
    if snapshot['branches']!={x['name']:x['commit']['sha'] for x in branches}: raise ValueError('Snapshot pin mismatch')
    byblob=collections.defaultdict(list)
    for path,blob in tgt.items(): byblob[blob].append(path)
    def best(paths): return min(paths,key=lambda x:('/verification/' in x or '/historical-' in x,len(x),x)) if paths else None
    ledger=[]
    for b in branches:
        head=b['commit']['sha']; name=b['name']; src=tree(head)
        if not ancestor(head,ARCHIVE): raise ValueError('Unpreserved original branch: '+name)
        common=text('merge-base',INITIAL,head).strip(); present=ancestor(head,target); changes=[]
        for line in text('diff','--name-status','--no-renames',common,head).splitlines():
            change,path=line.split('\t',1); blob=src.get(path); canonical=None
            if change=='D':
                status='ALREADY_PRESENT' if present or path not in tgt else 'BLOCKED'
                reason='Historical deletion; complete original history retained. No new deletion is performed.'
            elif tgt.get(path)==blob:
                canonical=path; status='INTEGRATED_ACCEPTED' if path in accepted else 'ALREADY_PRESENT'
                reason='Exact accepted source identity.' if path in accepted else 'Same source bytes present; no new mathematical acceptance.'
            elif blob in byblob:
                canonical=best(byblob[blob]);status='DUPLICATE_WITH_MAPPING'
                reason='Exact bytes at mapped destination; original independent provenance remains archived.'
            elif present:
                status='SUPERSEDED_BUT_PRESERVED';reason='Source commit is in integrated ancestry; later tree differs. Original bytes remain reachable.'
            else:
                status='BLOCKED';reason='Not incorporated at an exact mapped path; semantic/review/build disposition remains open. History is durably retained.'
            changes.append({'source_path':path,'source_blob':blob,'change':change,'disposition':status,
                            'canonical_destination':canonical,'preservation_location':f'{head}:{path}','retained_reference':'archive/agent-1/20261015T1904Z',
                            'verification_level':'SOURCE_BYTES_AND_ANCESTRY_ONLY' if status!='INTEGRATED_ACCEPTED' else 'REVIEWED_CORE_SOURCE_PIN',
                            'remaining_blocker':reason})
        blocked=[x['source_path'] for x in changes if x['disposition']=='BLOCKED']
        claimids=[c['id'] for c in core['claims'] if accepted[next(r['path'] for r in core['projects'][c['project']]['modules'].values() if r['path'].endswith('/'+c['module']+'.lean'))]['historical_source_commit']==head]
        disposition='ALREADY_PRESENT' if present else ('BLOCKED' if blocked else 'DUPLICATE_WITH_MAPPING')
        ledger.append({'source_branch':name,'source_commit':head,'source_pull_request':[x['number'] for x in prs if x['head']['ref']==name],
            'source_paths':changes,'claim_identifiers':claimids,'dependencies':'Exact import graph in ACCEPTED_BUILD.json for accepted claims; other source-specific dependencies remain under their retained source commits.',
            'unique_contribution':'Original branch delta and complete historical ancestry; not inferred from commit messages.',
            'verification_level':'GIT_OBJECTS_SOURCE_MAPPING_AND_PREEXISTING_REVIEW_REFERENCES_NOT_GLOBAL_REPROOF',
            'canonical_destination':'main' if present else None,'preservation_location':'archive/agent-1/20261015T1904Z',
            'archive_commit':ARCHIVE,'archive_ancestry_verified':True,'disposition':disposition,
            'integration_commit':target if present else None,'remaining_blocker':blocked,
            'retirement_authorized':False})
    pulls=[]
    for old in prs:
        head=old['head']['sha']; newer=latest_pr.get(old['number'],old); merged=newer.get('merged_at') is not None
        if not ancestor(head,ARCHIVE): raise ValueError('Unpreserved original PR head')
        onmain=ancestor(head,target)
        pulls.append({'source_pull_request':old['number'],'title':old['title'],'source_commit':head,
            'source_branch':old['head']['ref'],'original_base_branch':old['base']['ref'],
            'original_state':old['state'],'observed_platform_merged':merged,
            'observed_platform_merge_commit':newer.get('merge_commit_sha') if merged else None,
            'head_ancestry_on_integrated_main':onmain,'disposition':'ALREADY_PRESENT' if onmain else 'BLOCKED',
            'preservation_location':ARCHIVE,'integration_commit':target if onmain else None,
            'remaining_blocker':None if onmain else 'A platform merge into another branch is not main integration; inspect source mapping.'})
    coreclaims=[]
    for c in core['claims']:
        d=copy.deepcopy(c);d['disposition']='INTEGRATED_ACCEPTED';d['integration_commit']=target
        d['canonical_destination']=core['projects'][c['project']]['modules'][c['module']]['path']
        d['source_commit']=accepted[d['canonical_destination']]['historical_source_commit'];coreclaims.append(d)
    issues=[{'number':i['number'],'title':i['title'],'state':i['state'],'source_url':i['html_url'],
             'disposition':'BLOCKED' if i['state']=='open' else 'ALREADY_PRESENT',
             'remaining_blocker':'Underlying research obligation is not closed by this consolidation.' if i['state']=='open' else None}
            for i in load(a.initial_metadata/'issues_and_prs.json') if 'pull_request' not in i]
    coord=next(x['commit']['sha'] for x in now if x['name']=='p196/coordination');coordrows=[]
    for path,blob in tree(coord).items():
        if not path.startswith('proofs/coordination/'):continue
        r={'source_path':path,'source_commit':coord,'source_blob':blob,'disposition':'SUPERSEDED_BUT_PRESERVED',
           'canonical_destination':'p196/coordination:'+path,'acceptance_inferred':False}
        if path.endswith('.json'):
            try:
                data=json.loads(source(coord,path))
                if isinstance(data,dict):r['reported_fields']={k:data[k] for k in ['task_id','owner','status','branch','source_commit','last_activity'] if k in data}
            except (ValueError,UnicodeDecodeError):r['reported_fields_unavailable']=True
        coordrows.append(r)
    initial_heads={x['name']:x['commit']['sha'] for x in branches}
    delta=[{'source_branch':x['name'],'initial_commit':initial_heads.get(x['name']),
            'source_commit':x['commit']['sha'],'disposition':'READY_FOR_REVIEW',
            'remaining_blocker':'Post-snapshot change; not implicitly accepted by the initial pass.'}
           for x in now if initial_heads.get(x['name'])!=x['commit']['sha']]
    OUT.mkdir(parents=True,exist_ok=True)
    for label,folder in [('initial',a.initial_metadata),('resumption',a.resumption_metadata)]:
        for name in ['capture.json','branches.json','pull_requests.json','issues_and_prs.json','unavailable-pins.json','main-rules.json']:
            dest=OUT/'snapshots'/label/name;dest.parent.mkdir(parents=True,exist_ok=True)
            data=(folder/name).read_bytes()
            if dest.exists() and dest.read_bytes()!=data:raise ValueError('Refusing historical snapshot overwrite')
            dest.write_bytes(data)
    put(OUT/'contribution-ledger.json',{'agent':'Agent #1','starting_main':INITIAL,'integrated_main_examined':target,
         'preservation_archive':ARCHIVE,'snapshot_interval':[original['started_at'],original['finished_at']],
         'completeness':'Every original branch and PR has a disposition; BLOCKED does not mean consolidated or accepted.',
         'core_accepted_claims':coreclaims,'branches':ledger,'pull_requests':pulls,'research_issues':issues,
         'scope_limitations':['No unavailable local-only deliverable was reconstructed.','Source-byte coverage is not mathematical verification.','No branch or issue retirement is authorized.','Legacy accepted-scope census and non-core branch semantic reviews remain open.']})
    put(OUT/'delta-queue.json',{'agent':'Agent #1','captured_interval':[current['started_at'],current['finished_at']],
         'entries':delta,'new_pull_requests':[{'number':x['number'],'source_commit':x['head']['sha'],'base':x['base']['ref'],'title':x['title'],'disposition':'READY_FOR_REVIEW'} for x in latest_pr.values() if x['number'] not in {p['number'] for p in prs}]})
    put(OUT/'coordination-inventory.json',{'agent':'Agent #1','source_commit':coord,'records':coordrows,
         'local_only_deliverables':'Not recovered; a referenced local path or session claim is not source availability. Resolve those through exact published checkpoints.'})
    initial_tree=tree(INITIAL);manifest={s.split('  ',1)[1] for s in source(INITIAL,'proofs/MANIFEST.sha256').decode().splitlines()}
    omissions=[{'path':p,'blob':h} for p,h in initial_tree.items() if p.startswith('proofs/') and p!='proofs/MANIFEST.sha256' and p[7:] not in manifest]
    put(OUT/'baseline-coverage.json',{'source_commit':INITIAL,'unlisted_tracked_files':omissions,
         'unlisted_count':len(omissions),'unlisted_lean_count':sum(x['path'].endswith('.lean') for x in omissions),'mathematical_proof_check':False})
    counts=collections.Counter(x['disposition'] for x in ledger)
    rows='\n'.join(f"| `{x['source_branch']}` | `{x['source_commit'][:12]}` | {x['disposition']} | {len(x['remaining_blocker'])} |" for x in ledger)
    (ROOT/'CONSOLIDATION.md').write_text(f'''# P196 consolidated research entry point\n\nAgent #1. Original main: `{INITIAL}`. Integrated source snapshot examined: `{target}`.\n\n## Accepted build\n\nThe source-pinned `consolidation-core` contains {len(accepted)} modules and five precisely scoped claim families. It combines the thirteen two-digit-prefix results, five-step outer-map charge extinction, alternating spatial-cut obstruction, high-base arithmetic first-hit classification, and nine-carry reconstruction. It does not prove decimal Lychrel existence or the specific 196 claim.\n\n```sh\npython3 proofs/verify_project.py --lean /absolute/path/to/lean --project consolidation-core --output /tmp/p196-core-fresh\npython3 -B proofs/verify_release.py\n```\n\nUse official Lean 4.19.0, commit `6caaee842e94`, and a new output directory. The first command checks original source identities, import closure, a byte-proved foundation adapter, fresh compilation, named theorem endpoints and every project theorem's transitive axiom dependencies. The second checks publication bytes and complete tracked-file coverage, not mathematics. `--check-only` is not proof verification.\n\n[Exact accepted registry](ACCEPTED_BUILD.json), [semantic review]({OWN}/reviews/batch2.md), and [published clean replay]({OWN}/verification/core-entrypoint/build/verification.json) define the accepted scope. An axiom-audit declaration count includes generated auxiliaries and is not a count of independent research breakthroughs.\n\nThe default proof command without `--project` deliberately returns a non-success result while the global accepted catalogue is incomplete. Previously accepted results outside this first registry keep their original evidence labels and source-specific reproduction instructions in [REPRODUCE.md](REPRODUCE.md); they are not silently withdrawn, re-reviewed, or covered by the core's PASS. Completing their exact scope census and orchestrated verification remains OPEN.\n\n## Mathematical boundaries and open obligations\n\nThe outer-map and spatial-cut theorems concern their stated models; ordinary-arithmetic exterior bridges remain open. Nine complete carry words determine pair sums and the next integer, not the initial integer. The high-base classification requires canonical inputs, the documented pair-sum interval and base at least three, and concerns the first positive palindrome time. Finite controls do not replace these hypotheses or prove all-time palindrome avoidance.\n\nThe previously retained Agent113 review imported two missing Agent115 modules. The exact reviewed exterior-factorization package is restored with its [source identity and scope notice](contributions/agent-115/exterior-factorization/CONSOLIDATION_STATUS.md). This restores review reproducibility; it does not add that package to the 38-module core or formalize the written coordinate-update formula.\n\nNo uninstantiated conditional witness, omitted certificate, unfinished theorem, false historical claim, or compiler-trusted shortcut is promoted by file preservation. The registry lists only the inspected core. Other source-specific formal, finite, written, conditional and incomplete evidence retains its prior label.\n\n## Contribution provenance and retained research\n\nThe [contribution ledger]({OWN}/index/contribution-ledger.json) maps all {len(branches)} original branches and {len(prs)} original PR heads. Source histories are durably reachable from `archive/agent-1/20261015T1904Z` at `{ARCHIVE}`; every original head's ancestry was checked. This synthetic archive is not the accepted project and must not be merged into main or deleted as clutter.\n\nRetrieve an original file with `git show SOURCE_COMMIT:path`. The ledger records exact blobs and canonical destinations where available. A final empty diff or an ancestry match does not discard intermediate research: its full history remains reachable. `ALREADY_PRESENT` is a content/history disposition, not a fresh proof verdict. `BLOCKED` preserves a precise unresolved path, not an assertion of acceptance.\n\n| Original branch | Pinned head | Disposition | Unmapped paths |\n|---|---|---|---:|\n{rows}\n\nThe [delta queue]({OWN}/index/delta-queue.json) separately retains later observed heads and new requests. The [coordination inventory]({OWN}/index/coordination-inventory.json) records reported task fields without claiming control over independent sessions. Referenced local-only artifacts were not recovered. The separate paginated [discussion snapshot]({OWN}/verification/core-entrypoint/discussions.json) states its capture time and coverage.\n\n## Publication integrity\n\nThe original manifest omitted {len(omissions)} tracked proof files, including {sum(x['path'].endswith('.lean') for x in omissions)} Lean files. [Exact baseline omissions]({OWN}/index/baseline-coverage.json) preserve that failure separately from integration regressions. Current metadata is regenerated from the complete tracked/publication selection, keeping historical inventory rows, archived original bytes and earlier aggregate statistics. This repairs byte coverage only, not the incomplete accepted-scope census.\n\nNo branch, PR or research issue is retired by this checkpoint. Branch deletion still requires current ownership/dependency checks, an exact-head guard and a verified preservation mapping. Full consolidation remains incomplete while ledger blockers, legacy accepted-build coverage, or unresolved central mathematical obligations remain.\n''')
    links={'README.md':'Current research navigation and exact accepted scope', 'FINDINGS.md':'Current accepted scopes, exclusions and remaining mathematical obligations',
           'REPRODUCE.md':'Source-pinned combined verification entry point', 'REPORTS.md':'Contribution dispositions, retained history and delta queue'}
    for name,title in links.items():
        path=ROOT/name;old=path.read_text()
        if MARK not in old:path.write_text(f'{MARK}\n\n## Agent #1: {title}\n\nStart with [CONSOLIDATION.md](CONSOLIDATION.md). The core build is scoped; the global accepted catalogue remains incomplete. Historical sections below retain their original evidence scope and date.\n\n'+old)
    path=REPO/'README.md';old=path.read_text()
    if MARK not in old:path.write_text(f'{MARK}\n\n## Research entry point\n\nThe consolidated mathematical project starts at [proofs/CONSOLIDATION.md](proofs/CONSOLIDATION.md), with exact accepted scopes, verification commands, preserved research and open obligations. A successful scoped build is not a proof of decimal Lychrel existence or the 196 claim.\n\n'+old)
    # Preserve the old verifier as an indexed historical source before strengthening it.
    oldver=source(target,'proofs/verify_release.py').decode()
    guard='''    # A passing subset manifest is not complete publication verification.\n    listed = [line.split('  ', 1)[1] for line in (ROOT/'MANIFEST.sha256').read_text().splitlines()]\n    assert len(listed) == len(set(listed)), 'Duplicate manifest path'\n    for name in listed:\n        path = ROOT/name\n        assert not Path(name).is_absolute() and path.resolve().is_relative_to(ROOT.resolve()), 'Unsafe manifest path'\n        assert not path.is_symlink(), 'Manifest symlink: '+name\n    import subprocess\n    probe = subprocess.run(['git','rev-parse','--show-toplevel'],cwd=ROOT,capture_output=True,text=True)\n    if probe.returncode == 0 and Path(probe.stdout.strip()).resolve() == ROOT.parent.resolve():\n        tracked = subprocess.check_output(['git','ls-files','-z','--','proofs/'],cwd=ROOT.parent).decode().split('\\0')\n        expected = {name[len('proofs/'):] for name in tracked if name and name != 'proofs/MANIFEST.sha256'}\n        coverage_source = 'git-index'\n    else:\n        expected = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and p != ROOT/'MANIFEST.sha256' and '__pycache__' not in p.parts and p.suffix not in {'.olean','.ilean','.pyc','.o','.so'}}\n        coverage_source = 'export-tree-excluding-reproducible-compiled-products'\n    assert set(listed) == expected, {'unlisted': sorted(expected-set(listed)), 'unavailable': sorted(set(listed)-expected)}\n'''
    if 'A passing subset manifest' not in oldver:
        newver=oldver.replace('def main():\n','def main():\n'+guard,1).replace("'mathematical_proof_check':False", "'mathematical_proof_check':False,'complete_publication_coverage':True,'coverage_source':coverage_source")
        if newver==oldver:raise ValueError('Verifier edit anchor missing')
        (ROOT/'verify_release.py').write_text(newver)
    base_records=json.loads(source(target,'proofs/INVENTORY.json'));tsv=source(target,'proofs/INVENTORY.tsv').decode();relocated=[]
    for r in base_records:
        if r['publication']!='retained':continue
        current_path=ROOT/r['published_path']
        if current_path.is_file() and sha(current_path.read_bytes())==r['sha256'] and current_path.stat().st_size==r['bytes']:continue
        data=source(target,'proofs/'+r['published_path'])
        if sha(data)!=r['sha256'] or len(data)!=r['bytes']:raise ValueError('Historical exact bytes unavailable: '+r['published_path'])
        prior=r['published_path'];dest=f"{OWN}/index/historical-index/{r['sha256']}/{Path(prior).name}"
        (ROOT/dest).parent.mkdir(parents=True,exist_ok=True);(ROOT/dest).write_bytes(data)
        r.update(published_path=dest,superseded_published_path=prior,original_git_commit=target,reconciliation_note='Exact previously indexed bytes retained; current file has a new row.')
        lines=tsv.splitlines(keepends=True);changed=0
        for i,line in enumerate(lines):
            fields=line.rstrip('\n').split('\t')
            if len(fields)==7 and fields[2]==r['sha256'] and fields[6]==prior:
                fields[6]=dest;lines[i]='\t'.join(fields)+'\n';changed+=1
        if not changed:raise ValueError('Unmapped historical TSV row: '+prior)
        tsv=''.join(lines);relocated.append({'original_path':prior,'preserved_path':dest,'sha256':r['sha256']})
    put(OUT/'index-reconciliation.json',{'agent':'Agent #1','baseline_commit':target,'historical_records_preserved':len(base_records),
        'relocated_historical_records':relocated,'byte_coverage_only':True,'initial_branch_dispositions':dict(counts),
        'accepted_registry_mathematics_unchanged':True,'publication_blocker_separated_from_mathematical_census':True,'repository_wide_mathematical_pass':False})
    stats=json.loads(source(target,'proofs/release_stats.json'));validation=json.loads(source(target,'proofs/VALIDATION.json'))
    def paths():
        tracked={s[7:] for s in text('ls-files','proofs/').splitlines()}
        tracked.update(str(x.relative_to(ROOT)) for x in OUT.rglob('*') if x.is_file())
        tracked.add('CONSOLIDATION.md')
        if any(not (ROOT/s).is_file() for s in tracked):raise ValueError('Missing selected source')
        if any(s.endswith(('.olean','.ilean','.pyc','.o','.so')) or '__pycache__' in Path(s).parts for s in tracked):raise ValueError('Compiled/cache products in publication selection')
        return sorted(tracked)
    files=paths();records=copy.deepcopy(base_records);known={x['published_path'] for x in records if x['publication']=='retained'};added=[]
    for name in files:
        if name in known or name in SHARED:continue
        data=(ROOT/name).read_bytes();r={'source_path':name,'bytes':len(data),'sha256':sha(data),'publication':'retained',
            'published_path':name,'reason':'Complete tracked proof byte coverage; acceptance only through exact source-specific evidence.',
            'family_report':'CONSOLIDATION.md','source_snapshot':'agent1-consolidation-index-20261015',
            'semantic_status':'BYTE_INDEX_ONLY_NO_NEW_MATHEMATICAL_REVIEW'};records.append(r);added.append(r)
    put(ROOT/'INVENTORY.json',records);columns=('source_path','bytes','sha256','publication','reason','family_report','published_path')
    (ROOT/'INVENTORY.tsv').write_text(tsv.rstrip('\n')+'\n'+''.join('\t'.join(str(r.get(k,'')) for k in columns)+'\n' for r in added))
    (ROOT/'FILES.md').write_text('# Complete published proof file list\n\nPublication selection, not mathematical acceptance. Historical records remain in INVENTORY.json.\n\n'+''.join(f'- [{s}]({s})\n' for s in files))
    update={'integrated_source_snapshot':target,'tracked_publication_files':len(files),'historical_records_preserved':len(base_records),
            'new_byte_records':len(added),'historical_relocations':len(relocated),'complete_selection_manifest_generated':True,
            'mathematical_proof_check':False,'full_accepted_catalogue_complete':False}
    put(ROOT/'release_stats.json',dict(stats,agent1_consolidation_index=update));put(ROOT/'VALIDATION.json',dict(validation,agent1_consolidation_index=update))
    (ROOT/'MANIFEST.sha256').write_text(''.join(f'{sha((ROOT/s).read_bytes())}  {s}\n' for s in files if s!='MANIFEST.sha256'))
    if a.verify:subprocess.run(['python3','-B',str(ROOT/'verify_release.py')],cwd=REPO,check=True)
    print(json.dumps({'agent':'Agent #1','status':'INDEX_GENERATED_NO_MATHEMATICAL_ACCEPTANCE_CHANGE',**update},indent=2))

if __name__=='__main__':main()
