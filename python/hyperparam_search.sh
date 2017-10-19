rm "$1_hyperparam_search_log.txt"
for index in {1..16}
do
  python3 hyperparam_search.py "$1" "$index"
done
