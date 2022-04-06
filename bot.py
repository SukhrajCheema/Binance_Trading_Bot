import websocket
import json
import pprint
import numpy as np
import ta.momentum
import binance

# https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md#klinecandlestick-streams
SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = 'ETHUSD'
TRADE_QUANTITY = 20

closes = []
in_position = False


def on_open(ws):
    print("opened connection")


def on_close(ws):
    print("closed connection")


def on_message(ws, message):
    global closes
    print("received message")
    json_message = json.loads(message)  # converts string into python data structure we can manipulate.
    pprint.pprint(json_message)  # formats the message.

    candle = json_message['k']

    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        print(f"candle closed at {close}")
        closes.append(float(close))  # without float(), will remain as a string.
        print("closes")
        print(closes)

        if len(closes) > RSI_PERIOD:
            np_closes = np.arrary(closes)
            rsi = ta.momentum.RSIIndicator(np_closes, RSI_PERIOD) 
            print("All RSI computed so far:")
            print(rsi)
            last_rsi = rsi[-1]
            print(f"The current RSI is {last_rsi}")

            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                    print("Sell sell sell.")
                    # place selling logic here.
                else:
                    print("It is overbought, but we do not own any, nothing to do.")

            if last_rsi < RSI_OVERSOLD:
                if in_position:
                    print("It is oversold, but we already own it, nothing to do.")
                else:
                    print("Buy buy buy.")
                    # place buying logic here.


ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()
print(closes)
