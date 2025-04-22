import socket
import json
import keyboard  # pip install keyboard

HOST = '0.0.0.0'  # listen on all interfaces
PORT = 5050

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Server listening on port {PORT}...")

conn, addr = server_socket.accept()
print(f"Connection from {addr}")

try:
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break

        key_event = json.loads(data)
        key = key_event['key']
        action = key_event['action']

        if action == 'down':
            keyboard.press(key)
        elif action == 'up':
            keyboard.release(key)

except Exception as e:
    print("Error:", e)
finally:
    conn.close()
    server_socket.close()
