

==**Passo 1: Carregar e Inspecionar os Dados de Checkout**==

→ Checkout_1
![[Checkout_1.png]]
→ Checkout_2
![[Checkout_2.png]]

==**Passo 2: Código para Análise Exploratória**==

→ **Criação de um Script Python. Arquivo: "analise_checkout.py":**
```
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
```
***► Qual o raciocínio por trás da criação do código?***

	→ Pensei em utilizar o processo de ETL (Extract, Transform, Load).

→ De forma sucinta, o código faz o seguinte:

- **Extrai:** Pega dados brutos de diferentes fontes (os dois arquivos CSV).
- **Transforma:** Limpa e formata esses dados, convertendo a coluna de tempo em um formato numérico e ordenando a tabela para que faça sentido cronologicamente.
- **Carrega:** Disponibiliza o resultado (a tabela limpa e ordenada) para ser usado na próxima etapa, que seria a análise de fato, a criação de gráficos ou a geração de relatórios.

Em resumo, a função do código é deixar dados "sujos" e desorganizados prontos para uma análise útil.


==**Passo 3: Execução do código python**==

***Resultado do código:***
![[analise_checkout.py.png]]


==**Passo 4: Identificação do Comportamento Anômalo**==

► Como o desafio pede para "entender se há algum tipo de comportamento anômalo". Entendo que a maneira mais direta de fazer isso é comparar a coluna `today` com as colunas de referência (`yesterday`, `avg_last_week`, `avg_last_month`).

► Para isso vou adicionar um bloco de código ao arquivo "analise_checkout,py" que calcula a diferença entre as vendas de hoje e a média da última semana. Isso vai destacar as horas onde o comportamento de hoje foi mais incomum.

***Novo código com a inserção do bloco de análise exploratória:***
```
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
```
***Resultado do código:***
![[analise_exploratoria.py.png]]

***Análise da nova saída:*** 

→ O retorno nos trouxe duas tabelas:

- As 5 horas em que as vendas de `today` mais superaram a média da semana.
- As 5 horas em que as vendas de `today` mais ficaram abaixo da média da semana.
- Foco na última tabela, "Horas com MENOS vendas que a média da semana".


***Insight Principal - Anomalia Encontrada***

**→ A anomalia mais clara e crítica está na linha do tempo `15h`:**
- **`time`**: `15h`
- **`today`**: `0`
- **`avg_last_week`**: `22.427`
- **`diff_today_vs_avg_week`**: `-22.427`

#Conclusão: ***Às 15h, as vendas de "today" *caíram para zero*, enquanto o normal para esse horário (baseado na média da semana anterior) seria de aproximadamente 22 vendas. Uma queda total como essa é um forte indicativo de uma *falha crítica no sistema (ex: o gateway de pagamento caiu, um serviço ficou offline, etc.).***



==***Passo 5: Criar a Query SQL e o Gráfico***==

#Ação: ***transformar essa descoberta nos dois entregáveis que o desafio pede.***

#Raciocínio: ***O desafio pede uma query SQL que ajude a explicar a anomalia. Mesmo que esteja utilizando o Pandas, vou escrever a query como se os dados estivessem em um banco de dados. Desta forma, selecionando os dados que necessários para criação do gráfico.***


==***► Query SQL:***==
```
-- Query para comparar as vendas de hoje com a média da semana anterior, por hora.
-- O objetivo é visualizar a queda abrupta que indica a anomalia.

SELECT
    time,
    today,
    avg_last_week
FROM
    checkouts -- (Imaginando que os dados estão em uma tabela chamada 'checkouts')
ORDER BY
    CAST(REPLACE(time, 'h', '') AS INTEGER);
```

==***► Código Python para criação do gráfico:***==

#Raciocínio: ***O melhor jeito de mostrar a anomalia é com um gráfico de linhas. Ele vai exibir claramente a linha de `today` caindo para zero enquanto a linha da média se mantém.***

***→ Bloco de código ao final do seu script `analise_checkout.py`***
```
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
```

==***► O Gráfico***==

![[grafico_anomalia_checkout.png]]

#Analise:***O gráfico mostra de forma clara e inquestionável a anomalia que descoberta: a queda total nas vendas às 15h.***

