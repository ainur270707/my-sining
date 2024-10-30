import socket

HOST = '0.0.0.0'  # Слушать на всех интерфейсах
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print("Server is listening...")

while True:
    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")
    conn.sendall(b"Welcome to the server")
    conn.close()
