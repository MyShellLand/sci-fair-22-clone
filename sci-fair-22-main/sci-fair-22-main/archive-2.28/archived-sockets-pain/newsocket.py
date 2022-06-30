
# find public ip address so you don't have to check each 
# https://realpython.com/python-sockets/
#https://realpython.com/python-sockets/#socket-address-families

import requests, socket, os, json

class Socket:
    
    def __init__(self, recieved, private=False):
        print("Creating a new Socket object...")
        
        self.notable = ["67.170.231.145", "142.254.70.3", "24.7.0.200", "10.0.0.245", "10.0.0.176"]
        self.private = private
        self.port = 4321
        self.recieved = recieved # function to run when a message comes in
        
        # get current ip address
        if (self.private == False): # if in public mode
            endpoint = 'https://ipinfo.io/json'
            response = requests.get(endpoint, verify = True)
            if response.status_code != 200:
                return False
                exit()
            data = response.json()
            self.ipaddr = data['ip']
            print("Public mode detected, IP address "+self.ipaddr)
        elif (self.private == True): # if in private mode
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #redundant, fix later
            s.connect(("8.8.8.8", 80))
            self.ipaddr = s.getsockname()[0]
            s.close()
            print("Private mode detected, local address "+self.ipaddr)

        if self.private:
            self.socktype = socket.AF_INET
        else:
            self.socktype = socket.AF_INET6
            
        self.socket = socket.socket(self.socktype, socket.SOCK_STREAM) # creates the main socket
        self.socket.bind(("67.170.231.145", self.port)) 
        
        self.listen()
        
    def listen(self): # start listening
        print("Starting to listen...")
        self.socket.listen()
        conn, addr = self.socket.accept()
        with conn:
            print('New message from ', addr)
            data = conn.recv(1024)
        data = data.decode("utf-8")
        data = json.loads(data)
        print("Recieved: "+data)
        this.recieved(data)
    def send(object):
        data = json.dumps(object)
        self.socket.connect((self.ip_addr, self.port))
        s.send(f"{data}".encode())
        s.close()
        #do stuff here
        self.recieved("fdsf")
    def stop(self):
        self.socket.close()




def onrecieved(var):
    print(var)

bobby = Socket(onrecieved)


