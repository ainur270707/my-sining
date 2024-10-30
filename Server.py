import socket
import threading

# Настройки сервера
HOST = '0.0.0.0'  # Указывает, что сервер будет слушать на всех доступных интерфейсах
PORT = 40275       # Порт, на котором будет слушать сервер

# Создаем серверный сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))  # Привязываем сокет к адресу и порту
server_socket.listen(5)  # Максимум 5 клиентов в очереди
print(f"Сервер запущен и слушает на порту {PORT}...")

# Список клиентов
clients = []

# Функция для обработки клиента
def handle_client(client_socket, address):
    print(f"Подключен клиент: {address}")
    clients.append(client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Получено сообщение от {address}: {message}")
                broadcast(message, client_socket)  # Отправляем сообщение всем клиентам
            else:
                print(f"Клиент {address} отключился.")
                break
        except Exception as e:
            print(f"Ошибка: {e}")
            break

    # Удаляем клиента из списка и закрываем сокет
    clients.remove(client_socket)
    client_socket.close()

# Функция для рассылки сообщений всем клиентам
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:  # Не отправляем сообщение отправителю
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Ошибка отправки сообщения: {e}")

# Основной цикл сервера
while True:
    # Ожидаем подключения клиента
    client_socket, address = server_socket.accept()
    # Запускаем новый поток для обработки клиента
    threading.Thread(target=handle_client, args=(client_socket, address)).start()
