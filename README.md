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
```

## Test 6. Single Node Collective Communication	RCCL - All2All Performance
```
sudo docker pull prasadnairamd/rccl-tests:latest


docker run --rm   --device=/dev/kfd   --device=/dev/dri   --group-add video   --ipc=host   --network=host   --cap-add=SYS_PTRACE   --security-opt  seccomp=unconfined prasadnairamd/rccl-tests   ./build/alltoall_perf -b 8 -e 128M -f 2 -g 8
```

## Test 7. Single Node Collective Communication	Mori-EP
```
$ ./run_intra_mori.sh
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

Client Node:
bash
./ib_write_bw -d <ib_device> --use_rocm=<gpu_id> -a <server_ip>
Optional - DMABUF: If using a modern ROCm setup (e.g., MI300X), you can use --enable-rocm-dmabuf during configure and add --use_rocm_dmabuf to your run command for improved performance. 


``` 

Server-side example :
[vultr@Aliyun3 perftest]$ ./ib_write_bw -d ionic_0 --use_rocm=0 -a
Using sampled CPU speed 3295 MHz over reported speed 5008 MHz

************************************
* Waiting for client to connect... *
************************************
Connected: Tue Apr 21 08:12:52 2026

Using ROCm Device with ID: 0, Name: AMD Instinct MI355X, PCI Bus ID: 0x5, GCN Arch: gfx950:sramecc+:xnack-
allocated 16777216 bytes of GPU buffer at 0x7f042a400000
---------------------------------------------------------------------------------------
                    RDMA_Write BW Test
 Dual-port       : OFF          Device         : ionic_0
 Number of qps   : 1            Transport type : IB
 Connection type : RC           Using SRQ      : OFF
 PCIe relax order: ON           Lock-free      : OFF
 ibv_wr* API     : OFF          Using DDP      : OFF
 CQ Moderation   : 100
 CQE Poll Batch  : 16
 Mtu             : 4096[B]
 Link type       : Ethernet
 CPU freq        : 3295[MHz]
 GID index       : 0
 Max inline data : 0[B]
 rdma_cm QPs     : OFF
 Use ROCm memory : ON
 Data ex. method : Ethernet
---------------------------------------------------------------------------------------
 local address: LID 0000 QPN 0x0002 PSN 0x9c4c2e RKey 0x000182 VAddr 0x007f042ac00000
 GID: 254:128:00:00:00:00:00:00:06:144:129:255:254:54:91:176
 remote address: LID 0000 QPN 0x0002 PSN 0x398b12 RKey 0x000184 VAddr 0x007fe939e00000
 GID: 254:128:00:00:00:00:00:00:06:144:129:255:254:56:231:64
---------------------------------------------------------------------------------------
 #bytes     #iterations    BW peak[MiB/sec]    BW average[MiB/sec]   MsgRate[Mpps]
 8388608    5000             19044.44            19044.43                    0.002381
---------------------------------------------------------------------------------------
Completed: Tue Apr 21 08:12:57 2026

Total run time: 98.367s
deallocating GPU buffer 0x7f042a400000


Client-side example :
[vultr@Aliyun1 perftest]$ ./ib_write_bw -d ionic_0 --use_rocm=0 -a 45.76.25.46
Using sampled CPU speed 3295 MHz over reported speed 5022 MHz
Connected: Tue Apr 21 08:12:52 2026

Using ROCm Device with ID: 0, Name: AMD Instinct MI355X, PCI Bus ID: 0x5, GCN Arch: gfx950:sramecc+:xnack-
allocated 16777216 bytes of GPU buffer at 0x7fe939600000
---------------------------------------------------------------------------------------
                    RDMA_Write BW Test
 Dual-port       : OFF          Device         : ionic_0
 Number of qps   : 1            Transport type : IB
 Connection type : RC           Using SRQ      : OFF
 PCIe relax order: ON           Lock-free      : OFF
 ibv_wr* API     : OFF          Using DDP      : OFF
 TX depth        : 128
 CQ Moderation   : 100
 CQE Poll Batch  : 16
 Mtu             : 4096[B]
 Link type       : Ethernet
 CPU freq        : 3295[MHz]
 GID index       : 0
 Max inline data : 0[B]
 rdma_cm QPs     : OFF
 Use ROCm memory : ON
 Data ex. method : Ethernet
---------------------------------------------------------------------------------------
 local address: LID 0000 QPN 0x0002 PSN 0x398b12 RKey 0x000184 VAddr 0x007fe939e00000
 GID: 254:128:00:00:00:00:00:00:06:144:129:255:254:56:231:64
 remote address: LID 0000 QPN 0x0002 PSN 0x9c4c2e RKey 0x000182 VAddr 0x007f042ac00000
 GID: 254:128:00:00:00:00:00:00:06:144:129:255:254:54:91:176
---------------------------------------------------------------------------------------
 #bytes     #iterations    BW peak[MiB/sec]    BW average[MiB/sec]   MsgRate[Mpps]
 2          5000             6.82               6.76                 3.543784
 4          5000             13.65              13.60                3.565549
 8          5000             27.57              27.35                3.584287
 16         5000             54.77              54.53                3.573972
 32         5000             109.30             108.96               3.570471
 64         5000             220.76             219.55               3.597148
 128        5000             436.26             415.65               3.404981
 256        5000             881.12             880.74               3.607493
 512        5000             1750.74            1749.40              3.582769
 1024       5000             3516.78            3494.28              3.578147
 2048       5000             7002.95            6941.36              3.553975
 4096       5000             13693.01            13639.21                    3.491638
 8192       5000             19878.65            19871.68                    2.543574
 16384      5000             18647.48            18645.54                    1.193314
 32768      5000             19033.53            19032.42                    0.609037
 65536      5000             18683.01            18682.46                    0.298919
 131072     5000             18584.38            18583.90                    0.148671
 262144     5000             18579.35            18579.29                    0.074317
 524288     5000             18765.36            18765.26                    0.037531
 1048576    5000             18635.36            18635.27                    0.018635
 2097152    5000             18787.56            18787.52                    0.009394
 4194304    5000             19045.85            19045.80                    0.004761
 8388608    5000             19044.44            19044.43                    0.002381
---------------------------------------------------------------------------------------
Completed: Tue Apr 21 08:12:57 2026

Total run time: 5.459s
deallocating GPU buffer 0x7fe939600000



```


## Test 10. Multi Node Collective Communication	Mori-EP

For running multinode Mori tests run the script on both nodes simultaneously.

You have to configure the r2.sh file inside the container to set the ip address of remote device. 

$ ./run_inter_mori.sh 


## Test 11. Multi Node Collective Communication	RCCL - AllReduce Bandwidth

## Test 12. Multi Node Collective Communication	RCCL - AlltoAll Bandwidth
