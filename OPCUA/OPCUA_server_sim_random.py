import logging
import sys
import time
import random  # Biblioteca para gerar valores aleatórios
from opcua import ua, Server

sys.path.insert(0, "..")  # Garante que a biblioteca UA pode ser importada

class SubHandlerPrint:
    
    def datachange_notification(self, node, val, data):
        node_name = node.get_display_name().Text
        print(f"{node_name}: {val}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.CRITICAL)  # Configura para que só apareça Log de Erros Críticos

    # Configuração do Servidor
    server = Server()
    server.set_endpoint(f"opc.tcp://localhost:4840")

    # Configuração do NameSpace
    uri = "AUTOMACAO"
    idx = server.register_namespace(uri)

    # Configuração dos Objects
    objects = server.get_objects_node()
    myobj = objects.add_object(idx, "Variaveis")

    # Adiciona as variáveis Reais ao Objeto Variaveis
    myReal1 = myobj.add_variable(idx, "Real1", 0.0)  # Variável Real
    myReal2 = myobj.add_variable(idx, "Real2", 0.0)

    # Adiciona as variáveis Booleanas ao Objeto Variaveis
    myBool1 = myobj.add_variable(idx, "Bool1", False)  # Variável Booleana
    myBool2 = myobj.add_variable(idx, "Bool2", False)
    
    #print(f"Real1 NodeId: {myReal1.nodeid}")
    #print(f"Real2 NodeId: {myReal2.nodeid}")
    #print(f"Bool1 NodeId: {myBool1.nodeid}")
    #print(f"Bool2 NodeId: {myBool2.nodeid}")

    # Permite escrita nas variáveis
    myReal1.set_writable()
    myReal2.set_writable()
    myBool1.set_writable()
    myBool2.set_writable()

    # Inicia o servidor OPC UA
    server.start()

    try:
        handler = SubHandlerPrint()
        sub = server.create_subscription(500, handler)  # Configura o intervalo de publicação

        # Subscreve para mudanças de dados nas variáveis
        handler1 = sub.subscribe_data_change(myReal1)
        handler2 = sub.subscribe_data_change(myReal2)
        handler3 = sub.subscribe_data_change(myBool1)
        handler4 = sub.subscribe_data_change(myBool2)

        print("Servidor operando. Pressione CTRL+C para sair...")

        while True:
            # Atualiza as variáveis com valores aleatórios a cada segundo
            real_value1 = random.uniform(0.0, 100.0)  # Valor real aleatório entre 0 e 100
            real_value2 = random.uniform(0.0, 100.0)

            bool_value1 = random.choice([True, False])  # Valor booleano aleatório
            bool_value2 = random.choice([True, False])

            myReal1.set_value(ua.DataValue(ua.Variant(real_value1, ua.VariantType.Float)))
            myReal2.set_value(ua.DataValue(ua.Variant(real_value2, ua.VariantType.Float)))

            myBool1.set_value(ua.DataValue(ua.Variant(bool_value1, ua.VariantType.Boolean)))
            myBool2.set_value(ua.DataValue(ua.Variant(bool_value2, ua.VariantType.Boolean)))

            time.sleep(1)  # Intervalo de atualização de 1 segundo

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        server.stop()
