#!/usr/bin/env python
# coding: cp1251

# In[ ]:

# Код сервера с модификациями
import socket

def welcome_client(client_address):
    ip_address = client_address[0]
    try:
        with open("known_clients.txt", "r") as file:
            known_clients = file.readlines()
            for known_client in known_clients:
                if ip_address in known_client:
                    return known_client.split(":")[1].strip()
    except FileNotFoundError:
        pass

    # Если клиент неизвестен, запрашиваем его имя и записываем в файл
    name = input(f"Введите имя для клиента с IP-адресом {ip_address}: ")
    with open("known_clients.txt", "a") as file:
        file.write(f"{ip_address}:{name}\n")
    return name

host = sys.argv[1] if len(sys.argv) > 1 else ''
port = int(sys.argv[2]) if len(sys.argv) > 2 else 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)

print("Сервер запущен. Ожидание подключения...")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Подключение от {client_address}")

    client_name = welcome_client(client_address)
    print(f"Приветствуем клиента {client_name}!")

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode('utf-8')
            print(f"Принято от клиента {client_name}: {message}")

            if message.lower().strip() == "exit":
                break
            
            client_socket.sendall(data.upper())

    finally:
        client_socket.close()
        print(f"Соединение с клиентом {client_address} закрыто.")
