import multiprocessing
import os
import torch
import numpy as np

"""Optional variables (performance related - can be omitted)"""

os.environ["TOKENIZERS_PARALLELISM"] = "true"

available_cores = multiprocessing.cpu_count()  # Total cores
performance_cores = 8  # Mac M1 and M2 setup

os.environ["OMP_NUM_THREADS"] = str(performance_cores)
os.environ["OPENBLAS_NUM_THREADS"] = str(performance_cores)
os.environ["MKL_NUM_THREADS"] = str(performance_cores)
os.environ["VECLIB_MAXIMUM_THREADS"] = str(performance_cores)
os.environ["NUMEXPR_NUM_THREADS"] = str(performance_cores)

torch.set_num_threads(performance_cores)
torch.set_num_interop_threads(max(1, performance_cores // 4))  # Dynamic inter-op

print(f"PyTorch uses {torch.get_num_threads()} threads")
print("NumPy config:")
print(np.__config__.show())


"""Required variables"""

USE_LOCAL_LLAMA = True  # Set False to use OpenAI API
OPENAI_MODEL = "gpt-4"
LLAMA_MODEL = "llama3"
TEMPERATURE = 0.2  # Set the temperature for the models
REQUEST_TIMEOUT = 60.0  # Set the request timeout for the models
HUGGINGFACE_EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"

project_root = os.path.dirname(os.path.abspath(__file__))
