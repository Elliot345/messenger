import threading
import os
import config
import socket
import time

# special charictar functions

def send_message(message):
    if message == "\n":
        return
    main_connection.sendall(f"{config.user_name}: {message}".encode("utf-8"))
# normal functions

def get_connection(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    for i in range(10):
        try:
            s.connect((ip, port))
            break
        except ConnectionRefusedError:
            if i == 9:
                print("connection could not be secured, terminating")
                time.sleep(1)
                exit()
            else:
                print(f"could not connect to {config.ip} on port {config.port}, will retry {9 - i} more times before terminating")
                time.sleep(1)
        except BaseException:
            if i == 9:
                print("connection could not be secured, terminating")
                time.sleep(1)
                exit()
            else:
                print(f"could not find IP {config.ip}, will retry {9-i} more times")
                time.sleep(1)
    # sending username and password
    s.sendall(f"""{config.ID["username"]}:{config.ID["password"]}""".encode("utf-8"))
    worked = s.recv(1024)

    if worked == "correct".encode("utf-8"):
        return s
    else:
        print("Username or ID is incorrect")
        exit()


def update_display():

    s = get_connection(config.ip, config.port)

    s.sendall(chr(1000).encode("utf-8"))

    messages = ""

    while True:
        s.sendall("1".encode("utf-8"))
        current_messages = get_data(s)
        if current_messages == messages:
            continue
        else:
            messages = current_messages

        os.system("cls" if os.name == "nt" else "clear")

        print(messages)
        print("-------------")
        time.sleep(0.01)

def get_data(connection):
    return connection.recv(1024).decode("utf-8")

get_connection(config.ip, config.port)

updating_messages = threading.Thread(target=update_display)
updating_messages.daemon = True
updating_messages.start()

main_connection = get_connection(config.ip, config.port)

main_connection.sendall(chr(1001).encode("utf-8"))

while True:
    message = input()

    message = message.replace("\n", "")

    message = message + "\n"
    
    send_message(message)
