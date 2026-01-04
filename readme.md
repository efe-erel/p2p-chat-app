# P2P LAN Chat Application

A peer-to-peer chat application for local area networks (LAN) with optional end-to-end encryption using Diffie-Hellman key exchange and Triple DES.

## Features

- **Peer Discovery** – Automatically discovers active users on the local network via UDP broadcast
- **Secure Messaging** – Optional end-to-end encryption using Diffie-Hellman key exchange and 3DES
- **Unencrypted Messaging** – Simple plain-text chat option
- **User Status** – Shows online/away status based on last activity
- **Chat History** – Logs all sent and received messages with timestamps

## Architecture

The application consists of 4 main components:

| Component | Protocol | Port | Description |
|-----------|----------|------|-------------|
| `Service_Announcement.py` | UDP | 6000 | Broadcasts presence to the network every 8 seconds |
| `Peer_Discovery.py` | UDP | 6000 | Listens for broadcasts and maintains a list of active peers |
| `Chat_Responder.py` | TCP | 6001 | Receives incoming chat messages (acts as server) |
| `Chat_Initiator.py` | TCP | 6001 | Sends messages to other users (acts as client) |

## Requirements

- Python 3.x
- `pyDes` library for encryption

```bash
pip install pyDes
```

## Usage

### 1. Start Service Announcement (Terminal 1)

Broadcasts your presence to other users on the network.

```bash
python Service_Announcement.py
```

You will be prompted to enter your username.

### 2. Start Peer Discovery (Terminal 2)

Discovers other users on the network.

```bash
python Peer_Discovery.py
```

### 3. Start Chat Responder (Terminal 3)

Listens for incoming messages.

```bash
python Chat_Responder.py
```

### 4. Start Chat Initiator (Terminal 4)

Send messages to discovered users.

```bash
python Chat_Initiator.py
```

**Available commands:**
- `users` – List active users on the network
- `chat` – Start a chat session with a user
- `history` – View chat history

## Encryption

When starting a chat, you can choose to enable encryption:

1. **Secure Mode**: Uses Diffie-Hellman key exchange to establish a shared secret, then encrypts messages with Triple DES (3DES)
2. **Unencrypted Mode**: Sends plain-text messages

### Diffie-Hellman Parameters
- Prime (p): 19
- Generator (g): 2

## Files

| File | Description |
|------|-------------|
| `peers.txt` | JSON file storing discovered peers and their last seen time |
| `chat_log.txt` | Log file containing all sent and received messages |
| `my_username.txt` | Stores the current user's username |

## Network Configuration

The default broadcast address is set to `192.168.119.255`. You may need to modify this in `Service_Announcement.py` to match your network configuration:

```python
broadcast_addr = ('YOUR_BROADCAST_ADDRESS', 6000)
```

To find your broadcast address, check your network settings or use:
- **Linux/macOS**: `ifconfig` or `ip addr`
- **Windows**: `ipconfig`

## License

This project is open source and available under the MIT License.
