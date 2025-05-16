# NQ Streamlit Backtester

This project is a **natural language backtesting assistant** built using [Streamlit](https://streamlit.io), [OpenRouter](https://openrouter.ai), and your own structured intraday CSV data (1-minute NQ futures). It allows you to:

---

### 🚀 Features

- 📂 Upload or choose CSV chunks (split by 1Y, 3Y, 5Y)
- 🧠 Ask natural language questions (e.g. "How often did price move 3% after NFP?")
- 🔁 Layer follow-up questions (e.g. "How many of those had MACD > 0?")
- 📊 View sample of loaded data and model responses
- 🔐 Secure API access using `.env` file
- 💾 Export filtered or calculated results to Excel (color formatting optional)

---

### 📦 Installation

```bash
# Clone this repo
https://github.com/alesiosc/nq_streamlit_backtester.git
cd nq_streamlit_backtester

# (Optional) Set up virtual environment
python -m venv venv
./venv/Scripts/activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

---

### 🔐 Environment Setup

Create a `.env` file in the root with:
```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

Or enter your key directly into the app UI.

---

### ▶️ Run the app
```bash
streamlit run streamlit_app.py
```
Then open your browser to [http://localhost:8501](http://localhost:8501)

---

### 🧠 Supported LLMs
- `deepseek-chat`
- `mistral-7b-instruct`
- `openchat`
- _via [OpenRouter](https://openrouter.ai)_

---

### 🗂 Folder Structure
```
├── streamlit_app.py        # Main app
├── split_chunks/           # CSVs (1Y, 3Y, 5Y)
├── .env                    # API keys (excluded)
├── .gitignore              # Good hygiene
├── requirements.txt        # Dependencies
├── README.md               # This file
```

---

### 📜 License
MIT License — free to use, extend, and adapt.

---

### 🙋‍♂️ Questions?
Open an issue or DM @alesiosc on GitHub.
