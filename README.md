# Alibaba Tests

##Single node tests

Test 1. Single Card Performance	BF16 Matrix Multiplication

Test 2. Single Card Performance	Qwen2.5-32B Model Training Performance (BF16)

Test 3. Single Card Training Performance	Qwen2.5-32B Model Training Performance (BF16)

Test 4. Single Node Collective Communication	P2P Bandwidth

Test 5. Single Node Collective Communication	RCCL - AllReduce Performance

Test 6. Single Node Collective Communication	RCCL - All2All Performance

Test 7. Single Node Collective Communication	Mori-EP


##Multi-node tests

Test 8. Multi Node Collective Communication	ib_write_bw Test

Test 9. Multi Node Collective Communication	ib_write_bw GDR Test

Test 10. Multi Node Collective Communication	Mori-EP

Test 11. Multi Node Collective Communication	RCCL - AllReduce Bandwidth

Test 12. Multi Node Collective Communication	RCCL - AlltoAll Bandwidth



# Pre-requisite 

Install docker 
```
sudo dnf remove -y podman buildah containers-common

sudo dnf install -y dnf-plugins-core

sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo systemctl enable --now docker

sudo usermod -aG docker $USER

newgrp docker

docker run hello-world #test docker
```

Clone the alibaba repository as below:

```
git clone https://github.com/prasad-nair-amd/alibaba.git
```


# Tests

## Test 1. Single Card Performance	BF16 Matrix Multiplication

```
sudo docker pull prasadnairamd/rocm-tests:latest


docker run --rm   --device=/dev/kfd   --device=/dev/dri   --group-add video   --ipc=host   --network=host   --cap-add=SYS_PTRACE   --security-opt  seccomp=unconfined prasadnairamd/rocm-tests  python3 standard_gem.py 
```

## Test 2. Single Card Performance	Qwen2.5-32B Model Training Performance (BF16)

Access the Qwen_alibaba.tar file : https://drive.google.com/file/d/1UW0TwdFVzXI69cAmeTBG1xEftcRT2JML/view?usp=drive_link

Follow the steps below:
```
$ cd qwen
$ bash set_env
$ cd Training-Benchmark
$ bash  scripts/MI355/perf_test_qwen2.5_32b.sh

# result are under this directory
# ls qwen/Training-Benchmark/third_party/Primus/output

the result file is : log_mp_pretrain_qwen2.5_32B-BF16-pretrain.txt
 
```

