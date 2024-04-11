#!/usr/bin/env python
# coding: cp1251

# In[ ]:
import socket
import sys

def get_host_port():
    default_host = 'localhost'
    default_port = 9091

    print("Введите имя хоста (по умолчанию {}): ".format(default_host))
    host_input = sys.stdin.readline().strip()
    host = host_input or default_host

    print("Введите номер порта (по умолчанию {}): ".format(default_port))
    port_input = sys.stdin.readline().strip()
    port = port_input or default_port

    return host, int(port)

# Создаем TCP сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    host, port = get_host_port()

    # Связываем сокет с хостом и портом
    server_socket.bind((host, port))

    # Начинаем прослушивать порт, одновременно обслуживая только одно подключение
    server_socket.listen(1)

    print("Сервер запущен. Ожидание подключения на {}:{}".format(host, port))

    # Принимаем входящее подключение
    client_socket, client_address = server_socket.accept()
    print("Подключение от {}".format(client_address))

    try:
        while True:
            # Принимаем данные от клиента
            data = client_socket.recv(1024)
            if not data:
                break

            # Отправляем обратно клиенту те же данные в верхнем регистре
            client_socket.sendall(data.upper())
            print("Принято от клиента: {}".format(data.decode('utf-8')))

    finally:
        # Закрываем соединение с клиентом
        client_socket.close()
        print("Соединение с клиентом закрыто.")

except KeyboardInterrupt:
    print("\nСервер остановлен.")

except Exception as e:
    print("Произошла ошибка: {}".format(e))

finally:
    # Закрываем серверный сокет
    server_socket.close()

