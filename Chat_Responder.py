from socket import *
import json
from datetime import datetime
import random
import pyDes
from base64 import b64decode

p = 19
g = 2

def create_3des_key(shared_key_int):
    return str(shared_key_int).ljust(24)[:24].encode()

serverPort = 6001
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen()
serverSocket.settimeout(60)

print('ChatResponder is ready to receive connections on port 6001')

with open("chat_log.txt", "a", encoding="utf-8") as log_file:
    while True:
        try:
            connectionSocket, addr = serverSocket.accept()
            print(f"Connection established with {addr}")

            shared_key = None
            username = "Unknown"

            while True:
                message = connectionSocket.recv(1024)
                if not message:
                    print(f"Connection with {addr} closed.")
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log_file.write(f"[{now}] | {username}: CONNECTION CLOSED\n")
                    log_file.flush()
                    break

                try:
                    msg = json.loads(message.decode())
                except json.JSONDecodeError:
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print("Invalid JSON received.")
                    log_file.write(f"[{now}] | {username}: ERROR Invalid JSON.\n")
                    log_file.flush()
                    continue

                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                
                if "username" in msg:
                    username = msg["username"]

                if "key" in msg:
                    username = msg.get("username", username)
                    client_partial = int(msg["key"])
                    private = random.randint(1, p - 1)
                    responder_partial = pow(g, private, p)
                    shared_key = pow(client_partial, private, p)
                    print(f"Shared key established with {username}: {shared_key}")
                    response = json.dumps({"key": str(responder_partial)})
                    connectionSocket.send(response.encode())

                elif "encryptedmessage" in msg:
                    if shared_key is None:
                        print("No shared key established.")
                        #log_file.write(f"[{now}] | {username}: ERROR No shared key.\n")
                        #log_file.flush()
                        continue

                    encrypted_b64 = msg["encryptedmessage"]
                    try:
                        decoded = b64decode(encrypted_b64)
                        wowkey = create_3des_key(shared_key)

                        cipher = pyDes.triple_des(wowkey, padmode=pyDes.PAD_PKCS5)
                        recoveredmsg = cipher.decrypt(decoded)

                        decrypted_text = recoveredmsg.decode('utf-8', errors='replace')
                        print(f"Message from {username}: {decrypted_text}") 
                        log_file.write(f"[{now}] | {username} | RECEIVED | (encrypted) | {decrypted_text}\n")
                        log_file.flush()
                    except Exception as e:
                        print(f"Decryption failed: {e}")
                        #log_file.write(f"[{now}] {username}: ERROR Decryption failed - {e}\n")
                        #log_file.flush()

                elif "unencryptedmessage" in msg:
                    text = msg["unencryptedmessage"]
                    print(f"Message from {username}: {text}") 
                    log_file.write(f"[{now}] | {username} | RECEIVED | (unencrypted) | {text}\n")
                    log_file.flush()

            connectionSocket.close()

        except timeout:
            print('Timeout: No recent request received.')
            continue

serverSocket.close()