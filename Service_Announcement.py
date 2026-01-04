import socket
import json
import time

def service_announcement(username):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        broadcast_addr = ('192.168.119.255', 6000)

        while True:
            message = json.dumps({"username": username})
            try:
                sock.sendto(message.encode(), broadcast_addr)
                print(f"[Service Announcement] Sent: {message}")
            except Exception as e:
                print(f"[Service Announcement] Error sending broadcast: {e}")
            time.sleep(8)

    except Exception as e:
        print(f"[Service Announcement] Error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    username = input("Enter your username: ").strip()
    with open("my_username.txt", "w") as f:
        f.write(username)

    service_announcement(username)