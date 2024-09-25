from opcua import ua, Client
from time import sleep
import sys

sys.path.insert(0, "..")

def explore_node(node, depth=0):
    # Imprime o nome do nó com indentação para mostrar a profundidade
    indent = "  " * depth
    print(f"{indent}{node.get_browse_name().Name} (NodeId: {node.nodeid})")

    # Recursivamente explora os filhos do nó
    #for child in node.get_children():
        #explore_node(child, depth + 1)


if __name__ == "__main__":
    client = Client("opc.tcp://192.168.0.208:4840")
    
    try:
        client.connect() #inicia conexão
        print("Conectado ao Servidor!")
        
        root = client.get_root_node() #obtém nó raiz do servidor
        
        explore_node(root)
        
        #Caminho para obter as informações da variável
        myBool1 = root.get_child(["0:Objects", "2:Variaveis", "2:Bool1"]) #obtém nó filho da raiz
        myBool2 = root.get_child(["0:Objects", "2:Variaveis", "2:Bool2"])
        
        print("MyBool1 =", myBool1.get_value())
        print("MyBool2 =", myBool2.get_value())
        
        while True:
            sleep(5)
            myBool1.set_value(ua.DataValue(ua.Variant(True, ua.VariantType.Boolean)))
            myBool2.set_value(ua.DataValue(ua.Variant(True, ua.VariantType.Boolean)))
            sleep(5)
            myBool1.set_value(ua.DataValue(ua.Variant(False, ua.VariantType.Boolean)))
            myBool2.set_value(ua.DataValue(ua.Variant(False, ua.VariantType.Boolean)))
        
    except Exception as e:
        print("Erro: ", e)
    
    finally:
        print("Conexão encerrada!")
        client.disconnect()    
        
        
        