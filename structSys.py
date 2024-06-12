
import subprocess

class Form():                                                           #classe base para as telas
    def __init__(self):
       self.nameForm = "name"
       self.voltar = "voltar"
       self.call = {}                                                   #dicionário que guarda os nomes das opções e as funções correspondentes 

    def decorador(func):                                                #decorador para colocar rodapé nas paginas
        def wrapper(*args, **kwargs):
            subprocess.run(args=["cls"], shell=True)
            #print("\n")
            print("-------------------------------------------\n")
            func(*args, **kwargs)
        return wrapper
    

    @decorador        
    def outRun(self, opc):                                              #executa a função escolhida, executa as funções guardadas no dicionário 
        exec(list(self.call.values())[opc-1])



    @decorador
    def inRun(self):                                                    #print as funções disponiveis no dicionário, e espera um input de escolha
        flag = True
        #while(flag):
        cont = 1
            
        for key in self.call:
            print(f"    {cont}. {key}")
            cont += 1
        print(f"    {len(self.call)+1}. {self.voltar}\n\n")
            
        opc = int(input(">>>: "))
        if opc != len(self.call)+1:
            self.outRun(opc)
        else:
            flag = self.sair()
                         
    def sair(self):                                                     #retorna false para sair do loop while
       return False

