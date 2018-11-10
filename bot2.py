#!/usr/bin/python

# ~~~~~==============   HOW TO RUN   ==============~~~~~
# 1) Configure things in CONFIGURATION section
# 2) Change permissions: chmod +x bot.py
# 3) Run in loop: while true; do ./bot.py; sleep 1; done

from __future__ import print_function

import sys
import socket
import json
import time

# ~~~~~============== CONFIGURATION  ==============~~~~~
# replace REPLACEME with your team name!
team_name="NONAMEBOYS"
# This variable dictates whether or not the bot is connecting to the prod
# or test exchange. Be careful with this switch!
test_mode = False

# This setting changes which test exchange is connected to.
# 0 is prod-like
# 1 is slower
# 2 is empty
test_exchange_index=2
prod_exchange_hostname="production"

port=25000 + (test_exchange_index if test_mode else 0)
exchange_hostname = "test-exch-" + team_name if test_mode else prod_exchange_hostname

# ~~~~~============== NETWORKING CODE ==============~~~~~
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((exchange_hostname, port))
    return s.makefile('rw', 1)

def write_to_exchange(exchange, obj):
    json.dump(obj, exchange)
    exchange.write("\n")

def read_from_exchange(exchange):
    return json.loads(exchange.readline())

# ~~~~~============== TRADING CODE ==============~~~~~

def write_to_json(file, message):
    with open(file, 'a+') as f:
        json.dump(message, f)

"""def write_to_txt(file, data):
    with open(file, 'a+') as openfile:
        openfile.write(data) """
        

# ~~~~~============== MAIN LOOP ==============~~~~~

def main():
    exchange = connect()
    write_to_exchange(exchange, {"type": "hello", "team": team_name.upper()})
    hello_from_exchange = read_from_exchange(exchange)
    # A common mistake people make is to call write_to_exchange() > 1
    # time for every read_from_exchange() response.
    # Since many write messages generate marketdata, this will cause an
    # exponential explosion in pending messages. Please, don't do that!
    print("The exchange replied:", hello_from_exchange, file=sys.stderr)
    ID = 0
    public = ["open", "close", "trade", "book"]
    private = ["ack", "reject", "fill", "out"]
    while(True):
        i = 0 
        for i in range(40): 
            # bidding for BONDS - bigger profit_loss
            ID+=1
            write_to_exchange(exchange, {"type": "add", "order_id": ID, "symbol": "BOND", "dir": "BUY", "price": 998, "size": 5})
            exchange_message = read_from_exchange(exchange)
            if exchange_message["type"] in private:
                print("MI:", exchange_message, file=sys.stderr)
            ID+=1
            write_to_exchange(exchange, {"type": "add", "order_id": ID, "symbol": "BOND", "dir": "SELL", "price": 1002, "size": 5})
            # bidding for BONDS - smaller profit_loss
            ID+=1
            write_to_exchange(exchange, {"type": "add", "order_id": ID, "symbol": "BOND", "dir": "BUY", "price": 999, "size": 5})
            exchange_message = read_from_exchange(exchange)
            if exchange_message["type"] in private:
                print("MI:", exchange_message, file=sys.stderr)
            ID+=1
            write_to_exchange(exchange, {"type": "add", "order_id": ID, "symbol": "BOND", "dir": "SELL", "price": 1001, "size": 5})
            if exchange_message["type"] in private:
                print("MI:", exchange_message, file=sys.stderr)
            time.sleep(5)
                
        #writing/parsing exchange to json files
        """if exchange_message["type"] == "book":
            write_to_json('book.txt', exchange_message)
            if exchange_message["symbol"] == "VALBZ":
                write_to_json('book_buy_prices_for_ADR.txt', exchange_message["buy"])
                write_to_json('book_sell_prices_for_ADR.txt', exchange_message["sell"])
            if exchange_message["symbol"] == "BOND":
                write_to_json('book_buy_prices_for_BOND.txt', exchange_message["buy"])
                write_to_json('book_sell_prices_for_BOND.txt', exchange_message["sell"])"""
        if exchange_message["type"] == "trade":
            write_to_json('trade.txt',exchange_message)
        if exchange_message["type"] == "open":
            write_to_json('open.txt',exchange_message)
        if exchange_message["type"] == "close":
            write_to_json('close.txt',exchange_message)

if __name__ == "__main__":
    main()
