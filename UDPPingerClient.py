import socket
import time
import sys

def main():
    if len(sys.argv) != 3: # CLI incorrect usage 
        print("Usage: python UDP_Pinger_client.py <server_host> <server_port>")
        sys.exit(1)

    server_host = sys.argv[1]
    server_port = int(sys.argv[2])

    c_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    c_socket.settimeout(1)

    for seq_num in range(1, 11):
        message = f"Ping {seq_num} {time.time()}"
        start_time = time.time()

        try:
            c_socket.sendto(message.encode(), (server_host, server_port))
            response, server_address = c_socket.recvfrom(1024)
            end_time = time.time()
            rtt = end_time - start_time
            
            response_message = response.decode()
            
            parts = response_message.split()
            ping_number = parts[1]
            
            current_time = time.ctime() # current time for print message 

            print(f"Reply from {server_address[0]}: PING {ping_number} {current_time}") 
            print(f"RTT: {rtt}")

        except socket.timeout:
            print("Request timed out.")

    c_socket.close()

if __name__ == "__main__":
    main()
