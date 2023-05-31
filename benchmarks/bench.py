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

    # Generate a random signal based on https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html#r34b375daf612-1
    rng = np.random.default_rng()
    fs = 10e3
    amp = 2*np.sqrt(2)
    freq = 1234.0
    noise_power = 0.001 * fs / 2
    time = np.arange(size) / fs
    x = amp*np.sin(2*np.pi*freq*time)
    x += rng.normal(scale=np.sqrt(noise_power), size=time.shape)
    x = x.astype(np.float32)

    if namespace == "numpy":
        pass
    elif namespace == "cupy":
        x = cp.asarray(x, dtype=cp.float32)
    elif namespace == "torch_gpu":
        x = torch.asarray(x, device='cuda', dtype=torch.float32)
    elif namespace == "torch_cpu":
        x = torch.asarray(x, device='cpu', dtype=torch.float32)
    else:
        raise ValueError(f"unrecognized namespace requested for array backend: {namespace}")

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
