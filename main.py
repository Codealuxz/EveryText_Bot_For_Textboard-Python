import json
import time
import websocket
from websocket import create_connection
from tqdm import tqdm  

stx = 0  
sty = 0  

def on_open(ws):
    print('WebSocket connection established.')

    auth_token = "YOUR AUTH_TOKEN HERE"

    if auth_token:

        connect_message = f"""CONNECT
Authorization:{auth_token}
accept-version:1.2,1.1,1.0
heart-beat:10000,10000

\0"""

        ws.send(connect_message)

        ascii_art(ws, stx, sty)  

    else:
        print("Failed to retrieve the access token. Closing WebSocket connection.")
        ws.close()

def on_message(ws, message):

    pass

def on_error(ws, error):

    pass

def on_close(ws, close_status_code, close_msg):

    pass

def ascii_art(ws, start_x, start_y):

    try:
        with open('ascii_art.txt', 'r', encoding='utf-8') as file:
            ascii_art = file.read()
    except FileNotFoundError:
        print("The file ascii_art.txt is not found.")
        return

    total_characters = sum(len(line) for line in ascii_art.splitlines())

    start_time = time.time()

    with tqdm(total=total_characters, desc="Sending ASCII art", unit="char", dynamic_ncols=True, leave=False) as pbar:

        for i, line in enumerate(ascii_art.splitlines()):
            for j, char in enumerate(line):
                utf8_char = char.encode('utf-8')  

                send_data(ws, start_x + j, start_y + i, utf8_char.decode('utf-8'))
                time.sleep(0.03)  

                pbar.update(1)

    elapsed_time = time.time() - start_time

    print("\nDrawing complete!")
    print(f"Drawing URL: https://textboard.fr/?x={start_x}&y={start_y}")
    print(f"Number of characters sent: {total_characters}")
    print(f"Total time: {elapsed_time:.2f} seconds")

def send_data(ws, x, y, value):

    if len(value) != 1:
        return  

    json_body = json.dumps({"x": x, "y": y, "value": value})
    byte_length = len(json_body.encode())  

    send_message = f"""SEND
destination:/app/map/set
content-length:{byte_length}

{json_body}\0"""

    ws.send(send_message)

ws_url = "wss://aywenito.textboard.fr:25555/ws"

ws = websocket.WebSocketApp(ws_url, 
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

ws.run_forever()
