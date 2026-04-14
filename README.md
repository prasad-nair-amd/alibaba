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
Server:
```
[vultr@Aliyun3 ~]$ sudo ib_write_bw -b  -d ionic_1 --gid-index 1 -F --report_gbits -a -n 5000 -q 4
Using sampled CPU speed 3295 MHz over reported speed 5008 MHz

************************************
* Waiting for client to connect... *
************************************
Connected: Wed Apr 15 04:36:50 2026

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
 Data ex. method : Ethernet
---------------------------------------------------------------------------------------
 local address: LID 0000 QPN 0x0002 PSN 0x60ddb0 RKey 0x000107 VAddr 0x007fd500ec1000
 GID: 253:147:22:211:89:182:01:80:223:237:130:41:237:150:197:196
 local address: LID 0000 QPN 0x0800 PSN 0x71edda RKey 0x000107 VAddr 0x007fd5016c1000
 GID: 253:147:22:211:89:182:01:80:223:237:130:41:237:150:197:196
 local address: LID 0000 QPN 0x0003 PSN 0x9da31c RKey 0x000107 VAddr 0x007fd501ec1000
 GID: 253:147:22:211:89:182:01:80:223:237:130:41:237:150:197:196
 local address: LID 0000 QPN 0x0801 PSN 0xa03a3b RKey 0x000107 VAddr 0x007fd5026c1000
 GID: 253:147:22:211:89:182:01:80:223:237:130:41:237:150:197:196
 remote address: LID 0000 QPN 0x0002 PSN 0x7e0d8f RKey 0x000109 VAddr 0x007fe58f1b8000
 GID: 253:147:22:211:89:182:01:73:57:89:201:223:190:176:133:68
 remote address: LID 0000 QPN 0x0800 PSN 0xec1d04 RKey 0x000109 VAddr 0x007fe58f9b8000
 GID: 253:147:22:211:89:182:01:73:57:89:201:223:190:176:133:68
 remote address: LID 0000 QPN 0x0003 PSN 0x4500c8 RKey 0x000109 VAddr 0x007fe5901b8000
 GID: 253:147:22:211:89:182:01:73:57:89:201:223:190:176:133:68
 remote address: LID 0000 QPN 0x0801 PSN 0x253140 RKey 0x000109 VAddr 0x007fe5909b8000
 GID: 253:147:22:211:89:182:01:73:57:89:201:223:190:176:133:68
---------------------------------------------------------------------------------------
 #bytes     #iterations    BW peak[Gb/sec]    BW average[Gb/sec]   MsgRate[Mpps]
 2          20000           0.158676            0.156611            9.788187
 4          20000            0.32               0.32                 9.876338
 8          20000            0.64               0.63                 9.878891
 16         20000            1.29               1.26                 9.871497
 32         20000            2.59               2.54                 9.905190
 64         20000            5.16               5.07                 9.903763
 128        20000            10.29              10.09                9.858341
 256        20000            20.56              20.22                9.874291
 512        20000            41.22              40.44                9.873131
 1024       20000            82.40              81.14                9.904961
 2048       20000            162.51             160.47               9.794029
 4096       20000            324.29             318.79               9.728583
 8192       20000            637.53             633.80               9.671073
 16384      20000            753.98             736.52               5.619239
 32768      20000            774.86             774.66               2.955077
 65536      20000            775.39             775.25               1.478663
 131072     20000            777.00             776.96               0.740969
 262144     20000            777.70             777.42               0.370702
 524288     20000            777.78             774.66               0.184694
 1048576    20000            778.17             778.02               0.092747
 2097152    20000            778.16             777.88               0.046365
 4194304    20000            778.85             778.31               0.023195
 8388608    20000            778.53             777.79               0.011590
---------------------------------------------------------------------------------------
Completed: Wed Apr 15 04:36:58 2026

Total run time: 10.951s
```

