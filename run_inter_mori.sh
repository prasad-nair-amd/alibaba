#!/bin/bash

echo "Start docker Mori..."
docker run -d \
  --name mori \
  --privileged \
  --network=host \
  -v /dev/infiniband:/dev/infiniband \
  --device /dev/kfd \
  --device /dev/dri \
  --ulimit memlock=-1 \
  --cap-add SYS_ADMIN \
  --cap-add IPC_LOCK \
  --group-add video \
  --security-opt seccomp=unconfined \
  --shm-size=16g \
  -v ${PWD}:/root/cache \
  -v /mnt:/mnt \
  -v $HOME:$HOME \
  rocm/ali-private:alinux3_rocm7.2.1.76_cp310_torch2.9.1_20260331 sleep infinity

docker ps | grep mori

echo "Start running IntraNode Mori Test:"
docker exec -it mori bash -c "/root/cache/run_mori.sh"
echo "Installing AINIC Driver inside of docker"
docker exec -it mori bash -c "/root/cache/install_driver.sh"
echo "Start running InterNode Mori Test:"
docker exec -it mori bash -c "/root/cache/r2.sh"


#echo "Stop amd rm the docker mori"
#docker stop  mori
#docker rm mori
