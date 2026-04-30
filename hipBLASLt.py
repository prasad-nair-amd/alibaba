import torch

torch.backends.cuda.preferred_blas_library('hipblaslt')
device = torch.device('cuda:0')
print(f'GPU: {torch.cuda.get_device_name(0)}')

shapes = [
    (16384, 16384, 16384),
    (16384, 16384, 8192),
    (8192, 8192, 32768),
    (32768, 32768, 8192),
    (16384, 32768, 16384),
    (4096, 4096, 65536),
]

for m, n, k in shapes:
    try:
        a = torch.randn(m, k, dtype=torch.bfloat16, device=device)
        b = torch.randn(k, n, dtype=torch.bfloat16, device=device)

        for _ in range(20):
            c = torch.mm(a, b)
        torch.cuda.synchronize()

        iters = 50
        start = torch.cuda.Event(enable_timing=True)
        end = torch.cuda.Event(enable_timing=True)
        start.record()
        for _ in range(iters):
            c = torch.mm(a, b)
        end.record()
        torch.cuda.synchronize()

        ms = start.elapsed_time(end)
        tflops = (2 * m * n * k * iters) / (ms / 1000) / 1e12
        print(f'  {m}x{n}x{k}: {tflops:.2f} TFLOPS')
    except RuntimeError as e:
        print(f'  {m}x{n}x{k}: OOM - {e}')