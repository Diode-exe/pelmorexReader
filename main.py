"""This script connects to a streaming socket and prints lines of text received from it."""

import socket
import threading
import time

stop = threading.Event()

def reader(s, stop_evt):
    """Read lines from the socket and print them until stop_evt is set."""
    s.settimeout(1.0)
    buf = b''
    try:
        with open("output.xml", "wb") as f:
            while not stop_evt.is_set():
                try:
                    chunk = s.recv(4096)
                except socket.timeout:
                    continue
                if not chunk:
                    break
                buf += chunk
                while b'\n' in buf:
                    line, buf = buf.split(b'\n', 1)
                    print(line.decode('utf-8').strip())
                    f.write(line + b'\n')
    finally:
        s.close()

sock = socket.create_connection(("streaming1.naad-adna.pelmorex.com", 8080))
t = threading.Thread(target=reader, args=(sock, stop), daemon=False)
t.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Requesting clean shutdown...")
    stop.set()
    t.join(timeout=5)
    print("Exited cleanly.")
