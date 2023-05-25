import sys
import time
import os

import numpy as np
import torch
import cupy as cp

N_RUNS = 10

def allocate_arrays_scikit_learn(namespace):
    from sklearn.datasets import make_classification

    n_samples = 400_000
    n_features = 300
    X_np, y_np = make_classification(random_state=0,
                                     n_samples=n_samples,
                                     n_features=n_features
                                     )
    X_np, y_np = X_np.astype(np.float32), y_np.astype(np.float32)
    if namespace == 'numpy':
        X, y = X_np, y_np
    elif namespace == 'cupy':
        X = cp.asarray(X_np, dtype=cp.float32)
        y = cp.asarray(y_np, dtype=cp.float32)
    elif namespace == 'torch_cpu':
        X = torch.asarray(X_np)
        y = torch.asarray(y_np)
    elif namespace == 'torch_gpu':
        X = torch.asarray(X_np, device='cuda')
        y = torch.asarray(y_np, device='cuda')
    else:
        raise ValueError(f"unrecognized namespace requested for array backend: {namespace}")
    return X, y

def allocate_array_scipy(namespace):
    size = 50_000_000
    if namespace == "numpy":
        x = np.zeros(size, dtype=np.float32)
    elif namespace == "cupy":
        x = cp.zeros(size, dtype=cp.float32)
    elif namespace == "torch_gpu":
        torch.set_default_device("cuda")
        x = torch.zeros(size, dtype=torch.float32)
    elif namespace == "torch_cpu":
        torch.set_default_device("cpu")
        x = torch.zeros(size, dtype=torch.float32)
    else:
        raise ValueError(f"unrecognized namespace requested for array backend: {namespace}")
    x[0] = 1
    x[8] = 1
    return x

def sync(namespace):
    if namespace == 'torch_gpu':
        torch.cuda.synchronize(device="cuda")
    elif namespace == 'cupy':
        cp.cuda.stream.get_current_stream().synchronize()

def main(benchmark, namespace):
    if benchmark == 'scikit-learn':
        bench = bench_scikit_learn
    elif benchmark == 'scipy':
        bench = bench_scipy
    else:
        raise ValueError("benchmark must be 'scikit-learn' or 'scipy'")

    # Warmup run
    bench(namespace, print_times=False)

    for i in range(N_RUNS):
        bench(namespace)
        sys.stdout.flush()

def bench_scikit_learn(namespace, print_times=True):
    import sklearn
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

    sklearn.set_config(array_api_dispatch=True)
    lda_np = LinearDiscriminantAnalysis()
    X, y = allocate_arrays_scikit_learn(namespace=namespace)

    # fit
    sync(namespace)
    start = time.perf_counter()
    fitted = lda_np.fit(X, y)
    sync(namespace)
    end = time.perf_counter()
    fit_elapsed_time_sec = end - start
    if print_times:
        print(fit_elapsed_time_sec, namespace, 'fit', sep=',')

    # predict
    start = time.perf_counter()
    fitted.predict(X)
    sync(namespace)
    end = time.perf_counter()
    predict_elapsed_time_sec = end - start
    if print_times:
        print(predict_elapsed_time_sec, namespace, 'predict', sep=',')
    return fit_elapsed_time_sec, predict_elapsed_time_sec

def bench_scipy(namespace, print_times=True):
    from scipy.signal import welch

    x = allocate_array_scipy(namespace=namespace)

    sync(namespace)
    start = time.perf_counter()
    f, p = welch(x, nperseg=8)
    sync(namespace)
    end = time.perf_counter()
    elapsed_time_sec = end - start
    if print_times:
        print(elapsed_time_sec, namespace, 'SCIPY_STRICT_ARR_API' in os.environ, sep=',')

    return elapsed_time_sec

if __name__ == "__main__":
    benchmark, namespace = sys.argv[1:]
    main(benchmark, namespace)
