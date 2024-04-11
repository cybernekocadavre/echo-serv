#!/usr/bin/env python
# coding: cp1251

# In[ ]:
import socket

# Функция для чтения имен клиентов из файла
def read_clients():
    try:
        with open('clients.txt', 'r') as file:
            clients = {}
            for line in file:
                ip, name = line.strip().split(',')
                clients[ip] = name
        return clients
    except FileNotFoundError:
        return {}

# Функция для записи нового клиента в файл
def write_client(ip, name):
    with open('clients.txt', 'a') as file:
        file.write(f"{ip},{name}\n")

# Создаем TCP сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Получаем хост и порт для сервера
host = ''  # Пустая строка означает использование всех доступных интерфейсов
port = 9090  # Выбираем порт для сервера

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
        # Если клиент известен, приветствуем его по имени
        name = clients[ip]
        client_socket.send(f"Привет, {name}!".encode())
    else:
        # Если клиент неизвестен, запрашиваем у него имя
        client_socket.send("Привет! Пожалуйста, введите ваше имя: ".encode())
        name = client_socket.recv(1024).decode().strip()
        print(f"Новый клиент ({ip}): {name}")

        # Записываем имя клиента в файл
        write_client(ip, name)

        # Отправляем клиенту сообщение с приветствием
        client_socket.send(f"Привет, {name}! Ваше имя добавлено в список известных клиентов.".encode())

    # Закрываем соединение с клиентом
    client_socket.close()
