library(dplyr)

# Download invitrodb.csv and documentation from Clowder 
# documentation available at https://clowder.edap-cluster.com/files/62cee26ee4b055edffbba11d?dataset=62c435c7e4b01d27e3b2b61f&space=62bb560ee4b07abf29f88fef
stage = fs::dir_create("staging") |> fs::path("invitrodb.csv")
invitrodb = "https://clowder.edap-cluster.com/files/63642290e4b04f6bb140a10d/blob"

options(timeout = 600)
download.file(invitrodb, destfile = stage, mode = "wb")

df = readr::read_csv(stage)
out = fs::dir_create("brick/invitrodb.parquet")

# See
#  - analysis/dump-ddl.sh
#  - analysis/join.R
df <- df %>% mutate(across(
	c(
		aeid,
		chid,
		m4id,
		nconc,
		npts,
		nmed_gtbl,
		m5id,
		fitc,
	), as.integer))

# Write as a dataset to avoid the 2GB limit of a single parquet file
arrow::write_dataset(df, out, max_rows_per_file = 1e6)
