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