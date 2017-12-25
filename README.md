Small instruction how to check out connection plugin works:

1) Install and configure knockd service by following the link below
https://tecadmin.net/secure-ssh-connections-with-port-knocking-linux

2) Specify available_ports in the inventory file
 
3) Run command inside current folder: ansible-playbook -i inventory helloworld.yml
