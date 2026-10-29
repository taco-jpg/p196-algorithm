# N26 two-sector moving-frame decimal front
- **COMPUTED**, only for finite seed copies and time windows explicitly checked. Not a decimal Lychrel certificate.
- Let N_c be the period-8 shield seed from AgentN26DecimalP8Shield; define G_c(r,j) as the pair coefficient at spatial index 38+j and time t=88c+4+r, r=-16..88.
- Independent decimal digit-array replay: G_40 and G_42 agree for *all 105 frames* across j=0..251; G_40 and G_41 agree across only j=0..143 uniformly. At r=0 their common-prefix lengths are 270 versus 164.
- c=50 and c=60 show the same 252 versus 144 all-frame lengths; c=30 is transient (191 versus 144). Thus a two-copy/176-time-step moving-frame renormalisation is a concrete candidate, but it fails beyond these finite windows.
- Exact reproduction and data: calculation/new_structures/agent-N26/glider_renorm.py and glider_renorm_observations.csv; existing source data, decoder and independent arithmetic in same folder.
- Discussion: reports/AgentN26TwoSectorFront.md.
