import socket
import config
import _thread


def get_data(conn):
    data = conn.recv(1024)
    return data.decode("utf-8")

def display_client(conn):
    while True:
        _ = get_data(conn)
        with open("messages.txt", 'r') as f:
            lines = f.readlines()
        conn.sendall(
            "".join(lines).encode("utf-8")
        )
def message_client(conn):
    while True:
        data = get_data(conn)
        if data == chr(1001):
            continue
        with open("messages.txt", 'a') as f:
            f.write(data)
def threaded_client(conn):
    username_password = get_data(conn).split(":")

    if username_password[0] in config.user_IDs:
        if username_password[1] == config.user_IDs[username_password[0]]:
            conn.sendall("correct".encode("utf-8"))
        else:
            conn.sendall("incorrect".encode("utf-8"))
    else:
        conn.sendall("incorrect".encode("utf-8"))

    data = get_data(conn)

    if chr(1000) in data:
        display_client(conn)
    else:
        message_client(conn)
if True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((config.ip, config.port))
        s.listen()

        while True:

            connection, _ = s.accept()

            # security check

            _thread.start_new_thread(threaded_client, (connection, ))

