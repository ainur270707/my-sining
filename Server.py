import socket
import threading
import json

# Настройка сервера
HOST = '127.0.0.1'  # Локальный хост
PORT = 12345        # Порт сервера
print(1)
print(socket.gethostbyname_ex())
print(2)# Создаем серверный сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((socket.gethostbyname_ex()[-1][-1], PORT))
server_socket.listen()

clients = []

# Функция для рассылки сообщений всем клиентам
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            client.send(message)

# Функция для обработки клиентов
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(f"Получено сообщение: {message}")
                broadcast(message, client_socket)
            else:
                remove_client(client_socket)
                break
        except:
            remove_client(client_socket)
            break

# Функция удаления клиента из списка
def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)
        client_socket.close()

print("Сервер запущен...")

while True:
    client_socket, addr = server_socket.accept()
    clients.append(client_socket)
    print(f"Новое подключение: {addr}")
    threading.Thread(target=handle_client, args=(client_socket,)).start()
