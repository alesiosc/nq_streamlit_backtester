import streamlit as st
import pandas as pd
import os
import requests

st.set_page_config(page_title="📊 NQ Backtest Assistant", layout="wide")

st.title("📈 Natural Language NQ Backtesting (1-min Data)")
st.markdown("Choose a CSV, enter a question, and optionally export results.")

csv_folder = "split_chunks"
available_csvs = sorted([f for f in os.listdir(csv_folder) if f.endswith(".csv")])
selected_file = st.selectbox("Choose a CSV to analyze", available_csvs)
df = pd.read_csv(os.path.join(csv_folder, selected_file), nrows=50000)
st.dataframe(df.head(20))

user_query = st.text_input("Ask a question (e.g., 'How many times did price move 3% after NFP?')")
api_key = st.text_input("Enter your API key (DeepSeek/Mistral)", type="password")
model_endpoint = st.selectbox("Choose model provider", ["DeepSeek", "Mistral"])

def call_free_llm(query, model="deepseek", api_key=None):
    if not api_key:
        return "❌ API key required"
    url = "https://api.deepseek.com/v1/chat/completions" if model == "deepseek" else "https://api.mistral.com/v1/chat/completions"
    payload = {
        "model": "deepseek-chat" if model == "deepseek" else "mistral-small",
        "messages": [{"role": "user", "content": query}],
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=30)
        if res.status_code == 200:
            return res.json()["choices"][0]["message"]["content"]
        else:
            return f"⚠️ Error: {res.text}"
    except Exception as e:
        return f"⚠️ Request failed: {str(e)}"

if user_query and st.button("Submit"):
    with st.spinner("Asking model..."):
        answer = call_free_llm(user_query, model_endpoint.lower(), api_key)
        st.markdown("### 🧠 Response")
        st.write(answer)
