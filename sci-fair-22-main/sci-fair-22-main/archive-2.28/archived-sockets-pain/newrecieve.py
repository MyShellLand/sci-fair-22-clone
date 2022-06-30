#!/usr/bin/env python3

import socket, json

def listen(callback, port=4321, accept_from=""):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((accept_from, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            data = []
            print('Connected by', addr)
            while True:
                packet = conn.recv(1024)
                data.append(packet.decode("utf-8"))
                if len(packet) < 1024:
                    break
            data = json.loads("".join(data))
            reflex = callback(data, addr)
            if reflex:
                reflex = json.dumps(reflex)
                conn.sendall(bytes(reflex, encoding="utf-8"))
    return data


def func123(message, addr):
    print(message)
    print(addr)
    return "Hi this is the response"



listen(func123)




            

