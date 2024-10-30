import socket
import threading

# Настройки сервера
HOST = 'localhost'  # Это позволяет принимать соединения с любых IP-адресов
PORT = 52128      # Порт сервера

# Список клиентов
clients = []

# Функция для обработки сообщений от клиентов
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Получено сообщение: {message}")
                broadcast(message, client_socket)
            else:
                # Если сообщение пустое, клиент отключился
                remove_client(client_socket)
                break
        except:
            # Удаляем клиента в случае ошибки
            remove_client(client_socket)
            break

# Функция для отправки сообщения всем клиентам
def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                # Удаляем клиента в случае ошибки
                remove_client(client)

# Функция для удаления клиента
def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)
        client_socket.close()

# Запуск сервера
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Сервер запущен на {HOST}:{PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Подключен клиент: {addr}")
        clients.append(client_socket)

        # Запуск потока для обработки клиента
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
