from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


from ansible.plugins.connection.ssh import Connection as SSH_link
from ansible.errors import AnsibleError
from socket import create_connection
from time import sleep


try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()



class Connection(SSH_link):
    '''
    check_ports plugin implement a method of externally opening ports on a firewall by
    generating a connection attempt on a set of prespecified closed ports.
    Once a correct sequence of connection attempts is received, the firewall rules
    are dynamically modified to allow the host which sent the connection attempts
    to connect over specific port(s)

    Some docs how to configure port knocking for linux system to check it plugin works
    https://tecadmin.net/secure-ssh-connections-with-port-knocking-linux/
    '''
    def __init__(self, *args, **kwargs):
        super(Connection, self).__init__(*args, **kwargs)
        display.vvv("Using connection plugin to open the SSH port we will knock ports\n"
                    "from available_ports variable in inventory file\n"
                    "and when the sequence is completed correctly\n"
                    "it will run a command that will add a rule in the firewall\n"
                    "to allow the connection to our host via port 22", host=self.host)

    def set_host_overrides(self, host, hostvars=None):
        '''
        An optional method, which can be used to set connection plugin parameters
        from variables set on the host (or groups to which the host belongs)

        Any connection plugin using this should first initialize its attributes in
        an overridden `def __init__(self):`, and then use `host.get_vars()` to find
        variables which may be used to set those attributes in this method.
        '''

        if 'available_ports' in hostvars:
            ports = hostvars['available_ports']
            if not isinstance(ports, list):
                raise AnsibleError("available_ports parameter for host '{}' must be list!".format(host))

            delay = 1
            if 'time_delay' in hostvars:
                delay = hostvars['time_delay']

            for p in ports:
                display.vvv("Connecting to port: {0}".format(p), host=self.host)
                try:
                    create_connection((self.host, p), 1)
                except:
                    pass
                display.vvv("Waiting for {0} seconds after connection".format(delay), host=self.host)
                sleep(delay)