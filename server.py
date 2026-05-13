import socket
import threading
import os

# الإعدادات بناءً على صورة ريلوي
HOST = '0.0.0.0'
# ريلوي بيبعت البورت في متغير بيئة، ولو مش موجود هنستخدم 50000 زي الصورة
PORT = int(os.environ.get("PORT", 50000))

clients = []

def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                client.sendall(message)
            except:
                if client in clients: clients.remove(client)

def handle_client(conn, addr):
    print(f"[CONNECTED] {addr}")
    clients.append(conn)
    while True:
        try:
            data = conn.recv(4096)
            if not data: break
            broadcast(data, conn)
        except: break
    if conn in clients: clients.remove(conn)
    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server is listening on port {PORT}...")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
