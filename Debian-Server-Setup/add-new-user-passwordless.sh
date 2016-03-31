#!/bin/bash
# This script adds a new user to the remote server , adds it to sudoers list and enables passwordless login

read -p "Enter your Server IP:" serverIP #get server IP address

read -p "Enter a new username:" newusername #username for the new user
read -s -p "Enter the password for $newusername:" password #password

printf "\nEnter the root password of the server when prompted\n"

pass="$(perl -e 'print crypt($ARGV[0],"password")' $password)" #encrypt password

ssh root@$serverIP "useradd -m -p $pass $newusername;apt-get update && apt-get install sudo;usermod -a -G sudo $newusername" #add the new user


if [ ! -d /home/$USER/.ssh ]; then
    echo "Seems like you don't have an ssh key pair\nGenerating One..."
    ssh-keygen
fi

ssh-copy-id $newusername@$serverIP # enable passwordless login (adds your public key to authorized hosts)

read -p "Do you want to disable root login?[Y/n]" -n 1 -r
printf "\n"
if [[ $REPLY =~ ^[Yy]$ ]];then
  ssh root@$serverIP "cat /etc/ssh/sshd_config > /etc/ssh/sshd_config.bak;sed 's/#.*PermitRootLogin*/PermitRootLogin no/' /etc/ssh/sshd_config > /etc/ssh/sshd_config;systemctl restart ssh" #disable root login
fi

printf "Now you can login as $newusername to $serverIP by \n    ssh $newusername@$serverIP\n"
