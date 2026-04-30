import torch
import time

sizes = [1024, 2048, 4096, 8192, 16384]
device = torch.device('cuda:0')
print(f'GPU 0: {torch.cuda.get_device_name(0)}')

for s in sizes:
    a = torch.randn(s, s, dtype=torch.bfloat16, device=device)
    b = torch.randn(s, s, dtype=torch.bfloat16, device=device)

    for _ in range(5):
        c = torch.mm(a, b)
    torch.cuda.synchronize(device)

    iters = 20
    start = time.time()
    for _ in range(iters):
        c = torch.mm(a, b)
    torch.cuda.synchronize(device)
    elapsed = time.time() - start

    tflops = (2 * s * s * s * iters) / elapsed / 1e12
    print(f'  {s}x{s}: {tflops:.2f} TFLOPS (BF16)')