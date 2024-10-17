"""
This is the implementation of question 4 from the ING test
"""

import pandas as pd

__version__ = '1.0.0'

def main():
    df_fx_mkt_rates, port_values = read_input_data()
    df_total_pnl = calculate_total_PnL(df_fx_mkt_rates, port_values)
    var = calculate_var(df_total_pnl)
    print("The calculated 1-day VaR with 99% confidence interval for the question 4 is {}".format(var))

def read_input_data():
    file_path = "TRM Engineering_Interview_Option_VaR_.xlsx"
    sheet_name = "VaR Calculation"
    df = pd.read_excel(file_path, sheet_name=sheet_name, usecols='C:G', skiprows=5)
    df = df.rename(columns={'Unnamed: 2':'Count', 'market rate':'ccy1_mkt_rate', 'market rate.1':'ccy2_mkt_rate'})
    df = df.dropna(subset=['Count'])
    
    df_2 = pd.read_excel(file_path, sheet_name=sheet_name, usecols='A:C')
    portfolio_value_ccy1 = df_2.iloc[1, 2]
    portfolio_value_ccy2 = df_2.iloc[2, 2]
    port_values = [portfolio_value_ccy1, portfolio_value_ccy2]
    return df, port_values

def calculate_total_PnL(df, port_values):
    [portfolio_value_ccy1, portfolio_value_ccy2] = port_values
    df['ccy1_shift'] = df['ccy1_mkt_rate'] / df['ccy1_mkt_rate'].shift(-1) - 1
    df['ccy2_shift'] = df['ccy2_mkt_rate'] / df['ccy2_mkt_rate'].shift(-1) - 1
    df['ccy1_pnl'] = df['ccy1_shift'] * portfolio_value_ccy1
    df['ccy2_pnl'] = df['ccy2_shift'] * portfolio_value_ccy2
    df['total_pnl'] = df['ccy1_pnl'] + df['ccy2_pnl']
    df = df.dropna(subset=['total_pnl'])
    return df

def calculate_var(df_total_pnl):
    
    sorted_values = df_total_pnl['total_pnl'].sort_values().values

    second_lowest = sorted_values[1]
    third_lowest = sorted_values[2]

    var = 0.4 * second_lowest + 0.6 * third_lowest
    return var

if __name__ == '__main__':
    main()