import subprocess
import re
import ipaddress
import paramiko
from scp import SCPClient

config_file = 'C:\\setup.cfg'
user = "ubnt"
passw = "ubnt"

def ssh_connect_and_send_config(ip, username, password, config_file):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password)
    except:
        print("conexão não concluida")
        return -1
    
    print("\n>> configurando equipamento")
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(config_file, '/tmp/setup.cfg')

    stdin, stdout, stderr = ssh.exec_command('cat /tmp/setup.cfg > /tmp/system.cfg && cfgmtd -w && reboot')
    
    print(stdout.read().decode())
    print(stderr.read().decode())
    print("\n>> reboot")

    ssh.close()
    return 1


def get_connected_device():#procurando o rádio pelo MAC
    mac_address = "0"
    ip_address = "0"
    
    arp_output = subprocess.check_output(["arp", "-a"]).decode("latin-1")

    mac_position = arp_output.find("dc-9f-db")
    if mac_position>0:
        mac_address = arp_output[mac_position:mac_position+17]
        ip_address = arp_output[mac_position-22:mac_position].replace(" ", "")
    
    return ip_address, mac_address




while(1):
    print("\n1: Iniciar")
    print("\n2: User/passw")    
    opc = input("\n>>: ")
    
    if str(opc) == "1":
        for i in range(4):
            connected_device = get_connected_device()#obtendo ip e MAC do rádio
            if connected_device:
                print("\n>> MAC encontrado")
                sshreturn = ssh_connect_and_send_config(connected_device[0], "ubnt", "ubnt", config_file)
                if sshreturn == 1:
                    break
                
            else:
                print("\n>> ERRO: MAC não encontrado")
                pass
    
    elif str(opc) == 2:
        user = input("\nuser: ")
        passw = input("\npassw: ")
        


