import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Attempt to import yfinance
try:
    import yfinance as yf
except ImportError:
    st.error("❌ The 'yfinance' module is not available. Please install it using: pip install yfinance")
    st.stop()

# DCF valuation function
def dcf_valuation(avg_fcf, shares_outstanding, net_debt, growth_rate, discount_rate, terminal_growth=0.02, years=5):
    dcf_value = 0
    for year in range(1, years + 1):
        projected_fcf = avg_fcf * ((1 + growth_rate) ** year)
        dcf_value += projected_fcf / ((1 + discount_rate) ** year)

    terminal_fcf = avg_fcf * ((1 + growth_rate) ** years)
    terminal_value = (terminal_fcf * (1 + terminal_growth)) / (discount_rate - terminal_growth)
    terminal_value_discounted = terminal_value / ((1 + discount_rate) ** years)

    total_intrinsic_value = dcf_value + terminal_value_discounted
    equity_value = total_intrinsic_value - net_debt
    return equity_value / shares_outstanding if shares_outstanding else 0

# App title
st.title("📊 Intrinsic Value Estimator (DCF Model)")
st.markdown("Enter a stock ticker to estimate its intrinsic value using a Discounted Cash Flow (DCF) model.")

# Ticker input
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA, MSFT):").upper()

if ticker:
    stock = yf.Ticker(ticker)

    try:
        cf = stock.cashflow.T
        bs = stock.balance_sheet
        info = stock.info
        shares_outstanding = info.get("sharesOutstanding", None)

        op_cashflow = cf['Operating Cash Flow']
        capex = cf['Capital Expenditure']
        fcf = op_cashflow + capex
        avg_fcf = fcf.dropna().head(5).mean()

        cash_keys = ['Cash', 'Cash And Cash Equivalents', 'Cash And Short Term Investments']
        debt_keys = ['Total Debt', 'Short Long Term Debt Total', 'Long Term Debt']

        cash = next((bs.loc[k].iloc[0] for k in cash_keys if k in bs.index), 0)
        total_debt = next((bs.loc[k].iloc[0] for k in debt_keys if k in bs.index), 0)
        net_debt = total_debt - cash

        st.markdown(f"### 🧾 Assumptions for {ticker}")
        st.write(f"**Average FCF (5Y):** ${avg_fcf:,.0f}")
        st.write(f"**Total Debt:** ${total_debt:,.0f}")
        st.write(f"**Cash:** ${cash:,.0f}")
        st.write(f"**Net Debt:** ${net_debt:,.0f}")
        st.write(f"**Shares Outstanding:** {shares_outstanding:,}")

        discount_rates = [0.08, 0.09, 0.10, 0.11]
        growth_rates = [0.06, 0.08, 0.10, 0.12]
        sensitivity = pd.DataFrame(index=[f"{int(gr*100)}%" for gr in growth_rates],
                                   columns=[f"{int(dr*100)}%" for dr in discount_rates])

        for gr in growth_rates:
            for dr in discount_rates:
                value = dcf_valuation(avg_fcf, shares_outstanding, net_debt, gr, dr)
                sensitivity.loc[f"{int(gr*100)}%", f"{int(dr*100)}%"] = round(value, 2)

        st.markdown("### 📊 Sensitivity Analysis (Intrinsic Value per Share)")
        st.dataframe(sensitivity)

        # Plot heatmap
        fig, ax = plt.subplots()
        sns.heatmap(sensitivity.astype(float), annot=True, fmt=".2f", cmap="YlGnBu", cbar=True,
                    ax=ax, linewidths=0.5, linecolor='gray')
        ax.set_title(f"DCF Sensitivity for {ticker} (Growth vs. Discount Rate)")
        ax.set_xlabel("Discount Rate")
        ax.set_ylabel("FCF Growth Rate")
        st.pyplot(fig)

    except Exception as e:
        st.error(f"⚠️ Error processing {ticker.upper()}: {e}")
