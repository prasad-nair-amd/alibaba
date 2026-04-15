for d in /sys/class/infiniband/ionic_*; do
  DEV=$(basename $d)
  IFACE=$(ls $d/device/net)
  echo "$IFACE"

  IP=$(ip -6 addr show dev "$IFACE" | grep "fd93" | awk '{print $2}' | cut -d/ -f1)
  echo "$IP"
  SNET=$(echo $IP | cut -d: -f4)
  echo "$SNET"
  echo "$DEV $SNET"
done
