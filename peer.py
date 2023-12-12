import socket

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def download_file(self, output_path):
        with open(output_path, 'wb') as file:
            data = self.socket.recv(1024)
            while data:
                file.write(data)
                data = self.socket.recv(1024)
        print("File downloaded successfully.")
        self.socket.close()

if __name__ == "__main__":
    peer = Peer("127.0.0.1", 5000)
    peer.download_file("download/downloaded_file.txt")
