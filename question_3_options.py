"""
This is the implementation of question 3 from the ING test
"""

import numpy as np
from scipy.stats import norm
from datetime import date

__version__ = '1.0.0'

def main():
    base_case()

def Black_Scholes_Merton(op_type, K, T, S, q, r, sigma):
    # op_type = Call or Put
    # K = underlying strike price
    # T = time to maturity in years
    # S = underlying stock price
    # q = convenience yield
    # r = interest rate
    # sigma = volatility of the underlying 

    if S <= 0 or K<= 0 or sigma <= 0 or T<0:
        raise ValueError("Inconsistent parameters")
    
    if op_type[:1].upper() == 'C':
        alpha = 1
    else:
        alpha = -1
    
    if T == 0:
        return max(0, alpha * (S-K))
    
    if alpha * (S - K) > 0:
        option_status = "In the Money"
    elif S - K == 0:
        option_status = "At the Money"
    else:
        option_status = "Out of the Money"

    # convert to continous rate
    r = np.log(1+r)

    d1 = (np.log(S/K) + (r - q + (sigma**2)/2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    price = alpha * (S * np.exp(-q * T) * norm.cdf(alpha * d1) - K * np.exp(-r * T) * norm.cdf(alpha * d2))
    return (price, option_status)

def Put_Call_Parity(op_type, opt_price, S, K, T, r):
    """
    When provided a call price it is returned a put price for the option 
    with same characteristics and vice-versa, given by the put-call parity
    """
    # op_type = Call or Put
    # opt_price = option price
    # K = underlying strike price
    # T = time to maturity in years
    # S = underlying stock price
    # r = interest rate

    if op_type[:1].upper() == 'C':
        alpha = 1
    else:
        alpha = -1
    
    # convert to continous rate
    r = np.log(1+r)

    result_price = opt_price - alpha * (S - K * np.exp(-T * r))
    return result_price

def base_case():
    op_type = 'Call'
    K = 17
    trade_date = date(2022, 11, 23)
    expiry_date = date(2023, 5, 10)
    T = (expiry_date - trade_date).days / 365
    S = 19
    q = 0
    r = 0.005
    sigma = 0.3 
    call_option_price, option_status = Black_Scholes_Merton(op_type, K, T, S, q, r, sigma)
    put_option_price = Put_Call_Parity(op_type, call_option_price, S, K, T, r)
    print("The price for the European Vanilla Call given in the exercise is {}. And its status is {}".format(call_option_price, option_status))
    print("Given the put-call parity the price for the European Vanilla Put in the exercise is {}".format(put_option_price))
    
if __name__ == '__main__':
    main()