#!/usr/bin/env python3
"""Verify every PR119 archive member; optionally compare originals or recover bytes.
Uses Python standard library only. Does not run Lean or historical evidence scripts.
"""
import argparse
import hashlib
import json
import lzma
from pathlib import Path
import tarfile
from build_packet import safe_name, sha_file, source_paths, render_archive

def require(condition,message):
    if not condition:
        raise ValueError(message)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--packet-dir',type=Path,default=Path(__file__).resolve().parent)
    p.add_argument('--source-root',type=Path)
    p.add_argument('--extract',type=Path,help='Recover into a new, nonexistent directory after all checks pass')
    p.add_argument('--result',type=Path)
    args=p.parse_args()
    packet=args.packet_dir
    metadata=json.loads((packet/'ARCHIVE.json').read_text())
    require(sha_file(packet/'MEMBERS.json')=={k:metadata['member_manifest'][k] for k in ('bytes','sha256')},'Member-manifest identity mismatch')
    manifest=json.loads((packet/'MEMBERS.json').read_text())
    rows=manifest['members']; expected={r['path']:r for r in rows}
    require(len(rows)==len(expected),'Duplicate manifest paths')
    require(list(expected)==sorted(expected),'Manifest order is not lexicographic')
    for name in expected:
        safe_name(name)
    archive=packet/safe_name(metadata['archive'])
    require(sha_file(archive)=={'bytes':metadata['compressed_bytes'],'sha256':metadata['compressed_sha256']},'Compressed archive identity mismatch')
    raw_hash=hashlib.sha256(); raw_size=0
    with lzma.open(archive,'rb') as f:
        for chunk in iter(lambda:f.read(65536),b''):
            raw_hash.update(chunk); raw_size+=len(chunk)
    require(raw_size==metadata['uncompressed_tar_bytes'],'Uncompressed tar size mismatch')
    require(raw_hash.hexdigest()==metadata['uncompressed_tar_sha256'],'Uncompressed tar hash mismatch')
    names=[]; payload=0
    with tarfile.open(archive,'r:xz') as tar:
        for m in tar:
            safe_name(m.name)
            require(m.name not in names,'Duplicate archive member: '+m.name)
            require(m.isfile() and m.type==tarfile.REGTYPE,'Nonregular archive member: '+m.name)
            require(m.name in expected,'Unexpected member: '+m.name)
            require(not m.pax_headers and not m.linkname,'Extended header or link: '+m.name)
            require((m.mode,m.uid,m.gid,m.mtime,m.uname,m.gname)==(0o644,0,0,0,'',''),'Noncanonical tar metadata: '+m.name)
            row=expected[m.name]; h=hashlib.sha256(); size=0
            with tar.extractfile(m) as f:
                for chunk in iter(lambda:f.read(65536),b''):
                    h.update(chunk); size+=len(chunk)
            require(size==row['bytes']==m.size,'Member size mismatch: '+m.name)
            require(h.hexdigest()==row['sha256'],'Member hash mismatch: '+m.name)
            names.append(m.name); payload+=size
    require(names==list(expected),'Archive members differ from manifest order or coverage')
    require(len(names)==metadata['regular_member_count']==manifest['archive_regular_member_count'],'Count mismatch')
    require(payload==metadata['uncompressed_file_payload_bytes']==manifest['uncompressed_file_payload_bytes'],'Payload size mismatch')
    original_check='NOT_REQUESTED'; reproduction='NOT_REQUESTED'
    if args.source_root:
        require(source_paths(args.source_root)==names,'Current source inventory differs from archived inventory')
        for row in rows:
            require(sha_file(args.source_root/row['path'])=={k:row[k] for k in ('bytes','sha256')},'Original source changed: '+row['path'])
        original_check='PASS: every original file rehashed; inventory exactly matches'
        rebuilt=render_archive(args.source_root,rows)
        require(all(rebuilt[k]==metadata[k] for k in rebuilt),'Deterministic rebuild differs from archive')
        reproduction='PASS: second independent serialization has identical compressed and uncompressed hashes and sizes'
    report_copies={
        'PR119-SEMANTIC-REVIEW.md':'pr119-semantic/REVIEW.md',
        'PR119-EVIDENCE-REVIEW.md':'pr119-evidence/REVIEW.md',
    }
    copies=[]
    for copy, original in report_copies.items():
        if (packet/copy).exists():
            require(sha_file(packet/copy)=={k:expected[original][k] for k in ('bytes','sha256')},'Readable report copy differs: '+copy)
            copies.append(copy)
    recovered=0
    if args.extract:
        require(not args.extract.exists() and not args.extract.is_symlink(),'Recovery target must not exist')
        args.extract.mkdir(parents=True,exist_ok=False)
        with tarfile.open(archive,'r:xz') as tar:
            for m in tar:
                target=args.extract/m.name
                target.parent.mkdir(parents=True,exist_ok=True)
                with tar.extractfile(m) as source, target.open('xb') as output:
                    for chunk in iter(lambda:source.read(65536),b''):
                        output.write(chunk)
                require(sha_file(target)=={k:expected[m.name][k] for k in ('bytes','sha256')},'Recovered identity mismatch: '+m.name)
                recovered+=1
    result={
        'status':'PASS',
        'checked_archive':metadata['archive'],
        'compressed_bytes':metadata['compressed_bytes'],
        'compressed_sha256':metadata['compressed_sha256'],
        'uncompressed_tar_bytes':raw_size,
        'uncompressed_tar_sha256':raw_hash.hexdigest(),
        'regular_members_individually_checked':len(names),
        'file_payload_bytes':payload,
        'unsafe_paths':0,'duplicate_paths':0,'links':0,'special_files':0,
        'normalized_metadata':'PASS',
        'original_byte_recheck':original_check,
        'deterministic_reproduction':reproduction,
        'readable_reports_verified':copies,
        'recovered_files':recovered,
        'fresh_lean_execution':'NOT_RUN',
        'remote_operations':'NONE',
    }
    if args.result:
        require(not args.result.exists(),'Result path already exists')
        args.result.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
