# EPA ToxCast — High‑Throughput In Vitro Toxicity Screening Data

> **Brick ID:** `biobricks-ai/toxcast`
>
> **Release pinned:** **ToxCast/Tox21 invitroDB v3.6 (August 2023)**
> **Primary assets:** columnar **Parquet** tables converted from the EPA’s official invitroDB SQLite dump
> **Licence:** Public Domain (U.S. Government Works)

---

## What is ToxCast?

ToxCast is the U.S. EPA’s high‑throughput screening (HTS) program that measures the biological activity of thousands of environmental chemicals across >1 000 biochemical and cell‑based assays.  Together with Tox21, it provides the largest public in vitro toxicity dataset and underpins many new‑approach methodologies (NAMs) in computational toxicology.

---
## Quick start

List the tables and peek at endocrine‑disruptor hits:

```python
import biobricks, pyarrow.dataset as ds, pandas as pd

# 1. discover assets
tox = biobricks.assets("toxcast")
print(tox.__dict__.keys())

```

---

## Provenance & build pipeline

| Stage        | Script                       | Action                                                                   |
| ------------ | ---------------------------- | ------------------------------------------------------------------------ |
| **Download** | `stages/1_fetch.sh`          | Grabs `invitrodb_v3_6.sqlite.zip` + SHA‑256 from the EPA S3 bucket.      |
| **Extract**  | `stages/2_unzip.sh`          | Unzips to `invitrodb_v3_6.sqlite`.                                       |
| **Convert**  | `stages/3_sqlite2parquet.py` | Streams each major table into Arrow → Snappy Parquet, preserving dtypes. |
| **Manifest** | `stages/4_manifest.R`        | Records row counts + schema hashes.                                      |

The pipeline is wired with **DVC**; each time EPA publishes a new invitroDB version, a GitHub Action rebuilds and commits a new brick snapshot.

---

## Update cadence

Historically, ToxCast/Tox21 releases one invitroDB update per 1‑2 years.  The build bot checks quarterly and publishes a new commit when a higher minor version appears (e.g., v3.7).

---

## Tips & gotchas

* **Reference chemicals vs. screening set** – use `invivo_ref_parquet` to flag chemicals with known in vivo outcomes for model validation.
* **Burst / cytotoxicity filtering** – v3.6 already applies “burst correction” (masking non‑specific cytotoxic responses), but level‑5 fits provide raw parameters if you need custom filtering.
* **log10(AC50) handy** – many QSAR workflows convert `modl_acc` (M) to `–log10` to stabilise regression.

---

## Road‑map

* Provide **compound‑to‑assay sparse matrix** (chemicals × aeid, binary) for quick machine‑learning ingestion.
* Add **SSMD quality metrics** once EPA exposes them in v4.

---

## Citation

```
U.S. EPA. ToxCast & Tox21 invitroDB v3.6 (August 2023 release).  
BioBricks.ai – toxcast brick, commit <hash>.
```

---

## Licence

ToxCast data are U.S. Government Works and therefore in the **public domain**.  You may use, share, or modify without restriction; attribution to EPA is appreciated.
