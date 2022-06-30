#!/usr/bin/env python3

import socket, json, requests

class Radio:
    def __init__(self):
        print("New radio instantiated.")

    def find_ip(address):
        if address == "local":
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                foundaddr = s.getsockname()[0]
                s.close()
            except:
                return False
        elif address == "public":
            try:
                response = requests.get('https://ipinfo.io/json', verify = True)
                if response.status_code != 200:
                    return False
                data = response.json()
                foundaddr = data['ip']
            except:
                return False
        elif address == "localhost":
            foundaddr = "127.0.0.1"
        return foundaddr


def sendto(recipient, obj, port=4321): # ex. sendto("12.2.3.4.5", "hello")    returns response
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((recipient, port))
            s.sendall(bytes(json.dumps(obj), encoding="utf-8"))
            recieved = []
            while True:
                packet = s.recv(1024)
                recieved.append(packet.decode("utf-8"))
                if len(packet) < 1024:
                    break
        if len(recieved) > 0:
            recieved = json.loads("".join(recieved))
            return recieved
        else:
            return True
    except KeyboardInterrupt:
        print("Keyboard Interupt")
        return False
    except Exception as e:
        print(e)
        return False


print(sendto("127.0.0.1", [1, 2, 3, 4, 5]))








