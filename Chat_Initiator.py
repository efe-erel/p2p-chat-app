from socket import *
import json
from datetime import datetime
from base64 import b64encode
import pyDes

serverPort = 6001

def load_peers():
    try:
        with open("peers.txt", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def display_users():
    peers = load_peers()
    now = datetime.now()

    found = False
    for ip, info in peers.items():
        username = info.get("username", "Unknown")
        last_seen_str = info.get("last_seen")
        if last_seen_str:
            last_seen = datetime.strptime(last_seen_str, "%Y-%m-%d %H:%M:%S")
            seconds_since = (now - last_seen).total_seconds()

            if seconds_since < 15 * 60: # online within 10 sec, away within 10s to 900s, then offline
                status = "Online" if seconds_since < 10 else "Away"
                print(f"{username} ({status}) - {ip}")
                found = True

    if not found:
        print("No active users found.")

def view_history():
    try:
        with open("chat_log.txt", "r") as f:
            for line in f:
                print(line.strip())
    except FileNotFoundError:
        print("No chat history found.")

def chat_with_user():
    # tries to get username from service announcement to avoid different naming
    try:
        with open("my_username.txt", "r") as f:
            username = f.read().strip()
    except FileNotFoundError:
        username = input("Enter your username: ").strip()
    serverIP = input("Enter the IP address of the user to chat: ").strip()
    secure = input("Do you want to chat securely? (yes/no): ").strip().lower()

    clientSocket = socket(AF_INET, SOCK_STREAM)
    try:
        clientSocket.connect((serverIP, serverPort))
    except Exception as e:
        print(f"Error: Could not connect to {username} at {serverIP}. Reason: {e}")
        return

    if secure == "yes":
        p = 19
        g = 2
        a = int(input("Enter your private number (e.g., 5): "))
        A = pow(g, a, p)

        clientSocket.send(json.dumps({"key": str(A)}).encode())

        try:
            response = clientSocket.recv(1024).decode()
            B = int(json.loads(response)["key"])
        except Exception:
            print("Failed to receive valid Diffie-Hellman key from peer.")
            clientSocket.close()
            return

        shared_key = pow(B, a, p)
        key24 = str(shared_key).ljust(24)[:24].encode()
        des = pyDes.triple_des(key24, padmode=2)

        print("You are now chatting securely. Type /exit to end the session.")

        while True:
            message = input("You: ")
            if message.strip() == "/exit":
                break

            encrypted_bytes = des.encrypt(message)
            encrypted_b64 = b64encode(encrypted_bytes).decode()

            clientSocket.send(json.dumps({"encryptedmessage": encrypted_b64, "username": username}).encode())

            with open("chat_log.txt", "a") as log:
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log.write(f"[{now}] | {username} | SENT | (encrypted) | {message}\n")

    else:
        print("You are now chatting without encryption. Type /exit to end the session.")
        while True:
            message = input("You: ")
            if message.strip() == "/exit":
                break

            clientSocket.send(json.dumps({"unencryptedmessage": message, "username": username}).encode())

            with open("chat_log.txt", "a") as log:
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log.write(f"[{now}] | {username} | SENT | {message}\n")

    clientSocket.close()

while True:
    action = input("Choose action (Users / Chat / History): ").strip().lower()
    print("")

    if action == "users":
        display_users()
    elif action == "chat":
        chat_with_user()
    elif action == ("history"):
        view_history()
    else:
        print("Invalid option selected.")
    print("")