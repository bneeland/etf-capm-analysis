import yfinance as yf
import scipy.stats as sp
import pandas as pd
import matplotlib.pyplot as plt

def calculate_beta(b, m):

    # (Get string values)
    b_str = b
    m_str = m

    # Define instruments

    b = yf.Ticker(b_str)
    m = yf.Ticker(m_str)

    # Get instrument price data

    start = "2013-01-01"
    end = "2019-12-31"

    b_df = b.history(start=start, end=end, auto_adjust=True).add_prefix(b_str + "_")
    m_df = m.history(start=start, end=end, auto_adjust=True).add_prefix(m_str + "_")

    # Only keep the adjusted closing prices

    b_df = b_df[[b_str + "_Close"]]
    m_df = m_df[[m_str + "_Close"]]

    # Combine closing values into one dataframe

    df = pd.concat([b_df, m_df], axis=1, join="inner")

    # Calculate percent daily returns

    df[b_str + "_Return"] = df[b_str + "_Close"].pct_change()
    df[m_str + "_Return"] = df[m_str + "_Close"].pct_change()

    # Plot the returns

    plt.scatter(x=df[m_str + "_Return"], y=df[b_str + "_Return"])

    plt.show()

    # Beta calculations

    b_m_Cov = df[b_str + "_Return"].cov(df[m_str + "_Return"])

    m_Var = df[m_str + "_Return"].var()

    b_Beta = round(b_m_Cov / m_Var, 3)

    return b_Beta

def calculate_capm_return(r_f, r_m, beta, mer):

    # Calculate the CAPM returns from instrument "b" beta

    r_b = r_f + beta * (r_m - r_f) - mer

    r_b = round(r_b, 4)

    return r_b

"""
Other funds for reference:
VT: All world | MER = 0.08%
VTI: All US | MER = 0.03%
ZSP.TO: S&P 500 in CAD | MER = 0.08%
VOO: S&P 500 in USD | MER = 0.03%
SPHB: S&P 500 "high beta" | MER = 0.25%
VXC.TO: All world except Canada | MER = 0.25%
RZV: Small cap 600 | MER = 0.35%
"""

funds = [
    ["VOO", "S&P 500", "VTI", 0.03/100],
    ["SPHB", "S&P 500 'high beta'", "VTI", 0.25/100],
    ["RZV", "Small cap 600", "VTI", 0.35/100],
    ["VTI", "All US", "VT", 0.03/100],
    ["VWO", "Emerging markets", "VT", 0.1/100],
]

for fund in funds:
    fund.append(calculate_beta(b = fund[0], m = fund[2]))

for fund in funds:
    fund.append(calculate_capm_return(r_f = 1/100, r_m = 7/100, beta = fund[4], mer = fund[3]))

for fund in funds:
    print(fund)
