#!/bin/bash

arguments=("numpy" "torch_cpu" "torch_gpu" "cupy")
env_variables=("" "SCIPY_STRICT_ARR_API=1")

echo "Duration,Backend,Strict" > scipy_timings.csv

# Run the command 10 times for each combination
for env_var in "${env_variables[@]}"
do
    for arg in "${arguments[@]}"
    do
        command="$env_var python scipy_bench.py $arg"

        # Print the command
        echo "Running: $command"

        # Execute the command 10 times
        for ((i=1; i<=10; i++))
        do
            eval $command | tee -a scipy_timings.csv
        done

        echo ""
    done
done
