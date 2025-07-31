import pandas as pd
import re

# URLs dos datasets fornecidos no desafio
url1 = 'https://raw.githubusercontent.com/thais-menezes/monitoring/main/checkout_1.csv'
url2 = 'https://raw.githubusercontent.com/thais-menezes/monitoring/main/checkout_2.csv'

# Carregar os dois arquivos CSV em DataFrames
try:
    df1 = pd.read_csv(url1)
    df2 = pd.read_csv(url2)
    print("Arquivos CSV carregados com sucesso.")
except Exception as e:
    print(f"Erro ao carregar os arquivos: {e}")
    exit()

# Juntar os dois DataFrames em um só
df_total = pd.concat([df1, df2], ignore_index=True)
print("DataFrames combinados.")

# --- INSPECIONAR OS DADOS (VERSÃO CORRIGIDA) ---

# 1. Visualizar as 5 primeiras linhas para entender a estrutura
print("\n--- 1. Amostra dos Dados (head) ---")
print(df_total.head())

# 2. Obter informações sobre os tipos de dados e valores nulos
print("\n--- 2. Informações Gerais (info) ---")
df_total.info()

# 3. Obter estatísticas descritivas das colunas numéricas
print("\n--- 3. Estatísticas Descritivas (describe) ---")
print(df_total.describe())

# 4. (Opcional, mas recomendado) Limpar a coluna 'time' para ser numérica
# A coluna 'time' está como '00h', '01h', etc. Convertê-la para um número (0, 1)
# facilita a ordenação e a criação de gráficos.
print("\n--- 4. Limpando a coluna 'time' ---")
# Usamos uma expressão regular para extrair apenas os dígitos
df_total['hour'] = df_total['time'].str.extract('(\d+)').astype(int)
df_total = df_total.sort_values(by='hour') # Ordenar do início para o fim do dia
print("Coluna 'hour' numérica criada e dados ordenados.")
print(df_total.head())

# --- ENCONTRAR A ANOMALIA ---

print("\n--- Análise de Anomalias ---")
# Vamos calcular a diferença entre as vendas de hoje e a média da semana anterior
df_total['diff_today_vs_avg_week'] = df_total['today'] - df_total['avg_last_week']

# Agora, vamos ordenar os dados para ver onde a diferença foi maior (positiva ou negativa)
df_sorted_by_diff = df_total.sort_values(by='diff_today_vs_avg_week', ascending=False)

print("\nHoras com MAIS vendas que a média da semana:")
print(df_sorted_by_diff.head(5))

print("\nHoras com MENOS vendas que a média da semana:")
print(df_sorted_by_diff.tail(5))

import matplotlib.pyplot as plt

# --- GERAR O GRÁFICO DA ANOMALIA ---

print("\n--- Gerando gráfico da anomalia ---")

# Configurar o gráfico
plt.figure(figsize=(12, 6)) # Tamanho da figura

# Plotar as linhas
plt.plot(df_total['hour'], df_total['today'], marker='o', linestyle='-', label='Vendas de Hoje (Today)')
plt.plot(df_total['hour'], df_total['avg_last_week'], marker='x', linestyle='--', label='Média da Semana Anterior (avg_last_week)')

# Adicionar a anotação da anomalia
plt.annotate('Anomalia: Queda Total de Vendas',
             xy=(15, 0), # Ponto exato da anomalia
             xytext=(10, 10), # Posição do texto
             arrowprops=dict(facecolor='black', shrink=0.05),
             fontweight='bold')

# Títulos e legendas
plt.title('Comparativo de Vendas por Hora: Hoje vs Média da Semana Anterior')
plt.xlabel('Hora do Dia')
plt.ylabel('Número de Vendas')
plt.xticks(range(0, 24)) # Forçar todos os ticks de hora no eixo X
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend()

# Salvar o gráfico em um arquivo e exibi-lo
plt.savefig('grafico_anomalia_checkout.png')
print("Gráfico salvo como 'grafico_anomalia_checkout.png'")
plt.show()
