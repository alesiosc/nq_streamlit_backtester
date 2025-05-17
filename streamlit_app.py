import os
import json
import pandas as pd
import streamlit as st
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Natural Language NQ Backtesting", layout="wide")
st.title("📈 Natural Language NQ Backtesting (1-min Data)")

# === Select CSV and Load ===
csv_folder = "split_chunks"
os.makedirs(csv_folder, exist_ok=True)

available_csvs = sorted([f for f in os.listdir(csv_folder) if f.endswith(".csv")])
csv_file = st.selectbox("Choose a CSV to analyze", available_csvs)

df = None
if csv_file:
    df = pd.read_csv(os.path.join(csv_folder, csv_file))
    st.dataframe(df.head())

# === Input Prompt ===
question = st.text_input("Ask a question")

# === API Key Handling ===
st.markdown("Enter your API key (OpenRouter)")
api_key = os.getenv("OPENROUTER_API_KEY", "")
user_key_input = st.text_input("🔑 API Key (optional, overrides .env)", type="password")
if user_key_input:
    api_key = user_key_input

# === Model Selection ===
model_options = [
    "meta-llama/llama-3.3-8b-instruct:free",
    "openrouter/openchat",
    "openrouter/deepseek-chat",
    "nousresearch/deephermes-3-mistral-24b",
    "mistralai/mistral-medium",
    "deepseek-ai/deepseek-coder:free"
]
model = st.selectbox("Choose model", model_options)

# === Submit Button ===
if st.button("Submit") and question and api_key:
    st.subheader("🧠 Model Response")

    try:
        csv_sample = df.head(50).to_csv(index=False) if df is not None else ""

        headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "http://localhost",
            "X-Title": "NQ Backtester"
        }

        url = "https://openrouter.ai/api/v1/chat/completions"
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a financial analyst. You will receive CSV samples from historical NQ 1-min data and be asked to analyze or backtest patterns using this data. If you are not able to execute Python, respond with the exact code you would run, and the app will handle it."},
                {"role": "user", "content": f"Here is a sample of the dataset:\n\n{csv_sample}"},
                {"role": "user", "content": question}
            ]
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()["choices"][0]["message"]["content"]
        st.markdown(result)

    except Exception as e:
        st.error(f"❌ API Error: {e}")
