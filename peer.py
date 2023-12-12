import socket
import sys

# Constants for the Peer
HOST = "127.0.0.1"
PORT = 5000
FILE_PATH = "upload/a.txt"

class Peer:
    def __init__(self, host, port):
        # Initialize the Peer with its host, port, and create a socket for communication
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))  # Connect to the Tracker
 
    def download_file(self, output_path):
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
        print("File downloaded successfully.")
        self.socket.close()

if __name__ == "__main__":
    # Default values
    HOST = "127.0.0.1"
    PORT = 5000
    FILE_PATH = "upload/a.txt"

    # Check for command-line arguments
    # if len(sys.argv) == 4:
    #     HOST, PORT, FILE_PATH = sys.argv[1:]

    # Create a Peer instance and initiate the download process
    peer = Peer(HOST, int(PORT))
    peer.download_file("download/downloaded_file.txt")
