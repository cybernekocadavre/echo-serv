#!/usr/bin/env python
# coding: cp1251

# In[ ]:


import socket
import logging

def setup_logging():
    # Настройка логгирования
    logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def load_client_info(filename='clients.txt'):
    # Загружаем информацию о клиентах из файла
    client_info = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                ip_address, name = line.strip().split(',')
                client_info[ip_address] = name
    except FileNotFoundError:
        pass  # Если файл не найден, оставляем информацию о клиентах пустой
    return client_info

def save_client_info(client_info, filename='clients.txt'):
    # Сохраняем информацию о клиентах в файл
    with open(filename, 'w') as file:
        for ip_address, name in client_info.items():
            file.write(f"{ip_address},{name}\n")

def handle_client(client_socket, client_address, client_info):
    try:
        # Проверяем, известен ли клиент
        if client_address[0] in client_info:
            name = client_info[client_address[0]]
            client_socket.sendall(f"Привет, {name}!\n".encode('utf-8'))
        else:
            # Если клиент неизвестен, запрашиваем его имя
            client_socket.sendall("Привет! Как тебя зовут? ".encode('utf-8'))
            name = client_socket.recv(1024).decode('utf-8').strip()
            client_info[client_address[0]] = name
            save_client_info(client_info)
            client_socket.sendall(f"Приятно познакомиться, {name}!\n".encode('utf-8'))

        while True:
            # Принимаем сообщение от клиента
            message = client_socket.recv(1024).decode('utf-8')
            logging.info(f"Принято от {name}: {message}")

            if message.lower() == 'exit':
                break

            # Отправляем ответ клиенту
            response = f"Принято от сервера: {message}\n"
            client_socket.sendall(response.encode('utf-8'))
            logging.info(f"Отправлено клиенту {name}: {response.strip()}")

    finally:
        # Закрываем соединение с клиентом
        client_socket.close()
        logging.info("Соединение с клиентом закрыто.")

def main():
    setup_logging()
    client_info = load_client_info()

    # Создаем TCP сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Получаем номер порта от пользователя
    while True:
        port_str = input("Введите номер порта сервера (по умолчанию 9090): ").strip()
        if not port_str:
            port = 9090  # По умолчанию порт 9090
            break
        elif port_str.isdigit():
            port = int(port_str)
            break
        else:
            print("Ошибка: Номер порта должен быть целым числом.")

    # Получаем хост от пользователя
    host = input("Введите имя хоста сервера (по умолчанию localhost): ").strip()
    if not host:
        host = 'localhost'  # По умолчанию используется локальный хост

    while True:
        try:
            # Связываем сокет с хостом и портом
            server_socket.bind((host, port))
            break
        except OSError:
            print(f"Порт {port} занят. Попробуйте другой.")
            port_str = input("Введите другой номер порта сервера: ").strip()
            if not port_str:
                port = 9090  # По умолчанию порт 9090
            elif port_str.isdigit():
                port = int(port_str)
            else:
                print("Ошибка: Номер порта должен быть целым числом.")

    # Начинаем прослушивать порт, одновременно обслуживая только одно подключение
    server_socket.listen(1)

    logging.info(f"Сервер запущен. Ожидание подключения на порту {port}...")

    while True:
        # Принимаем входящее подключение
        client_socket, client_address = server_socket.accept()
        logging.info(f"Подключение от {client_address}")

        # Обрабатываем подключение в отдельном потоке
        handle_client(client_socket, client_address, client_info)

if __name__ == "__main__":
    main()

