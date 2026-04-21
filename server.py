import socket
import threading
import os

# الإعدادات: Railway بيحدد البورت ديناميكياً
HOST = '0.0.0.0'
PORT = int(os.environ.get("PORT", 50000))

clients = []

def broadcast(message, current_conn):
    """إرسال الرسالة لكل الناس ماعدا اللي بعتها"""
    for client in clients:
        if client != current_conn:
            try:
                client.send(message)
            except:
                clients.remove(client)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    clients.append(conn)
    
    while True:
        try:
            message = conn.recv(1024)
            if not message:
                break
            # إعادة توجيه الرسالة للجميع
            broadcast(message, conn)
        except:
            break

    clients.remove(conn)
    conn.close()
    print(f"[DISCONNECTED] {addr} left.")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[LISTENING] Server is running on port {PORT}...")
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()