
cat <<EOF > /etc/sysconfig/network-scripts/ifcfg-$1
DEVICE="${1}"
NAME="${1}"
NM_CONTROLLED="no"
ONBOOT=yes
TYPE=Ethernet
BOOTPROTO=dhcp
EOF
