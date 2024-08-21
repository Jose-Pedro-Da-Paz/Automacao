from pyModbusTCP.client import ModbusClient
from time import sleep
import struct

class ClientModbus():
    
    def __init__(self, ip_servidor, porta):
        
        self._client = ModbusClient(host = ip_servidor, port = porta)
    
        # Método que separa um numero real em dois inteiros
    def float_to_registers(self, value):
        packed_value = struct.pack('>f', value)
        registers = struct.unpack('>HH', packed_value)
        
        return registers

    # Método que une dois números inteiros em um número real
    def registers_to_float(self, registers):
        packad_value = struct.pack('>HH', registers[0], registers[1])
        value = struct.unpack('>f', packad_value)[0]
        
        return value
           
    def run(self, ip, porta):
        self._client.open()
        print("Cliente Modbus em Operação")
        
        pc = ModbusClient(host=ip, port=porta)
        
        try:
            if not pc.open():
                print("Não foi possível conectar ao servidor!")
                exit()
            
            registers = self.float_to_registers(88.174)
            self._client.write_multiple_registers(10, list(registers))
         
            while True:
                print("======================")
                print("Tabela ModBus")
                read_input_registers = self._client.read_input_registers(8,2)
                read_value = self.registers_to_float(read_input_registers)
                print(f'Valor Real (Server Side): {read_value:.2f}')
                
                read_holding_registers = self._client.read_holding_registers(10,2)
                read_value2 = self.registers_to_float(read_holding_registers)
                print(f'Valor Real (Client Side): {read_value2:.3f}')
                
                sleep(5)
                        
        except Exception as e:
            print("Erro: ", e.args)
            
client = ClientModbus('127.0.0.1', 502)
client.run('127.0.0.1', 502)