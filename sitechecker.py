import sys
import socket

if len(sys.argv) not in [2, 3]:
    print(
        """
        Improper number of arguments: at least one is required and not more 
        than two are allowed: 
        - http server's address (required)
        - port number (defaults to 80 if not specified)
        """
    )
    sys.exit(1)

try: 
    port = sys.argv[2]
except IndexError: 
    port = 80

try: 
    port = int(port) 
    assert port in range(1, 65535)
except:  
    print("Port number is invalid - exiting.")
    sys.exit(2)

server_addr = sys.argv[1]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.settimeout(10)

try: 
    sock.connect((server_addr, port))
    sock.send(b"HEAD / HTTP/1.1\r\nHost: " +
          bytes(server_addr, "utf8") +
          b"\r\nConnection: close\r\n\r\n")
except socket.timeout: 
    print("Connection timed out.")
    sys.exit(3)
except socket.gaierror:  
    print("Server address" + server_addr + "is invalid or malformed - sorry.")
    sys.exit(4)
else: 
    reply = sock.recv(100).decode("utf8")
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    print(reply[:reply.find('\r')])


