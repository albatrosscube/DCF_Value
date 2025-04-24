# 💸 Streamlit DCF Valuation App

A simple and powerful **Discounted Cash Flow (DCF) Valuation Tool** built with [Streamlit](https://streamlit.io) and [yfinance](https://pypi.org/project/yfinance/).

This app lets you analyze the intrinsic value of public companies based on projected Free Cash Flow, discount rates, and growth assumptions.

---

## 🚀 Features

- Pulls **real-time financials** via Yahoo Finance
- Calculates **average Free Cash Flow (FCF)**
- Performs full **DCF analysis** with:
  - 5-year FCF projections
  - Terminal value using Gordon Growth Model
- Adjusts for **net debt** (Total Debt - Cash)
- Displays **intrinsic value per share**
- Renders a **sensitivity matrix and heatmap** (growth vs. discount rate)

---

## 📈 Example Output

![Heatmap Example](https://user-images.githubusercontent.com/yourusername/yourimage.png)

---

## 🛠 How to Run Locally

```bash
# Clone the repo
git clone https://github.com/yourusername/dcf-valuation-app.git
cd dcf-valuation-app

# Create a virtual environment (optional)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run streamlit_dcf_app.py
