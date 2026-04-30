import torch
import os

os.environ['PYTORCH_TUNABLEOP_ENABLED'] = '1'
os.environ['PYTORCH_TUNABLEOP_TUNING'] = '1'
os.environ['PYTORCH_TUNABLEOP_MAX_TUNING_DURATION_MS'] = '30000'

torch.backends.cuda.preferred_blas_library('hipblaslt')
device = torch.device('cuda:0')
print(f'GPU: {torch.cuda.get_device_name(0)}')
print('TunableOp: searching for best kernel (this will take a few minutes)...')

m, n, k = 4096, 4096, 65536
a = torch.randn(m, k, dtype=torch.bfloat16, device=device)
b = torch.randn(k, n, dtype=torch.bfloat16, device=device)

for _ in range(30):
    c = torch.mm(a, b)
torch.cuda.synchronize()
print('Tuning complete. Benchmarking...')

iters = 100
start = torch.cuda.Event(enable_timing=True)
end = torch.cuda.Event(enable_timing=True)
start.record()
for _ in range(iters):
    c = torch.mm(a, b)
end.record()
torch.cuda.synchronize()

ms = start.elapsed_time(end)
tflops = (2 * m * n * k * iters) / (ms / 1000) / 1e12
print(f'TunableOp BF16 {m}x{n}x{k}: {tflops:.2f} TFLOPS')