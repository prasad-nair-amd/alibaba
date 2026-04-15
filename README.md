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

For running IB bandwidth test you should first find the mapping of rdma interfaces between two nodes. 
You can refer to the document Alinux RDMA Guide.docx in the repo. In the below example ionic_7 interface 
is mapped to ionic_1

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

## Test 10. Multi Node Collective Communication	Mori-EP

## Test 11. Multi Node Collective Communication	RCCL - AllReduce Bandwidth

## Test 12. Multi Node Collective Communication	RCCL - AlltoAll Bandwidth
