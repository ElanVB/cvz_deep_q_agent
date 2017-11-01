rm "$1_hyperparam_search_log.txt"
rm "$1.log"
for index in {0..16}
do
  python3 hyperparam_search.py "$1" "$index"
done
