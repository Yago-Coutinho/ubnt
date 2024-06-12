import subprocess
import ipaddress
import paramiko
from scp import SCPClient
import time

def send_config(ssh ,config_file):
    
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(config_file, '/tmp/setup.cfg')

    stdin, stdout, stderr = ssh.exec_command('cat /tmp/setup.cfg > /tmp/system.cfg && cfgmtd -w && reboot')
    
    print(stdout.read().decode())
    print(stderr.read().decode())
    print("\n>> reboot")

    ssh.close()
    return 1



def ssh_connect(ip, username, password):#faz a conexão via ssh
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username=username, password=password)
    
    except paramiko.ssh_exception.AuthenticationException:
        return 0    
    
    except:
        return -1
    
    return ssh, 1

def get_connected_device(prefixo_mac):#procurando o rádio pelo prefixo MAC na tabela arp, retorna (ip, mac)
    arp_output = subprocess.check_output(["arp", "-a"]).decode("latin-1")

    mac_position = arp_output.find(prefixo_mac)
    if mac_position>0:
        mac_address = arp_output[mac_position:mac_position+17]
        ip_address = arp_output[mac_position-22:mac_position].replace(" ", "")
        return ip_address, mac_address
    else:
        return None    
    

  
def ping(cfg):
    with open(cfg) as file:
        cfg = file.read()       
        posi = cfg.find("netconf.2.ip=192.168")
        ip = cfg[posi+13:posi+24]
        time.sleep(5)

        while(True):
            try:
                retorno = subprocess.check_output(args=["ping", ip], shell=True).decode("latin-1")
                print("")
                print(retorno)
                break

            except:
                print("ip não encontrado")
