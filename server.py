import socket
import threading


PORT = 9090
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"

clients, names = [], []

server = socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM)

server.bind(ADDRESS)


def startChat():
    print("server is working on " + SERVER)
    server.listen()

    while True:
        conn, addr = server.accept()
        conn.send("NAME".encode(FORMAT))

        name = conn.recv(1024).decode(FORMAT)

        names.append(name)
        clients.append(conn)

        conn.send('Успешное подключение!'.encode(FORMAT))
        thread = threading.Thread(target=handle,
                                  args=(conn, addr))
        thread.start()

        print(f" Имя: { name}")
        broadcastMessage(f"{name} присоединился к чату!".encode(FORMAT))

        print(f"active connections {threading.activeCount() - 1}")

def handle(conn, addr):
    print(f"new connection {addr}")
    connected = True

    while connected:
        message = conn.recv(1024)
        broadcastMessage(message)
    conn.close()

def broadcastMessage(message):
    for client in clients:
        client.send(message)


startChat()