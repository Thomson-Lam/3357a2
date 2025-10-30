import socket
import sys
import threading
import os

# Define constants
HOST = 'localhost'
PORT = 8888
BUFFER_SIZE = 8192
CACHE_DIR = 'cache'

def main():
    # Create cache directory if it doesn't exist
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    # Create a TCP socket
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address
    try:
        proxy_socket.bind((HOST, PORT))
    except socket.error as e:
        print(f"Binding failed: {e}")
        sys.exit()

    # Listen for incoming connections
    proxy_socket.listen(10)
    print(f"Proxy server running on {HOST}:{PORT}... Press Ctrl+C to stop.")

    while True:
        try:
            # Accept a new connection
            client_socket, addr = proxy_socket.accept()
            print(f"Received a connection from: {addr}")

            # Create a new thread to handle the request
            threading.Thread(target=handle_request, args=(client_socket,)).start()
        except KeyboardInterrupt:
            proxy_socket.close()
            print("\nProxy server shutting down.")
            sys.exit()

def handle_request(client_socket):
    # Receive the request from the client
    request = client_socket.recv(BUFFER_SIZE).decode('utf-8', errors='ignore')
    print("Raw request:")
    print(request)

    # Parse the request
    try:
        method = request.split(' ')[0]
        url = request.split(' ')[1]
    except IndexError:
        client_socket.close()
        return

    # Handle non-GET requests
    if method != 'GET':
        response = "HTTP/1.0 405 Method Not Allowed\r\nContent-Type: text/plain\r\nContent-Length: 22\r\n\r\n405 Method Not Allowed"
        client_socket.send(response.encode('utf-8'))
        client_socket.close()
        return

    # Parse the URL
    try:
        if '://' in url:
            url = url.split('://')[1]
        
        if '/' in url:
            host, path = url.split('/', 1)
            path = '/' + path
        else:
            host = url
            path = '/'
        
        if ':' in host:
            host, port = host.split(':')
            port = int(port)
        else:
            port = 80

    except Exception as e:
        print(f"Error parsing URL: {e}")
        client_socket.close()
        return
        
    print("Extracted:")
    print(f"Host: {host}, Port:{port}, Path: {path}")

    # Construct cache file path
    cache_file_name = f"{host}_{port}{path.replace('/', '_')}"
    if path == '/':
        cache_file_name += 'index.html'
    if cache_file_name.endswith('_'):
        cache_file_name = cache_file_name[:-1]
    cache_file_path = os.path.join(CACHE_DIR, cache_file_name)

    # Check if the file is in cache
    if os.path.exists(cache_file_path):
        print(">>> CACHE HIT <<<")
        print(f"Served from Local Cache: {cache_file_path}")
        with open(cache_file_path, 'rb') as f:
            response = f.read()
        client_socket.sendall(response)
    else:
        print("<<< CACHE MISS >>>")
        try:
            # Create a socket to connect to the origin server
            origin_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            origin_socket.connect((host, port))
            print(f"Connecting to Server...\nConnection successful to {host}:{port}")

            # Send the request to the origin server
            request_to_server = f"GET {path} HTTP/1.0\r\nHost: {host}\r\nConnection: close\r\nUser-Agent: SimpleProxy/1.0\r\n\r\n"
            origin_socket.send(request_to_server.encode('utf-8'))

            # Receive the response from the origin server
            response_from_server = b""
            while True:
                data = origin_socket.recv(BUFFER_SIZE)
                if not data:
                    break
                response_from_server += data
                client_socket.sendall(data)

            # Save the response to the cache
            with open(cache_file_path, 'wb') as f:
                f.write(response_from_server)
            print(f"Saved {len(response_from_server)} bytes to cache")

            origin_socket.close()
        except socket.error as e:
            print(f"Error connecting to origin server: {e}")
            response = "HTTP/1.0 502 Bad Gateway\r\nContent-Type: text/plain\r\nContent-Length: 15\r\n\r\n502 Bad Gateway"
            client_socket.send(response.encode('utf-8'))

    client_socket.close()

if __name__ == "__main__":
    main()
