import socket                                               
server = socket.socket()            # создаем объект сокета
hostname = socket.gethostname()   
print(hostname)# получаем имя хоста локальной машины
port = 12345
server.bind((hostname, port))
server.listen(5)                    # начинаем прослушиваени


print("Server starts")

con, addr = server.accept()     # принимаем клиента
print("connection: ", con)
print("client address: ", addr)                             
message = "Hello Client!"       # сообщение для отправки клиенту
con.send(message.encode())      # отправляем сообщение клиенту
con.close()                     # закрываем подключение

print("Server ends")
server.close()

