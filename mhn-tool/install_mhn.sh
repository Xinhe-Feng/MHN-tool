#!/bin/bash



if [ "$(whoami)" != "root" ]
then
    echo -e "You must be root to run this script"
    exit 1
fi

set -e
set -x

MHN_HOME=`dirname "$(readlink -f "$0")"`
WWW_OWNER="www-data"
SCRIPTS="$MHN_HOME/scripts/"
cd $SCRIPTS

if [ -f /etc/redhat-release ]; then
    export PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:$PATH
    #yum updates + health
    yum clean all -y
    yum update -y

    #Dump yum info for troubleshooting
    echo -e "Yum Repo List:\n"
    yum repolist
    echo -e "Yum Dev Group Packages:\n"
    yum grouplist | grep -i development
    echo -e "Attempting to install Dev Tools"
    yum groupinfo mark install "Development Tools"
    yum groupinfo mark convert "Development Tools"
    yum groupinstall "Development Tools" -y
    echo -e "Development Tools successfully installed\n"

    WWW_OWNER="nginx"
    ./install_sqlite.sh

    if [ ! -f /usr/local/bin/python2.7 ]; then
        echo "[`date`] Installing Python2.7 as a pre-req"
       ./install_python2.7.sh
    fi

     ./install_supervisord.sh
fi

if [ -f /etc/debian_version ]; then
#    apt-get update && apt-get upgrade -y
    apt-get install -y python-pip
    pip install --upgrade pip
    #export LANGUAGE=en_US.UTF-8
    #export LANG=en_US.UTF-8
    #sudo locale-gen en_US.UTF-8
    sudo pip install celery
fi

echo "[`date`] Starting Installation of all MHN packages"

echo "[`date`] ========= Installing hpfeeds ========="
 ./install_hpfeeds.sh

echo "[`date`] ========= Installing menmosyne ========="
 ./install_mnemosyne.sh

echo "[`date`] ========= Installing Honeymap ========="
 ./install_honeymap.sh

echo "[`date`] ========= Installing MHN Server ========="
 ./install_mhnserver.sh

echo "[`date`] ========= MHN Server Install Finished ========="
echo ""

chown $WWW_OWNER /var/log/mhn/mhn.log
supervisorctl restart mhn-celery-worker

echo "[`date`] Completed Installation of all MHN packages"

