import sys
import time

import sklearn
from sklearn.datasets import make_classification
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import numpy as np
import torch
import cupy as cp


def allocate_array(namespace):
    n_samples = 500_00
    n_features = 300
    X_np, y_np = make_classification(random_state=0,
                                     n_samples=n_samples,
                                     n_features=n_features
                                     )
    X_np, y_np = X_np.astype(np.float32), y_np.astype(np.float32)
    if namespace == 'numpy':
        X, y = X_np, y_np
    elif namespace == 'cupy':
        X = cp.asarray(X_np)
        y = cp.asarray(y_np)
    elif namespace == 'torch_cpu':
        X = torch.asarray(X_np)
        y = torch.asarray(y_np)
    elif namespace == 'torch_gpu':
        X = torch.asarray(X_np, device='cuda')
        y = torch.asarray(y_np, device='cuda')
    else:
        raise ValueError(f"unrecognized namespace requested for array backend: {namespace}")
    return X, y

def main():
    namespace = sys.argv[1]
    X, y = allocate_array(namespace=namespace)
    sklearn.set_config(array_api_dispatch=True)
    lda_np = LinearDiscriminantAnalysis()

    # fit
    start = time.perf_counter()
    fitted = lda_np.fit(X, y)
    end = time.perf_counter()
    elapsed_time_sec = end - start
    print(elapsed_time_sec, namespace, 'fit', sep=',')

    # predict
    start = time.perf_counter()
    fitted.predict(X)
    end = time.perf_counter()
    elapsed_time_sec = end - start
    print(elapsed_time_sec, namespace, 'predict', sep=',')

if __name__ == "__main__":
    main()
