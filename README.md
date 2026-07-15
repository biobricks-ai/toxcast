# toxcast

US EPA ToxCast / **invitrodb v4.3** (August 2025) high-throughput in vitro
bioactivity data.

- **Source:** EPA-ORD-CCTE Clowder, invitrodb v4.3 space
  <https://clowder.edap-cluster.com/spaces/687e388ce4b02565bc3e28e4>
  (`INVITRODB_SUMMARY.zip` → `mc5-6_winning_model_fits-flags_invitrodbv4_3_AUG2024.csv`)
- **DOI:** <https://doi.org/10.23645/epacomptox.6062623.v14>
- **License:** Public domain (US Government work) — commercial use OK.

## Table

| table | rows | cols | description |
|-------|-----:|-----:|-------------|
| `invitrodb.parquet` | 3,527,285 | 65 | Level-5/6 (mc5-6) winning-model fits and flags: one row per assay endpoint x sample (`aeid` x `spid`), with tcplfit2 concentration-response curve fits, potency estimates (`ac50`, `bmd`, `acc`, `top`), continuous hit calls (`hitcall`, `hitc`), fit category (`fitc`) and mc6 flags. |

Built from the invitrodb v4.3 mc5-6 summary CSV. invitrodb v4.x uses the
`tcplfit2` curve-fitting engine, so this schema differs from the previous
v3.5 build (per-model `cnst_*/hill_*/gnls_*/modl_*` columns are replaced by
flattened tcplfit2 winning-model parameters). `hitcall` is a continuous
value in [0,1]; a value >= 0.9 is treated as active.
