import pygame as pg
import socket
pg.init()

# I want to create online tic tac toe game using pygame and socket
# I have created a server and client file

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "localhost"
port = 3000

# send data to server
def send_data(data):
    data = str(data)
    data = data.encode()
    sock.send(data)

# receive data from server
def receive_data():
    data = sock.recv(1024)
    data = data.decode()
    return data


def disconnect():
    send_data("disconnect")
    sock.close()    