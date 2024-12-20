import json
import time
import websocket
from websocket import create_connection
from tqdm import tqdm  # Import the tqdm library

stx = 0  # Starting x coordinate
sty = 0  # Starting y coordinate

# WebSocket connection using the accessToken
def on_open(ws):
    print('WebSocket connection established.')
    
    auth_token = "YOUR AUTH_TOKEN HERE"

    if auth_token:
        # Prepare the CONNECT message
        connect_message = f"""CONNECT
Authorization:{auth_token}
accept-version:1.2,1.1,1.0
heart-beat:10000,10000

\0"""
        
        # Send the CONNECT message
        ws.send(connect_message)
        
        # After connection, send the ASCII art
        ascii_art(ws, stx, sty)  # Starting coordinates

    else:
        print("Failed to retrieve the access token. Closing WebSocket connection.")
        ws.close()

def on_message(ws, message):
    # No display here for received messages
    pass

def on_error(ws, error):
    # No display for errors
    pass

def on_close(ws, close_status_code, close_msg):
    # No display for closure
    pass

# Function to send ASCII art from a text file with a persistent progress bar
def ascii_art(ws, start_x, start_y):
    # Read the ASCII art file
    try:
        with open('ascii_art.txt', 'r', encoding='utf-8') as file:
            ascii_art = file.read()
    except FileNotFoundError:
        print("The file ascii_art.txt is not found.")
        return
    
    # Calculate the total number of characters to send
    total_characters = sum(len(line) for line in ascii_art.splitlines())
    
    # Start timing
    start_time = time.time()
    
    # Create a progress bar with tqdm
    with tqdm(total=total_characters, desc="Sending ASCII art", unit="char", dynamic_ncols=True, leave=False) as pbar:
        # Send each character one by one
        for i, line in enumerate(ascii_art.splitlines()):
            for j, char in enumerate(line):
                utf8_char = char.encode('utf-8')  # Convert the character to UTF-8

                # Send each character to its coordinates
                send_data(ws, start_x + j, start_y + i, utf8_char.decode('utf-8'))
                time.sleep(0.03)  # Delay of 30 milliseconds
                
                # Update the progress bar
                pbar.update(1)
    
    # End timing
    elapsed_time = time.time() - start_time

    # Display the summary at the end
    print("\nDrawing complete!")
    print(f"Drawing URL: https://textboard.fr/?x={start_x}&y={start_y}")
    print(f"Number of characters sent: {total_characters}")
    print(f"Total time: {elapsed_time:.2f} seconds")

# Function to send data to the WebSocket server
def send_data(ws, x, y, value):
    # Ensure the value is a single character
    if len(value) != 1:
        return  # Do nothing if the value is not a single character

    # Encode the data in JSON
    json_body = json.dumps({"x": x, "y": y, "value": value})
    byte_length = len(json_body.encode())  # Byte length of the JSON

    # Construct the SEND message
    send_message = f"""SEND
destination:/app/map/set
content-length:{byte_length}

{json_body}\0"""

    # Send the message without displaying it in the terminal
    ws.send(send_message)

# WebSocket URL
ws_url = "wss://aywenito.textboard.fr:25555/ws"

# Configure the WebSocket connection
ws = websocket.WebSocketApp(ws_url, 
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

# Launch the WebSocket client
ws.run_forever()
