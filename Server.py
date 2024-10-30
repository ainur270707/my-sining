import socket
import threading

# Настройки сервера
HOST = '0.0.0.0'  # Прислушиваться на всех доступных интерфейсах
PORT = 52128      # Порт должен совпадать с портом на Railway (замените на фактический, если он другой)

# Создаем серверный сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print("Сервер запущен и ожидает подключений...")

# Функция для обработки клиентов
def handle_client(client_socket, address):
    print(f"Подключен клиент: {address}")
    try:
        while True:
            # Принимаем сообщение от клиента
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Сообщение от {address}: {message}")
            
            # Отправляем ответ клиенту
            response = f"Сервер получил: {message}"
            client_socket.send(response.encode('utf-8'))
    except Exception as e:
        print(f"Ошибка с клиентом {address}: {e}")
    finally:
        client_socket.close()
        print(f"Клиент {address} отключился")

# Основной цикл сервера для принятия подключений
while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
