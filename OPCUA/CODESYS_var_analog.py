#Código para integrar um sistema de Cliente OPC/UA
#ao CODESYS sistema de programação de CLPs
# que estará rodando um sistema OPC/UA Server #

from opcua import ua, Client
import sys

sys.path.insert(0, "..")

class CodesysOPCUA():
    
    def __init__(self, ip_clp, porta):
        self._client = Client(f"opc.tcp://{ip_clp}:{porta}")
        
    def assistente(self):
        self._client.connect()
        print("Cliente OPC/UA em operação")
        assistente = True
        
        try:
            namespace = input("Informe o NameSpace: ")
            while assistente == True:
                operacao = input(f"""Deseja realizar uma leitura ou escrita? (1- Leitura | 2- Escrita | 3- Encerrar): """)
                
                if operacao == '1':
                    identifier = input(f"Informe o Identifier: ")
                    print(f"Leitura: {self.leitura(namespace, identifier)}")
                elif operacao == '2':
                    identifier = input(f"Informe o Identifier: ")
                    valor = input(f"Informe o valor que será escrito: ")
                    self.escrita(namespace,identifier, float(valor))
                elif operacao == '3':
                    self._client.disconnect()
                    break
                else:
                    print(f"Operação Inválida!")
        except Exception as e:
            print('Erro: ', e.args)
        finally:
            self._client.disconnect()
        
    def leitura(self, namespace, identifier):
        var = self._client.get_node(f"ns={namespace};s={identifier}")
        return var.get_value()
    
    def escrita(self, namespace, identifier, valor):
        var = self._client.get_node(f"ns={namespace};s={identifier}")
        return var.set_value(ua.DataValue(ua.Variant(valor, ua.VariantType.Float)))
    
s = CodesysOPCUA('localhost', 4840)
s.assistente()