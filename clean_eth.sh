set -x
#ip addr |grep mtu|grep -v lo|awk -F ":" '{print $2}'
echo -n "enter ethernet card name:"
read ethcard
cat -e 'DEVICE="${ethcard}"\nNAME="${ethcard}"\nNM_CONTROLLED="no"\nONBOOT=yes\nTYPE=Ethernet\nBOOTPROTO=dhcp\n'>/etc/sysconfig/network-scripts/ifcfg-${ethcard}
echo /etc/sysconfig/network-scripts/ifcfg-${ethcard}
