from opcua import ua, Client
import time
import sys
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import threading

sys.path.insert(0, "..")


def client_opcua():
    
    client = Client("opc.tcp://localhost:4840")
    
    try:
        client.connect() #inicia conexão
        print("Conectado ao Servidor OPC/UA!")
        
        
        #Caminho para obter as informações da variável
        myReal1 = client.get_node("ns=2;i=2")  # NodeId do Real1
        myReal2 = client.get_node("ns=2;i=3")  # NodeId do Real2
        myBool1 = client.get_node("ns=2;i=4")  # NodeId do Bool1
        myBool2 = client.get_node("ns=2;i=5")  # NodeId do Bool2
        
        while True:
            
            #coletar dados dos sensores
            real1_value = myReal1.get_value()
            real2_value = myReal2.get_value()
            bool1_value = myBool1.get_value()
            bool2_value = myBool2.get_value()
            # retorna os valores coletados
            yield real1_value, real2_value, bool1_value, bool2_value
            time.sleep(1)
        
    except Exception as e:
        print("Erro: ", e)
    
    finally:
        print("Conexão encerrada!")
        client.disconnect()

# Iniciar o Cliente OPC/UA e a aplicação Dash(Relatório)
app = Dash(__name__, suppress_callback_exceptions=True)
opcua_data = client_opcua()
opcua_data_lock = threading.Lock()

# Variáveis de estado para armazenar os dados
real1_values = []
real2_values = []
bool1_values = []
bool2_values = []

# Layout do aplicativo
app.layout = html.Div([
    dcc.Graph(id='real1-graph'),
    dcc.Graph(id='real2-graph'),
    dcc.Graph(id='bool1-graph'),
    dcc.Graph(id='bool2-graph'),
    dcc.Interval(
        id='interval-component',
        interval=5*1000,  # Atualiza a cada segundo
        n_intervals=0
    )
])

@app.callback(
    [Output('real1-graph', 'figure'),
     Output('real2-graph', 'figure'),
     Output('bool1-graph', 'figure'),
     Output('bool2-graph', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n_intervals):
    global real1_values, real2_values, bool1_values, bool2_values

    with opcua_data_lock:  # Bloqueia o acesso ao gerador
        try:
            real1, real2, bool1, bool2 = next(opcua_data)
            print(f"Valores recebidos: Real1={real1}, Real2={real2}, Bool1={bool1}, Bool2={bool2}")

            # Armazena os valores para gráficos contínuos
            real1_values.append(real1)
            real2_values.append(real2)
            bool1_values.append(int(bool1))
            bool2_values.append(int(bool2))

            # Cria as figuras para cada gráfico
            real1_fig = {
                'data': [{'x': list(range(len(real1_values))), 'y': real1_values, 'type': 'line', 'name': 'Real1'}],
                'layout': {'title': 'Real1 ao Longo do Tempo'}
            }

            real2_fig = {
                'data': [{'x': list(range(len(real2_values))), 'y': real2_values, 'type': 'line', 'name': 'Real2'}],
                'layout': {'title': 'Real2 ao Longo do Tempo'}
            }

            bool1_fig = {
                'data': [{'x': list(range(len(bool1_values))), 'y': [int(b) for b in bool1_values], 'type': 'line', 'name': 'Bool1'}],
                'layout': {'title': 'Bool1 ao Longo do Tempo'}
            }

            bool2_fig = {
                'data': [{'x': list(range(len(bool2_values))), 'y': [int(b) for b in bool2_values], 'type': 'line', 'name': 'Bool2'}],
                'layout': {'title': 'Bool2 ao Longo do Tempo'}
            }

            return real1_fig, real2_fig, bool1_fig, bool2_fig

        except StopIteration:
            print("Fim dos dados do OPC/UA")
        except Exception as e:
            print(f"Erro ao acessar o gerador: {e}")

if __name__ == '__main__':
    app.run_server(debug=True)