import tools
import time
import structSys as sys
import json
import subprocess
import paramiko


with open("cfg.json") as file:
    data = json.load(file)



class Backup(sys.Form):
    def __init__(self):
        super().__init__()

        self.call["iniciar"] = "self.form()"

    def inRun(self):
        return self.form()
    
    def form(self):
        ip_device = None

        for i in range(1, 4):                                                                      #buscar mac com ip correspondente
            ip_device = tools.get_connected_device(data["mac"])
            print(f"\n>> {i} Procurando mac, prefixo: {data["mac"]}")
            
            if ip_device == None:                                                                  #se não encontrar
                print("\n>> mac não encontrado")
                time.sleep(2)

            else:
                ssh_obj, ret = tools.ssh_connect(ip_device[0], data["user"], data["passw"])        #iniciando conexão ssh
                
                if ret == 1:
                    print("\n upload de arquivo .cfg")                                                  
                    tools.send_config(ssh_obj, data["config_file"])
                    tools.ping(data["config_file"]) 
                    print("\n SUCESSO...")
                    input("APERTE ENTER")
                    break



                elif ssh_obj == 0:
                    print("\n>> senha incorreta")
                elif ssh_obj == -1:
                    print("\n>> Falha na conexão ssh")


    


class Manual(sys.Form):
    def __init__(self):
        super().__init__()
        self.call["alterar login ssh"] = "self.alterar_login_ssh()"
        self.call["alterar .cfg"] = "self.path_cfg()"
        self.call["alterar prefixo MAC"] = "self.prefix_mac()"

    
    def alterar_login_ssh(self):
        print(f"\nlogin atual: {data["user"]}/{data["passw"]}")
        data["user"] = str(input("usuário: "))
        data["passw"] = str(input("passw: "))
        self.saveJson()

    def path_cfg(self):
        
        print(f"\ncaminho atual: {data["config_file"]}")
        data["config_file"] = str(input(">>: "))
        self.saveJson()

    def prefix_mac(self):
        print(f"\nprefixo mac atual: {data["mac"]}")
        data["mac"] = str(input(">>: "))
        self.saveJson()        

    def saveJson(self):
        with open("cfg.json", "w") as file:
            json.dump(data, file, indent=4)



class Inicio(sys.Form):
    def __init__(self):
        super().__init__()
        self.voltar = "sair"
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
