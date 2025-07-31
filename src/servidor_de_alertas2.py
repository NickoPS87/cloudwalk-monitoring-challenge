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
