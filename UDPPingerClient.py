import socket
import time
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python UDP_Pinger_client.py <server_host> <server_port>")
        sys.exit(1)

    server_host = sys.argv[1]
    server_port = int(sys.argv[2])

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(1)

    for sequence_number in range(1, 11):
        message = f"Ping {sequence_number} {time.time()}"
        start_time = time.time()

        try:
            client_socket.sendto(message.encode(), (server_host, server_port))
            response, server_address = client_socket.recvfrom(1024)
            end_time = time.time()
            rtt = end_time - start_time
            
            response_message = response.decode()
            
            parts = response_message.split()
            ping_number = parts[1]
            
            current_time = time.ctime()

            print(f"Reply from {server_address[0]}: PING {ping_number} {current_time}")
            print(f"RTT: {rtt}")

        except socket.timeout:
            print("Request timed out.")

    client_socket.close()

if __name__ == "__main__":
    main()
