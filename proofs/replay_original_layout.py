#!/usr/bin/env python3
"""Reconstruct original paths from the preserved mapping, verifying and using matching flattened current source.

Create only an external temporary directory; never overwrite the working tree. Retain the check workspace for failure investigation.
"""
from __future__ import annotations
import hashlib,json,os,subprocess,sys,tempfile
from pathlib import Path,PurePosixPath

def git(repo,*args):
    p=subprocess.run(['git','-C',str(repo),*args],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if p.returncode:raise RuntimeError(p.stderr.decode('utf-8','replace'))
    return p.stdout

def main(argv=None):
    argv=list(sys.argv[1:] if argv is None else argv)
    if argv[:1]==['--']:argv=argv[1:]
    if not argv:raise RuntimeError('Provide an explicit check command after --.')
    here=Path(__file__).resolve().parent
    mapping=json.loads((here/'SOURCE_MAP.json').read_text(encoding='utf-8'))
    root=Path(git(here,'rev-parse','--show-toplevel').decode().strip())
    work=Path(tempfile.mkdtemp(prefix='p196-original-layout-'))/'repo'
    p=subprocess.run(['git','clone','--no-checkout','--shared',str(root),str(work)])
    if p.returncode:raise RuntimeError('Cannot create the isolated check repository.')
    git(work,'symbolic-ref','HEAD','refs/heads/p196-replay')
    git(work,'update-ref','refs/heads/p196-replay',mapping['base'])
    git(work,'read-tree',mapping['base'])
    for old,info in mapping['paths'].items():
        parts=PurePosixPath(old).parts
        if not parts or PurePosixPath(old).is_absolute() or '..' in parts or '.git' in parts:
            raise RuntimeError('Unsafe mapped path: '+old)
        selected=info.get('current') or info['preserved']
        source=root/selected
        if info['mode']=='120000':
            data=os.fsencode(os.readlink(source))
        else:
            if source.is_symlink():raise RuntimeError('A regular file was replaced by a symbolic link: '+selected)
            data=source.read_bytes()
        if hashlib.sha256(data).hexdigest()!=info['sha256']:
            raise RuntimeError('Source changed; results for an old hash cannot be applied to new content: '+selected)
        target=work/old
        target.parent.mkdir(parents=True,exist_ok=True)
        if any(p.is_symlink() for p in target.parents if p!=work.parent):raise RuntimeError('A target ancestor is a symlink.')
        if info['mode']=='120000':os.symlink(os.fsdecode(data),target)
        else:
            target.write_bytes(data);target.chmod(0o755 if info['mode']=='100755' else 0o644)
    print('Original-layout check workspace (retained): '+str(work),flush=True)
    result=subprocess.run(argv,cwd=work)
    raise SystemExit(result.returncode)
if __name__=='__main__':
    try:main()
    except (RuntimeError,OSError,ValueError,KeyError) as e:print('Original-layout replay failed: '+str(e),file=sys.stderr);sys.exit(2)
