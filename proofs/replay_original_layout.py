#!/usr/bin/env python3
"""从已保存映射重建旧路径，同时核验并使用对应的平铺当前源码。

只创建仓库外临时目录，不覆盖用户工作树。检查输出目录保留用于调查失败。
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
    if not argv:raise RuntimeError('必须在 -- 后提供明确的检查命令。')
    here=Path(__file__).resolve().parent
    mapping=json.loads((here/'SOURCE_MAP.json').read_text(encoding='utf-8'))
    root=Path(git(here,'rev-parse','--show-toplevel').decode().strip())
    work=Path(tempfile.mkdtemp(prefix='p196-original-layout-'))/'repo'
    p=subprocess.run(['git','clone','--no-checkout','--shared',str(root),str(work)])
    if p.returncode:raise RuntimeError('不能创建隔离检查仓库。')
    git(work,'symbolic-ref','HEAD','refs/heads/p196-replay')
    git(work,'update-ref','refs/heads/p196-replay',mapping['base'])
    git(work,'read-tree',mapping['base'])
    for old,info in mapping['paths'].items():
        parts=PurePosixPath(old).parts
        if not parts or PurePosixPath(old).is_absolute() or '..' in parts or '.git' in parts:
            raise RuntimeError('映射路径不安全：'+old)
        selected=info.get('current') or info['preserved']
        source=root/selected
        if info['mode']=='120000':
            data=os.fsencode(os.readlink(source))
        else:
            if source.is_symlink():raise RuntimeError('普通文件被替换为符号链接：'+selected)
            data=source.read_bytes()
        if hashlib.sha256(data).hexdigest()!=info['sha256']:
            raise RuntimeError('源文件改变，不能把旧哈希的结果套用到新内容：'+selected)
        target=work/old
        target.parent.mkdir(parents=True,exist_ok=True)
        if any(p.is_symlink() for p in target.parents if p!=work.parent):raise RuntimeError('目标祖先含 symlink。')
        if info['mode']=='120000':os.symlink(os.fsdecode(data),target)
        else:
            target.write_bytes(data);target.chmod(0o755 if info['mode']=='100755' else 0o644)
    print('原布局检查工作区（保留）：'+str(work),flush=True)
    result=subprocess.run(argv,cwd=work)
    raise SystemExit(result.returncode)
if __name__=='__main__':
    try:main()
    except (RuntimeError,OSError,ValueError,KeyError) as e:print('旧路径重放失败：'+str(e),file=sys.stderr);sys.exit(2)
