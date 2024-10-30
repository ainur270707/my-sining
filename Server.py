import socket
import threading

# Настройки сервера
HOST = socket.gethostbyname_ex(socket.gethostname())[-1][-1]  # Позволяет принимать подключения со всех интерфейсов
PORT = 12345  # Порт, на котором будет работать сервер

# Список клиентов
clients = []
# Блокировка для синхронизации
lock = threading.Lock()

def handle_client(client_socket, address):
    print(f"[Новый клиент] Подключен: {address}")
    
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            
            print(f"[Сообщение от {address}] {message}")

            # Отправляем сообщение всем клиентам
            with lock:
                for client in clients:
                    if client != client_socket:  # Не отправляем сообщение отправителю
                        client.send(f"[{address}] {message}".encode('utf-8'))
        
        except:
            break
    
    # Удаляем клиента из списка
    with lock:
        clients.remove(client_socket)
    print(f"[Клиент отключился] {address}")
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"[Сервер запущен] Подключение на {HOST}:{PORT}")

    while True:
        client_socket, address = server_socket.accept()
        clients.append(client_socket)  # Добавляем клиента в список
        threading.Thread(target=handle_client, args=(client_socket, address)).start()

if __name__ == "__main__":
    start_server()
