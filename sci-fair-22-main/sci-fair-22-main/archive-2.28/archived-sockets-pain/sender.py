import socket
import os
import argparse

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096

host = "0.0.0.0"

port = 25565

filename = "C:/transmission.txt"

filesize = os.path.getsize(filename)


s = socket.socket()
print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")


s.send(f"{filename}{SEPARATOR}{filesize}".encode())

s.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Simple File Sender")
    parser.add_argument("file", help="File name to send")
    parser.add_argument("host", help="The host/IP address of the receiver")
    parser.add_argument("-p", "--port", help="Port to use, default is 5001", default=5001)
    args = parser.parse_args()
    filename = args.file
    host = args.host
    port = args.port
    send_file(filename, host, port)
