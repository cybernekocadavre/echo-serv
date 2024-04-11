#!/usr/bin/env python
# coding: cp1251

# In[ ]:

import socket

def get_host_port():
    default_host = 'localhost'
    default_port = 9091

    host = input(f"Введите имя хоста (по умолчанию {default_host}): ") or default_host
    port = input(f"Введите номер порта (по умолчанию {default_port}): ") or default_port

    return host, int(port)

# Создаем TCP сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    host, port = get_host_port()

    # Подключаемся к серверу
    client_socket.connect((host, port))
    print("Подключение к серверу установлено.")

    try:
        # Отправляем данные серверу
        message = 'hello, world!'
        client_socket.sendall(message.encode('utf-8'))
        print(f"Отправлено серверу: {message}")

        # Получаем ответ от сервера
        data = client_socket.recv(1024)
        print(f"Получено от сервера: {data.decode('utf-8')}")

    finally:
        # Закрываем соединение с сервером
        client_socket.close()
        print("Соединение с сервером закрыто.")

except KeyboardInterrupt:
    print("\nКлиент остановлен.")
