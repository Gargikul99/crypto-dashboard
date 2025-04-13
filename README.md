# Real-Time Crypto Streaming Dashboard

This project demonstrates a fully cloud-native, real-time streaming pipeline that ingests live cryptocurrency data, processes it using modern data engineering tools, and visualizes it through an interactive dashboard.

## Project Overview

The pipeline continuously fetches Bitcoin and Ethereum prices from CoinGecko and pushes them to Kafka. From there, Databricks reads the stream and writes it into Delta Lake tables. A public Streamlit dashboard visualizes this data.

## Tech Stack

- CoinGecko API – Live crypto market data source
- Python Kafka Producer – Hosted on Azure VM to push data to Kafka
- Confluent Kafka Cloud – Cloud-based streaming platform
- Databricks – Streaming pipeline and Delta table management
- Delta Lake – Storage format for streaming & batch processing
- Streamlit Cloud – Deployed interactive dashboard

## Pipeline Architecture


CoinGecko API → Azure VM (Python Producer) → Confluent Kafka → Databricks Delta Table → Streamlit Dashboard


## Features

- Real-time ingestion and processing of Bitcoin & Ethereum prices
- Cloud-hosted Kafka producer
- Delta Lake-backed streaming table on Databricks
- Auto-refreshing public dashboard using Streamlit
- Fully cloud-native and scalable

## Live Demo

Dashboard: [Streamlit App](https://streamlit.io/crypto-dashboard)  
GitHub Repo: [github.com/Gargikul99/crypto-dashboard](https://github.com/Gargikul99/crypto-dashboard)  
Demo Video: *Attach in LinkedIn post or README if available*

## What I Learned

This project wasn’t just about writing code — it deepened my understanding of how production-grade streaming systems work, including message delivery, Delta streaming internals, cloud orchestration, and real-time analytics.

## How to Run

**Kafka producer:**
1. SSH into your Azure VM
2. Run coingeko_producer.py with nohup python3 coingeko_producer.py &

**Streamlit dashboard:**
1. Deploy streamlit_app.py to [Streamlit Cloud](https://streamlit.io/cloud)
2. Connect to Databricks SQL warehouse with Delta table access

## Connect
Open to feedback, collaborations, or just chatting about real-time data systems.


#Kafka #Databricks #Streamlit #Azure #Python #RealTimeData #DataEngineering #PortfolioProject

