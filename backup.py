import tools
import time
import structSys as sys

config_file = 'C:\\setup.cfg'
user = "ubnt"
passw = "ubnt"
mac = "dc-9f-db"

class Backup(sys.Form):
    def __init__(self):
        super().__init__()
        self.user = user
        self.passw = passw
        self.call["iniciar"] = "self.form()"
    

    def form(self):
        ip_device = None

        for i in range(1, 4):#buscar mac com ip correspondente
            ip_device = tools.get_connected_device(mac)
            print(f"\n>> {i} Procurando mac, prefixo: {mac}")
            
            if ip_device == None:#se não encontrar
                print(">> mac não encontrado")
                time.sleep(2)

            elif ip_device != None:#função (tools.get_connected_device) retorna zero caso não encontre o mac
                ssh_obj = tools.ssh_connect(ip_device[0], self.user, self.passw)#iniciando conexão ssh
                
                if ssh_obj != -1:#função (tools.ssh_connect) retorna -1 se ouver erro
                    send = tools.send_config(ssh_obj, config_file)#envia arquivo de configuração
                else:
                    print("\n>> Falha na conexão ssh")
            

        

class Manual(sys.Form):
    def __init__(self):
        super().__init__()
        self.conf = config_file
        self.mac = mac
        self.user = user
        self.passw = passw
        
        self.call["alterar login ssh"] = "self.alterar_login_ssh()"
        self.call["alterar .cfg"] = "self.path_cfg()"
        self.call["alterar prefixo MAC"] = "self.prefix_mac()"

    
    def alterar_login_ssh(self):
        global user
        global passw
        print(f"\n {self.user}")
        user = str(input("usuário: "))
        passw = str(input("passw: "))

    def path_cfg(self):
        global config_file
        print(f"\n caminho atual: {self.conf}")
        config_file = str(input(">>: "))

    def prefix_mac(self):
        global mac
        print(f"\n prefixo mac atual: {self.mac}")
        mac = str(input(">>: "))



class Inicio(sys.Form):
    def __init__(self):
        super().__init__()
        self.call["Backup automático"] = "self.Backup_aut()"
        self.call["config manual"] = "self.manual()"

    def Backup_aut(self):
        backup = Backup()
        backup.inRun()

    def manual(self):
        manual = Manual()
        manual.inRun()

    def sair(self):
        return exit()

while(1):
    inicio = Inicio()
    inicio.inRun()