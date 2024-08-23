#MEB ou Machine Expert Basic
# É o sistema da Schneider Eletronics para programação e simulação de CLPs
# O código a seguir tem como objetivo criar um Cliente Modbus que possa se comunicar com MEB.
# Com esse código podemo realizar a leitura e escrita dos registradores do CLP#

from pyModbusTCP.client import ModbusClient

class SchneiderModbusTCP():
    
    def __init__(self, ip_clp, porta):
        self._client = ModbusClient(host= ip_clp, port= porta)
        
    def assistente(self):
        self._client.open()
        print("Cliente Modbus em operação")
        assistente = True
        
        try:
            while assistente == True:
                operacao = input(f"""Deseja realizar uma leitura ou escrita? (1- Leitura | 2- Escrita | 3- Encerrar): """)
                
                if operacao == '1':
                    endereco = input(f"Qual o bit de memória que deseja ler? ")
                    print(f"Leitura: {self.leitura(int(endereco))}")
                elif operacao == '2':
                    endereco = input(f"Qual o bit de memória que deseja escrever? ")
                    valor = input(f"Informe o valor que será escrito (0->Falso ou 1->Verdadeiro)? ")
                    self.escrita(int(endereco), int(valor))
                elif operacao == '3':
                    self._client.close()
                    assistente = False
                else:
                    print(f"Operação Inválida!")
        except Exception as e:
            print('Erro: ', e.args)
        
        
    def leitura(self, endereco):
        return self._client.read_coils(endereco)
    
    def escrita(self, endereco, valor):
        return self._client.write_single_coil(endereco, valor)
    
s = SchneiderModbusTCP('localhost', 502)
s.assistente()