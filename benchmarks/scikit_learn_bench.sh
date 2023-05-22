#!/bin/bash

arguments=("numpy" "torch_cpu" "torch_gpu" "cupy")

echo "Duration,Backend,Method" > scikit_learn_timings.csv

# Run the command 10 times for each library
for arg in "${arguments[@]}"
do
    command="python scikit_learn_bench.py $arg"

    echo "Running: $command"

    for ((i=1; i<=10; i++))
    do
        eval $command | tee -a scikit_learn_timings.csv
    done

    echo ""
done
