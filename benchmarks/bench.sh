#!/bin/bash

libraries=("numpy" "torch_cpu" "torch_gpu" "cupy")
benchmark=$1

if [[ "$benchmark" != "scikit-learn" && "$benchmark" != "scipy" ]]; then
    echo "Invalid benchmark argument. Please specify either 'scikit-learn' or 'scipy'."
    exit 1
fi

csv_file="${benchmark}_timings.csv"

if [[ "$benchmark" == "scikit-learn" ]]; then
    echo "Duration,Backend,Method" > "$csv_file"
    env_variables=("")
else
    echo "Duration,Backend,Strict" > "$csv_file"
    env_variables=("" "SCIPY_STRICT_ARR_API=1")
fi

# Run each benchmark in a separate process
for env_var in "${env_variables[@]}"
do
    for arg in "${libraries[@]}"
    do
        command="$env_var python bench.py $benchmark $arg"

        echo "Running: $command"

        eval "$command" | tee -a "$csv_file"

        echo ""
    done
done
