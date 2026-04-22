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


## Test 11. Multi Node Collective Communication	RCCL - AllReduce Bandwidth

## Test 12. Multi Node Collective Communication	RCCL - AlltoAll Bandwidth
