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
    while(True):
        for i in range(20):
            ID+=1
            write_to_exchange(exchange, {"type": "add", "order_id": ID, "symbol": "BOND", "dir": "BUY", "price": 998, "size": 40})
            exchange_message = read_from_exchange(exchange)
            if exchange_message["type"] != "book":
                print("The exchange replied:", exchange_message, file=sys.stderr)
            ID+=1
            write_to_exchange(exchange, {"type": "add", "order_id": ID, "symbol": "BOND", "dir": "SELL", "price": 1002, "size": 40})
            exchange_message = read_from_exchange(exchange)
            if exchange_message["type"] != "book":
            print("The exchange replied:", exchange_message, file=sys.stderr)
                exchange_message = read_from_exchange(exchange)
            with open('data.txt', 'w') as outfile:
                if exchange_message["type"] == "book":
                    json.dump(exchange_message, outfile)
        time.sleep(5)
    
    #while(True):
        #exchange_message = read_from_exchange(exchange)
        #with open('data.txt', 'w') as outfile:
            #json.dump(exchange_message, outfile)


if __name__ == "__main__":
    main()
