enc_t = input('Enter a valid enc-t:  ')
stock = input("Enter your Stock: ")
view = input("Enter Your view: (red or green): ")
from kite_trade import *
import time
from datetime import datetime
kite = KiteApp(enc_t)



def price_fetcher(symbol):
    start_time = time.time()  # Record the start time
    
    while True:
        try:
            # Attempt to fetch the price
            price = kite.ltp(["NSE:" + symbol])
            final_price = price["NSE:" + symbol]["last_price"]
            return final_price
        except KeyError as e:
            # Handle KeyError
            elapsed_time = time.time() - start_time
            if elapsed_time >= 60:
                # If 60 seconds have passed and price is still not fetched, raise an exception
                raise Exception("Failed to fetch price for symbol {} after 60 seconds".format(symbol))
            
            # Sleep for a short interval before retrying
            time.sleep(0.001)  # Retry every 0.25 seconds



h_c_o = [] #list used for hieken ashi calculation which stores only opens of the candles
h_c_c = [] #list used for hieken ashi calculation which stores closing values for the hieken ashi calculation
nature = []


def init_ha(stock):
  open = price_fetcher(stock)
  start = time.time()
  now = time.time()
  while now - start <=15:
    now = time.time()
  close = price_fetcher(stock)
  h_c_o.append(open)
  h_c_c.append(close)
  if close > open:
    nature.append("green")
  else:
    nature.append("red")





def hieken_ashi(fsym):
  open = price_fetcher(stock)
  low = price_fetcher(stock)

  high = price_fetcher(stock)
  start = time.time()
  now = time.time()
  while now - start <= 15 :
    curr_price = price_fetcher(stock)
    if curr_price > high:
      high = curr_price
    if curr_price < low:
      low = curr_price
    now = time.time()
  close = price_fetcher(fsym)

  curr_open = (h_c_o[-1]+h_c_c[-1])/2
  curr_close = (open+low+high+close)/4

  h_c_o.append(curr_open)
  h_c_c.append(curr_close)


  if curr_open >= curr_close:
    curr_nature = "red"
  if curr_close > curr_open:
    curr_nature = "green"

  nature.append(curr_nature)
  return curr_nature


#FIRST INIT should be called after that hieken_ashi() should be called because hieken_ashi() requires some initial data which will be provided by init





def main(fsym):
  while True:
    cuurent_trend = hieken_ashi(fsym)
  
  if nature[-1] != nature[-2] and nature[-1] == view:
    if nature[-1] == "green":
      print("buy signal generated",price_fetcher(stock))
      print("put a buy order")
      red_obs(fsym)
    if nature[-1] == "red":
      print("short order generated",price_fetcher(stock))
      print("short sell order triggered")
      green_obs(stock)




def red_obs(stock):
    current_trend = hieken_ashi(stock)
    if nature[-1] == "red":
        print("Functional call to sell the bought entity")
        print("Buy squared off")
        if datetime.now().time().hour >= 15:  # Check if current hour is 15 (3 PM) or later
            print("It's past 3 PM. Breaking out of the function.")
            return  # Break out of the function if it's past 3 PM
        main(stock)

def green_obs(stock):
    current_trend = hieken_ashi(stock)
    if nature[-1] == "green":
        print("Functional call to buy back the shorted instrument")
        print("Short sell squared off")
        if datetime.now().time().hour >= 15:  # Check if current hour is 15 (3 PM) or later
            print("It's past 3 PM. Breaking out of the function.")
            return  # Break out of the function if it's past 3 PM
        main(stock)



stock = "WIPRO"
init_ha("WIPRO")
hieken_ashi("WIPRO")
main("WIPRO")