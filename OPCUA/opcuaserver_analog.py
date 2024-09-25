import logging
from opcua import ua, Server
import sys, time

sys.path.insert(0,"..") #Garante que a biblioteca UA pode ser importada

class SubHandlerPrint():
    
    def datachange_notification(self, node, val, data):
        node_name = node.get_display_name().Text
        print(f"{node_name}: {val}")
        
if __name__ == "__main__":
    logging.basicConfig(level=logging.CRITICAL) #Configura para que só aparece Log de Erros Criticos
    
    #Configuração do Servidor
    server = Server()
    server.set_endpoint(f"opc.tcp://192.168.0.208:4840")
    #Configuração do NameSpace
    uri = "AUTOMACAO"
    idx = server.register_namespace(uri)
    #Configuração dos Objects
    objects = server.get_objects_node()
    myobj = objects.add_object(idx, "Variaveis")
    
    # Adiciona as variáveis Reais ao Objeto Variaveis
    myReal1 = myobj.add_variable(idx, "Real1", 0.0) #Ao colocar como 0.0 0 OPC UA já interpreta como Real
    myReal2 = myobj.add_variable(idx, "Real2", 0.0)
    
    myReal1.set_writable()
    myReal2.set_writable()
    
    server.start()
    
    try:
        handler = SubHandlerPrint()
        sub = server.create_subscription(500, handler) # Configura o intervalo de publicação
        
        handler1 = sub.subscribe_data_change(myReal1)
        handler2 = sub.subscribe_data_change(myReal2)
        print("Servidor operando. Pressione CTRL+C para sair...")
        
        while True:
            time.sleep(1)  
    
    except Exception as e:
        print(f"Erro: {e}")    
    
    finally:
        server.stop()
    
