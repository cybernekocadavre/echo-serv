#!/usr/bin/env python
# coding: cp1251

# In[ ]:
import socket

# Создаем TCP сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Получаем хост и порт для сервера
host = ''  # Пустая строка означает использование всех доступных интерфейсов
port = 9091  # Выбираем порт для сервера

# Связываем сокет с хостом и портом
server_socket.bind((host, port))

while True:
    # Начинаем прослушивать порт, одновременно обслуживая только одно подключение
    server_socket.listen(1)

    print("Сервер запущен. Ожидание подключения...")

    # Принимаем входящее подключение
    client_socket, client_address = server_socket.accept()
    print(f"Подключение от {client_address}")

    try:
        while True:
            # Принимаем данные от клиента
            data = client_socket.recv(1024)
            if not data:
                break

            # Отправляем обратно клиенту те же данные в верхнем регистре
            client_socket.sendall(data.upper())
            print(f"Принято от клиента: {data.decode('utf-8')}")

    finally:
        # Закрываем соединение с клиентом
        client_socket.close()
        print("Соединение с клиентом закрыто.")

# Закрываем серверный сокет
server_socket.close()
