set -x
#ip addr |grep mtu|grep -v lo|awk -F ":" '{print $2}'
echo -n "enter ethernet card name:"
read ethcard
cat <<EOF > /etc/sysconfig/network-scripts/ifcfg-${ethcard}
DEVICE="${ethcard}"
NAME="${ethcard}"
NM_CONTROLLED="no"
ONBOOT=yes
TYPE=Ethernet
BOOTPROTO=dhcp
EOF
cat /etc/sysconfig/network-scripts/ifcfg-${ethcard}
