import socket
import threading

# Constants for the Tracker
HOST = "127.0.0.1"
PORT = 5000
FILE_PATH = "upload/a.txt"

class Tracker:
    def __init__(self, host, port, file_path):
        # Initialize the Tracker with host, port, file_path, and an empty list of peers
        self.host = host
        self.port = port
        # Mapping of file names to their paths
        self.files = {"a.txt": "upload/a.txt", "b.txt": "upload/b.txt", "c.txt": "upload/c.txt"} 
        # List to store connected Peers
        self.peers = []  
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))

    def start(self):
        # Start listening for incoming connections
        self.server.listen()
        print(f"Tracker listening on {self.host}:{self.port}")

        while True:
            # Accept incoming connection from a Peer
            client_socket, addr = self.server.accept()
            peer = Peer(client_socket, addr, self)
            self.peers.append(peer) # Add the Peer to the list of connected Peers
            threading.Thread(target=peer.handle_peer).start()

class Peer:
    # Initialize the Peer with its socket, address, and the tracker
    def __init__(self, socket, addr, tracker):
        self.socket = socket
        self.addr = addr
        self.tracker = tracker

    def handle_peer(self):
        # Handle the communication with the connected Peer
        print(f"Connection from {self.addr}")

        # Open the file and send its content to the connected Peer
        self.send_file_list()
        file_name = self.receive_file_name()
        if file_name in self.tracker.files:
            file_path = self.tracker.files[file_name]
            self.send_file(file_path)
        else:
            print(f"File '{file_name}' not found.")

        # Close the socket after sending the file
        self.socket.close() 
    
    def send_file_list(self):
        # Send the list of available files to the Peer
        file_list = ",".join(self.tracker.files.keys())
        self.socket.send(file_list.encode())

    def receive_file_name(self):
        # Receive the selected file name from the Peer
        file_name = self.socket.recv(1024).decode()
        return file_name

    def send_file(self, file_path):
        # Send the selected file to the Peer
        with open(file_path, 'rb') as file:
            data = file.read(1024)
            while data:
                self.socket.send(data)
                data = file.read(1024)
        print(f"File '{file_path}' sent to {self.addr}")

if __name__ == "__main__":
    # Create a Tracker instance and start listening for connections
    tracker = Tracker(HOST, PORT, FILE_PATH)
    tracker.start()
