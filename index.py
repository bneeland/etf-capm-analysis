import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def get_instrument(i, start, end):

    # (Get string values)

    i_str = i

    # Define instruments

    i = yf.Ticker(i_str)

    # Get instrument price data

    i_df = i.history(start=start, end=end, auto_adjust=True).add_prefix(i_str + "_")

    # Only keep the adjusted closing prices

    i_df = i_df[[i_str + "_Close"]]

    return i_df

def calculate_beta(b, m):

    # Get string values

    b_str = b
    m_str = m

    start = "2012-01-01"
    end = "2021-05-31"

    b_df = get_instrument(b, start, end)
    m_df = get_instrument(m, start, end)

    # Combine closing values into one dataframe

    df = pd.concat([b_df, m_df], axis=1, join="inner")

    # Calculate percent daily returns

    df[b_str + "_Return"] = df[b_str + "_Close"].pct_change()
    df[m_str + "_Return"] = df[m_str + "_Close"].pct_change()

    # Plot the returns

    plt.scatter(x=df[m_str + "_Return"], y=df[b_str + "_Return"])

    plt.title(b_str)

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

def get_historical_returns(b):# Get string values

    # Get string value

    b_str = b

    # Get historical returns

    start = "2012-01-01"
    end = "2021-05-31"

    b_df = get_instrument(b, start, end)

    # Calculate mean historical returns

    b_df[b_str + "_Return"] = b_df[b_str + "_Close"].pct_change()

    # Print returns

    print(b_df)

    # Calculate mean return

    r_b = b_df[b_str + "_Return"].mean()

    r_b = (1 + r_b) ** 365 - 1

    r_b = round(r_b, 3)

    print(r_b)

    # Plot returns

    plt.plot(b_df[b_str + "_Return"])

    plt.show()

    return r_b

# get_historical_returns("SPHB")

def get_capm_returns():

    # [Symbol, Name, Comparison (market), MER]
    funds = [
        ["VOO", "S&P 500", "VT", 0.0003],
        ["SPHB", "S&P 500 'high beta'", "VT", 0.0025],
        ["RZV", "Small cap 600", "VT", 0.0035],
        ["VTI", "All US", "VT", 0.0003],
        ["VWO", "Emerging markets", "VT", 0.001],
        ["VTHR", "Russel 3000", "VT", 0.001],
        ["VINIX", "Vanguard Insitutional Index", "VT", 0.0003],
        ["VEXAX", "Vanguard Extended Market Index", "VT", 0.0006],
        ["TCIEX", "TIAA-CREF International Equity", "VT", 0.0005],
    ]

    for fund in funds:
        fund.append(calculate_beta(b = fund[0], m = fund[2]))

    r_f = 1/100
    r_m = 7/100

    for fund in funds:
        fund.append(calculate_capm_return(r_f, r_m, beta = fund[4], mer = fund[3]))

    for fund in funds:
        print(fund)

get_capm_returns()
