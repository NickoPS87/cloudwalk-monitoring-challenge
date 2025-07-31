
#Objetivo: ***Projetar um sistema de monitoramento e alerta que detecta quando transações com falha, revertidas ou negadas estão acima do normal.***


#Raciocínio: ***Primeiro é necessário carregar e entender os novos dados. São dois arquivos: um com as transações e outro que descreve os códigos de status. Em seguida, combinar ambos os arquivos.***

***→ Transactions***
![[Transactions.png]]
****Obs: Imagem é apenas uma amostra do arquivo "Transactions.csv". O arquivo possui 25.921 linhas.

***→ Transactions_auth_codes 1***
![[Transactions_auth_codes 1.png]]
****Obs: Imagem é apenas uma amostra do arquivo "Transactions_auth_codes 1.csv". O arquivo possui 12.961 linhas.



==***Passo 1: Criar um Código Para Carregar e Preparar os Dados de Transações***==

#Raciocínio ***Da perspectiva de cibersegurança: eu tenho um log de eventos (ex: ID de regra de firewall), mas esses eventos não significam nada sozinhos. Eu preciso de uma tabela separada para traduzir o ID em uma descrição (ex: "Acesso de IP malicioso bloqueado").***


***► Criação de um novo script Python. Arquivo: "sistema_alertas.py" ***
```
import pandas as pd

# O único URL que precisamos é o de transações
url_trans = 'https://raw.githubusercontent.com/everton-cw/monitoring_test/main/transactions.csv'

print("--- Carregando dataset de transações ---")
try:
    # Usamos o 'encoding' para garantir que não haverá erros de leitura
    df = pd.read_csv(url_trans, encoding='utf-8-sig')
    print("Dataset carregado com sucesso.")
except Exception as e:
    print(f"Erro ao carregar o arquivo: {e}")
    exit()

# --- Organizando os Dados ---
# O passo mais importante: transformar a tabela para o formato correto.
# Queremos que cada 'status' de transação vire uma coluna. Usamos pivot_table para isso.

print("\n--- Reorganizando a tabela (pivot) ---")
# Converte a coluna de tempo para o formato de data/hora
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Cria a tabela pivotada
df_pivot = df.pivot_table(
    index='timestamp',    # As linhas serão os momentos no tempo
    columns='status',     # As colunas serão os diferentes status (Approved, Denied, etc)
    values='count',       # Os valores dentro da tabela serão a contagem (count)
    fill_value=0          # Se não houver um status em um timestamp, preenche com 0
)

print("Tabela reorganizada com sucesso.")
print("\nAmostra da nova tabela de dados:")
print(df_pivot.head())

print("\nColunas disponíveis para monitoramento:")
print(df_pivot.columns.tolist())
```


***► Qual o raciocínio por trás da criação do código?***

**→ A função do código é preparar os dados no formato ideal para:**

1. **Criar gráficos:** Facilita plotar cada status como uma linha diferente em um gráfico de tempo.

2. **Análise Comparativa:** Permite comparar diretamente o número de transações aprovadas versus negadas no mesmo instante.

→ De forma sucinta, o código faz o seguinte:

- Pega um registro bruto e o transforma em uma série temporal pronta para análise e visualização.
- Transforma a tabela de um formato de "lista de eventos" para um formato de "painel de controle" (dashboard).



==**Passo 2: Execução do código python**==

***Resultado do código:***
![[sistemas_alerta.py.png]]
#Analise: ***Como resultado eu obtive uma tabela onde cada linha é um minuto e cada coluna é um tipo de transação. Com isso, podemos criar os alertas facilmente. Com isso poderei definir as regras de alerta.***


==***Passo 3: Criação de Código Para Definir a "Normalidade" e as Regras de Alerta***==

#Raciocínio: *O desafio pede para alertar quando as transações `denied`, `failed` e `reversed` estiverem "acima do normal". Uma abordagem estatística comum e eficaz é usar a média + um número de desvios padrão:*
- **Média (`mean`):** O valor comum de transações de um certo status por minuto. 
- **Desvio Padrão (`std`):** O quanto esse valor costuma variar.

