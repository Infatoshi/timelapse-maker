import os
import socket

# Configuration
IP = "0.0.0.0"  # Listen on all available interfaces
PORT = 12345
SAVE_DIR = "pi_imgs"
DELIMITER = b"<<DELIMITER>>"


def receive_until_delimiter(conn):
    data = b""
    while True:
        chunk = conn.recv(1024)
        if DELIMITER in chunk:
            data += chunk[: chunk.index(DELIMITER)]
            return data
        data += chunk


def receive_file():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((IP, PORT))
        s.listen()

        print(f"Listening on port {PORT}")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")

                # Receive filename
                filename = receive_until_delimiter(conn).decode()

                # Receive file size
                filesize = int(receive_until_delimiter(conn).decode())

                # Receive file content
                data = b""
                while len(data) < filesize:
                    packet = conn.recv(4096)
                    if not packet:
                        break
                    data += packet

                # Save the file
                if not os.path.exists(SAVE_DIR):
                    os.makedirs(SAVE_DIR)

                filepath = os.path.join(SAVE_DIR, filename)
                with open(filepath, "wb") as f:
                    f.write(data)

                print(f"Received and saved: {filepath}")


if __name__ == "__main__":
    receive_file()
