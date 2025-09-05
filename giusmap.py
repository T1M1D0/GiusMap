#!/usr/bin/env python3


import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse

MAX_IP_WORKERS = 500
MAX_PORT_WORKERS = 2000

#This function identifies the subnet, and returns in case the starting subnet header is not valid.
#This also passes the target IP's throughout the code
def all_subnets():
    local_host = socket.gethostname()
    host_ip = socket.gethostbyname(local_host)
    ip_raw = host_ip.split('.')
    if len(ip_raw) != 4 or (ip_raw[0] not in ['10', '172', '192'] and ip_raw[0] != '127'):
        print("Somethings wrong with your ip dawg")
        return
    print(f"Scanning subnet, {ip_raw[0]}.{ip_raw[1]}.0.0")
    with ThreadPoolExecutor(max_workers=MAX_IP_WORKERS) as ip_executor:    
        for s in range(256):
            for f in range(256):
                target_ip = f"{ip_raw[0]}.{ip_raw[1]}.{s}.{f}"
                ip_executor.submit(scan_host, target_ip)
                
#Using multithreading, this passes the target IP and scans all ports possible
def scan_host(host, start_port=1, end_port=65535):
    with ThreadPoolExecutor(max_workers=MAX_PORT_WORKERS) as port_executor:
        future_to_port = {
            port_executor.submit(scan_port, host, port): port
            for port in range(start_port, end_port + 1)
        }
        for future in as_completed(future_to_port):
            pass
        
#scans and reports if port is open or closed
def scan_port(host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.1)
        try:
            s.connect((host, port))
            print(f"{host}:{port} is open")
            return True
        except (socket.timeout, ConnectionRefusedError):
            print(f"{host}:{port} is DOWN")
        finally:
            s.close()

def main():
    parser = argparse.ArgumentParser(description="A multithreaded port scanner.")
    parser.add_argument("-i","--ip", help="The IP address to scan.")
    parser.add_argument("-p", "--ports", default="1-65535", help="Port range to scan (e.g., 1-1024 or 80,443). Keep blank for all ports")
    args = parser.parse_args()
    
    if args.ip:
        ip_list = [ip.strip() for ip in args.ip.split(',')]
        # User wants to scan specific IP(s)
        if ',' in args.ports:
            ports = [int(p.strip()) for p in args.ports.split(',')]
            for ip in ip_list:
                for port in ports:
                    scan_port(ip, port)
        elif '-' in args.ports:
            start_port, end_port = map(int, args.ports.split('-'))
            for ip in ip_list:
                scan_host(ip, start_port, end_port)
        else:
            port = int(args.ports)
            for ip in ip_list:
                scan_port(ip, port)
    else:
        # No IP was provided, so scan the entire local subnet
        print("No IP address provided. Scanning the entire local subnet...")
        all_subnets()
        
if __name__ == "__main__":
    main()