#Regra: Se o valor atual for maior que a `média + 2 * desvio_padrão`, é uma anomalia. Portanto, deve ser alertada.


***► Bloco de código adicionado ao final do script `sistema_alertas.py`:***
```
# --- DEFINIR REGRAS E LIMITES DE ALERTA ---

print("\n--- Calculando Limites para Alertas (Média + 2 * Desvio Padrão) ---")

# Colunas que queremos monitorar
colunas_para_alertar = ['denied', 'failed', 'reversed']

# Dicionário para guardar os limites de cada status
limites_de_alerta = {}

for status in colunas_para_alertar:
    media = df_pivot[status].mean()
    desvio_padrao = df_pivot[status].std()
    # Definimos o limite como a média mais dois desvios padrão
    limite = media + (2 * desvio_padrao)
    limites_de_alerta[status] = limite
    print(f"Limite de alerta para '{status}': {limite:.2f} transações por minuto.")


# --- Simulação da Verificação de Alertas ---
print("\n--- Simulando a verificação de alertas nos 5 primeiros minutos ---")

# Vamos checar as 5 primeiras linhas (minutos) da nossa tabela
for timestamp, linha in df_pivot.head().iterrows():
    print(f"\nVerificando o minuto: {timestamp}")
    for status in colunas_para_alertar:
        valor_atual = linha[status]
        limite_atual = limites_de_alerta[status]
        
        # Verifica se o valor atual excede o limite
        if valor_atual > limite_atual:
            print(f"  -> ALERTA! Status '{status}' está acima do normal. Valor: {valor_atual}, Limite: {limite_atual:.2f}")
        else:
            print(f"  -> OK. Status '{status}' está normal. Valor: {valor_atual}, Limite: {limite_atual:.2f}")
```
***►Analise do resultado: O código acima calcula os limites para os status que me interessam (`denied`, `failed`, `reversed`) e depois simula a verificação desses alertas. O retorno obtido foi o seguinte:***

- Os limites calculados para `denied`, `failed` e `reversed`. Você verá uma frase como: "Limite de alerta para 'denied': 8.50 transações por minuto."
- Uma simulação para os 5 primeiros minutos, mostrando se cada status geraria um alerta ou não, comparando o valor do minuto com o limite calculado.

*→ Em outras palavras: a simulação mostra minha lógica de alerta funcionando, identificando corretamente os momentos em que o status `reversed` ultrapassou o limite.*



==***Passo Final: Código Para Criar o Endpoint de Alerta com Flask***==

#Raciocínio Vou utilizar o *Flask* para criar pequenos servidores web. Este código final combina tudo o que foi feio em um único arquivo que roda um servidor de alerta.

