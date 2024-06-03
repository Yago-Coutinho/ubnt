import subprocess
import ipaddress
import paramiko
from scp import SCPClient


def send_config(ssh ,config_file):
    
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(config_file, '/tmp/setup.cfg')

    stdin, stdout, stderr = ssh.exec_command('cat /tmp/setup.cfg > /tmp/system.cfg && cfgmtd -w && reboot')
    
    print(stdout.read().decode())
    print(stderr.read().decode())
    print("\n>> reboot")

    ssh.close()
    return 1



def ssh_connect(ip, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password)
    except:
        return -1
    
    return ssh

def get_connected_device(prefixo_mac):#procurando o rádio pelo MAC
    mac_address = "0"
    ip_address = "0"
    
    arp_output = subprocess.check_output(["arp", "-a"]).decode("latin-1")

    mac_position = arp_output.find(prefixo_mac)
    if mac_position>0:
        mac_address = arp_output[mac_position:mac_position+17]
        ip_address = arp_output[mac_position-22:mac_position].replace(" ", "")
    
    return ip_address, mac_address