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
        
        #explore_node(root)
        
        #Caminho para obter as informações da variável
        myReal1 = root.get_child(["0:Objects", "2:Variaveis", "2:Real1"]) #obtém nó filho da raiz
        myReal2 = root.get_child(["0:Objects", "2:Variaveis", "2:Real2"])
        
        print("myReal1 =", myReal1.get_value())
        print("myReal2 =", myReal2.get_value())
        
        while True:
            sleep(5)
            myReal1.set_value(ua.DataValue(ua.Variant(50.25, ua.VariantType.Float)))
            myReal2.set_value(ua.DataValue(ua.Variant(100.25, ua.VariantType.Float)))
            sleep(5)
            myReal1.set_value(ua.DataValue(ua.Variant(250.85, ua.VariantType.Float)))
            myReal2.set_value(ua.DataValue(ua.Variant(500.85, ua.VariantType.Float)))
        
    except Exception as e:
        print("Erro: ", e)
    
    finally:
        print("Conexão encerrada!")
        client.disconnect()