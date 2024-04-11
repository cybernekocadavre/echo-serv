#!/usr/bin/env python
# coding: cp1251

# In[ ]:

import socket

# Создаем TCP сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Получаем хост и порт сервера
host = 'localhost'  # Хост сервера
port = 9091  # Порт сервера, должен совпадать с портом сервера

# Подключаемся к серверу
client_socket.connect((host, port))
print("Подключение к серверу установлено.")

try:
    # Отправляем данные серверу
    message = 'блин виртуалка не работает'
    client_socket.sendall(message.encode('utf-8'))
    print(f"Отправлено серверу: {message}")

    # Получаем ответ от сервера
    data = client_socket.recv(1024)
    print(f"Получено от сервера: {data.decode('utf-8')}")

finally:
    # Закрываем соединение с сервером
    client_socket.close()
    print("Соединение с сервером закрыто.")
