import socket
import threading
import os

# --- الإعدادات ---
# Railway بيحط البورت في متغير بيئة اسمه PORT
HOST = '0.0.0.0'
PORT = int(os.environ.get("PORT", 59644))

# قائمة لحفظ اتصالات الكلاينتس
clients = []

def broadcast(message, current_conn):
    """إرسال الداتا لكل الناس ماعدا الشخص اللي بعتها"""
    for client in clients:
        if client != current_conn:
            try:
                # بنستخدم sendall لضمان وصول الداتا كاملة (مهمة للملفات الكبيرة)
                client.sendall(message)
            except:
                # لو فشل الإرسال لكلاينت، بنشيله من القائمة
                if client in clients:
                    clients.remove(client)

def handle_client(conn, addr):
    """التعامل مع كل كلاينت في Thread منفصل"""
    print(f"[NEW CONNECTION] {addr} connected.")
    clients.append(conn)
    
    while True:
        try:
            # زودنا الحجم لـ 4096 عشان سرعة نقل ملفات الـ Base64
            data = conn.recv(4096)
            
            if not data:
                break
            
            # السيرفر هنا شغال "وسيط" (Mediator) 
            # بياخد الداتا (نص أو ملف مشفر) يبعتها للباقيين فوراً
            broadcast(data, conn)
            
        except:
            break

    # تنظيف القائمة عند الخروج
    if conn in clients:
        clients.remove(conn)
    conn.close()
    print(f"[DISCONNECTED] {addr} left.")

def start_server():
    """تشغيل السيرفر وعمل الـ Accept loop"""
    # إنشاء السوكيت (TCP)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # حل مشكلة "Address already in use" لو السيرفر رستر بسرعة
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((HOST, PORT))
        server.listen()
        print(f"[LISTENING] Server is running on {HOST}:{PORT}...")
    except Exception as e:
        print(f"[ERROR] Binding failed: {e}")
        return

    while True:
        # استقبال اتصال جديد
        conn, addr = server.accept()
        
        # تشغيل Thread خاص للكلاينت ده
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        
        # طباعة عدد المتصلين حالياً (مفيد للمتابعة على ريلوي)
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()