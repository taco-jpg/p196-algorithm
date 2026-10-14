"""Archive every comparison certificate without modifying the audited checkers."""
from __future__ import annotations
import contextlib,gzip,hashlib,io,json
from pathlib import Path
import padded_core_classification as pc
import return_composition as rc
import third_gate_check as tc
HERE=Path(__file__).resolve().parent

def main():
 records=[]
 for module,base in ((pc,5),(rc,9),(tc,13)):
  pc.GAP=pc.run.Length((1,),base)
  with contextlib.redirect_stdout(io.StringIO()):module.main()
  name=module.__name__
  data=json.dumps(pc.COMPARISONS,sort_keys=True,separators=(',',':')).encode()
  summary=json.loads((HERE/(name+'.json')).read_text())['uniform_comparison_certificate']
  digest=hashlib.sha256(data).hexdigest()
  assert digest==summary['witness_stream_sha256']
  assert len(pc.COMPARISONS)==summary['comparisons']
  target=HERE/(name+'_comparisons.json.gz')
  target.write_bytes(gzip.compress(data,mtime=0))
  assert gzip.decompress(target.read_bytes())==data
  records.append({'source':name+'.py','affine_base':base,'archive':target.name,
     'comparison_records':len(pc.COMPARISONS),'uncompressed_bytes':len(data),
     'compressed_bytes':target.stat().st_size,'uncompressed_sha256':digest,
     'archive_sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
 result={'status':'complete comparison streams retained and checked against audited result hashes',
         'total_records':sum(x['comparison_records'] for x in records),'archives':records}
 assert result['total_records']==5204
 (HERE/'capture_witnesses.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))

if __name__=='__main__':main()
