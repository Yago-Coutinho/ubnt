import tools
import time

config_file = 'C:\\setup.cfg'
user = "ubnt"
passw = "ubnt"
mac = "dc-9f-db"

class Backup():
    def __init__(self):
        pass
    

    def form(self):
        ip_device = [0, 0]

        for i in range(1, 4):#buscar mac com ip correspondente
            ip_device = tools.get_connected_device(mac)
            print(f"\n>> {i} Procurando mac, prefixo: {mac}")
            
            if ip_device[0] == 0:#se não encontrar
                print("\n>> mac não encontrado")
                time.sleep(2)

            else: 
                break
            

        if ip_device != 0:#função (tools.get_connected_device) retorna zero caso não encontre o mac
            ssh_obj = tools.ssh_connect(ip_device[0], user, passw)#iniciando conexão ssh
            
            if ssh_obj != -1:#função (tools.ssh_connect) retorna -1 se ouver erro
                send = tools.send_config(ssh_obj, config_file)#envia arquivo de configuração
            else:
                print("\n>> Falha na conexão ssh")


class Manual():
    def __init__(self):
        self.conf = config_file
        self.mac = mac
        self.user = user
        self.passw = passw
        pass

    def form(self):
        print("\n\n")
        print("1. alterar user/passw")
        print("2. alterar alterar caminho do arquivo de configuração")
        print("3. alterar prefixo do mac")
        
        opc = str(input("\n>>: "))

        match opc:
            case "1":                
                global user
                global passw

                print(f"\n {self.user}")
                user = str(input("usuário: "))
                passw = str(input("passw: "))
            
            case "2":
                global config_file

                print(f"\n caminho atual: {self.conf}")
                config_file = str(input(">>: "))
            
            case "3":
                global mac

                print(f"\n prefixo mac atual: {self.mac}")
                mac = str(input(">>: "))

while(1):

    print("\n###   Backup auto   ###\n\n")
    print(" 1. Backup automático")
    print(" 2. Configuração manual")
    print(" 3. sair")

    opc = str(input("\n>>>: "))

    match opc:
        case "1":
            backup = Backup()
            backup.form()
        
        case "2":
            manual = Manual()
            manual.form()
        
        case "3":
            break