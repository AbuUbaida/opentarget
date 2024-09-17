# bash ./eval.sh > eval.log

###################################################################################################################
config=../config/config-bertweet.txt
test_data=../path_to_test_data.csv
model_dir=./path_to_trained_model

seed=3

echo "Start training on seed ${seed}......"
python eval.py -s ${seed} -c ${config} -test ${test_data} -mod_dir ${model_dir} -m bertweet
###################################################################################################################