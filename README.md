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
```

## Test 6. Single Node Collective Communication	RCCL - All2All Performance
```
sudo docker pull prasadnairamd/rccl-tests:latest


docker run --rm   --device=/dev/kfd   --device=/dev/dri   --group-add video   --ipc=host   --network=host   --cap-add=SYS_PTRACE   --security-opt  seccomp=unconfined prasadnairamd/rccl-tests   ./build/alltoall_perf -b 8 -e 128M -f 2 -g 8
```

## Test 7. Single Node Collective Communication	Mori-EP
```
cd Mori
$ ./run_intra_mori.sh
```
## Test 8. Multi Node Collective Communication	ib_write_bw Test
```
[vultr@Aliyun1 ~]$ ib_write_bw -d ionic_0 -q 2 -F -x 1 -a --report_gbits -b -p 5001
Using sampled CPU speed 3295 MHz over reported speed 5008 MHz

************************************
* Waiting for client to connect... *
************************************
Connected: Wed Apr 15 06:09:02 2026

---------------------------------------------------------------------------------------
                    RDMA_Write Bidirectional BW Test
 Dual-port       : OFF          Device         : ionic_0
 Number of qps   : 2            Transport type : IB
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
 local address: LID 0000 QPN 0x0002 PSN 0x151ca RKey 0x000114 VAddr 0x007f87f3823000
 GID: 253:147:22:211:89:182:01:79:119:76:46:183:177:87:149:75
 local address: LID 0000 QPN 0x0800 PSN 0xab8ec RKey 0x000114 VAddr 0x007f87f4023000
 GID: 253:147:22:211:89:182:01:79:119:76:46:183:177:87:149:75
 remote address: LID 0000 QPN 0x0800 PSN 0xe77286 RKey 0x000108 VAddr 0x007ffa301ee000
 GID: 253:147:22:211:89:182:01:74:189:15:59:47:29:252:16:135
 remote address: LID 0000 QPN 0x0002 PSN 0x36042f RKey 0x000108 VAddr 0x007ffa309ee000
 GID: 253:147:22:211:89:182:01:74:189:15:59:47:29:252:16:135
---------------------------------------------------------------------------------------
 #bytes     #iterations    BW peak[Gb/sec]    BW average[Gb/sec]   MsgRate[Mpps]
 2          10000           0.109376            0.109152            6.822015
 4          10000            0.22               0.22                 6.850886
 8          10000            0.44               0.44                 6.817539
 16         10000            0.88               0.88                 6.850112
 32         10000            1.75               1.75                 6.828895
 64         10000            3.49               3.49                 6.816610
 128        10000            7.00               7.00                 6.831384
 256        10000            13.94              13.94                6.805300
 512        10000            28.06              28.04                6.845515
 1024       10000            55.97              55.93                6.827587
 2048       10000            111.21             111.12               6.782249
 4096       10000            221.99             221.80               6.768730
 8192       10000            444.17             443.76               6.771294
 16384      10000            769.07             767.62               5.856500
 32768      10000            774.24             773.75               2.951620
 65536      10000            775.98             774.12               1.476522
 131072     10000            776.89             776.89               0.740901
 262144     10000            777.24             777.22               0.370608
 524288     10000            778.53             778.09               0.185510
 1048576    10000            778.91             778.91               0.092853
 2097152    10000            779.03             779.03               0.046434
 4194304    10000            779.14             779.14               0.023220
 8388608    10000            779.09             779.09               0.011609
---------------------------------------------------------------------------------------
Completed: Wed Apr 15 06:09:06 2026

Total run time: 23.619s

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

[vultr@Aliyun3 ~]$ ib_write_bw -d ionic_1 -q 2 -F -x 1 -a --report_gbits -b -p 5001 66.42.116.72
Using sampled CPU speed 3295 MHz over reported speed 5008 MHz
Connected: Wed Apr 15 06:09:02 2026

---------------------------------------------------------------------------------------
                    RDMA_Write Bidirectional BW Test
 Dual-port       : OFF          Device         : ionic_1
 Number of qps   : 2            Transport type : IB
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
 local address: LID 0000 QPN 0x0800 PSN 0xe77286 RKey 0x000108 VAddr 0x007ffa301ee000
 GID: 253:147:22:211:89:182:01:74:189:15:59:47:29:252:16:135
 local address: LID 0000 QPN 0x0002 PSN 0x36042f RKey 0x000108 VAddr 0x007ffa309ee000
 GID: 253:147:22:211:89:182:01:74:189:15:59:47:29:252:16:135
 remote address: LID 0000 QPN 0x0002 PSN 0x151ca RKey 0x000114 VAddr 0x007f87f3823000
 GID: 253:147:22:211:89:182:01:79:119:76:46:183:177:87:149:75
 remote address: LID 0000 QPN 0x0800 PSN 0xab8ec RKey 0x000114 VAddr 0x007f87f4023000
 GID: 253:147:22:211:89:182:01:79:119:76:46:183:177:87:149:75
---------------------------------------------------------------------------------------
 #bytes     #iterations    BW peak[Gb/sec]    BW average[Gb/sec]   MsgRate[Mpps]
 2          10000           0.109376            0.109152            6.822015
 4          10000            0.22               0.22                 6.850886
 8          10000            0.44               0.44                 6.817539
 16         10000            0.88               0.88                 6.850112
 32         10000            1.75               1.75                 6.828895
 64         10000            3.49               3.49                 6.816610
 128        10000            7.00               7.00                 6.831384
 256        10000            13.94              13.94                6.805300
 512        10000            28.06              28.04                6.845515
 1024       10000            55.97              55.93                6.827587
 2048       10000            111.21             111.12               6.782249
 4096       10000            221.99             221.80               6.768730
 8192       10000            444.17             443.76               6.771294
 16384      10000            769.07             767.62               5.856500
 32768      10000            774.24             773.75               2.951620
 65536      10000            775.98             774.12               1.476522
 131072     10000            776.89             776.89               0.740901
 262144     10000            777.24             777.22               0.370608
 524288     10000            778.53             778.09               0.185510
 1048576    10000            778.91             778.91               0.092853
 2097152    10000            779.03             779.03               0.046434
 4194304    10000            779.14             779.14               0.023220
 8388608    10000            779.09             779.09               0.011609
---------------------------------------------------------------------------------------
Completed: Wed Apr 15 06:09:06 2026

Total run time: 4.580s


```

## Test 9. Multi Node Collective Communication	ib_write_bw GDR Test

## Test 10. Multi Node Collective Communication	Mori-EP

## Test 11. Multi Node Collective Communication	RCCL - AllReduce Bandwidth

## Test 12. Multi Node Collective Communication	RCCL - AlltoAll Bandwidth
