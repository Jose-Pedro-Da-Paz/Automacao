#MEB ou Machine Expert Basic
# É o sistema da Schneider Eletronics para programação e simulação de CLPs
# O código a seguir tem como objetivo criar um Cliente Modbus que possa se comunicar com MEB.
# Com esse código podemo realizar a leitura e escrita dos registradores do CLP#

from pyModbusTCP.client import ModbusClient
import struct

class SchneiderModbusTCP():
    
    def __init__(self, ip_clp, porta):
        self._client = ModbusClient(host= ip_clp, port= porta)
        
    # Método que separa um numero real em dois inteiros
    def float_to_registers(self, value):
        packed_value = struct.pack('<f', value)
        registers = struct.unpack('<HH', packed_value)
        
        return registers

    # Método que une dois números inteiros em um número real
    def registers_to_float(self, registers):
        packad_value = struct.pack('<HH', registers[0], registers[1])
        value = struct.unpack('<f', packad_value)[0]
        
        return value
        
    def assistente(self):
        self._client.open()
        print("Cliente Modbus em operação")
        assistente = True
        
        try:
            while assistente == True:
                operacao = input(f"""Deseja realizar uma leitura ou escrita? (1- Leitura | 2- Escrita | 3- Encerrar): """)
                
                if operacao == '1':
                    endereco = input(f"Qual a palavra de memória que deseja ler? ")
                    print(f"Leitura: {self.leitura(int(endereco))}")
                elif operacao == '2':
                    endereco = input(f"Qual a palavra de memória que deseja escrever? ")
                    valor = input(f"Informe o valor que será escrito? ")
                    self.escrita(int(endereco), float(valor))
                elif operacao == '3':
                    print(f"Cliente Modbus encerrando")
                    self._client.close()
                    assistente = False
                    
                else:
                    print(f"Operação Inválida!")
        except Exception as e:
            print('Erro: ', e.args)
        
        
    def leitura(self, endereco):
        registers = self._client.read_holding_registers(endereco, 2)
        valor = self.registers_to_float(registers)
        return round(valor, 2) #função round permite definir o número de casas decimais
    
    def escrita(self, endereco, valor):
        registers = self.float_to_registers(valor)
        result = self._client.write_multiple_registers(endereco, registers)
        return round(result, 2)
    
s = SchneiderModbusTCP('localhost', 502)
s.assistente()