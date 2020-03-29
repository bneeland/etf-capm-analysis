import yfinance as yf
import pandas as pd

def beta(b, m):

    # (Get string values)
    b_str = b
    m_str = m

    # Define funds

    b = yf.Ticker(b_str)
    m = yf.Ticker(m_str)

    # Get fund price data

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

    # Beta calculations

    b_m_Cov = df[b_str + "_Return"].cov(df[m_str + "_Return"])

    m_Var = df[m_str + "_Return"].var()

    b_Beta = round(b_m_Cov / m_Var, 3)

    return {
        "cov": b_m_Cov,
        "var": m_Var,
        "beta": b_Beta,
    }

def capm_return(r_f, r_m, beta, mer):

    # Calculate the CAPM returns from fund "b" beta

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
IRX: Short-term US Treasury bills
"""

beta_parameters = beta(b = "SPHB", m = "VT")

beta = beta_parameters["beta"]

print(beta)

capm_return = capm_return(r_f = 1/100, r_m=7/100, beta=beta, mer=0.25/100)

print(capm_return)
