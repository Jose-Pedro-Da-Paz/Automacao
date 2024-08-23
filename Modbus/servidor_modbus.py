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
            
            # escreve o valor digital nas entradas
            self._db.set_discrete_inputs(0, [False])
            self._db.set_discrete_inputs(1, [True])
            
            # escreve o valor nas Coils
            self._db.set_coils(0, [True])
            self._db.set_coils(1, [False])
            
            sleep(1) # delay de 1 segundo
            
            while True:
                print("======================")
                print("Tabela Modbus")
                print(f'Discrete Inputs \r\n DI0: {self._db.get_discrete_inputs(0)}\r\n DI1: {self._db.get_discrete_inputs(1)}') # realiza a leitura da entrada e disponibiliza em formato de tabela
                print(f'Coils \r\n C0: {self._db.get_coils(0)} \r\n C1: {self._db.get_coils(1)}')
                
                sleep(5)
                
        except Exception as e:
                print("Erro: ",e.args)

servidor = ServidorModbus('127.0.0.1', 502)
servidor.run()