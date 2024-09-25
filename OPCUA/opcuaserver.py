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
    
    # Adiciona as variáveis Booleanas ao Objeto Variaveis
    myBool1 = myobj.add_variable(idx, "Bool1", False)
    myBool2 = myobj.add_variable(idx, "Bool2", False)
    
    myBool1.set_writable()
    myBool2.set_writable()
    
    server.start()
    
    try:
        handler = SubHandlerPrint()
        sub = server.create_subscription(500, handler) # Configura o intervalo de publicação
        
        handler1 = sub.subscribe_data_change(myBool1)
        handler2 = sub.subscribe_data_change(myBool2)
        print("Servidor operando. Pressione CTRL+C para sair...")
        
        while True:
            time.sleep(1)  
    
    except Exception as e:
        print(f"Erro: {e.args}")    
    
    finally:
        server.stop()
    
