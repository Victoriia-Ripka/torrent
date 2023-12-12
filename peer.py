import socket
import sys

# Constants for the Peer
HOST = "127.0.0.1"
PORT = 5000


class Peer:
    def __init__(self, host, port):
        # Initialize the Peer with its host, port, and create a socket for communication
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))  # Connect to the Tracker
 
    def download_file(self, file_name, output_path):
        # Inform the tracker about the desired file
        self.socket.send(file_name.encode())

        # Receive the list of available files from the tracker
        file_list = self.socket.recv(1024).decode()
        print("Available files:", file_list)

        # Download a file from the Tracker and save it to the specified output_path
        with open(output_path, 'wb') as file:
            # Receive data from the Tracker
            data = self.socket.recv(1024)
            while data:
                # Write the received data to the file
                file.write(data)
                # Continue receiving data
                data = self.socket.recv(1024)
        # Close the socket after downloading the file
        print(f"File '{file_name}' downloaded successfully.")
        self.socket.close()


if __name__ == "__main__":
    # Check for command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python peer.py <file_name>")
        sys.exit(1)

    # Create a Peer instance and initiate the download process
    file_name = sys.argv[1]
    peer = Peer(HOST, PORT)
    peer.download_file(file_name, f"download/{file_name}")
