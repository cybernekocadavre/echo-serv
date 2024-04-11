#!/usr/bin/env python
# coding: cp1251

# In[ ]:
import socket
import logging

# Настройка логирования
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Функция для чтения IP-адресов клиентов из файла
def read_clients():
    try:
        with open('clients.txt', 'r') as file:
            clients = [line.strip() for line in file]
        return clients
    except FileNotFoundError:
        return []

# Функция для записи нового клиента в файл
def write_client(ip):
    with open('clients.txt', 'a') as file:
        file.write(f"{ip}\n")

# Создаем TCP сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Получаем хост и порт для сервера
host = ''  # Пустая строка означает использование всех доступных интерфейсов
port = 9091

# Связываем сокет с хостом и портом
server_socket.bind((host, port))

# Начинаем прослушивать порт, одновременно обслуживая только одно подключение
server_socket.listen(1)

print("Сервер запущен. Ожидание подключения...")

while True:
    # Принимаем входящее подключение
    client_socket, client_address = server_socket.accept()
    print(f"Подключение от {client_address}")

    ip = client_address[0]

    # Читаем информацию о клиентах из файла
    clients = read_clients()

    if ip in clients:
        # Если клиент известен, приветствуем его как постоянного гостя
        client_socket.send("Снова здравствуйте!".encode())
    else:
        # Если клиент неизвестен, приветствуем как новичка
        client_socket.send("Привет!".encode())
        # Записываем нового клиента в файл
        write_client(ip)

    try:
        while True:
            # Получаем данные от клиента
            data = client_socket.recv(1024)
            if not data:
                break

            # Преобразуем данные в верхний регистр и отправляем обратно клиенту
            client_socket.send(data.upper())
            # Логируем принятые данные
            logging.info(data.decode())

    except ConnectionResetError:
        print("Соединение с клиентом разорвано.")
        client_socket.close()

