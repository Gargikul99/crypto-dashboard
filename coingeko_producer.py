from confluent_kafka import Producer
import requests
import json
import time
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

import logging

logging.basicConfig(
    filename="producer.log",          
    filemode="a",                      
    level=logging.INFO,                
    format="%(asctime)s - %(levelname)s - %(message)s"
)

CLOUD_BOOTSTRAP_SERVERS = os.getenv("CLOUD_BOOTSTRAP_SERVERS")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")


TOPIC = "crypto-prices"

conf = {
    'bootstrap.servers': CLOUD_BOOTSTRAP_SERVERS,
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'PLAIN',
    'sasl.username': API_KEY,
    'sasl.password': API_SECRET
}

producer = Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(f"Delivered to {msg.topic()} [{msg.partition()}]")

def fetch_and_send():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"

    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                data['fetched_at'] = datetime.utcnow().isoformat()
                value = json.dumps(data)
                logging.info(f"Sent to Kafka: {value}")
                producer.produce(TOPIC, value=value, callback=delivery_report)
                producer.poll(0)
            else:
                logging.error(f"API error: Status {response.status_code} - {response.text}")
        except Exception as e:
            logging.exception(f" Exception occurred while fetching or sending: {e}")

        time.sleep(60)  

if __name__ == "__main__":
    fetch_and_send()
