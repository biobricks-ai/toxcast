library(dplyr)

mysql <- readr::read_tsv('mysql-schema.tsv') %>%
	distinct( name , .keep_all=TRUE )
parquet <- readr::read_tsv('parquet-schema.tsv')

join <- inner_join( mysql, parquet, by=c('name') ) %>%
	filter( type.x != 'double' & type.y == 'DOUBLE' )

print(join)
print(join %>% select(name) )