## Test 3. Single Card Training Performance	Qwen2.5-32B Model Training Performance (BF16)
Instructions same as Test 2. You can configure the script to make it run on 1 GPU or 8 GPU
Access the Qwen_alibaba.tar file in this repo and untar the file. Follow the steps below:
```
$ cd qwen
$ bash set_env
$ cd Training-Benchmark
$ bash  scripts/MI355/perf_test_qwen2.5_32b.sh

# result are under this directory
# ls qwen/Training-Benchmark/third_party/Primus/output

the result file is : log_mp_pretrain_qwen2.5_32B-BF16-pretrain.txt
 
```
## Test 4. Single Node Collective Communication	P2P Bandwidth
```
git clone https://github.com/prasad-nair-amd/rapido.git
cd rapido
python3 rapido-collect.py -a -m -p -v
# a json file will be generated. Use the json file in the below command
 python3 rapido-report.py -f1 serverinfo_Aliyun.json -o p2p_report.html
# a html report called p2p_report.html is generated . Under the microbenchmaks tab you will see the P2P bandwidth test results
 
```
![P2P Bandwidth Rapido Report](https://raw.githubusercontent.com/prasad-nair-amd/rapido/refs/heads/main/Microbenchmarks.png)
![P2P Bandwidth Rapido Report](https://raw.githubusercontent.com/prasad-nair-amd/rapido/refs/heads/main/p2p_bandwidth.png)

## Test 5. Single Node Collective Communication	RCCL - AllReduce Performance
```
sudo docker pull prasadnairamd/rccl-tests:latest


docker run --rm   --device=/dev/kfd   --device=/dev/dri   --group-add video   --ipc=host   --network=host   --cap-add=SYS_PTRACE   --security-opt  seccomp=unconfined prasadnairamd/rccl-tests   ./build/all_reduce_perf -f 2 -g 8 -b 4 -e 1G

[vultr@Aliyun3 ~]$ docker run --rm   --device=/dev/kfd   --device=/dev/dri   --group-add video   --ipc=host   --network=host   --cap-add=SYS_PTRACE   --security-opt  seccomp=unconfined prasadnairamd/rccl-tests   ./build/all_reduce_perf -f 2 -g 8 -b 4 -e 1G
# rccl-tests version 2.17.9-develop:2596ca5f71 rccl-headers=22803 rccl-library=22707
# Collective test starting: all_reduce_perf
# nThread 1 nGpus 8 minBytes 4 maxBytes 1073741824 step: 2(factor) warmup iters: 1 iters: 20 agg iters: 1 validation: 1 graph: 0
#
# Using devices
#  Rank  0 Group  0 Pid      1 on    Aliyun3 device  0 [0000:05:00] AMD Radeon Graphics
#  Rank  1 Group  0 Pid      1 on    Aliyun3 device  1 [0000:15:00] AMD Radeon Graphics
#  Rank  2 Group  0 Pid      1 on    Aliyun3 device  2 [0000:65:00] AMD Radeon Graphics
#  Rank  3 Group  0 Pid      1 on    Aliyun3 device  3 [0000:75:00] AMD Radeon Graphics
#  Rank  4 Group  0 Pid      1 on    Aliyun3 device  4 [0000:85:00] AMD Radeon Graphics
#  Rank  5 Group  0 Pid      1 on    Aliyun3 device  5 [0000:95:00] AMD Radeon Graphics
#  Rank  6 Group  0 Pid      1 on    Aliyun3 device  6 [0000:e5:00] AMD Radeon Graphics
#  Rank  7 Group  0 Pid      1 on    Aliyun3 device  7 [0000:f5:00] AMD Radeon Graphics
#
#                                                              out-of-place                       in-place
#       size         count      type   redop    root     time   algbw   busbw  #wrong     time   algbw   busbw  #wrong
#        (B)    (elements)                               (us)  (GB/s)  (GB/s)             (us)  (GB/s)  (GB/s)
           4             1     float     sum      -1    42.02    0.00    0.00       0    37.48    0.00    0.00       0
           8             2     float     sum      -1    35.49    0.00    0.00       0    34.42    0.00    0.00       0
          16             4     float     sum      -1    35.80    0.00    0.00       0    34.39    0.00    0.00       0
          32             8     float     sum      -1    35.99    0.00    0.00       0    34.62    0.00    0.00       0
          64            16     float     sum      -1    35.79    0.00    0.00       0    34.45    0.00    0.00       0
         128            32     float     sum      -1    35.83    0.00    0.01       0    34.34    0.00    0.01       0
         256            64     float     sum      -1    35.79    0.01    0.01       0    34.32    0.01    0.01       0
         512           128     float     sum      -1    34.36    0.01    0.03       0    34.48    0.01    0.03       0
        1024           256     float     sum      -1    34.29    0.03    0.05       0    33.52    0.03    0.05       0
        2048           512     float     sum      -1    33.50    0.06    0.11       0    34.73    0.06    0.10       0
        4096          1024     float     sum      -1    32.97    0.12    0.22       0    33.08    0.12    0.22       0
        8192          2048     float     sum      -1    31.98    0.26    0.45       0    33.33    0.25    0.43       0
       16384          4096     float     sum      -1    33.09    0.50    0.87       0    33.20    0.49    0.86       0
       32768          8192     float     sum      -1    32.95    0.99    1.74       0    34.55    0.95    1.66       0
       65536         16384     float     sum      -1    33.44    1.96    3.43       0    32.07    2.04    3.58       0
      131072         32768     float     sum      -1    37.83    3.46    6.06       0    38.94    3.37    5.89       0
      262144         65536     float     sum      -1    38.79    6.76   11.83       0    37.17    7.05   12.34       0
      524288        131072     float     sum      -1    39.01   13.44   23.52       0    41.67   12.58   22.02       0
     1048576        262144     float     sum      -1    37.37   28.06   49.11       0    37.64   27.86   48.75       0
     2097152        524288     float     sum      -1    39.65   52.89   92.55       0    39.43   53.18   93.07       0
     4194304       1048576     float     sum      -1    47.95   87.47  153.07       0    48.54   86.41  151.22       0
     8388608       2097152     float     sum      -1    71.12  117.94  206.40       0    71.13  117.94  206.39       0
    16777216       4194304     float     sum      -1   116.74  143.71  251.49       0   118.08  142.08  248.64       0
    33554432       8388608     float     sum      -1   183.45  182.91  320.09       0   182.32  184.04  322.07       0
    67108864      16777216     float     sum      -1   324.09  207.07  362.37       0   323.75  207.29  362.76       0
   134217728      33554432     float     sum      -1   611.47  219.50  384.13       0   611.59  219.46  384.05       0
   268435456      67108864     float     sum      -1  1188.45  225.87  395.27       0  1190.90  225.41  394.46       0
   536870912     134217728     float     sum      -1  2351.27  228.33  399.58       0  2347.45  228.70  400.23       0
  1073741824     268435456     float     sum      -1  4667.81  230.03  402.55       0  4675.42  229.66  401.90       0

# Out of bounds values : 0 OK
# Avg bus bandwidth    : 105.615
#
# Collective test concluded: all_reduce_perf

```

## Test 6. Single Node Collective Communication	RCCL - All2All Performance
```
sudo docker pull prasadnairamd/rccl-tests:latest


docker run --rm   --device=/dev/kfd   --device=/dev/dri   --group-add video   --ipc=host   --network=host   --cap-add=SYS_PTRACE   --security-opt  seccomp=unconfined prasadnairamd/rccl-tests   ./build/alltoall_perf -b 8 -e 128M -f 2 -g 8

[vultr@Aliyun3 ~]$ docker run --rm   --device=/dev/kfd   --device=/dev/dri   --group-add video   --ipc=host   --network=host   --cap-add=SYS_PTRACE   --security-opt  seccomp=unconfined prasadnairamd/rccl-tests   ./build/alltoall_perf -b 8 -e 128M -f 2 -g 8
# rccl-tests version 2.17.9-develop:2596ca5f71 rccl-headers=22803 rccl-library=22707
# Collective test starting: alltoall_perf
# nThread 1 nGpus 8 minBytes 8 maxBytes 134217728 step: 2(factor) warmup iters: 1 iters: 20 agg iters: 1 validation: 1 graph: 0
#
# Using devices
#  Rank  0 Group  0 Pid      1 on    Aliyun3 device  0 [0000:05:00] AMD Radeon Graphics
#  Rank  1 Group  0 Pid      1 on    Aliyun3 device  1 [0000:15:00] AMD Radeon Graphics
#  Rank  2 Group  0 Pid      1 on    Aliyun3 device  2 [0000:65:00] AMD Radeon Graphics
#  Rank  3 Group  0 Pid      1 on    Aliyun3 device  3 [0000:75:00] AMD Radeon Graphics
#  Rank  4 Group  0 Pid      1 on    Aliyun3 device  4 [0000:85:00] AMD Radeon Graphics
#  Rank  5 Group  0 Pid      1 on    Aliyun3 device  5 [0000:95:00] AMD Radeon Graphics
#  Rank  6 Group  0 Pid      1 on    Aliyun3 device  6 [0000:e5:00] AMD Radeon Graphics
#  Rank  7 Group  0 Pid      1 on    Aliyun3 device  7 [0000:f5:00] AMD Radeon Graphics
#
#                                                              out-of-place                       in-place
#       size         count      type   redop    root     time   algbw   busbw  #wrong     time   algbw   busbw  #wrong
#        (B)    (elements)                               (us)  (GB/s)  (GB/s)             (us)  (GB/s)  (GB/s)
           0             0     float    none      -1     0.94    0.00    0.00       0     0.76    0.00    0.00    N/A
           0             0     float    none      -1     0.73    0.00    0.00       0     0.72    0.00    0.00    N/A
           0             0     float    none      -1     0.79    0.00    0.00       0     0.82    0.00    0.00    N/A
           0             0     float    none      -1     0.72    0.00    0.00       0     0.82    0.00    0.00    N/A
         128             4     float    none      -1    40.87    0.00    0.00       0    59.46    0.00    0.00    N/A
         256             8     float    none      -1    30.80    0.01    0.01       0    47.19    0.01    0.00    N/A
         512            16     float    none      -1    31.13    0.02    0.01       0    47.45    0.01    0.01    N/A
        1024            32     float    none      -1    29.83    0.03    0.03       0    46.95    0.02    0.02    N/A
        2048            64     float    none      -1    29.78    0.07    0.06       0    48.13    0.04    0.04    N/A
        4096           128     float    none      -1    30.82    0.13    0.12       0    46.50    0.09    0.08    N/A
        8192           256     float    none      -1    29.89    0.27    0.24       0    46.53    0.18    0.15    N/A
       16384           512     float    none      -1    33.01    0.50    0.43       0    47.67    0.34    0.30    N/A
       32768          1024     float    none      -1    32.79    1.00    0.87       0    47.85    0.68    0.60    N/A
       65536          2048     float    none      -1    32.40    2.02    1.77       0    50.74    1.29    1.13    N/A
      131072          4096     float    none      -1    31.57    4.15    3.63       0    51.60    2.54    2.22    N/A
      262144          8192     float    none      -1    37.49    6.99    6.12       0    57.08    4.59    4.02    N/A
      524288         16384     float    none      -1    36.50   14.36   12.57       0    57.38    9.14    8.00    N/A
     1048576         32768     float    none      -1    37.45   28.00   24.50       0    49.02   21.39   18.72    N/A
     2097152         65536     float    none      -1    37.20   56.38   49.33       0    53.73   39.03   34.15    N/A
     4194304        131072     float    none      -1    36.10  116.17  101.65       0    57.70   72.69   63.61    N/A
     8388608        262144     float    none      -1    38.98  215.23  188.32       0    58.33  143.80  125.83    N/A
    16777216        524288     float    none      -1    59.45  282.19  246.91       0    62.17  269.87  236.14    N/A
    33554432       1048576     float    none      -1   101.79  329.63  288.43       0   109.36  306.83  268.48    N/A
    67108864       2097152     float    none      -1   196.69  341.19  298.54       0   199.69  336.06  294.05    N/A
   134217728       4194304     float    none      -1   364.47  368.25  322.22       0   371.15  361.62  316.42    N/A
# Out of bounds values : 0 OK
# Avg bus bandwidth    : 58.3947
#
# Collective test concluded: alltoall_perf
#


```

## Test 7. Single Node Collective Communication	Mori-EP
```
$ ./run_intra_mori.sh

------------------------------------------------------------
[Gloo] Rank 0 is connected to 7 peer ranks. Expected number of connected peer ranks is : 7
[Gloo] Rank 1 is connected to 7 peer ranks. Expected number of connected peer ranks is : 7
[Gloo] Rank 2 is connected to 7 peer ranks. Expected number of connected peer ranks is : 7
[Gloo] Rank 3 is connected to 7 peer ranks. Expected number of connected peer ranks is : 7
[Gloo] Rank 4 is connected to 7 peer ranks. Expected number of connected peer ranks is : 7
[Gloo] Rank 5 is connected to 7 peer ranks. Expected number of connected peer ranks is : 7
[Gloo] Rank 7 is connected to 7 peer ranks. Expected number of connected peer ranks is : 7
[Gloo] Rank 6 is connected to 7 peer ranks. Expected number of connected peer ranks is : 7

============================================================
Benchmarking with dispatch_block_num=80, dispatch_warp_per_block=16 combine_block_num=80, combine_warp_per_block=4
============================================================
Dispatch result:
Round 0 duration(us) [848.5, 846.1, 846.5, 847.7, 849.3, 850.2, 845.9, 848.4] bandwidth(GB/s) [366.52, 366.96, 365.92, 366.6, 366.38, 365.73, 367.83, 365.4] avg bytes(MB) 296.27 lat 847.8 bw 366.42 / 553.46
Round 1 duration(us) [848.9, 847.0, 848.3, 851.5, 849.9, 851.5, 847.5, 849.3] bandwidth(GB/s) [366.37, 366.59, 365.14, 364.96, 366.14, 365.17, 367.16, 365.01] avg bytes(MB) 296.27 lat 849.2 bw 365.82 / 552.55
Round 2 duration(us) [848.3, 848.1, 848.5, 849.8, 849.8, 851.0, 847.5, 849.9] bandwidth(GB/s) [366.61, 366.11, 365.06, 365.69, 366.19, 365.36, 367.15, 364.77] avg bytes(MB) 296.27 lat 849.1 bw 365.87 / 552.63
Round 3 duration(us) [843.0, 841.0, 842.4, 842.1, 843.8, 843.1, 842.3, 843.5] bandwidth(GB/s) [368.94, 369.21, 367.72, 369.0, 368.79, 368.82, 369.4, 367.51] avg bytes(MB) 296.27 lat 842.7 bw 368.67 / 556.87
Round 4 duration(us) [849.5, 847.4, 849.5, 849.9, 849.6, 851.9, 847.9, 851.0] bandwidth(GB/s) [366.1, 366.38, 364.66, 365.61, 366.25, 364.99, 366.96, 364.3] avg bytes(MB) 296.27 lat 849.6 bw 365.66 / 552.31
Round 5 duration(us) [846.3, 845.4, 845.1, 848.7, 846.5, 848.9, 847.1, 848.1] bandwidth(GB/s) [367.5, 367.28, 366.52, 366.16, 367.6, 366.28, 367.33, 365.55] avg bytes(MB) 296.27 lat 847.0 bw 366.78 / 554.00
Round 6 duration(us) [850.4, 848.0, 850.8, 850.4, 851.1, 853.4, 849.9, 850.7] bandwidth(GB/s) [365.71, 366.12, 364.07, 365.41, 365.6, 364.36, 366.1, 364.44] avg bytes(MB) 296.27 lat 850.6 bw 365.23 / 551.66
Round 7 duration(us) [848.2, 847.6, 847.5, 848.9, 849.2, 849.9, 846.9, 849.5] bandwidth(GB/s) [366.68, 366.3, 365.48, 366.06, 366.44, 365.83, 367.43, 364.93] avg bytes(MB) 296.27 lat 848.5 bw 366.14 / 553.05
Round 8 duration(us) [845.5, 845.3, 845.7, 846.6, 848.1, 847.8, 845.2, 847.0] bandwidth(GB/s) [367.83, 367.33, 366.28, 367.07, 366.9, 366.76, 368.14, 366.0] avg bytes(MB) 296.27 lat 846.4 bw 367.04 / 554.40
Round 9 duration(us) [848.6, 845.6, 846.5, 848.1, 848.5, 850.1, 846.0, 850.0] bandwidth(GB/s) [366.49, 367.19, 365.92, 366.42, 366.74, 365.74, 367.79, 364.7] avg bytes(MB) 296.27 lat 847.9 bw 366.37 / 553.39

Combine result:
Round 0 duration(us) [808.7, 810.0, 810.3, 808.6, 807.2, 806.8, 810.4, 808.1] bandwidth(GB/s) [384.56, 383.3, 382.3, 384.29, 385.51, 385.41, 383.95, 383.63] avg bytes(MB) 296.27 lat 808.8 bw 384.12 / 580.20
Round 1 duration(us) [809.5, 810.8, 809.5, 806.8, 807.9, 806.1, 810.8, 808.0] bandwidth(GB/s) [384.19, 382.95, 382.67, 385.16, 385.15, 385.74, 383.77, 383.68] avg bytes(MB) 296.27 lat 808.7 bw 384.16 / 580.27
Round 2 duration(us) [809.1, 808.9, 808.5, 808.0, 807.4, 805.9, 809.5, 807.4] bandwidth(GB/s) [384.41, 383.85, 383.14, 384.57, 385.4, 385.82, 384.38, 383.96] avg bytes(MB) 296.27 lat 808.1 bw 384.44 / 580.68
Round 3 duration(us) [808.9, 811.0, 808.7, 809.6, 808.1, 808.2, 808.5, 807.1] bandwidth(GB/s) [384.46, 382.86, 383.05, 383.84, 385.09, 384.74, 384.86, 384.11] avg bytes(MB) 296.27 lat 808.8 bw 384.13 / 580.21
Round 4 duration(us) [808.6, 810.0, 808.5, 808.9, 808.6, 805.2, 809.9, 807.0] bandwidth(GB/s) [384.64, 383.33, 383.15, 384.17, 384.83, 386.16, 384.18, 384.17] avg bytes(MB) 296.27 lat 808.3 bw 384.33 / 580.51
Round 5 duration(us) [808.7, 809.9, 809.7, 806.2, 808.1, 805.9, 808.1, 807.4] bandwidth(GB/s) [384.58, 383.34, 382.55, 385.43, 385.08, 385.8, 385.06, 383.97] avg bytes(MB) 296.27 lat 808.0 bw 384.48 / 580.74
Round 6 duration(us) [808.1, 810.4, 807.4, 807.6, 807.6, 805.4, 809.0, 808.0] bandwidth(GB/s) [384.88, 383.12, 383.63, 384.77, 385.32, 386.08, 384.61, 383.68] avg bytes(MB) 296.27 lat 807.9 bw 384.51 / 580.79
Round 7 duration(us) [809.3, 809.8, 810.4, 808.5, 808.0, 807.2, 810.8, 807.4] bandwidth(GB/s) [384.27, 383.42, 382.25, 384.34, 385.14, 385.18, 383.78, 383.95] avg bytes(MB) 296.27 lat 808.9 bw 384.04 / 580.08
Round 8 duration(us) [809.1, 810.0, 809.4, 808.6, 806.9, 806.8, 809.8, 808.2] bandwidth(GB/s) [384.39, 383.3, 382.69, 384.32, 385.66, 385.4, 384.27, 383.6] avg bytes(MB) 296.27 lat 808.6 bw 384.20 / 580.33
Round 9 duration(us) [808.1, 811.4, 810.2, 808.3, 807.8, 806.3, 810.2, 806.0] bandwidth(GB/s) [384.84, 382.67, 382.34, 384.43, 385.2, 385.62, 384.04, 384.62] avg bytes(MB) 296.27 lat 808.5 bw 384.22 / 580.35

End-to-end result:
Note: e2e is one full-graph replay; separate results use two graph replays, so sep total is usually higher.
Round 0 e2e(us) [1632.8, 1633.1, 1632.9, 1633.2, 1633.0, 1633.1, 1633.6, 1633.3]
Round 1 e2e(us) [1635.2, 1634.1, 1634.1, 1633.8, 1634.1, 1633.7, 1634.4, 1634.2]
Round 2 e2e(us) [1636.9, 1637.8, 1637.1, 1637.0, 1637.3, 1636.8, 1637.7, 1637.0]
Round 3 e2e(us) [1633.2, 1633.3, 1633.7, 1633.2, 1633.1, 1633.1, 1633.5, 1633.1]
Round 4 e2e(us) [1632.9, 1633.5, 1633.1, 1632.5, 1633.0, 1632.7, 1633.1, 1633.0]
Round 5 e2e(us) [1634.2, 1634.2, 1633.6, 1633.4, 1633.7, 1633.0, 1633.9, 1633.9]
Round 6 e2e(us) [1636.1, 1635.7, 1636.5, 1635.8, 1636.4, 1635.6, 1636.0, 1636.2]
Round 7 e2e(us) [1635.3, 1635.5, 1635.2, 1635.5, 1635.3, 1634.8, 1635.4, 1635.3]
Round 8 e2e(us) [1636.4, 1636.1, 1636.2, 1636.6, 1636.9, 1636.0, 1636.7, 1636.3]
Round 9 e2e(us) [1639.5, 1639.0, 1638.7, 1639.1, 1638.8, 1638.6, 1638.7, 1639.4]
Stop amd rm the docker mori
mori



```
## Test 8. Multi Node Collective Communication	ib_write_bw Test

For running IB bandwidth test you should first find the mapping of rdma interfaces between two nodes. 
You can refer to the document ![Alinux RDMA Guide.docx](https://github.com/prasad-nair-amd/alibaba/raw/refs/heads/main/Alinux%20RDMA%20Guide.docx) in the repo for running the test in parallel. 
You can use the script provided in the repo (ionic_mapping.sh) to findout the mapping of rdma interfaces.

In the below example ionic_7 interface is mapped to ionic_1

```


[vultr@Aliyun1 ~]$ sudo ib_write_bw -d ionic_7 -x 1 -b -q 4 -F -a -n 5000 --report_gbits -p 10000 &
[1] 650300
[vultr@Aliyun1 ~]$ Using sampled CPU speed 3295 MHz over reported speed 5037 MHz

************************************
* Waiting for client to connect... *
************************************
Connected: Thu Apr 16 05:49:19 2026

---------------------------------------------------------------------------------------
                    RDMA_Write Bidirectional BW Test
 Dual-port       : OFF          Device         : ionic_7
 Number of qps   : 4            Transport type : IB
 Connection type : RC           Using SRQ      : OFF
 PCIe relax order: ON           Lock-free      : OFF
 ibv_wr* API     : OFF          Using DDP      : OFF
 TX depth        : 128
 CQ Moderation   : 100
 CQE Poll Batch  : 16
 Mtu             : 4096[B]
 Link type       : Ethernet
 CPU freq        : 3295[MHz]
 GID index       : 1
 Max inline data : 0[B]
 rdma_cm QPs     : OFF
 Data ex. method : Ethernet
---------------------------------------------------------------------------------------
 local address: LID 0000 QPN 0x0800 PSN 0x9755de RKey 0x00012d VAddr 0x007f5eff13f000
 GID: 253:147:22:211:89:182:01:80:158:08:58:179:95:199:124:202
 local address: LID 0000 QPN 0x0002 PSN 0x46d70 RKey 0x00012d VAddr 0x007f5eff93f000
 GID: 253:147:22:211:89:182:01:80:158:08:58:179:95:199:124:202
 local address: LID 0000 QPN 0x0801 PSN 0xe6b9fa RKey 0x00012d VAddr 0x007f5f0013f000
 GID: 253:147:22:211:89:182:01:80:158:08:58:179:95:199:124:202
 local address: LID 0000 QPN 0x0003 PSN 0xf26ac1 RKey 0x00012d VAddr 0x007f5f0093f000
 GID: 253:147:22:211:89:182:01:80:158:08:58:179:95:199:124:202
 remote address: LID 0000 QPN 0x0800 PSN 0x551dbe RKey 0x000143 VAddr 0x007fb3debff000
 GID: 253:147:22:211:89:182:01:80:06:144:129:255:254:54:91:176
 remote address: LID 0000 QPN 0x0002 PSN 0xe5c7d0 RKey 0x000143 VAddr 0x007fb3df3ff000
 GID: 253:147:22:211:89:182:01:80:06:144:129:255:254:54:91:176
 remote address: LID 0000 QPN 0x0801 PSN 0x8c74da RKey 0x000143 VAddr 0x007fb3dfbff000
 GID: 253:147:22:211:89:182:01:80:06:144:129:255:254:54:91:176
 remote address: LID 0000 QPN 0x0003 PSN 0xe83c21 RKey 0x000143 VAddr 0x007fb3e03ff000
 GID: 253:147:22:211:89:182:01:80:06:144:129:255:254:54:91:176
---------------------------------------------------------------------------------------
 #bytes     #iterations    BW peak[Gb/sec]    BW average[Gb/sec]   MsgRate[Mpps]
 2          20000           0.147331            0.146472            9.154486
 4          20000            0.30               0.30                 9.239950
 8          20000            0.60               0.59                 9.224424
 16         20000            1.20               1.18                 9.235043
 32         20000            1.94               1.92                 7.496597
 64         20000            3.87               3.84                 7.499745
 128        20000            7.75               7.69                 7.506438
 256        20000            15.52              15.40                7.520808
 512        20000            31.04              30.79                7.516752
 1024       20000            60.78              60.26                7.356253
 2048       20000            123.25             122.10               7.452446
 4096       20000            246.35             243.94               7.444587
 8192       20000            485.25             481.20               7.342513
 16384      20000            773.59             773.21               5.899086
 32768      20000            776.90             776.75               2.963059
 65536      20000            775.85             775.03               1.478245
 131072     20000            777.86             777.81               0.741774
 262144     20000            778.50             778.47               0.371202
 524288     20000            778.95             778.93               0.185712
 1048576    20000            779.09             779.08               0.092874
 2097152    20000            779.16             779.16               0.046441
 4194304    20000            779.16             779.16               0.023221
 8388608    20000            779.21             779.21               0.011611
---------------------------------------------------------------------------------------
Completed: Thu Apr 16 05:49:32 2026

Total run time: 187.693s

[1]+  Done                    sudo ib_write_bw -d ionic_7 -x 1 -b -q 4 -F -a -n 5000 --report_gbits -p 10000

<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
[vultr@Aliyun3 ~]$ sudo ib_write_bw -d ionic_1 -x 1 -b -q 4 -F -a -n 5000 --report_gbits -p 10000 66.42.116.72
---------------------------------------------------------------------------------------
                    RDMA_Write Bidirectional BW Test
 Dual-port       : OFF          Device         : ionic_1
 Number of qps   : 4            Transport type : IB
 Connection type : RC           Using SRQ      : OFF
 PCIe relax order: ON           Lock-free      : OFF
 ibv_wr* API     : OFF          Using Enhanced Reorder      : OFF
 TX depth        : 128
 CQ Moderation   : 100
 CQE Poll Batch  : Dynamic
 Mtu             : 4096[B]
 Link type       : Ethernet
 GID index       : 1
 Max inline data : 0[B]
 rdma_cm QPs     : OFF
 Data ex. method : Ethernet
---------------------------------------------------------------------------------------
 local address: LID 0000 QPN 0x0800 PSN 0x551dbe RKey 0x000143 VAddr 0x007fb3debff000
 GID: 253:147:22:211:89:182:01:80:06:144:129:255:254:54:91:176
 local address: LID 0000 QPN 0x0002 PSN 0xe5c7d0 RKey 0x000143 VAddr 0x007fb3df3ff000
 GID: 253:147:22:211:89:182:01:80:06:144:129:255:254:54:91:176
 local address: LID 0000 QPN 0x0801 PSN 0x8c74da RKey 0x000143 VAddr 0x007fb3dfbff000
 GID: 253:147:22:211:89:182:01:80:06:144:129:255:254:54:91:176
 local address: LID 0000 QPN 0x0003 PSN 0xe83c21 RKey 0x000143 VAddr 0x007fb3e03ff000
 GID: 253:147:22:211:89:182:01:80:06:144:129:255:254:54:91:176
 remote address: LID 0000 QPN 0x0800 PSN 0x9755de RKey 0x00012d VAddr 0x007f5eff13f000
 GID: 253:147:22:211:89:182:01:80:158:08:58:179:95:199:124:202
 remote address: LID 0000 QPN 0x0002 PSN 0x46d70 RKey 0x00012d VAddr 0x007f5eff93f000
 GID: 253:147:22:211:89:182:01:80:158:08:58:179:95:199:124:202
 remote address: LID 0000 QPN 0x0801 PSN 0xe6b9fa RKey 0x00012d VAddr 0x007f5f0013f000
 GID: 253:147:22:211:89:182:01:80:158:08:58:179:95:199:124:202
 remote address: LID 0000 QPN 0x0003 PSN 0xf26ac1 RKey 0x00012d VAddr 0x007f5f0093f000
 GID: 253:147:22:211:89:182:01:80:158:08:58:179:95:199:124:202
---------------------------------------------------------------------------------------
 #bytes     #iterations    BW peak[Gb/sec]    BW average[Gb/sec]   MsgRate[Mpps]
 2          20000           0.147331            0.146472            9.154486
 4          20000            0.30               0.30                 9.239950
 8          20000            0.60               0.59                 9.224424
 16         20000            1.20               1.18                 9.235043
 32         20000            1.94               1.92                 7.496597
 64         20000            3.87               3.84                 7.499745
 128        20000            7.75               7.69                 7.506438
 256        20000            15.52              15.40                7.520808
 512        20000            31.04              30.79                7.516752
 1024       20000            60.78              60.26                7.356253
 2048       20000            123.25             122.10               7.452446
 4096       20000            246.35             243.94               7.444587
 8192       20000            485.25             481.20               7.342513
 16384      20000            773.59             773.21               5.899086
 32768      20000            776.90             776.75               2.963059
 65536      20000            775.85             775.03               1.478245
 131072     20000            777.86             777.81               0.741774
 262144     20000            778.50             778.47               0.371202
 524288     20000            778.95             778.93               0.185712
 1048576    20000            779.09             779.08               0.092874
 2097152    20000            779.16             779.16               0.046441
 4194304    20000            779.16             779.16               0.023221
 8388608    20000            779.21             779.21               0.011611
---------------------------------------------------------------------------------------




```

## Test 9. Multi Node Collective Communication	ib_write_bw GDR Test

Download the AINIC driver package file from here : [AI NIC driver package](https://drive.google.com/file/d/1ZUF1ecHVYp85xjiF5jR72UHdo8hzXTKA/view?usp=drive_link)

Testing GPUDirect RDMA (GDR) on AMD GPUs using ib_write_bw requires building the perftest package with ROCm support to enable direct memory access between the InfiniBand/RoCE NIC and AMD GPU memory, bypassing the CPU. 


1. Build Perftest for AMD ROCm 
You must compile perftest with ROCm enabled.
Navigate to the driver directory:

bash
tar -xvf ainic_bundle_1.117.5-a-82.tar.gz
cd ainic_bundle_1.117.5-a-82/host_sw_pkg/ionic_driver/src/drivers-linux/perftest

Configure and build:
bash
./autogen.sh
./configure --prefix=`pwd` --enable-rocm --with-rocm=/opt/rocm
make
sudo make install

Verify installation:
Run ib_write_bw -h and check for the --use_rocm flag. 

2. Prepare the System
Load ib_peer_mem: Ensure the kernel module is loaded to allow IB devices to access ROCm memory.

bash
lsmod | grep ib_peer_mem
Enable P2P/Disable ACS: Ensure the NIC and GPU are on the same PCIe bridge and that PCIe Access Control Services (ACS) are disabled to allow Peer-to-Peer (P2P) traffic. 

3. Running the Test

Server Node:
bash


-d is the IB device (e.g., mlx5_0), -a is bidirectional, --use_rocm allows GPU
./ib_write_bw -d <ib_device> --use_rocm=<gpu_id> -a
for example : ./ib_write_bw -d ionic_1 -i 1 -F -x 1 -q 4 --tclass 104 -a --report_gbits -b -p 5001 --use_rocm=1

Client Node:
bash
./ib_write_bw -d <ib_device> --use_rocm=<gpu_id> -a <server_ip>
for example : ./ib_write_bw -d ionic_1 -i 1 -F -x 1 -q 4 --tclass 104 -a --report_gbits -b -p 5001 --use_rocm=1 66.42.116.72
Optional - DMABUF: If using a modern ROCm setup (e.g., MI300X), you can use --enable-rocm-dmabuf during configure and add --use_rocm_dmabuf to your run command for improved performance. 


``` 
Server-side example :
[vultr@Aliyun1 perftest]$ ./ib_write_bw -d ionic_1 -i 1 -F -x 1 -q 4 --tclass 104 -a --report_gbits -b -p 5001 --use_rocm=1
Using sampled CPU speed 3295 MHz over reported speed 5008 MHz

************************************
* Waiting for client to connect... *
************************************
Connected: Thu Apr 23 01:20:55 2026

Using ROCm Device with ID: 1, Name: AMD Instinct MI355X, PCI Bus ID: 0x15, GCN Arch: gfx950:sramecc+:xnack-
allocated 67108864 bytes of GPU buffer at 0x7f9c1ee00000
---------------------------------------------------------------------------------------
                    RDMA_Write Bidirectional BW Test
 Dual-port       : OFF          Device         : ionic_1
 Number of qps   : 4            Transport type : IB
 Connection type : RC           Using SRQ      : OFF
 PCIe relax order: ON           Lock-free      : OFF
 ibv_wr* API     : OFF          Using DDP      : OFF
 TX depth        : 128
 CQ Moderation   : 100
 CQE Poll Batch  : 16
 Mtu             : 4096[B]
 Link type       : Ethernet
 CPU freq        : 3295[MHz]
 GID index       : 1
 Max inline data : 0[B]
 rdma_cm QPs     : OFF
 Use ROCm memory : ON
 Data ex. method : Ethernet
---------------------------------------------------------------------------------------
 local address: LID 0000 QPN 0x0800 PSN 0x2cf9f2 RKey 0x0001de VAddr 0x007f9c20e00000
 GID: 253:147:22:211:89:182:01:79:06:144:129:255:254:58:54:80
 local address: LID 0000 QPN 0x0002 PSN 0x9541f4 RKey 0x0001de VAddr 0x007f9c21600000
 GID: 253:147:22:211:89:182:01:79:06:144:129:255:254:58:54:80
 local address: LID 0000 QPN 0x0801 PSN 0x2fce2e RKey 0x0001de VAddr 0x007f9c21e00000
 GID: 253:147:22:211:89:182:01:79:06:144:129:255:254:58:54:80
 local address: LID 0000 QPN 0x0003 PSN 0x26bce5 RKey 0x0001de VAddr 0x007f9c22600000
 GID: 253:147:22:211:89:182:01:79:06:144:129:255:254:58:54:80
 remote address: LID 0000 QPN 0x0002 PSN 0x9b98a6 RKey 0x0001ee VAddr 0x007f50a4e00000
 GID: 253:147:22:211:89:182:01:77:06:144:129:255:254:54:177:120
 remote address: LID 0000 QPN 0x0800 PSN 0x348c98 RKey 0x0001ee VAddr 0x007f50a5600000
 GID: 253:147:22:211:89:182:01:77:06:144:129:255:254:54:177:120
 remote address: LID 0000 QPN 0x0003 PSN 0x41ee02 RKey 0x0001ee VAddr 0x007f50a5e00000
 GID: 253:147:22:211:89:182:01:77:06:144:129:255:254:54:177:120
 remote address: LID 0000 QPN 0x0801 PSN 0xe6c229 RKey 0x0001ee VAddr 0x007f50a6600000
 GID: 253:147:22:211:89:182:01:77:06:144:129:255:254:54:177:120
---------------------------------------------------------------------------------------
 #bytes     #iterations    BW peak[Gb/sec]    BW average[Gb/sec]   MsgRate[Mpps]
 2          20000           0.147580            0.146905            9.181552
 4          20000            0.30               0.30                 9.255260
 8          20000            0.60               0.59                 9.264019
 16         20000            1.19               1.19                 9.287408
 32         20000            2.38               2.37                 9.265968
 64         20000            4.78               4.76                 9.295219
 128        20000            9.52               9.49                 9.272243
 256        20000            19.05              18.99                9.270065
 512        20000            38.15              38.05                9.288649
 1024       20000            76.14              75.39                9.202821
 2048       20000            151.97             150.88               9.209194
 4096       20000            302.87             301.83               9.211057
 8192       20000            600.97             577.28               8.808607
 16384      20000            681.23             673.94               5.141754
 32768      20000            684.39             682.26               2.602598
 65536      20000            688.00             687.41               1.311139
 131072     20000            689.06             688.63               0.656726
 262144     20000            693.30             692.89               0.330395
 524288     20000            695.82             695.40               0.165796
 1048576    20000            697.11             696.64               0.083045
 2097152    20000            697.43             696.98               0.041543
 4194304    20000            697.87             697.42               0.020785
 8388608    20000            698.41             697.97               0.010401
---------------------------------------------------------------------------------------
Completed: Thu Apr 23 01:21:05 2026

Total run time: 98.662s
deallocating GPU buffer 0x7f9c1ee00000



<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
Client-side example :
[vultr@Aliyun3 perftest]$ ./ib_write_bw -d ionic_1 -i 1 -F -x 1 -q 4 --tclass 104 -a --report_gbits -b -p 5001 --use_rocm=1 66.42.116.72
Using sampled CPU speed 3295 MHz over reported speed 5008 MHz
Connected: Thu Apr 23 01:20:55 2026

Using ROCm Device with ID: 1, Name: AMD Instinct MI355X, PCI Bus ID: 0x15, GCN Arch: gfx950:sramecc+:xnack-
allocated 67108864 bytes of GPU buffer at 0x7f50a2e00000
---------------------------------------------------------------------------------------
                    RDMA_Write Bidirectional BW Test
 Dual-port       : OFF          Device         : ionic_1
 Number of qps   : 4            Transport type : IB
 Connection type : RC           Using SRQ      : OFF
 PCIe relax order: ON           Lock-free      : OFF
 ibv_wr* API     : OFF          Using DDP      : OFF
 TX depth        : 128
 CQ Moderation   : 100
 CQE Poll Batch  : 16
 Mtu             : 4096[B]
 Link type       : Ethernet
 CPU freq        : 3295[MHz]
 GID index       : 1
 Max inline data : 0[B]
 rdma_cm QPs     : OFF
 Use ROCm memory : ON
 Data ex. method : Ethernet
---------------------------------------------------------------------------------------
 local address: LID 0000 QPN 0x0002 PSN 0x9b98a6 RKey 0x0001ee VAddr 0x007f50a4e00000
 GID: 253:147:22:211:89:182:01:77:06:144:129:255:254:54:177:120
 local address: LID 0000 QPN 0x0800 PSN 0x348c98 RKey 0x0001ee VAddr 0x007f50a5600000
 GID: 253:147:22:211:89:182:01:77:06:144:129:255:254:54:177:120
 local address: LID 0000 QPN 0x0003 PSN 0x41ee02 RKey 0x0001ee VAddr 0x007f50a5e00000
 GID: 253:147:22:211:89:182:01:77:06:144:129:255:254:54:177:120
 local address: LID 0000 QPN 0x0801 PSN 0xe6c229 RKey 0x0001ee VAddr 0x007f50a6600000
 GID: 253:147:22:211:89:182:01:77:06:144:129:255:254:54:177:120
 remote address: LID 0000 QPN 0x0800 PSN 0x2cf9f2 RKey 0x0001de VAddr 0x007f9c20e00000
 GID: 253:147:22:211:89:182:01:79:06:144:129:255:254:58:54:80
 remote address: LID 0000 QPN 0x0002 PSN 0x9541f4 RKey 0x0001de VAddr 0x007f9c21600000
 GID: 253:147:22:211:89:182:01:79:06:144:129:255:254:58:54:80
 remote address: LID 0000 QPN 0x0801 PSN 0x2fce2e RKey 0x0001de VAddr 0x007f9c21e00000
 GID: 253:147:22:211:89:182:01:79:06:144:129:255:254:58:54:80
 remote address: LID 0000 QPN 0x0003 PSN 0x26bce5 RKey 0x0001de VAddr 0x007f9c22600000
 GID: 253:147:22:211:89:182:01:79:06:144:129:255:254:58:54:80
---------------------------------------------------------------------------------------
 #bytes     #iterations    BW peak[Gb/sec]    BW average[Gb/sec]   MsgRate[Mpps]
 2          20000           0.147580            0.146905            9.181552
 4          20000            0.30               0.30                 9.255260
 8          20000            0.60               0.59                 9.264019
 16         20000            1.19               1.19                 9.287408
 32         20000            2.38               2.37                 9.265968
 64         20000            4.78               4.76                 9.295219
 128        20000            9.52               9.49                 9.272243
 256        20000            19.05              18.99                9.270065
 512        20000            38.15              38.05                9.288649
 1024       20000            76.14              75.39                9.202821
 2048       20000            151.97             150.88               9.209194
 4096       20000            302.87             301.83               9.211057
 8192       20000            600.97             577.28               8.808607
 16384      20000            681.23             673.94               5.141754
 32768      20000            684.39             682.26               2.602598
 65536      20000            688.00             687.41               1.311139
 131072     20000            689.06             688.63               0.656726
 262144     20000            693.30             692.89               0.330395
 524288     20000            695.82             695.40               0.165796
 1048576    20000            697.11             696.64               0.083045
 2097152    20000            697.43             696.98               0.041543
 4194304    20000            697.87             697.42               0.020785
 8388608    20000            698.41             697.97               0.010401
---------------------------------------------------------------------------------------
Completed: Thu Apr 23 01:21:05 2026

Total run time: 10.032s
deallocating GPU buffer 0x7f50a2e00000


```


## Test 10. Multi Node Collective Communication	Mori-EP

For running multinode Mori tests run the script on both nodes simultaneously.

You have to configure the r2.sh file inside the container to set the ip address of remote device. 

$ ./run_inter_mori.sh 
```
+----------------------------------------------------------------------------------------------+
|                               Dispatch Performance (bfloat16)                                |
+---------+-----------------------+-----------------------+---------------------+--------------+
| Metrics | RDMA Bandwidth (GB/s) | XGMI Bandwidth (GB/s) | LL Bandwidth (GB/s) | Latency (us) |
+---------+-----------------------+-----------------------+---------------------+--------------+
|   Best  |          76.1         |         248.88        |        308.6        |   1538.06    |
|  Worst  |          62.8         |         205.11        |        254.33       |   1861.22    |
| Average |          68.4         |         223.75        |        277.45       |    1714.7    |
+---------+-----------------------+-----------------------+---------------------+--------------+
+----------------------------------------------------------------------------------------------+
|                                Combine Performance (bfloat16)                                |
+---------+-----------------------+-----------------------+---------------------+--------------+
| Metrics | RDMA Bandwidth (GB/s) | XGMI Bandwidth (GB/s) | LL Bandwidth (GB/s) | Latency (us) |
+---------+-----------------------+-----------------------+---------------------+--------------+
|   Best  |          77.4         |         253.82        |        314.74       |   1510.17    |
|  Worst  |         64.53         |         210.95        |        261.58       |   1813.62    |
| Average |         70.66         |         231.15        |        286.62       |   1659.39    |
+---------+-----------------------+-----------------------+---------------------+--------------+
```

## Test 11. Multi Node Collective Communication	RCCL - AllReduce Bandwidth

For building the docker clone the below repo. Do this on both the nodes you are trying to run the RCCL multi-node test : 
```
git clone https://github.com/ROCm/rocm-systems.git -b users/atulkulk/mndock
cd /home/vultr/code/rocm-systems/projects/rccl/docker
time GPU_TARGETS="gfx950" python3 -m mnctl --launch-all --nic-type ainic --volume /home/vultr/fjw/drivers-linux:/root/cache/drivers-linux --post-setup post-setup/ --hostfile hostfile --dockerfile Dockerfile.Multinode.ALinux3 --verbose --rebuild 2>&1 | tee blddemo.log
```
How to run ( This step required only on one node, ensure that docker is running on both nodes) 
```
docker exec -it rccl-mn /bin/bash

create a hostfile with following entry
[root@Aliyun3 workspace]# vim hostfile
66.42.116.72 slots=8
45.76.25.46 slots=8

running the test

[root@Aliyun3 workspace]# mpirun --mca btl_tcp_if_include eth1 --mca oob_tcp_if_include eth1 --hostfile hostfile -np 16 --allow-run-as-root -x NCCL_SOCKET_IFNAME=eth1 -x NCCL_IB_GID_INDEX=1 -x NCCL_GDR_FLUSH_DISABLE=1  -x NCCL_GDRCOPY_ENABLE=0 -x NCCL_IB_HCA=ionic_0,ionic_1,ionic_2,ionic_3,ionic_4,ionic_5,ionic_6,ionic_7 --mca btl ^vader,openib -x NCCL_IB_QPS_PER_CONNECTION=2 -x NCCL_IB_TC=104 -x NCCL_IB_FIFO_TC=184  -x NCCL_IGNORE_CPU_AFFINITY=1  -x NCCL_DEBUG=VERSION -x NET_OPTIONAL_RECV_COMPLETION=1  -x HSA_NO_SCRATCH_RECLAIM=1 -x RCCL_GDR_FLUSH_GPU_MEM_NO_RELAXED_ORDERING=0 -x NCCL_TOPO_DUMP_FILE=/tmp/system_run2.txt -x NCCL_IB_USE_INLINE=1 -x IONIC_LOCKFREE=all  -x NCCL_PXN_DISABLE=0 /workspace/rocm-systems/projects/rccl-tests/build/all_reduce_perf -b 16 -e 16G -f 2 -g 1 -n 20 -c 1 -w 5
[1776961424.585035] [Aliyun1:3315 :0]          parser.c:2033 UCX  WARN  unused environment variable: UCX_PREFIX
[1776961424.585035] [Aliyun1:3315 :0]          parser.c:2033 UCX  WARN  (set UCX_WARN_UNUSED_ENV_VARS=n to suppress this warning)
[1776961424.640401] [Aliyun1:3316 :0]          parser.c:2033 UCX  WARN  unused environment variable: UCX_PREFIX
[1776961424.640401] [Aliyun1:3316 :0]          parser.c:2033 UCX  WARN  (set UCX_WARN_UNUSED_ENV_VARS=n to suppress this warning)
[1776961424.745584] [Aliyun1:3319 :0]          parser.c:2033 UCX  WARN  unused environment variable: UCX_PREFIX
[1776961424.745584] [Aliyun1:3319 :0]          parser.c:2033 UCX  WARN  (set UCX_WARN_UNUSED_ENV_VARS=n to suppress this warning)
[1776961424.897036] [Aliyun1:3320 :0]          parser.c:2033 UCX  WARN  unused environment variable: UCX_PREFIX
[1776961424.897036] [Aliyun1:3320 :0]          parser.c:2033 UCX  WARN  (set UCX_WARN_UNUSED_ENV_VARS=n to suppress this warning)
[1776961424.970278] [Aliyun1:3317 :0]          parser.c:2033 UCX  WARN  unused environment variable: UCX_PREFIX
[1776961424.970278] [Aliyun1:3317 :0]          parser.c:2033 UCX  WARN  (set UCX_WARN_UNUSED_ENV_VARS=n to suppress this warning)
[1776961424.994705] [Aliyun1:3322 :0]          parser.c:2033 UCX  WARN  unused environment variable: UCX_PREFIX
[1776961424.994705] [Aliyun1:3322 :0]          parser.c:2033 UCX  WARN  (set UCX_WARN_UNUSED_ENV_VARS=n to suppress this warning)
[1776961425.224937] [Aliyun1:3321 :0]          parser.c:2033 UCX  WARN  unused environment variable: UCX_PREFIX
[1776961425.224937] [Aliyun1:3321 :0]          parser.c:2033 UCX  WARN  (set UCX_WARN_UNUSED_ENV_VARS=n to suppress this warning)
[1776961425.239146] [Aliyun1:3318 :0]          parser.c:2033 UCX  WARN  unused environment variable: UCX_PREFIX
[1776961425.239146] [Aliyun1:3318 :0]          parser.c:2033 UCX  WARN  (set UCX_WARN_UNUSED_ENV_VARS=n to suppress this warning)
# rccl-tests version 2.17.9-develop:4a65e8d rccl-headers=22707 rccl-library=22707
# Collective test starting: all_reduce_perf
# nThread 1 nGpus 1 minBytes 16 maxBytes 17179869184 step: 2(factor) warmup iters: 5 iters: 20 agg iters: 1 validation: 1 graph: 0
#
# Using devices
#  Rank  0 Group  0 Pid   3379 on    Aliyun3 device  0 [0000:05:00] AMD Radeon Graphics
#  Rank  1 Group  0 Pid   3380 on    Aliyun3 device  1 [0000:15:00] AMD Radeon Graphics
#  Rank  2 Group  0 Pid   3381 on    Aliyun3 device  2 [0000:65:00] AMD Radeon Graphics
#  Rank  3 Group  0 Pid   3382 on    Aliyun3 device  3 [0000:75:00] AMD Radeon Graphics
#  Rank  4 Group  0 Pid   3383 on    Aliyun3 device  4 [0000:85:00] AMD Radeon Graphics
#  Rank  5 Group  0 Pid   3384 on    Aliyun3 device  5 [0000:95:00] AMD Radeon Graphics
#  Rank  6 Group  0 Pid   3385 on    Aliyun3 device  6 [0000:e5:00] AMD Radeon Graphics
#  Rank  7 Group  0 Pid   3386 on    Aliyun3 device  7 [0000:f5:00] AMD Radeon Graphics
#  Rank  8 Group  0 Pid   3315 on    Aliyun1 device  0 [0000:05:00] AMD Radeon Graphics
#  Rank  9 Group  0 Pid   3316 on    Aliyun1 device  1 [0000:15:00] AMD Radeon Graphics
#  Rank 10 Group  0 Pid   3317 on    Aliyun1 device  2 [0000:65:00] AMD Radeon Graphics
#  Rank 11 Group  0 Pid   3318 on    Aliyun1 device  3 [0000:75:00] AMD Radeon Graphics
#  Rank 12 Group  0 Pid   3319 on    Aliyun1 device  4 [0000:85:00] AMD Radeon Graphics
#  Rank 13 Group  0 Pid   3320 on    Aliyun1 device  5 [0000:95:00] AMD Radeon Graphics
#  Rank 14 Group  0 Pid   3321 on    Aliyun1 device  6 [0000:e5:00] AMD Radeon Graphics
#  Rank 15 Group  0 Pid   3322 on    Aliyun1 device  7 [0000:f5:00] AMD Radeon Graphics
RCCL version : 2.27.7-HEAD:96a25b5
HIP version  : 7.2.53211-671d39a71e
ROCm version : 7.2.2.0-86-671d39a71e
Hostname     : Aliyun3
Librccl path : /opt/rocm/lib/librccl.so.1
#
#                                                              out-of-place                       in-place
#       size         count      type   redop    root     time   algbw   busbw  #wrong     time   algbw   busbw  #wrong
#        (B)    (elements)                               (us)  (GB/s)  (GB/s)             (us)  (GB/s)  (GB/s)
          16             4     float     sum      -1    37.35    0.00    0.00       0    37.32    0.00    0.00       0
          32             8     float     sum      -1    36.56    0.00    0.00       0    37.43    0.00    0.00       0
          64            16     float     sum      -1    37.86    0.00    0.00       0    37.32    0.00    0.00       0
         128            32     float     sum      -1    38.28    0.00    0.01       0    37.73    0.00    0.01       0
         256            64     float     sum      -1    38.51    0.01    0.01       0    37.91    0.01    0.01       0
         512           128     float     sum      -1    38.55    0.01    0.02       0    38.47    0.01    0.02       0
        1024           256     float     sum      -1    42.14    0.02    0.05       0    41.79    0.02    0.05       0
        2048           512     float     sum      -1    44.28    0.05    0.09       0    43.77    0.05    0.09       0
        4096          1024     float     sum      -1    46.88    0.09    0.16       0    46.16    0.09    0.17       0
        8192          2048     float     sum      -1    45.68    0.18    0.34       0    46.13    0.18    0.33       0
       16384          4096     float     sum      -1    46.65    0.35    0.66       0    45.93    0.36    0.67       0
       32768          8192     float     sum      -1    46.68    0.70    1.32       0    46.70    0.70    1.32       0
       65536         16384     float     sum      -1    49.99    1.31    2.46       0    49.59    1.32    2.48       0
      131072         32768     float     sum      -1    51.33    2.55    4.79       0    51.76    2.53    4.75       0
      262144         65536     float     sum      -1    60.19    4.35    8.17       0    59.32    4.42    8.29       0
      524288        131072     float     sum      -1    62.27    8.42   15.79       0    61.64    8.51   15.95       0
     1048576        262144     float     sum      -1    69.03   15.19   28.48       0    68.26   15.36   28.80       0
     2097152        524288     float     sum      -1    76.38   27.46   51.48       0    75.08   27.93   52.37       0
     4194304       1048576     float     sum      -1    88.58   47.35   88.78       0    89.37   46.93   88.00       0
     8388608       2097152     float     sum      -1   110.24   76.09  142.67       0   109.71   76.46  143.36       0
    16777216       4194304     float     sum      -1   177.14   94.71  177.58       0   176.17   95.23  178.56       0
    33554432       8388608     float     sum      -1   262.18  127.98  239.97       0   261.63  128.25  240.47       0
    67108864      16777216     float     sum      -1   439.32  152.76  286.42       0   438.96  152.88  286.65       0
   134217728      33554432     float     sum      -1   860.65  155.95  292.41       0   853.17  157.32  294.97       0
   268435456      67108864     float     sum      -1  1355.74  198.00  371.25       0  1355.29  198.06  371.37       0
   536870912     134217728     float     sum      -1  2668.77  201.17  377.19       0  2668.08  201.22  377.29       0
  1073741824     268435456     float     sum      -1  5302.00  202.52  379.72       0  5287.42  203.07  380.77       0
  2147483648     536870912     float     sum      -1  10580.6  202.96  380.56       0  10563.5  203.29  381.17       0
  4294967296    1073741824     float     sum      -1  21033.4  204.20  382.87       0  21035.3  204.18  382.84       0
  8589934592    2147483648     float     sum      -1  41862.6  205.19  384.74       0  41865.2  205.18  384.71       0
 17179869184    4294967296     float     sum      -1  83456.7  205.85  385.98       0  83462.8  205.84  385.95       0
# Out of bounds values : 0 OK
# Avg bus bandwidth    : 129.28
#
# Collective test concluded: all_reduce_perf


```


## Test 12. Multi Node Collective Communication	RCCL - AlltoAll Bandwidth

For building the docker clone the below repo .  Do this on both the nodes you are trying to run the RCCL multi-node test : 
```
git clone https://github.com/ROCm/rocm-systems.git -b users/atulkulk/mndock
cd /home/vultr/code/rocm-systems/projects/rccl/docker
time GPU_TARGETS="gfx950" python3 -m mnctl --launch-all --nic-type ainic --volume /home/vultr/fjw/drivers-linux:/root/cache/drivers-linux --post-setup post-setup/ --hostfile hostfile --dockerfile Dockerfile.Multinode.ALinux3 --verbose --rebuild 2>&1 | tee blddemo.log
```
How to run ( This step required only on one node, ensure that docker is running on both nodes) 
```
docker exec -it rccl-mn /bin/bash

create a hostfile with following entry
[root@Aliyun3 workspace]# vim hostfile
66.42.116.72 slots=8
45.76.25.46 slots=8

running the test
[root@Aliyun3 workspace]#  mpirun --mca btl_tcp_if_include eth1 --mca oob_tcp_if_include eth1 --hostfile hostfile -np 16 --allow-run-as-root -x NCCL_SOCKET_IFNAME=eth1 -x NCCL_IB_GID_INDEX=1 -x NCCL_GDR_FLUSH_DISABLE=1  -x NCCL_GDRCOPY_ENABLE=0 -x NCCL_IB_HCA=ionic_0,ionic_1,ionic_2,ionic_3,ionic_4,ionic_5,ionic_6,ionic_7 --mca btl ^vader,openib -x NCCL_IB_QPS_PER_CONNECTION=2 -x NCCL_IB_TC=104 -x NCCL_IB_FIFO_TC=184  -x NCCL_IGNORE_CPU_AFFINITY=1  -x NCCL_DEBUG=VERSION -x NET_OPTIONAL_RECV_COMPLETION=1  -x HSA_NO_SCRATCH_RECLAIM=1 -x RCCL_GDR_FLUSH_GPU_MEM_NO_RELAXED_ORDERING=0 -x NCCL_TOPO_DUMP_FILE=/tmp/system_run2.txt -x NCCL_IB_USE_INLINE=1 -x IONIC_LOCKFREE=all  -x NCCL_PXN_DISABLE=0 /workspace/rocm-systems/projects/rccl-tests/build/alltoall_perf -b 16 -e 16G -f 2 -g 1 -n 20 -c 1 -w 5
[1776962610.613053] [Aliyun1:3557 :0]          parser.c:2033 UCX  WARN  unused environment variable: UCX_PREFIX
[1776962610.613053] [Aliyun1:3557 :0]          parser.c:2033 UCX  WARN  (set UCX_WARN_UNUSED_ENV_VARS=n to suppress this warning)
[1776962610.834868] [Aliyun1:3561 :0]          parser.c:2033 UCX  WARN  unused environment variable: UCX_PREFIX
[1776962610.834868] [Aliyun1:3561 :0]          parser.c:2033 UCX  WARN  (set UCX_WARN_UNUSED_ENV_VARS=n to suppress this warning)
[1776962610.887749] [Aliyun1:3556 :0]          parser.c:2033 UCX  WARN  unused environment variable: UCX_PREFIX
[1776962610.887749] [Aliyun1:3556 :0]          parser.c:2033 UCX  WARN  (set UCX_WARN_UNUSED_ENV_VARS=n to suppress this warning)
[1776962610.965610] [Aliyun1:3560 :0]          parser.c:2033 UCX  WARN  unused environment variable: UCX_PREFIX
[1776962610.965610] [Aliyun1:3560 :0]          parser.c:2033 UCX  WARN  (set UCX_WARN_UNUSED_ENV_VARS=n to suppress this warning)
[1776962611.086010] [Aliyun1:3554 :0]          parser.c:2033 UCX  WARN  unused environment variable: UCX_PREFIX
[1776962611.086010] [Aliyun1:3554 :0]          parser.c:2033 UCX  WARN  (set UCX_WARN_UNUSED_ENV_VARS=n to suppress this warning)
[1776962611.100560] [Aliyun1:3555 :0]          parser.c:2033 UCX  WARN  unused environment variable: UCX_PREFIX
[1776962611.100560] [Aliyun1:3555 :0]          parser.c:2033 UCX  WARN  (set UCX_WARN_UNUSED_ENV_VARS=n to suppress this warning)
[1776962611.240006] [Aliyun1:3559 :0]          parser.c:2033 UCX  WARN  unused environment variable: UCX_PREFIX
[1776962611.240006] [Aliyun1:3559 :0]          parser.c:2033 UCX  WARN  (set UCX_WARN_UNUSED_ENV_VARS=n to suppress this warning)
[1776962611.251829] [Aliyun1:3558 :0]          parser.c:2033 UCX  WARN  unused environment variable: UCX_PREFIX
[1776962611.251829] [Aliyun1:3558 :0]          parser.c:2033 UCX  WARN  (set UCX_WARN_UNUSED_ENV_VARS=n to suppress this warning)
# rccl-tests version 2.17.9-develop:4a65e8d rccl-headers=22707 rccl-library=22707
# Collective test starting: alltoall_perf
# nThread 1 nGpus 1 minBytes 16 maxBytes 17179869184 step: 2(factor) warmup iters: 5 iters: 20 agg iters: 1 validation: 1 graph: 0
#
# Using devices
#  Rank  0 Group  0 Pid   3625 on    Aliyun3 device  0 [0000:05:00] AMD Radeon Graphics
#  Rank  1 Group  0 Pid   3626 on    Aliyun3 device  1 [0000:15:00] AMD Radeon Graphics
#  Rank  2 Group  0 Pid   3627 on    Aliyun3 device  2 [0000:65:00] AMD Radeon Graphics
#  Rank  3 Group  0 Pid   3628 on    Aliyun3 device  3 [0000:75:00] AMD Radeon Graphics
#  Rank  4 Group  0 Pid   3629 on    Aliyun3 device  4 [0000:85:00] AMD Radeon Graphics
#  Rank  5 Group  0 Pid   3630 on    Aliyun3 device  5 [0000:95:00] AMD Radeon Graphics
#  Rank  6 Group  0 Pid   3631 on    Aliyun3 device  6 [0000:e5:00] AMD Radeon Graphics
#  Rank  7 Group  0 Pid   3632 on    Aliyun3 device  7 [0000:f5:00] AMD Radeon Graphics
#  Rank  8 Group  0 Pid   3554 on    Aliyun1 device  0 [0000:05:00] AMD Radeon Graphics
#  Rank  9 Group  0 Pid   3555 on    Aliyun1 device  1 [0000:15:00] AMD Radeon Graphics
#  Rank 10 Group  0 Pid   3556 on    Aliyun1 device  2 [0000:65:00] AMD Radeon Graphics
#  Rank 11 Group  0 Pid   3557 on    Aliyun1 device  3 [0000:75:00] AMD Radeon Graphics
#  Rank 12 Group  0 Pid   3558 on    Aliyun1 device  4 [0000:85:00] AMD Radeon Graphics
#  Rank 13 Group  0 Pid   3559 on    Aliyun1 device  5 [0000:95:00] AMD Radeon Graphics
#  Rank 14 Group  0 Pid   3560 on    Aliyun1 device  6 [0000:e5:00] AMD Radeon Graphics
#  Rank 15 Group  0 Pid   3561 on    Aliyun1 device  7 [0000:f5:00] AMD Radeon Graphics
RCCL version : 2.27.7-HEAD:96a25b5
HIP version  : 7.2.53211-671d39a71e
ROCm version : 7.2.2.0-86-671d39a71e
Hostname     : Aliyun3
Librccl path : /opt/rocm/lib/librccl.so.1
#
#                                                              out-of-place                       in-place
#       size         count      type   redop    root     time   algbw   busbw  #wrong     time   algbw   busbw  #wrong
#        (B)    (elements)                               (us)  (GB/s)  (GB/s)             (us)  (GB/s)  (GB/s)
           0             0     float    none      -1     0.06    0.00    0.00       0     0.04    0.00    0.00    N/A
           0             0     float    none      -1     0.04    0.00    0.00       0     0.04    0.00    0.00    N/A
           0             0     float    none      -1     0.04    0.00    0.00       0     0.04    0.00    0.00    N/A
           0             0     float    none      -1     0.04    0.00    0.00       0     0.04    0.00    0.00    N/A
         256             4     float    none      -1    38.61    0.01    0.01       0    37.29    0.01    0.01    N/A
         512             8     float    none      -1    39.15    0.01    0.01       0    37.41    0.01    0.01    N/A
        1024            16     float    none      -1    37.45    0.03    0.03       0    61.84    0.02    0.02    N/A
        2048            32     float    none      -1    37.35    0.05    0.05       0    38.31    0.05    0.05    N/A
        4096            64     float    none      -1    38.75    0.11    0.10       0    37.73    0.11    0.10    N/A
        8192           128     float    none      -1    37.85    0.22    0.20       0    38.77    0.21    0.20    N/A
       16384           256     float    none      -1    34.52    0.47    0.44       0    35.31    0.46    0.44    N/A
       32768           512     float    none      -1    36.62    0.89    0.84       0    35.34    0.93    0.87    N/A
       65536          1024     float    none      -1    36.97    1.77    1.66       0    36.43    1.80    1.69    N/A
      131072          2048     float    none      -1    36.78    3.56    3.34       0    38.77    3.38    3.17    N/A
      262144          4096     float    none      -1    40.67    6.45    6.04       0    40.13    6.53    6.12    N/A
      524288          8192     float    none      -1    45.42   11.54   10.82       0    45.51   11.52   10.80    N/A
     1048576         16384     float    none      -1    54.99   19.07   17.88       0    55.90   18.76   17.59    N/A
     2097152         32768     float    none      -1    66.22   31.67   29.69       0    65.77   31.89   29.89    N/A
     4194304         65536     float    none      -1    87.84   47.75   44.76       0    88.12   47.60   44.62    N/A
     8388608        131072     float    none      -1   160.22   52.36   49.09       0   132.22   63.44   59.48    N/A
    16777216        262144     float    none      -1   223.32   75.13   70.43       0   219.45   76.45   71.67    N/A
    33554432        524288     float    none      -1   401.10   83.66   78.43       0   401.56   83.56   78.34    N/A
    67108864       1048576     float    none      -1   750.95   89.37   83.78       0   750.44   89.43   83.84    N/A
   134217728       2097152     float    none      -1  1449.19   92.62   86.83       0  1449.73   92.58   86.80    N/A
   268435456       4194304     float    none      -1  2884.99   93.05   87.23       0  2866.37   93.65   87.80    N/A
   536870912       8388608     float    none      -1  5711.08   94.01   88.13       0  5708.98   94.04   88.16    N/A
  1073741824      16777216     float    none      -1  11253.5   95.41   89.45       0  11254.5   95.41   89.44    N/A
  2147483648      33554432     float    none      -1  22288.5   96.35   90.33       0  22289.7   96.34   90.32    N/A
  4294967296      67108864     float    none      -1  44361.2   96.82   90.77       0  44361.6   96.82   90.77    N/A
  8589934592     134217728     float    none      -1  88508.6   97.05   90.99       0  88509.2   97.05   90.99    N/A
 17179869184     268435456     float    none      -1   176806   97.17   91.09       0   176804   97.17   91.10    N/A
# Out of bounds values : 0 OK
# Avg bus bandwidth    : 36.0754
#
# Collective test concluded: alltoall_perf




```




