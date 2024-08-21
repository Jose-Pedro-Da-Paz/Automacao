from pyModbusTCP.server import DataBank, ModbusServer
from time import sleep

class ServidorModbus():
    
    def __init__(self, ip, porta):
        self._db = DataBank()
        self._server = ModbusServer(host=ip, port=porta, no_block= True, data_bank= self._db)
        
    def run(self):
        try:
            
            # inicia o servidor
            self._server.start()
            print("Servidor Modbus em operação")
            
            # escreve o valor analógico nos registradores de entrada
            self._db.set_input_registers(0, [int(350)])
            self._db.set_input_registers(2, [int(1483)])
            
            # escreve o valor analógico nos Holding Registers
            self._db.set_holding_registers(4, [int(31)])
            self._db.set_holding_registers(6, [int(3268)])
            
            sleep(1) # delay de 1 segundo
            
            while True:
                print("======================")
                print("Tabela Modbus")
                print(f'Input Registers \r\n IR0:{self._db.get_input_registers(0)} \r\n IR2: {self._db.get_input_registers(2)}') # realiza a leitura da entrada e disponibiliza em formato de tabela
                print(f'Holding Registers \r\n HR4: {self._db.get_holding_registers(4)} \r\n HR6: {self._db.get_holding_registers(6)}')
                
                sleep(5)
                
        except Exception as e:
                print("Erro: ",e.args)

servidor = ServidorModbus('127.0.0.1', 502)
servidor.run()