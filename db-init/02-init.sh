# import data from csv files to postgres
DB_SCHEMA="sber_avtopodpiska"

function import_data {
    # $1 - data
    # $2 - table_name
    header=`head -n 1 $1`
    psql -d $POSTGRES_DB \
        -U $POSTGRES_USER \
        -c "COPY $DB_SCHEMA.$2 ($header) FROM '$1' DELIMITER ',' CSV HEADER;"
}

for path in `ls usr/data/*.csv`; do
    table_name="raw_`expr "$path" : "usr/data/ga_\(.*\)\.csv"`"
    import_data "/$path" $table_name
    rm "/$path"
    echo "Imported $path to $table_name"
done
