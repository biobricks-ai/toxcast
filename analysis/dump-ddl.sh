#!/bin/sh

## Requires:
##   wget     <pkg:deb/debian/wget>
##   zcat     <pkg:deb/debian/gzip>
##   perl     <pkg:deb/debian/perl-base>
##   echo     <pkg:deb/debian/coreutils>
##   duckdb

set -eu

MYSQL_DUMP_FILE="invitrodb_v4_1_mysql.gz"
MYSQL_DDL_OUT="toxcast.ddl"

[ -f "$MYSQL_DUMP_FILE" ] \
	|| wget --content-disposition 'https://clowder.edap-cluster.com/api/files/6481e47ce4b08a6b394e669f/blob'

[ -f "$MYSQL_DDL_OUT" ] \
	|| zcat invitrodb_v4_1_mysql.gz \
		| perl -ne 'print if /^CREATE TABLE/../^\)/' \
		> "$MYSQL_DDL_OUT"

< "$MYSQL_DDL_OUT" perl -n -'Mv5.10;say join "\t", qw(name type);' -E '
		next if /CREATE TABLE|KEY/;
		next unless /\`/;
		say join "\t", /\`([^\`]+)\`\s+(\S+)/;
	' > mysql-schema.tsv

duckdb -csv -separator "$(/bin/echo -e "\t")" \
	-c 'SELECT name, type FROM parquet_schema("brick/invitrodb.parquet/part-0.parquet")' \
	> parquet-schema.tsv
