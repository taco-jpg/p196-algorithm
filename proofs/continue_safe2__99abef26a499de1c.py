"""One final bounded r=2 safe-image construction; keep the 100k cap record."""
import json
import time
from residual_kernel import HERE,base_machine
from safe_ancestry import safe_source,image_of,accepted
from image_ancestry import product_observer
from compact_kernel import run

start=time.monotonic()
deadline=start+240
saved=json.loads((HERE/'safe_image1_machine.json').read_text())
image,build=image_of(safe_source((saved['delta'],saved['finish'])),deadline,
                     cap=1000000,nfa_save=HERE/'safe_image2_nfa.json')
report=dict(seconds_cap=240,subset_cap=1000000,build=build,
            status=build['status'],live_class_count=None)
if image is not None:
    (HERE/'safe_image2_machine.json').write_text(json.dumps(dict(delta=image[0],finish=image[1]),separators=(',',':'))+'\n')
    report['splice_in_safe_image']=accepted(image,((5,0,5,13,17),None))
    product=product_observer(base_machine(),image,cap=1000000)
    if product is None:
        report['status']='UNKNOWN_observer_cap'
    elif time.monotonic()>deadline:
        report['status']='UNKNOWN_time_cap_before_kernel'
    else:
        (HERE/'observation_safe2_depth0.json').write_text(json.dumps(dict(depth=0,delta=product[0],finish=product[1]),separators=(',',':'))+'\n')
        result=run(0,3000000,max(0,deadline-time.monotonic()),'safe2_')
        report['kernel']=result
        report['status']=result['status']
        report['live_class_count']=result.get('live_class_count')
report['seconds']=time.monotonic()-start
(HERE/'safe2_extended_report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report),flush=True)
