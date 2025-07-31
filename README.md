Desafio de Análise de Monitoramento - CloudWalk
Este repositório contém a solução completa para o desafio técnico da vaga de Monitoring Intelligence Analyst. O projeto está dividido em duas partes principais: uma análise exploratória de dados de checkout e a prototipação de um sistema de alertas para transações.

📂 Estrutura do Projeto
O repositório está organizado da seguinte forma:

/src: Contém todos os scripts Python desenvolvidos.

/assets: Armazena os gráficos e imagens gerados pela análise.

/csv: Contém os arquivos de dados brutos utilizados no desafio.

/[Cloudwalk].../: Contém a documentação detalhada e as notas do processo de desenvolvimento (feito no Obsidian).

🚀 Como Executar
Parte 1: Análise de Checkout
Para replicar a análise, execute o script principal:

Bash

python src/analise_checkout.py
Este script irá gerar o arquivo grafico_anomalia_checkout.png na pasta assets/.

Parte 2: Servidor de Alertas
Para iniciar o sistema de monitoramento:

Instale as dependências: pip install Flask pandas

Inicie o servidor:

Bash

python src/servidor_de_alertas.py
Para testar o endpoint, use os comandos curl em outro terminal.

🔎 Análise e Resultados
Parte 1: Anomalia nos Dados de Checkout
A análise revelou uma queda abrupta e total no volume de vendas às 15h, um forte indicativo de falha sistêmica.

Ver documentação detalhada da Análise

Ver Gráfico da Anomalia

Parte 2: Sistema de Alertas
Foi desenvolvido um sistema que alerta quando o volume de transações denied, failed ou reversed excede um limiar estatístico (média + 2 desvios padrão), calculado com base no histórico dos dados.

Ver documentação detalhada da Solução
