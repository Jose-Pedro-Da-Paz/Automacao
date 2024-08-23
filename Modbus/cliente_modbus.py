from pyModbusTCP.client import ModbusClient
from time import sleep

class ClientModbus():
    
    def __init__(self, ip_servidor, porta):
        
        self._client = ModbusClient(host = ip_servidor, port = porta)
    
    def run(self):
        self._client.open()
        print("Cliente Modbus em Operação")
        
        pc = ModbusClient(host= '127.0.0.1', port=502)
        
        try:
            if not pc.open():
                print("Não foi possível conectar ao servidor!")
                exit()
            
            self._client.write_single_coil(0, [True])
            self._client.write_single_coil(1, [True])
            
            while True:
                print("======================")
                print("Tabela ModBus")
                print(f'Discrete Input: \r\n DI0: {self._client.read_discrete_inputs(0)} \r\n DI1: {self._client.read_discrete_inputs(1)}')
                print(f'Coils \r\n C0: {self._client.read_coils(0)} \r\n C1: {self._client.read_coils(1)}')
                
                
                sleep(5)
                        
        except Exception as e:
            print("Erro: ", e.args)
            
client = ClientModbus('127.0.0.1', 502)
client.run()