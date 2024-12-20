import json
import time
import websocket
from websocket import create_connection
from tqdm import tqdm  # Importer la bibliothèque tqdm

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
        
        # Après la connexion, envoyer l'ASCII art
        ascii_art(ws, 0, 0)  # Coordonnées de départ

    else:
        print("Failed to retrieve the access token. Closing WebSocket connection.")
        ws.close()

def on_message(ws, message):
    # Pas d'affichage ici pour les messages reçus
    pass

def on_error(ws, error):
    # Pas d'affichage d'erreurs
    pass

def on_close(ws, close_status_code, close_msg):
    # Pas d'affichage de la fermeture
    pass


# Fonction pour envoyer l'ASCII art depuis un fichier texte avec une barre de progression persistante
def ascii_art(ws, start_x, start_y):
    # Lire le fichier ASCII art
    try:
        with open('ascii_art.txt', 'r', encoding='utf-8') as file:
            ascii_art = file.read()
    except FileNotFoundError:
        print("Le fichier ascii_art.txt est introuvable.")
        return
    
    # Calculer le nombre total de caractères à envoyer
    total_characters = sum(len(line) for line in ascii_art.splitlines())
    
    # Débuter le chronométrage
    start_time = time.time()
    
    # Créer une barre de progression avec tqdm
    with tqdm(total=total_characters, desc="Sending ASCII art", unit="char", dynamic_ncols=True, leave=False) as pbar:
        # Envoyer chaque caractère un par un
        for i, line in enumerate(ascii_art.splitlines()):
            for j, char in enumerate(line):
                utf8_char = char.encode('utf-8')  # Convertir le caractère en UTF-8

                # Envoyer chaque caractère à ses coordonnées
                send_data(ws, start_x + j, start_y + i, utf8_char.decode('utf-8'))
                time.sleep(0.03)  # Délai de 30 millisecondes
                
                # Mettre à jour la barre de progression
                pbar.update(1)
    
    # Fin du chronométrage
    elapsed_time = time.time() - start_time

    # Afficher le résumé à la fin
    print("\nDessin terminé!")
    print(f"URL du dessin : https://textboard.fr/?x={start_x}&y={start_y}")
    print(f"Nombre de caractères envoyés : {total_characters}")
    print(f"Temps total : {elapsed_time:.2f} secondes")


# Fonction pour envoyer les données au serveur WebSocket
def send_data(ws, x, y, value):
    # S'assurer que la valeur est un seul caractère
    if len(value) != 1:
        return  # Ne rien faire si la valeur n'est pas un seul caractère

    # Encoder les données en JSON
    json_body = json.dumps({"x": x, "y": y, "value": value})
    byte_length = len(json_body.encode())  # Longueur en octets du JSON

    # Construire le message SEND
    send_message = f"""SEND
destination:/app/map/set
content-length:{byte_length}

{json_body}\0"""

    # Envoyer le message sans l'afficher dans le terminal
    ws.send(send_message)

# URL du WebSocket
ws_url = "wss://aywenito.textboard.fr:25555/ws"

# Configurer la connexion WebSocket
ws = websocket.WebSocketApp(ws_url, 
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

# Lancer le client WebSocket
ws.run_forever()
