import socket
import threading

class Tracker:
    def __init__(self, host, port, file_path):
        self.host = host
        self.port = port
        self.file_path = file_path
        self.peers = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))

    def start(self):
        self.server.listen()
        print(f"Tracker listening on {self.host}:{self.port}")

        while True:
            client_socket, addr = self.server.accept()
            peer = Peer(client_socket, addr, self.file_path)
            self.peers.append(peer)
            threading.Thread(target=peer.handle_peer).start()

class Peer:
    def __init__(self, socket, addr, file_path):
        self.socket = socket
        self.addr = addr
        self.file_path = file_path

    def handle_peer(self):
        print(f"Connection from {self.addr}")
        with open(self.file_path, 'rb') as file:
            data = file.read(1024)
            while data:
                self.socket.send(data)
                data = file.read(1024)
        print(f"File sent to {self.addr}")
        self.socket.close()

if __name__ == "__main__":
    tracker = Tracker("127.0.0.1", 5000, "upload/a.txt")
    tracker.start()
