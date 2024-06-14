import subprocess
import paramiko
from scp import SCPClient
import time
import json


def upload(ip, user, passw, config_file):
    ssh_obj, ret = ssh_connect(ip, user, passw)
                
    if ret == 1:
        print("upload de arquivo .cfg")                                                  
        send_config(ssh_obj, config_file)

        with open(config_file) as file:
            cfg = file.readlines()
            ip_cfg = cfg[146][13:24]

        ping(ip_cfg)
        ssh_obj.close()

        print("SUCESSO...")
        input("APERTE ENTER")

    elif ret == 0:
        print("senha incorreta")
            

    elif ret == -1:
        print("Falha na conexão ssh")


def send_config(ssh ,config_file):    
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(config_file, '/tmp/setup.cfg')

    stdin, stdout, stderr = ssh.exec_command('cat /tmp/setup.cfg > /tmp/system.cfg && cfgmtd -w && reboot')
    
    print(stdout.read().decode())
    print(stderr.read().decode())
    print("\n>> reboot")

    return 1

def ssh_connect(ip, username, password):#faz a conexão via ssh
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(ip, username=username, password=password)    
    except paramiko.ssh_exception.AuthenticationException:
        return None, 0     
    except:
        return None, -1
    
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
  
def ping(ip):
    time.sleep(5)

    while(True):
        try:
            retorno = subprocess.check_output(args=["ping", ip], shell=True).decode("latin-1")
            print("")
            print(retorno)
            break

        except:
            print("ip não encontrado")

def scan_arp(mac):
    for i in range(1, 4):                                                                      #buscar mac com ip correspondente
        ip_device = get_connected_device(mac)
        print(f"{i}. Procurando mac, prefixo: {mac}")
            
        if ip_device == None:                                                                  #se não encontrar
            print("mac não encontrado")
            time.sleep(2)

        else:
            return ip_device
        
    return None

def alterar_login_ssh(data):
    print(f"\nlogin atual: {data["user"]}/{data["passw"]}")
    data["user"] = str(input("novo usuário: "))
    data["passw"] = str(input("nova senha: "))
    saveJson(data)

def path_cfg(data):       
    print(f"\ncaminho atual: {data["config_file"]}")
    data["config_file"] = str(input("novo caminho de arquivo .cfg: "))
    saveJson(data)

def prefix_mac(data):
    print(f"\nprefixo mac atual: {data["mac"]}")
    data["mac"] = str(input("novo prefixo mac: "))
    saveJson(data)        

def saveJson(data):
    with open("cfg.json", "w") as file:
        json.dump(data, file, indent=4)

def radio_scan(user, passw, config_file):    
    with open(config_file) as file:
        cfg = file.readlines()
        ip_cfg = cfg[146][13:24]

    ssh_obj, ret = ssh_connect(ip_cfg, user, passw)

    if ret == 1:                                                 
        stdin, stdout, stderr = ssh_obj.exec_command('iwlist ath0 scan')
        print(stdout.read().decode())
        print(stderr.read().decode())

        ssh_obj.close()

    elif ret == 0:
        print("senha incorreta")            

    elif ret == -1:
        print("Falha na conexão ssh")

def ssh_ubnt(user, passw, config_file):

    with open(config_file) as file:
       cfg = file.readlines()
       ip_cfg = cfg[146][13:24]

    ssh_obj, ret = ssh_connect(ip_cfg, user, passw)

    if ret == 1:                                                 
        while(1):
            comando = input(">>>: ")
            if comando != "exit":
                stdin, stdout, stderr = ssh_obj.exec_command(comando)
                print(stdin.read().decode())
                print(stdout.read().decode())
                print(stderr.read().decode())
            else:
                 ssh_obj.close()
                 break

    elif ret == 0:
        print("senha incorreta")            

    elif ret == -1:
        print("Falha na conexão ssh")
