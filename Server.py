import socket
import threading
import json

# Настройка сервера
HOST = '0.0.0.0'  # Указываем 0.0.0.0, чтобы сервер слушал на всех интерфейсах
PORT = 52128       # Порт сервера

# Создаем серверный сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print("Сервер запущен. Хост:", socket.gethostname(), "Порт:", PORT)

def handle_client(client_socket):
    # Обработка клиента
    request = client_socket.recv(1024).decode('utf-8')
    print("Получен запрос:", request)
    client_socket.send("Ответ от сервера".encode('utf-8'))
    client_socket.close()

while True:
    client_socket, addr = server_socket.accept()
    print("Подключен клиент:", addr)
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()
