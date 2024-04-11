#!/usr/bin/env python
# coding: cp1251

# In[ ]:

import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = input("Введите имя хоста сервера: ")
port = int(input("Введите номер порта сервера: "))

client_socket.connect((host, port))
print("Подключение к серверу установлено.")

try:
    while True:
        message = input("Введите сообщение для отправки серверу ('exit' для завершения): ")
        if message.lower() == "exit":
            break

        client_socket.sendall(message.encode('utf-8'))
        print(f"Отправлено серверу: {message}")

        data = client_socket.recv(1024)
        print(f"Получено от сервера: {data.decode('utf-8')}")

finally:
    client_socket.close()
    print("Соединение с сервером закрыто.")
