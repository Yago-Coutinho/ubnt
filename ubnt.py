import tools
import json
import argparse

with open("C:\\cfg.json") as file:
    data = json.load(file)

with open("C:\\ABCD.cfg") as file:
    cfg = file.readlines()
    ip = cfg[146][13:24]

parser = argparse.ArgumentParser()
parser.add_argument("opc")
parser.add_argument("-user", metavar="-u", default=[data["user"], data["passw"]], nargs=2)
parser.add_argument("-ip", default=ip)

argv = parser.parse_args()

if __name__=="__main__":

    match argv.opc:
        case "up":
            ip_mac = tools.scan_arp(data["mac"])
            if ip_mac != None:
                tools.upload(ip_mac[0], argv.user[0], argv.user[1], data["config_file"])

        case "path":
            tools.path_cfg(data)

        case "mac":
            tools.prefix_mac(data)

        case "login":
            tools.alterar_login_ssh(data)

        case "scan":
            tools.radio_scan(argv.user[0], argv.user[1], data["config_file"])

        case "ssh":
            tools.ssh_ubnt(argv.user[0], argv.user[1], data["config_file"])

        case "opc":
            opc = ["up : upload .cfg",
                   "scan : busca através do rádio",
                   "login : alterar login",
                   "ssh : ainda não funciona direito",
                   "path : alterar caminho de arquivo .cfg"]
            
            for i in opc:
                print(i)
                