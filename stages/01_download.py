#!/usr/bin/env python3
"""Download the invitrodb v4.3 summary package (US EPA ToxCast).

Source: EPA-ORD-CCTE Clowder, "invitrodb v4.3" space (Aug 2025 release).
  space:   https://clowder.edap-cluster.com/spaces/687e388ce4b02565bc3e28e4
  dataset: Summary_Files (687e392ae4b02565bc3e2914)
  file:    INVITRODB_SUMMARY.zip (blob 68af6b70e4b02565fc7c3a98)

The zip holds the chemical-by-assay variable matrix output (mc5/mc6
level-5/6 summary), assay annotations and cytotox tables. We keep the
level-5 (mc5) winning-model summary CSV -- the same layer the prior
brick built (previously the standalone invitrodb v3.5 mc5 flat CSV).
"""
from pathlib import Path
import sys
import requests

URL = "https://clowder.edap-cluster.com/api/files/68af6b70e4b02565fc7c3a98/blob"
FILENAME = "INVITRODB_SUMMARY.zip"
EXPECTED_SIZE = 7502075199  # bytes, verified against Clowder file metadata


def main():
    download_path = Path("download")
    download_path.mkdir(exist_ok=True)
    dest = download_path / FILENAME

    if dest.exists() and dest.stat().st_size == EXPECTED_SIZE:
        print(f"{FILENAME} already present ({dest.stat().st_size} bytes); skipping download.")
        return

    print(f"Downloading {FILENAME} from {URL} ...")
    with requests.get(URL, stream=True, timeout=600) as resp:
        resp.raise_for_status()
        with open(dest, "wb") as out:
            for chunk in resp.iter_content(chunk_size=1 << 20):
                out.write(chunk)

    size = dest.stat().st_size
    print(f"Saved {FILENAME}: {size} bytes")
    if size != EXPECTED_SIZE:
        print(f"WARNING: expected {EXPECTED_SIZE} bytes, got {size}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
