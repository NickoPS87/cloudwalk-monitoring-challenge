# Monitoring Analyst Challenge - CloudWalk

This repository contains the complete solution for the Monitoring Intelligence Analyst technical challenge. The project is divided into two main parts: an exploratory data analysis of checkout data and a prototype of an alert system for transactions.

---

## 📂 Project Structure

The repository is organized as follows:

- **/src**: Contains all the Python scripts developed for the challenge.
- **/assets**: Stores charts and images generated during the analysis.
- **/csv**: Contains the raw data files used in the challenge.
- **/[Cloudwalk].../**: Contains detailed documentation and development notes from the process (created in Obsidian).

---

## 🚀 How to Run

### Part 1: Checkout Analysis

To replicate the analysis, execute the main script:
```bash
python src/analise_checkout.py
```

# This script will generate the grafico_anomalia_checkout.png file in the assets/ folder.

### Part 2: Alerting Server
To start the monitoring system:

1. Install dependencies:
```bash
pip install Flask pandas
```
2. Start the server:
```bash
python src/servidor_de_alertas.py
```
3. To test the endpoint, use the curl commands in a separate terminal.

## 🔎 Analysis & Results

### Part 1: Anomaly in Checkout Data
The analysis revealed a sharp and total drop in sales volume at 3:00 PM (15h), a strong indicator of a system failure.

See detailed analysis documentation

See Anomaly Chart

### Part 2: Alerting System

A system was developed to alert when the volume of denied, failed, or reversed transactions exceeds a statistical threshold (mean + 2 standard deviations), calculated based on the historical data.

- **[See detailed solution documentation](./[Cloudwalk]%20Selection%20Process%20-%20Monitoring%20Intelligence%20Analyst%20(Night%20Shift)%20-%20Challenge/Solve%20the%20problem.md)**
