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
