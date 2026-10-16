"""Lossless, ordered <=6 MB publication parts with two layers of hashes.

Generate archives only from actual saved runs. A capped LRAT trace remains
explicitly incomplete and is never converted into a claimed refutation.
"""
from pathlib import Path
import gzip, hashlib, json, shutil, tempfile

ROOT=Path(__file__).parent
LIMIT=6_000_000
SOURCES=[
 ('dfa4_neg2.cnf','complete primary formula'),
 ('dfa4_neg2.lrat','complete primary UNSAT proof, independently verified'),
 ('dfa4_sym_neg2.cnf','complete corroborating formula'),
 ('dfa4_sym_neg2.lrat','complete corroborating UNSAT proof, independently verified'),
 ('dfa5_sym_neg2.cnf','complete capped-run formula; five-state status UNKNOWN'),
 ('dfa5_sym_neg2.lrat.gz','incomplete capped trace; not an UNSAT proof'),
]


def digest(path,decoded=False):
    h=hashlib.sha256();size=0
    op=gzip.open if decoded and str(path).endswith('.gz') else open
    with op(path,'rb') as f:
        for data in iter(lambda:f.read(1<<20),b''):
            h.update(data);size+=len(data)
    return size,h.hexdigest()


def main():
    dest=ROOT/'evidence_parts';dest.mkdir(exist_ok=True)
    entries=[]
    with tempfile.TemporaryDirectory(prefix='safe-language-archive-') as temp:
        for name,status in SOURCES:
            src=ROOT/name
            if name.endswith('.gz'):
                archive=src;decoded_name=name[:-3]
            else:
                archive=Path(temp)/(name+'.gz');decoded_name=name
                with src.open('rb') as f,archive.open('wb') as g:
                    with gzip.GzipFile(filename='',mode='wb',fileobj=g,compresslevel=9,mtime=0) as z:
                        shutil.copyfileobj(f,z,1<<20)
            decoded_size,decoded_sha=digest(src,True)
            archive_size,archive_sha=digest(archive)
            parts=[]
            with archive.open('rb') as f:
                for i,data in enumerate(iter(lambda:f.read(LIMIT),b''),1):
                    part=dest/(decoded_name+'.gz.part'+str(i).zfill(3))
                    part.write_bytes(data)
                    parts.append(dict(file=part.name,bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
            entry=dict(source=name,decoded_filename=decoded_name,semantic_status=status,
                       decoded_bytes=decoded_size,decoded_sha256=decoded_sha,
                       archive_format='gzip',archive_bytes=archive_size,archive_sha256=archive_sha,
                       parts=parts)
            entries.append(entry)
            print(json.dumps({k:v for k,v in entry.items() if k!='parts'}),flush=True)
    (dest/'MANIFEST.json').write_text(json.dumps(dict(part_limit_bytes=LIMIT,artifacts=entries),indent=2)+'\n')


if __name__=='__main__':main()