***► Script "servidor_de_alertas.py":***
```
import pandas as pd
from flask import Flask, request, jsonify

# --- 1. PREPARAÇÃO INICIAL (executa uma vez quando o servidor sobe) ---

print("--- Iniciando o servidor de alertas ---")
# Carrega e prepara os dados históricos para definir a normalidade
url_trans = 'https://raw.githubusercontent.com/everton-cw/monitoring_test/main/transactions.csv'
df = pd.read_csv(url_trans, encoding='utf-8-sig')
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Cria a tabela pivotada com os status como colunas
df_pivot = df.pivot_table(
    index='timestamp',
    columns='status',
    values='count',
    fill_value=0
)
print("Dados históricos carregados e preparados.")

# Calcula e armazena os limites de alerta
colunas_para_alertar = ['denied', 'failed', 'reversed']
limites_de_alerta = {}
for status in colunas_para_alertar:
    media = df_pivot[status].mean()
    desvio_padrao = df_pivot[status].std()
    limite = media + (2 * desvio_padrao)
    limites_de_alerta[status] = limite
    print(f"-> Limite de alerta para '{status}' definido como: {limite:.2f}")

# --- 2. CRIAÇÃO DO SERVIDOR E DO ENDPOINT ---

app = Flask(__name__)

# Define o endpoint '/check' que aceita requisições POST
@app.route('/check', methods=['POST'])
def check_transaction_data():
    """
    Recebe dados de transações do último minuto via JSON e retorna
    uma recomendação de 'alert' ou 'ok'.
    """
    # Pega os dados JSON enviados na requisição
    dados_minuto_atual = request.get_json()

    if not dados_minuto_atual:
        return jsonify({"error": "Nenhum dado enviado"}), 400

    alertas_gerados = []

    # Compara os dados recebidos com os limites pré-calculados
    for status in colunas_para_alertar:
        valor_atual = dados_minuto_atual.get(status, 0) # Pega o valor, ou 0 se não for enviado
        limite_atual = limites_de_alerta[status]

        if valor_atual > limite_atual:
            alerta = {
                "status": status,
                "valor_atual": valor_atual,
                "limite": round(limite_atual, 2)
            }
            alertas_gerados.append(alerta)

    # Monta a resposta final
    if alertas_gerados:
        return jsonify({
            "recommendation": "alert",
            "details": alertas_gerados
        })
    else:
        return jsonify({"recommendation": "ok"})


# --- 3. EXECUÇÃO DO SERVIDOR ---

if __name__ == '__main__':
    # Roda o servidor na porta 5000
    print("\nServidor pronto para receber requisições em http://127.0.0.1:5000/check")
    app.run(debug=True, port=5000)
```

==*Utilizando e Testando*==

***► Passo A: Rodar o Servidor:***
![[servidor_de_alertas.py.png]]
#Analise: *Como resultado eu obtenho as mensagens de inicialização e por último uma linha dizendo que o servidor está rodando. *

***► Passo B: Testando o Endpoint (em outro terminal):***
1. *Cenário Normal (não deve gerar alerta): curl -X POST -H "Content-Type: application/json" -d "{\"denied\": 10, \"failed\": 0, \"reversed\": 1}" http://127.0.0.1:5000/check*
![[Cenário Normal.png]]
2. *Cenário de Anomalia (deve gerar alerta): curl -X POST -H "Content-Type: application/json" -d "{\"denied\": 10, \"failed\": 0, \"reversed\": 5}" http://127.0.0.1:5000/check*
![[Cenário de Anomalia.png]]


# Conclusão

Com base nas imagens, o cenário demonstra o teste de um endpoint de API (`http://127.0.0.1:5000/check`) que parece analisar dados de transações para emitir uma recomendação.

## **Análise do Cenário:**

1. **Primeiro Teste (Resultado "ok"):**
    
    - **Requisição:** Um `POST` é enviado com o seguinte payload JSON: `{"denied": 10, "failed": 0, "reversed": 1}`.
        
    - **Resposta:** A API retorna `{"recommendation": "ok"}`.
        
    - **Conclusão:** Com 1 transação "reversed", a situação é considerada normal.
        
2. **Segundo Teste (Resultado "alert"):**
    
    - **Requisição:** Um `POST` é enviado com o payload JSON modificado: `{"denied": 10, "failed": 0, "reversed": 5}`. A única alteração foi o aumento no valor de `"reversed"`.
        
    - **Resposta:** A API retorna um alerta com detalhes: `{"details": [{"limite": 2.98, "status": "reversed", "valor_atual": 5}], "recommendation": "alert"}`.
        
    - **Conclusão:** Ao aumentar o número de transações "reversed" para 5, o sistema gerou um alerta. A resposta indica que o `valor_atual` (5) para o status `"reversed"` ultrapassou o `limite` definido de 2.98.
        

==***Em resumo, o sistema de monitoramento está configurado para disparar um alerta quando o número de transações estornadas (`reversed`) excede um limite pré-estabelecido, que neste caso é de aproximadamente 2.98.***==
