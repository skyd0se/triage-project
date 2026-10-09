import requests
import socket

target_host = "192.168.122.197"
target_port = 80

# Kirim raw HTTP request dengan header yang invalid untuk memaksa 400
raw_request = (
    b"GET / HTTP/1.1\r\n"
    b"Host: 192.168.122.197\r\n"
    b"Content-Length: -1\r\n"  # Content-Length negatif = invalid
    b"\r\n"
)

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    s.connect((target_host, target_port))
    s.send(raw_request)
    response = s.recv(1024)
    print(response.decode(errors='replace')[:200])
    s.close()
except Exception as e:
    print(f"Error: {e}")