Client:
```
[vultr@Aliyun1 ~]$ sudo ib_write_bw -b -d ionic_1 --gid-index 1 -F --report_gbits -a -n 5000 -q 4 45.76.25.46
Using sampled CPU speed 3295 MHz over reported speed 5008 MHz
Connected: Wed Apr 15 04:36:50 2026

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
 Data ex. method : Ethernet
---------------------------------------------------------------------------------------
 local address: LID 0000 QPN 0x0002 PSN 0x7e0d8f RKey 0x000109 VAddr 0x007fe58f1b8000
 GID: 253:147:22:211:89:182:01:73:57:89:201:223:190:176:133:68
 local address: LID 0000 QPN 0x0800 PSN 0xec1d04 RKey 0x000109 VAddr 0x007fe58f9b8000
 GID: 253:147:22:211:89:182:01:73:57:89:201:223:190:176:133:68
 local address: LID 0000 QPN 0x0003 PSN 0x4500c8 RKey 0x000109 VAddr 0x007fe5901b8000
 GID: 253:147:22:211:89:182:01:73:57:89:201:223:190:176:133:68
 local address: LID 0000 QPN 0x0801 PSN 0x253140 RKey 0x000109 VAddr 0x007fe5909b8000
 GID: 253:147:22:211:89:182:01:73:57:89:201:223:190:176:133:68
 remote address: LID 0000 QPN 0x0002 PSN 0x60ddb0 RKey 0x000107 VAddr 0x007fd500ec1000
 GID: 253:147:22:211:89:182:01:80:223:237:130:41:237:150:197:196
 remote address: LID 0000 QPN 0x0800 PSN 0x71edda RKey 0x000107 VAddr 0x007fd5016c1000
 GID: 253:147:22:211:89:182:01:80:223:237:130:41:237:150:197:196
 remote address: LID 0000 QPN 0x0003 PSN 0x9da31c RKey 0x000107 VAddr 0x007fd501ec1000
 GID: 253:147:22:211:89:182:01:80:223:237:130:41:237:150:197:196
 remote address: LID 0000 QPN 0x0801 PSN 0xa03a3b RKey 0x000107 VAddr 0x007fd5026c1000
 GID: 253:147:22:211:89:182:01:80:223:237:130:41:237:150:197:196
---------------------------------------------------------------------------------------
 #bytes     #iterations    BW peak[Gb/sec]    BW average[Gb/sec]   MsgRate[Mpps]
 2          20000           0.158676            0.156611            9.788187
 4          20000            0.32               0.32                 9.876338
 8          20000            0.64               0.63                 9.878891
 16         20000            1.29               1.26                 9.871497
 32         20000            2.59               2.54                 9.905190
 64         20000            5.16               5.07                 9.903763
 128        20000            10.29              10.09                9.858341
 256        20000            20.56              20.22                9.874291
 512        20000            41.22              40.44                9.873131
 1024       20000            82.40              81.14                9.904961
 2048       20000            162.51             160.47               9.794029
 4096       20000            324.29             318.79               9.728583
 8192       20000            637.53             633.80               9.671073
 16384      20000            753.98             736.52               5.619239
 32768      20000            774.86             774.66               2.955077
 65536      20000            775.39             775.25               1.478663
 131072     20000            777.00             776.96               0.740969
 262144     20000            777.70             777.42               0.370702
 524288     20000            777.78             774.66               0.184694
 1048576    20000            778.17             778.02               0.092747
 2097152    20000            778.16             777.88               0.046365
 4194304    20000            778.85             778.31               0.023195
 8388608    20000            778.53             777.79               0.011590
---------------------------------------------------------------------------------------
Completed: Wed Apr 15 04:36:58 2026

```

## Test 9. Multi Node Collective Communication	ib_write_bw GDR Test

## Test 10. Multi Node Collective Communication	Mori-EP

## Test 11. Multi Node Collective Communication	RCCL - AllReduce Bandwidth

## Test 12. Multi Node Collective Communication	RCCL - AlltoAll Bandwidth
