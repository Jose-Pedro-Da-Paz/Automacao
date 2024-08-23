from pyModbusTCP.server import DataBank, ModbusServer
from time import sleep
import struct

class ServidorModbus():
    
    def __init__(self, ip, porta):
        self._db = DataBank()
        self._server = ModbusServer(host=ip, port=porta, no_block= True, data_bank= self._db)
    
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
        
        
    def run(self):
        try:
            
            # inicia o servidor
            self._server.start()
            print("Servidor Modbus em operação")
            input_registers = self.float_to_registers(125.66)
            holding_registers = self.float_to_registers(844.55)
            self._db.set_input_registers(8, list(input_registers))
            self._db.set_holding_registers(10, list(holding_registers))
            
            sleep(1) # delay de 1 segundo
            
            while True:
                print("======================")
                print("Tabela Modbus")
                read_register1 = self._db.get_input_registers(8,2) # endereço 8 e 9
                read_register2 = self._db.get_holding_registers(10,2) # endereço 10 e 11
                
                read_value1 = self.registers_to_float(read_register1)
                read_value2 = self.registers_to_float(read_register2)
                
                print(f'Valor Real obtido de IR8 e IR9: {read_value1:.2f}')
                print(f'Valor Real obtido de HR10 e HR11: {read_value2:.2f}')
                print(f'IR8: {self._db.get_input_registers(8)}')
                print(f'IR9: {self._db.get_input_registers(9)}')
                print(f'HR10: {self._db.get_holding_registers(10)}')
                print(f'HR11: {self._db.get_holding_registers(11)}')
                
                sleep(5)
                
        except Exception as e:
                print("Erro: ",e.args)

servidor = ServidorModbus('127.0.0.1', 502)
servidor.run()