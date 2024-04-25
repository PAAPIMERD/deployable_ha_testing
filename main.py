enc_t = "2MjMfpL06n5Hb0Ur507BfBwZhMOGvm+yP8CkwSMl5269t77/f2/ceOLSuB6TQVo4V/OG+Zc5kRxHxemZS9DEqoW9/LBwoLW3pOT5/sImFFg48equgCGdHA=="
stock = "BANKINDIA"
view = "green"
c_email = "avinash9588@gmail.com"
#amt = int(input("ENTER the amount with which you are gonna trade: "))
from kite_trade import *
import time
import datetime
kite = KiteApp(enc_t)
wallet = 0



import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(sender_email, sender_password, receiver_email, subject, body):
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Add message body
    message.attach(MIMEText(body, 'plain'))

    # Connect to the server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    # Login to your gmail account
    server.login(sender_email, sender_password)

    # Send Email
    server.sendmail(sender_email, receiver_email, message.as_string())

    # Quit the server
    server.quit()



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
            time.sleep(0.001)  # Retry every 0.001 seconds



h_c_o = [] #list used for hieken ashi calculation which stores only opens of the candles
h_c_c = [] #list used for hieken ashi calculation which stores closing values for the hieken ashi calculation
nature = []
place_ordertime = 0
first = False


def init_ha(stock):
  open = price_fetcher(stock)
  start = time.time()
  now = time.time()
  while now - start <=300:
    now = time.time()
  close = price_fetcher(stock)
  h_c_o.append(open)
  h_c_c.append(close)
  if close > open:
    nature.append("green")
  else:
    nature.append("red")





def hieken_ashi(stock):
  open = price_fetcher(stock)
  low = price_fetcher(stock)

  high = price_fetcher(stock)
  start = time.time()
  now = time.time()
  while now - start <= 300 :
    curr_price = price_fetcher(stock)
    if curr_price > high:
      high = curr_price
    if curr_price < low:
      low = curr_price
    now = time.time()
  close = price_fetcher(stock)

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




def buy_trade(stock):
  global wallet
  global first
  print("now a buy order mail will be sent")
  print("api and network compnonents and hardware are working fine")
  sender_email = "avinashaws9588@gmail.com"
  sender_password = "mcst rhrz krcr baoe"
  receiver_email = c_email
  subject = "Trade Execution Mail"
  body = "This is To inform you that we have just placed a BUY trade on your behalf with the wallet condition is "+str(wallet)
  send_email(sender_email, sender_password, receiver_email, subject, body)
  first = True

def sell_trade(stock):
  global first
  global wallet
  print("now a sell order mail will be sent")
  print("api and network compnonents and hardware are working fine")
  sender_email = "avinashaws9588@gmail.com"
  sender_password = "mcst rhrz krcr baoe"
  receiver_email = c_email
  subject = "Trade Execution Mail"
  body = "This is To inform you that we have just placed a SELL trade on your behalf with the wallet condition is "+str(wallet)
  send_email(sender_email, sender_password, receiver_email, subject, body)
  first = True


def main(stock):
  now = time.time()
  cuurent_trend = hieken_ashi(stock)
  global place_ordertime
  global first
  global wallet
  while True and (place_ordertime - time.time() > 1200 or first == False):
    now = time.time
    if nature[-1] != nature[-2] and nature[-1] == view:
      now = time.time()
      if nature[-1] == "green" and (place_ordertime -now > 1200 or first == False) :
        print("buy signal generated",price_fetcher(stock))
        print("put a buy order")
        
        wallet -= price_fetcher(stock)
        buy_trade(stock)

        place_ordertime = time.time()
        red_obs(stock)
        break
      if nature[-1] == "red" and (place_ordertime -now > 1200 or first == False):
        print("short order generated",price_fetcher(stock))
        print("short sell order triggered")
        sell_trade(stock)
        place_ordertime= time.time()
        green_obs(stock)
        break
    cuurent_trend = hieken_ashi(stock)





def red_obs(stock):
  global first
  global wallet
  trend = hieken_ashi(stock)
  while True:
    if trend == "red":

      print("buy sqaured off",price_fetcher(stock))
      
      wallet += price_fetcher(stock)
      sell_trade(stock)
      print("your current pnl after the first trade is ",wallet)
      return main(stock)

    trend = hieken_ashi(stock)


def green_obs(stock):
  global first

  trend = hieken_ashi(stock)
  while True:
    if trend == "green":

      print("Short sell sqaured off",price_fetcher(stock))
      buy_trade(stock)
      return main(stock)

    trend = hieken_ashi(stock)









'''def execute_functions_at_915(stock):
    while True:
        now = datetime.datetime.now()
        curr_hour = now.hour + 5
        curr_minute = now.hour + 30
        if curr_hour == 9 and curr_minute == 15:
            init_ha(stock)
            hieken_ashi(stock)
            main(stock)
            break  # Exit loop after executing functions
        time.sleep(1)  # Check every minute'''


#execute_functions_at_915(stock)

init_ha(stock)
hieken_ashi(stock)
main(stock)
