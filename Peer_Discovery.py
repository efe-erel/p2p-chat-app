import socket
import json
import time
from datetime import datetime

def peer_discovery():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', 6000))

        users = {}

        print("Discovery started:\n")

        while True:
            try:
                data, addr = sock.recvfrom(1024)
                ip = addr[0]
                message = json.loads(data.decode())
                username = message["username"]

                is_new = ip not in users
                users[ip] = {"username": username, "last_seen": time.time()}

                if is_new:
                    print(f"[Peer Discovery] {username} is discovered.")

                now = time.time()
                to_remove = [ip for ip, info in users.items() if now - info["last_seen"] > 24]
                for expired_ip in to_remove:
                    print(f"[Peer Discovery] {users[expired_ip]['username']} at {expired_ip} is now offline")
                    del users[expired_ip]

                with open("peers.txt", "w") as f:
                    json.dump({
                        ip: {
                            "username": info["username"],
                            "last_seen": datetime.fromtimestamp(info["last_seen"]).strftime("%Y-%m-%d %H:%M:%S")
                        } for ip, info in users.items()
                    }, f, indent=2)

            except json.JSONDecodeError:
                print("[Peer Discovery] Invalid JSON received")
            except Exception as e:
                print(f"[Peer Discovery] Error: {e}")

    except Exception as e:
        print(f"[Peer Discovery] Fatal error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    peer_discovery()