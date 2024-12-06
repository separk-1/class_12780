import random
import numpy as np
import torch

def set_seed(seed=42):
    """
    Sets random seeds for reproducibility across different environments.
    Automatically handles GPU and CPU configurations.
    """
    random.seed(seed)                          # Python random
    np.random.seed(seed)                       # NumPy random
    torch.manual_seed(seed)                    # PyTorch random (CPU)

    #if torch.cuda.is_available():              # Check if CUDA is available
    #    torch.cuda.manual_seed(seed)           # Set CUDA random seed
    #    torch.cuda.manual_seed_all(seed)       # Set CUDA random seed for all GPUs
    #    torch.backends.cudnn.deterministic = True
    #    torch.backends.cudnn.benchmark = False
    #    print("CUDA is available.")
    #else:
    #    print("CUDA not available.")