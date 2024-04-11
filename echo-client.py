#!/usr/bin/env python
# coding: cp1251

# In[ ]:


import socket

def main():
    # Создаем TCP сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Получаем имя хоста и номер порта сервера от пользователя
    host = input("Введите имя хоста сервера (по умолчанию localhost): ").strip()
    if not host:
        host = 'localhost'  # По умолчанию используется локальный хост

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

    # Подключаемся к серверу
    client_socket.connect((host, port))
    print("Подключение к серверу установлено.")

    try:
        while True:
            # Отправляем сообщение серверу
            message = input("Введите сообщение для отправки серверу ('exit' для завершения): ")
            client_socket.sendall(message.encode('utf-8'))

            if message.lower() == 'exit':
                break

            # Получаем ответ от сервера
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Получено от сервера: {response}")

    finally:
        # Закрываем соединение с сервером
        client_socket.close()
        print("Соединение с сервером закрыто.")

if __name__ == "__main__":
    main()

