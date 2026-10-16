#!/usr/bin/env python3
"""Build the deterministic PR119 support archive from preserved original bytes.
No network, Git mutation, Lean execution, or source modification is performed.
"""
import argparse
import hashlib
import json
import lzma
from pathlib import Path, PurePosixPath
import stat
import tarfile

SOURCE_ROOT = '/dev/shm/p196-agent16-session2b196284'
ARCHIVE_NAME = 'agent16-session2b196284-pr119-support-20261016.tar.xz'
SOURCE_DIRS = ('pr119-semantic', 'pr119-evidence')
ROOT_FILES = ('pr119-combination-initial.json', 'pr119-retarget.json', 'pr119-ownership-correction.json')
EXPECTED_REPORTS = {
    'pr119-semantic/REVIEW.md': 'c651f506f299dadda499f9375c5f137b7565258c2dd2a4b97f4f0a88d8c6cf61',
    'pr119-evidence/REVIEW.md': 'e9ab685012b9bec2ce1051c1292aee026abb3188377f49db94dbc0df42458c16',
}

def sha_file(path):
    h=hashlib.sha256(); size=0
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(65536), b''):
            h.update(chunk); size+=len(chunk)
    return {'bytes':size, 'sha256':h.hexdigest()}

def safe_name(name):
    p=PurePosixPath(name)
    if not name or p.is_absolute() or str(p)!=name or '\\' in name or any(x in ('.','..') for x in p.parts):
        raise ValueError('Unsafe or noncanonical path: '+repr(name))
    return name

def source_paths(root):
    root=Path(root)
    found=[]
    for name in SOURCE_DIRS:
        d=root/name
        if d.is_symlink() or not d.is_dir():
            raise ValueError('Source directory missing or linked: '+str(d))
        for f in d.rglob('*'):
            mode=f.lstat().st_mode
            if stat.S_ISDIR(mode):
                continue
            if not stat.S_ISREG(mode):
                raise ValueError('Nonregular source: '+str(f))
            found.append(safe_name(f.relative_to(root).as_posix()))
    for name in ROOT_FILES:
        if not stat.S_ISREG((root/name).lstat().st_mode):
            raise ValueError('Nonregular root receipt: '+name)
        found.append(name)
    if len(found)!=len(set(found)):
        raise ValueError('Duplicate source path')
    return sorted(found)

class XZWriter:
    """Hash raw tar and compressed bytes while writing only compressed bytes."""
    def __init__(self, destination=None):
        self.destination=destination
        self.raw_hash=hashlib.sha256(); self.raw_size=0
        self.xz_hash=hashlib.sha256(); self.xz_size=0
        self.compressor=lzma.LZMACompressor(format=lzma.FORMAT_XZ, check=lzma.CHECK_CRC64, preset=0)
    def _output(self,data):
        self.xz_hash.update(data); self.xz_size+=len(data)
        if self.destination is not None:
            self.destination.write(data)
    def write(self,data):
        self.raw_hash.update(data); self.raw_size+=len(data)
        self._output(self.compressor.compress(data))
        return len(data)
    def flush(self):
        if self.destination is not None:
            self.destination.flush()
    def finish(self):
        self._output(self.compressor.flush())
        self.flush()
        return {
            'compressed_bytes':self.xz_size,
            'compressed_sha256':self.xz_hash.hexdigest(),
            'uncompressed_tar_bytes':self.raw_size,
            'uncompressed_tar_sha256':self.raw_hash.hexdigest(),
        }

def render_archive(root, members, destination=None):
    writer=XZWriter(destination)
    with tarfile.open(fileobj=writer, mode='w|', format=tarfile.USTAR_FORMAT) as tar:
        for row in members:
            info=tarfile.TarInfo(row['path'])
            info.type=tarfile.REGTYPE; info.size=row['bytes']; info.mode=0o644
            info.uid=info.gid=info.mtime=0; info.uname=info.gname=''
            with (Path(root)/row['path']).open('rb') as source:
                tar.addfile(info, source)
    return writer.finish()

def dump(path, value):
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=True)+'\n', encoding='utf-8')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-root', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args=p.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    for name in ('MEMBERS.json','ARCHIVE.json',ARCHIVE_NAME):
        if (args.output/name).exists():
            raise FileExistsError(args.output/name)
    paths=source_paths(args.source_root)
    rows=[{'path':name, **sha_file(args.source_root/name)} for name in paths]
    by_path={r['path']:r for r in rows}
    for path, expected in EXPECTED_REPORTS.items():
        if by_path[path]['sha256']!=expected:
            raise ValueError('Frozen report changed: '+path)
    payload=sum(r['bytes'] for r in rows)
    if payload>=20*1024*1024:
        raise ValueError('Source payload exceeds the 20 MiB packet budget')
    manifest={
        'schema_version':1,
        'scope':'Every regular file in both completed PR119 review directories and all three root integration/ownership receipts; no exclusions.',
        'original_local_root':SOURCE_ROOT,
        'source_directories':list(SOURCE_DIRS),
        'root_receipts':list(ROOT_FILES),
        'excluded_files':[],
        'preservation':'All original file bytes retained, including original downloaded archives, extracted copies, failed attempts, and the earlier review subarchive. File ownership, times and modes are normalized in the archive.',
        'archive_regular_member_count':len(rows),
        'uncompressed_file_payload_bytes':payload,
        'members':rows,
    }
    dump(args.output/'MEMBERS.json',manifest)
    with (args.output/ARCHIVE_NAME).open('xb') as f:
        measures=render_archive(args.source_root,rows,f)
    if measures['compressed_bytes']>=5*1024*1024:
        raise ValueError('Compressed packet exceeds the 5 MiB packet budget')
    metadata={
        'schema_version':1,
        'archive':ARCHIVE_NAME,
        **measures,
        'regular_member_count':len(rows),
        'uncompressed_file_payload_bytes':payload,
        'member_manifest':{'path':'MEMBERS.json',**sha_file(args.output/'MEMBERS.json')},
        'deterministic_format':{
            'tar':'Python tarfile USTAR_FORMAT; lexicographic regular-file order; no directory records',
            'member_mode':'0644', 'uid':0, 'gid':0, 'mtime':0, 'uname':'', 'gname':'',
            'compression':'XZ; LZMA preset 0; CRC64; one stream',
            'pax_headers':False, 'links':False, 'special_files':False,
        },
        'fresh_lean_execution':'NOT_RUN',
        'publication_status':'Prepared locally for the coordinating parent; no remote writes performed by packet builder.',
    }
    dump(args.output/'ARCHIVE.json',metadata)
    print(json.dumps(metadata,indent=2))

if __name__=='__main__':
    main()
