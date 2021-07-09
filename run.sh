for i in {1,2,3}
do
    echo "running ClickHouse test"
    python ./src/run.py ch
    echo 1 > /proc/sys/vm/drop_caches
    echo "running OpenLookeng test"
    python ./src/run.py ol
    echo 1 > /proc/sys/vm/drop_caches
done