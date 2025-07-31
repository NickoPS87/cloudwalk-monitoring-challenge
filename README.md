# Desafio de Análise de Monitoramento - CloudWalk

Este repositório contém a solução completa para o desafio técnico da vaga de Monitoring Intelligence Analyst. O projeto está dividido em duas partes principais: uma análise exploratória de dados de checkout e a prototipação de um sistema de alertas para transações.

---

## 📂 Estrutura do Projeto

O repositório está organizado da seguinte forma:

- **/src**: Contém todos os scripts Python desenvolvidos.
- **/assets**: Armazena os gráficos e imagens gerados pela análise.
- **/csv**: Contém os arquivos de dados brutos utilizados no desafio.
- **/[Cloudwalk].../**: Contém a documentação detalhada e as notas do processo de desenvolvimento (feito no Obsidian).

---

## 🚀 Como Executar

### Parte 1: Análise de Checkout

Para replicar a análise, execute o script principal:
```bash
python src/analise_checkout.py

---

## 🔎 Análise e Resultados

### Parte 1: Anomalia nos Dados de Checkout

A análise revelou uma queda abrupta e total no volume de vendas às **15h**, um forte indicativo de falha sistêmica.

- **[Ver documentação detalhada da Análise](./[Cloudwalk]%20Selection%20Process%20-%20Monitoring%20Intelligence%20Analyst%20(Night%20Shift)%20-%20Challenge/Get%20your%20hands%20dirty.md)**
- **[Ver Gráfico da Anomalia](./assets/grafico_anomalia_checkout.png)**

### Parte 2: Sistema de Alertas

Foi desenvolvido um sistema que alerta quando o volume de transações `denied`, `failed` ou `reversed` excede um limiar estatístico (média + 2 desvios padrão), calculado com base no histórico dos dados.

- **[Ver documentação detalhada da Solução](./[Cloudwalk]%20Selection%20Process%20-%20Monitoring%20Intelligence%20Analyst%20(Night%20Shift)%20-%20Challenge/Solve%20the%20problem.md)**
