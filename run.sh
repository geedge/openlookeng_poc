for i in {1,2,3}
do
python ./src/autotest.py ch
echo 1 > /proc/sys/vm/drop_caches
python ./src/autotest.py ol
echo 1 > /proc/sys/vm/drop_caches
done