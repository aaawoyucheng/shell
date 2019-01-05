curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
sed -i '/aliyuncs/d ' /etc/yum.repos.d/CentOS-Base.repo
sed -i '/gpgcheck/c gpgcheck=0 ' /etc/yum.repos.d/CentOS-Base.repo
#cat /etc/yum.repos.d/CentOS-Base.repo
curl -o /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
sed -i '/aliyuncs/d ' /etc/yum.repos.d/epel.repo
sed -i '/gpgcheck/c gpgcheck=0 ' /etc/yum.repos.d/epel.repo
#cat /etc/yum.repos.d/epel.repo
yum clean all
rm -rf /var/cache/yum
yum makecache
