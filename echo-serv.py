#!/usr/bin/env python
# coding: cp1251

# In[ ]:
import socket

# Функция для чтения IP-адресов клиентов из файла
def read_clients():
    try:
        with open('clients.txt', 'r') as file:
            clients = [line.strip() for line in file]
        return clients

# Функция для записи нового клиента в файл
def write_client(ip):
    with open('clients.txt', 'a') as file:
        # a это append
        file.write(f"{ip}\n")

# Создаем TCP сокет
# AF_INET указывает на использование сетевого протокола IPv4
# SOCK_STREAM указывает, что мы используем протокол TCP для надежной передачи потока данных
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Получаем хост и порт для сервера
host = ''  # Пустая строка означает использование всех доступных интерфейсов
port = 9091

# Связываем сокет с хостом и портом
server_socket.bind((host, port))

# Начинаем прослушивать порт, одновременно обслуживая только одно подключение
server_socket.listen(1)

print("Сервер запущен. Ожидание подключения...")

# Читаем информацию о клиентах из файла
clients = read_clients()

while True:
    # Принимаем входящее подключение
    client_socket, client_address = server_socket.accept()
    print(f"Подключение от {client_address}")

    ip = client_address[0]

    if ip in clients:
        # Если клиент известен, приветствуем его как постоянного клиента
        client_socket.send("Снова здравствуйте!".encode())
    else:
        # Если клиент неизвестен, записываем его IP-адрес в файл и приветствуем
        write_client(ip)
        client_socket.send("Привет!".encode())

    # Закрываем соединение с клиентом
    client_socket.close()

    # Переопределяем список клиентов после обработки текущего подключения
    clients = read_clients()
