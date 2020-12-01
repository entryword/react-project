#!/bin/bash

set -ex

mysql=(mysql -u root -p12345678 -D pyladies)
for f in /sql_init/*; do
    case "$f" in
        *.sql)    echo "$0: running $f"; "${mysql[@]}" < "$f"; echo ;;
        *.sql.gz) echo "$0: running $f"; gunzip -c "$f" | "${mysql[@]}"; echo ;;
        *)        echo "$0: ignoring $f" ;;
    esac
    echo
done