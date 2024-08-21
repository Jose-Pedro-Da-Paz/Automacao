from pyModbusTCP.client import ModbusClient
from time import sleep

class ClientModbus():
    
    def __init__(self, ip_servidor, porta):
        
        self._client = ModbusClient(host = ip_servidor, port = porta)
    
    def run(self, ip, porta):
        self._client.open()
        print("Cliente Modbus em Operação")
        
        pc = ModbusClient(host=ip, port=porta)
        
        try:
            if not pc.open():
                print("Não foi possível conectar ao servidor!")
                exit()
            
            self._client.write_single_register(4, int(4000))
            self._client.write_single_register(6, int(6000))
            
            while True:
                print("======================")
                print("Tabela ModBus")
                print(f'Input Register: \r\n IR0: {self._client.read_input_registers(0)} \r\n IR2: {self._client.read_input_registers(2)}')
                print(f'Holding Registers \r\n HR4: {self._client.read_holding_registers(4)} \r\n HR6: {self._client.read_holding_registers(6)}')
                
                sleep(5)
                        
        except Exception as e:
            print("Erro: ", e.args)
            
client = ClientModbus('127.0.0.1', 502)
client.run('127.0.0.1', 502)