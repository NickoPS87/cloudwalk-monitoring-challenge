import matplotlib.pyplot as plt

# --- PASSO 3: GERAR O GRÁFICO DA ANOMALIA ---

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
