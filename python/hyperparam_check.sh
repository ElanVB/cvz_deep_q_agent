rm "$1.log"
for index in {0..16}
do
  python3 hyperparam_check.py "$1" "$index"
done
