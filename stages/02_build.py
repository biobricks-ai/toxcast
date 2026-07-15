#!/usr/bin/env python3
"""Build the invitrodb v4.3 level-5/6 (mc5-6) winning-model summary table.

Reads the mc5-6 winning-model-fits + flags CSV directly from
download/INVITRODB_SUMMARY.zip and writes it as a partitioned parquet
dataset at brick/invitrodb.parquet (same single-table layout the prior
brick produced from the invitrodb v3.5 mc5 flat CSV).

Note: invitrodb v4.x uses the tcplfit2 curve-fitting engine, so this
summary schema differs from the v3.5 mc5 file (per-model cnst_*/hill_*/
gnls_*/modl_* columns are replaced by flattened tcplfit2 winning-model
parameters: ac50, top, ga, la, bmd, bmdl, bmdu, hitcall, model_type ...).
"""
from pathlib import Path
import zipfile
import pandas as pd
import pyarrow as pa
import pyarrow.dataset as pads

ZIP_NAME = "INVITRODB_SUMMARY.zip"
CSV_MEMBER = "mc5-6_winning_model_fits-flags_invitrodbv4_3_AUG2024.csv"

# Columns that are genuinely integer counts / ids in invitrodb v4.3.
# (whitelist only -- do NOT blanket-coerce string columns)
INT_COLS = [
    "aeid", "chid", "m4id", "m5id",
    "nconc", "npts",
    "nmed_gtbl_pos", "nmed_gtbl_neg",
    "fitc",
]
# NB: nrep is left as float -- in invitrodb v4.3 it can be fractional
# (a replicate-count average), unlike the integer nrep in v3.5.


def main():
    download_path = Path("download")
    brick_path = Path("brick")
    out = brick_path / "invitrodb.parquet"
    out.mkdir(parents=True, exist_ok=True)

    zip_path = download_path / ZIP_NAME
    print(f"Reading {CSV_MEMBER} from {zip_path} ...")

    with zipfile.ZipFile(zip_path) as z:
        with z.open(CSV_MEMBER) as fh:
            # latin1: the file contains non-ASCII characters (e.g. +/- signs)
            df = pd.read_csv(fh, encoding="latin1", low_memory=False)

    print(f"Loaded {len(df):,} rows x {len(df.columns)} cols")

    for c in INT_COLS:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").astype("Int64")

    # Write as a dataset (multiple parquet files) to avoid the 2GB
    # single-file parquet limit.
    table = pa.Table.from_pandas(df, preserve_index=False)
    pads.write_dataset(
        table,
        out,
        format="parquet",
        max_rows_per_file=1_000_000,
        max_rows_per_group=1_000_000,
        existing_data_behavior="delete_matching",
        basename_template="part-{i}.parquet",
    )

    n_files = len(list(out.glob("*.parquet")))
    print(f"Wrote {out} ({n_files} files): {len(df):,} rows x {len(df.columns)} cols")


if __name__ == "__main__":
    main()
