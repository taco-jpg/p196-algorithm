#!/usr/bin/env python3
"""Verify this lossless publication package and optionally restore original logical paths."""
import argparse,hashlib,json
from pathlib import Path,PurePosixPath
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--package',type=Path,required=True)
p.add_argument('--output',type=Path)
a=p.parse_args();root=a.package.resolve()
def h(data):return hashlib.sha256(data).hexdigest()
def safe(name):
 x=PurePosixPath(name)
 if x.is_absolute() or '..' in x.parts or not x.parts:raise RuntimeError('Unsafe path: '+name)
 return x
manifest=json.loads((root/'MANIFEST.json').read_text())
for x in manifest['files']:
 path=root/safe(x['path']);data=path.read_bytes()
 if len(data)!=x['bytes'] or h(data)!=x['sha256']:raise RuntimeError('Manifest mismatch: '+x['path'])
index=json.loads((root/'LOSSLESS_INDEX.json').read_text())
if a.output is not None:a.output.mkdir(parents=True,exist_ok=False)
for x in index['files']:
 data=(root/safe(x['stored_as'])).read_bytes()
 if len(data)!=x['bytes'] or h(data)!=x['sha256']:raise RuntimeError('Logical content mismatch: '+x['logical_path'])
 if a.output is not None:
  dest=a.output/safe(x['logical_path']);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
  if dest.read_bytes()!=data:raise RuntimeError('Restoration mismatch: '+x['logical_path'])
print(json.dumps({'status':'PASS','physical_files_verified':len(manifest['files']),
 'logical_files_verified':len(index['files']),'restored':a.output is not None,'output':str(a.output) if a.output else None,
 'compiled_object_exclusions':len(json.loads((root/'EXCLUSIONS.json').read_text())['compiled_objects'])},indent=2))
