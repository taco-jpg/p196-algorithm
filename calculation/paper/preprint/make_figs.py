import csv, statistics as st
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.family":"serif","mathtext.fontset":"stix","font.size":10,
    "axes.linewidth":0.6,"xtick.direction":"in","ytick.direction":"in","axes.spines.top":False,
    "axes.spines.right":False,"pdf.fonttype":42})
rows=[]
for r in csv.DictReader(open("../data/throughput.csv")):
    rows.append(dict(it=int(r["iteration"]),dg=int(r["digits"]),eng=r["engine"].replace("cuda196_",""),
        sps=float(r["steps_per_s"]) if r["steps_per_s"] else None,
        pw=float(r["power_w"]) if r["power_w"] else None))
col={"v6r2":"#999999","v6r3":"#56B4E9","v8":"#009E73","v9":"#E69F00","v10":"#D55E00"}
lab={"v6r2":"v6r2","v6r3":"v6r3","v8":"v8","v9":"v9","v10":"v10"}
good=[r for r in rows if r["sps"] and (r["pw"] is None or r["pw"]>30) and r["it"]>523226464]
# medians for consistency check
for e in col:
    v=[r["sps"] for r in good if r["eng"]==e and r["pw"] is not None]; print(e,len(v),round(st.median(v)))
fig,ax=plt.subplots(1,2,figsize=(7.0,3.0))
for e in col:
    g=[r for r in good if r["eng"]==e]
    ax[0].plot([r["it"]/1e9 for r in g],[r["sps"] for r in g],".",ms=1.4,color=col[e],label=lab[e],rasterized=True)
    ax[1].plot([r["it"]/1e9 for r in g],[r["sps"]*r["dg"]/1e12 for r in g],".",ms=1.4,color=col[e],rasterized=True)
ax[1].axvline(3.70,color="k",lw=.5,ls=":"); ax[1].text(3.74,1.0,"GPU clock\n1.71 → 1.93 GHz",fontsize=8,va="bottom")
ax[0].set_ylabel("steps per second"); ax[1].set_ylabel(r"digit-steps per second ($10^{12}$)")
for a,t in zip(ax,"ab"):
    a.set_xlabel(r"iteration $t$ ($10^9$)"); a.text(-0.17,1.06,f"({t})",transform=a.transAxes,fontweight="bold")
    a.set_xlim(0.4,6.1); a.grid(alpha=.25,lw=.4)
ax[0].set_ylim(1000,5300); ax[1].set_ylim(0.9,4.6)
leg=ax[0].legend(markerscale=6,frameon=False,ncol=2,loc="upper right",handletextpad=.2,columnspacing=.8)
fig.tight_layout(); fig.savefig("figs/fig_throughput.pdf",dpi=300)
# growth
fig,ax=plt.subplots(1,2,figsize=(7.0,2.8))
ax[0].plot([r["it"]/1e9 for r in rows],[r["dg"]/1e9 for r in rows],color="k",lw=1)
ax[0].set_ylabel(r"digits ($10^9$)"); ax[0].set_xlabel(r"iteration $t$ ($10^9$)"); ax[0].grid(alpha=.25,lw=.4)
ax[0].axhline(2.5,color="#D55E00",lw=.7,ls="--"); ax[0].text(0.55,2.30,r"$2.5\times10^{9}$ digits",color="#D55E00",fontsize=9)
prev=None; xs=[];ys=[]
for r in rows:
    if prev and r["it"]-prev["it"]==1_000_000:
        xs.append(r["it"]/1e9); ys.append((r["dg"]-prev["dg"])/1e6)
    prev=r
ax[1].plot(xs,ys,".",ms=1.4,color="k",rasterized=True)
ax[1].axhline(0.41393,color="#D55E00",lw=.7,ls="--"); ax[1].set_ylim(0.4125,0.4150)
ax[1].set_ylabel("digits gained per iteration"); ax[1].set_xlabel(r"iteration $t$ ($10^9$)"); ax[1].grid(alpha=.25,lw=.4)
for a,t in zip(ax,"ab"): a.text(-0.17,1.06,f"({t})",transform=a.transAxes,fontweight="bold")
print("growth mean",np.mean(ys),np.std(ys),min(ys),max(ys))
fig.tight_layout(); fig.savefig("figs/fig_growth.pdf",dpi=300)
