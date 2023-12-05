import os
from bittorrent import Torrent, TorrentSession

def create_torrent(file_path, output_path):
    torrent = Torrent(file_path, tracker="udp://tracker.openbittorrent.com:80/announce")
    torrent.save(output_path)

def share_torrent(torrent_path, download_dir):
    torrent = Torrent.load(torrent_path)
    torrent.share(destination=download_dir)

def download_torrent(torrent_path, download_dir):
    torrent = Torrent.load(torrent_path)
    session = TorrentSession()
    torrent_handle = session.add_torrent(torrent, download_dir)
    torrent_handle.download()

if __name__ == "__main__":
    txt_file_path = "path/to/your/textfile.txt"
    torrent_output_path = "path/to/your/output.torrent"
    download_directory = "path/to/your/download/directory"
    create_torrent(txt_file_path, torrent_output_path)
    share_torrent(torrent_output_path, download_directory)
    download_torrent(torrent_output_path, download_directory)
    print("Torrent created, sharing started, and download initiated.")
